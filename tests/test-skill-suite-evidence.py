#!/usr/bin/env python3
"""Check deterministic skill-suite inventory, schema, and executable fixtures."""

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


def parse_distribution(value: str) -> tuple[str, str, str]:
    match = re.fullmatch(
        r"(active|optional), (agent-discoverable|user-only) — `(skills/[^`]+)`\.",
        value,
    )
    assert match, f"invalid distribution classification: {value}"
    return match.group(1), match.group(2), match.group(3)


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
        actual = parse_distribution(skills[name]["Distribution / discovery"])
        assert actual == (distribution, discovery, relative_dir), (
            f"wrong distribution classification for {name}: {actual}"
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
    check_dynamic_inventory(audit)
    check_decision_bearing_fixtures()
    print("skill-suite evidence ok: inventory, schema, and executable fixtures complete")


if __name__ == "__main__":
    main()
