#!/usr/bin/env python3
"""Focused structural contract checks for dispatch-tickets."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "skills/engineering/dispatch-tickets/SKILL.md"
MANIFEST_ENTRY = "./skills/engineering/dispatch-tickets"
EXPECTED_PROMPT = """Repository: <repository>
Ticket: <ticket>
Load and follow installed `orchestrate`. Resolve all governing context and complete this Ticket yourself.
Return exactly one single-line JSON object with required string fields \"ticket\": \"<ticket>\" and \"status\": one of \"delivered\", \"blocked\", \"failed\", or \"cancelled\". Include non-empty string \"ref\" only for an essential durable reference and non-empty string \"blocker\" only when applicable. Include no other fields or output."""


def require(text: str, *fragments: str) -> None:
    for fragment in fragments:
        assert fragment in text, f"missing contract fragment: {fragment}"


def main() -> None:
    skill = SKILL_PATH.read_text()
    frontmatter = re.match(r"\A---\n(.*?)\n---", skill, re.DOTALL)
    assert frontmatter, "dispatch-tickets frontmatter is missing"
    require(
        frontmatter.group(1),
        "name: dispatch-tickets",
        "description: Dispatch ",
        "disable-model-invocation: true",
    )

    manifests = [
        json.loads((ROOT / ".codex-plugin/plugin.json").read_text()),
        json.loads((ROOT / ".claude-plugin/plugin.json").read_text()),
    ]
    assert manifests[0] == manifests[1], "plugin manifests are not mirrored"
    assert manifests[0]["skills"].count(MANIFEST_ENTRY) == 1

    require(
        (ROOT / "README.md").read_text(),
        "(./skills/engineering/dispatch-tickets/SKILL.md)",
    )
    require(
        (ROOT / "skills/engineering/README.md").read_text(),
        "(./dispatch-tickets/SKILL.md)",
    )
    require(
        (ROOT / "scripts/check-catalog.py").read_text(),
        '"dispatch-tickets"',
    )

    prompt_match = re.search(
        r"Use this exact coordinator prompt, replacing both placeholders without adding text:\n\n"
        r"```text\n(.*?)\n```",
        skill,
        re.DOTALL,
    )
    assert prompt_match, "exact coordinator prompt is not extractable"
    prompt = prompt_match.group(1)
    assert prompt == EXPECTED_PROMPT, "coordinator prompt widened or changed"
    for forbidden in ("next", "writer", "reviewer", "diff", "tests", "acceptance criteria"):
        assert forbidden not in prompt.lower(), f"coordinator prompt contains work detail: {forbidden}"

    require(
        skill,
        "Load and follow the installed `caveman` skill before every root report.",
        "`<owner>/<repository>#<positive-integer>`",
        "only ASCII letters, digits, `.`, `_`, or `-`",
        "explicitly states Mission authorization",
        "performs no tracker, file, or remote discovery",
        "only `ticket`, `coordinator`, `state`, and `outcome`",
        "`subagent_start`",
        '`delivery: "async"`',
        '`delivery: "direct"`',
        "`maxDepth: 3`",
        "`maxChildren: 1`",
        "clean coordinator conversation without the parent transcript",
        "Omit `tools`",
        "without waiting, sleeping, polling",
        "exactly one later pong",
        "no later pong",
        "one top-level JSON object",
        '`"delivered"`, `"blocked"`, `"failed"`, or `"cancelled"`',
        "Reject missing required keys, unknown keys",
        "byte-for-byte",
        "Do not adjudicate implementation semantics",
        "Never report `Mission complete`",
        "no wormhole, tmux, persistent Mission state",
        "Queue/TTS side effect, publishing, tagging, release",
        "no steering or interruption mechanics",
    )

    print("dispatch-tickets contract ok")


if __name__ == "__main__":
    main()
