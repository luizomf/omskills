#!/usr/bin/env python3
"""Fail-closed completeness and contract checks for the skill-suite audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "docs/audits/2026-08-skill-suite-compatibility.md"
MANIFESTS = (
    ROOT / ".codex-plugin/plugin.json",
    ROOT / ".claude-plugin/plugin.json",
)
SKILL_FIELDS = {
    "Distribution / discovery",
    "Invocation / composition",
    "Inheritance / clean context",
    "Role / depth",
    "Delivery / modes",
    "Cancellation / effects",
    "Authorization / continuation / completion",
    "Bundled resources",
    "Evidence / classification",
}
RESOURCE_FIELDS = {
    "Decision role",
    "Owner / loading",
    "Compatibility",
    "Evidence",
}


def frontmatter(skill_file: Path) -> str:
    match = re.match(r"\A---\n(.*?)\n---", skill_file.read_text(), re.DOTALL)
    assert match, f"missing frontmatter: {skill_file.relative_to(ROOT)}"
    return match.group(1)


def frontmatter_name(skill_file: Path) -> str:
    match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+)", frontmatter(skill_file))
    assert match, f"missing frontmatter name: {skill_file.relative_to(ROOT)}"
    return match.group(1).strip()


def is_user_only(skill_file: Path) -> bool:
    return bool(
        re.search(
            r"(?m)^disable-model-invocation:\s*true\s*$",
            frontmatter(skill_file),
        )
    )


def parse_classifications(
    audit: str, start: str, end: str | None, expected_fields: set[str]
) -> dict[str, dict[str, str]]:
    section = audit.split(start, 1)[1]
    if end is not None:
        section = section.split(end, 1)[0]
    matches = list(
        re.finditer(
            r"(?ms)^### `([^`]+)`\n(.*?)(?=^### `|\Z)",
            section,
        )
    )
    parsed: dict[str, dict[str, str]] = {}
    for match in matches:
        identity, body = match.groups()
        assert identity not in parsed, f"duplicate audit classification: {identity}"
        fields = {
            field: value.strip()
            for field, value in re.findall(
                r"(?m)^- \*\*([^*]+):\*\* (.+)$", body
            )
        }
        assert fields.keys() == expected_fields, (
            f"wrong fields for {identity}: "
            f"missing={sorted(expected_fields - fields.keys())}, "
            f"extra={sorted(fields.keys() - expected_fields)}"
        )
        assert all(fields.values()), f"empty classification field: {identity}"
        parsed[identity] = fields
    return parsed


def check_dynamic_inventory(audit: str) -> None:
    manifests = [json.loads(path.read_text()) for path in MANIFESTS]
    assert manifests[0] == manifests[1], "plugin manifests differ"
    active_paths = {entry.removeprefix("./") for entry in manifests[0]["skills"]}

    skill_files = sorted((ROOT / "skills").glob("*/*/SKILL.md"))
    skill_by_name = {frontmatter_name(path): path for path in skill_files}
    assert len(skill_by_name) == len(skill_files), "duplicate live skill name"

    resources = {
        path.relative_to(ROOT).as_posix()
        for skill_file in skill_files
        for path in skill_file.parent.rglob("*")
        if path.is_file() and path.name != "SKILL.md"
    }

    skills = parse_classifications(
        audit,
        "## Skill classifications",
        "## Bundled resource classifications",
        SKILL_FIELDS,
    )
    resource_rows = parse_classifications(
        audit,
        "## Bundled resource classifications",
        "## Preserved findings",
        RESOURCE_FIELDS,
    )
    assert skills.keys() == skill_by_name.keys(), (
        f"skill audit drift: missing={sorted(skill_by_name.keys() - skills.keys())}, "
        f"extra={sorted(skills.keys() - skill_by_name.keys())}"
    )
    assert resource_rows.keys() == resources, (
        f"resource audit drift: missing={sorted(resources - resource_rows.keys())}, "
        f"extra={sorted(resource_rows.keys() - resources)}"
    )

    for name, skill_file in skill_by_name.items():
        relative_dir = skill_file.parent.relative_to(ROOT).as_posix()
        distribution = "active" if relative_dir in active_paths else "optional"
        discovery = "user-only" if is_user_only(skill_file) else "agent-discoverable"
        actual = skills[name]["Distribution / discovery"].lower()
        assert distribution in actual, f"wrong distribution for {name}"
        assert discovery in actual, f"wrong discovery state for {name}"
        assert relative_dir in skills[name]["Distribution / discovery"], (
            f"missing skill path for {name}"
        )

        owned_resources = sorted(
            path.relative_to(ROOT).as_posix()
            for path in skill_file.parent.rglob("*")
            if path.is_file() and path.name != "SKILL.md"
        )
        recorded = re.findall(r"`(skills/[^`]+)`", skills[name]["Bundled resources"])
        assert recorded == owned_resources, f"wrong bundled resources for {name}"
        for resource in owned_resources:
            assert name in resource_rows[resource]["Owner / loading"], (
                f"wrong resource owner for {resource}"
            )

    assert len(active_paths) == len(manifests[0]["skills"])
    assert all(
        "decision-bearing" in row["Decision role"].lower()
        for row in resource_rows.values()
    )
    assert all(
        "compatible" in row["Compatibility"].lower()
        for row in resource_rows.values()
    )
    assert all(
        "compatible" in row["Evidence / classification"].lower()
        for row in skills.values()
    )


def require(path: str, *fragments: str) -> None:
    text = (ROOT / path).read_text()
    for fragment in fragments:
        assert fragment in text, f"{path} missing contract fragment: {fragment}"


def check_architecture_contracts() -> None:
    require(
        "skills/engineering/orchestrate/SKILL.md",
        "Accept exactly one explicitly Mission-authorized Ticket identity",
        "direct delivery",
        "fresh, non-delegating, single-pass depth-3 leaves",
        "Never return work to the writer",
        "Do not delegate corrections or request another review",
        "exactly one compact single-line JSON object",
    )
    orchestrate = (ROOT / "skills/engineering/orchestrate/SKILL.md").read_text()
    for stale in ("fixed Ticket queue", "queue cursor", "transfer watchdog"):
        assert stale not in orchestrate, f"orchestrate retains stale architecture: {stale}"

    require(
        "skills/engineering/dispatch-tickets/SKILL.md",
        "minimal depth-1 **Ticket dispatcher**",
        "performs no tracker, repository, or remote discovery",
        '`delivery: "async"`',
        '`delivery: "direct"`',
        "No child receives or returns `next`",
        "no wormhole or tmux dependency",
        "no Queue/TTS side effect",
    )
    for path in (
        "skills/engineering/code-review/SKILL.md",
        "skills/engineering/improve-codebase-architecture/SKILL.md",
        "skills/engineering/research/SKILL.md",
        "skills/productivity/prompt-comprehension-audits/SKILL.md",
    ):
        require(path, "depth-3", "direct delivery", "no later asynchronous completion notification")

    require(
        "skills/engineering/tdd/SKILL.md",
        "In a Mission-authorized Ticket",
        "return the unresolved seam as a blocker directly to the Ticket coordinator",
        "Print/headless execution never waits for a conversational answer",
    )
    require(
        "skills/productivity/write-a-skill/SKILL.md",
        "In a Mission-authorized Ticket",
        "return it as a blocker directly to the Ticket coordinator",
        "without opening a user review Question",
    )
    require(
        "skills/engineering/codebase-design/DESIGN-IT-TWICE.md",
        "does not by itself authorize a third specialist",
        "A depth-3 writer or reviewer resolves accepted sources directly",
    )
    for path in (
        "skills/engineering/implement/SKILL.md",
        "skills/engineering/diagnosing-bugs/SKILL.md",
        "skills/engineering/prototype/SKILL.md",
        "skills/engineering/resolving-merge-conflicts/SKILL.md",
    ):
        text = (ROOT / path).read_text()
        assert "subagent_start" not in text and "spawn_agent" not in text, (
            f"audited leaf opens delegation: {path}"
        )

    require(
        "skills/productivity/tmux-worker/SKILL.md",
        "owns only this visible transport and lifecycle",
        "not an Accepted continuation mechanism",
    )
    require(
        "skills/productivity/wormhole/SKILL.md",
        "The transfer creates neither work nor authority",
        "first Safe turn boundary",
    )


def check_decision_bearing_fixtures() -> None:
    hitl = ROOT / "skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh"
    subprocess.run(["bash", "-n", str(hitl)], check=True)

    scene_path = ROOT / "skills/productivity/excalidraw/assets/diagram-base.excalidraw"
    before = hashlib.sha256(scene_path.read_bytes()).hexdigest()
    scene = json.loads(scene_path.read_text())
    assert scene["type"] == "excalidraw" and scene["version"] == 2
    assert scene["elements"] == [] and scene["files"] == {}
    assert scene["appState"]["bindingPreference"] == "enabled"
    assert hashlib.sha256(scene_path.read_bytes()).hexdigest() == before

    voice = (ROOT / "skills/productivity/voice/SKILL.md").read_text()
    command_match = re.search(
        r"(?ms)^\s*```sh\n(.*?)^\s*```", voice
    )
    assert command_match, "voice Queue command is not extractable"
    command = textwrap.dedent(command_match.group(1)).replace(
        "Your natural spoken response goes here.", "Safe compatibility fixture."
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        fake_bq = tmp_path / "bq"
        args_path = tmp_path / "args"
        stdin_path = tmp_path / "stdin"
        fake_bq.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$CAPTURE_ARGS\"\n"
            "cat > \"$CAPTURE_STDIN\"\n"
        )
        fake_bq.chmod(0o755)
        env = os.environ.copy()
        env.update(
            PATH=f"{tmp_path}:{env['PATH']}",
            CAPTURE_ARGS=str(args_path),
            CAPTURE_STDIN=str(stdin_path),
        )
        subprocess.run(["bash", "-c", command], check=True, env=env)
        assert args_path.read_text().splitlines() == [
            "--stdin",
            "--label",
            "pi_voice_playback",
            "--concurrency-key",
            "audio-playback",
            "--",
            "edgetts",
            "--stdin",
            "--quiet",
        ]
        assert stdin_path.read_text() == "Safe compatibility fixture.\n"


def main() -> None:
    audit = AUDIT.read_text()
    assert "/Users/" not in audit, "audit contains an absolute home path"
    assert ".scratch/" not in audit, "audit cites ignored scratch material"
    for fragment in (
        "8a0c2df5e3c771a7fc6bb3dd42ffd24c9c2ebcd2",
        "c3aa6aa26878ce8c9f73cb51cf3b826b98439cd8",
        "5 test files passed; 70 tests passed",
        "Historical only",
        "Sannux",
        "separate authorization",
    ):
        assert fragment in audit, f"audit missing evidence boundary: {fragment}"

    check_dynamic_inventory(audit)
    check_architecture_contracts()
    check_decision_bearing_fixtures()
    print("skill-suite evidence ok: dynamic catalog and resource contracts complete")


if __name__ == "__main__":
    main()
