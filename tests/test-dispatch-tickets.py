#!/usr/bin/env python3
"""Focused structural and reference-scenario checks for dispatch-tickets."""

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


class ObjectPairs(list[tuple[str, object]]):
    """Distinguish decoded JSON objects from arrays and retain duplicate keys."""


ALLOWED_STATUSES = {"delivered", "blocked", "failed", "cancelled"}
ALLOWED_KEYS = {"ticket", "status", "ref", "blocker"}


def validate_outcome(message: str, expected_ticket: str) -> tuple[str, dict]:
    trimmed = message.strip()
    if "\n" in trimmed or "\r" in trimmed:
        return "syntax", {}
    try:
        decoded = json.loads(trimmed, object_pairs_hook=ObjectPairs)
    except (json.JSONDecodeError, TypeError):
        return "syntax", {}
    if not isinstance(decoded, ObjectPairs):
        return "shape", {}

    keys = [key for key, _ in decoded]
    if len(keys) != len(set(keys)):
        return "shape", {}
    outcome = dict(decoded)
    if not {"ticket", "status"} <= outcome.keys() or outcome.keys() - ALLOWED_KEYS:
        return "shape", {}
    if not isinstance(outcome["ticket"], str) or not isinstance(
        outcome["status"], str
    ):
        return "shape", {}
    if any(
        key in outcome
        and (not isinstance(outcome[key], str) or not outcome[key])
        for key in ("ref", "blocker")
    ):
        return "shape", {}
    if outcome["ticket"] != expected_ticket:
        return "identity", {}
    if outcome["status"] not in ALLOWED_STATUSES:
        return "status", {}
    return "accepted", outcome


def dispatch_report(ticket: str, coordinator: int, mode: str) -> str | None:
    if mode == "print":
        return None
    return f"{ticket} dispatched (#{coordinator}); root available; outcome pending."


def terminal_report(message: str, ticket: str, mode: str) -> str:
    result, outcome = validate_outcome(message, ticket)
    suffix = (
        "root available."
        if mode == "interactive"
        else "print settled; no pong pending."
    )
    if result != "accepted":
        return f"{ticket} outcome rejected ({result}); {suffix}"
    details = "".join(
        f"; {key} {outcome[key]}" for key in ("ref", "blocker") if key in outcome
    )
    return f"{ticket} {outcome['status']}{details}; {suffix}"


def check_reference_scenarios() -> None:
    ticket = "luizomf/omskills#34"
    scenarios = [
        (
            '{"ticket":"luizomf/omskills#34","status":"delivered","ref":"abc123"}',
            "interactive",
            "luizomf/omskills#34 delivered; ref abc123; root available.",
        ),
        (
            '{"ticket":"luizomf/omskills#34","status":"blocked","blocker":"setup missing"}',
            "print",
            "luizomf/omskills#34 blocked; blocker setup missing; print settled; no pong pending.",
        ),
        ("[]", "interactive", f"{ticket} outcome rejected (shape); root available."),
        (
            '{"ticket":"luizomf/omskills#34"}',
            "print",
            f"{ticket} outcome rejected (shape); print settled; no pong pending.",
        ),
        (
            '{"ticket":"luizomf/omskills#34","ticket":"luizomf/omskills#34","status":"delivered"}',
            "interactive",
            f"{ticket} outcome rejected (shape); root available.",
        ),
        (
            '{"ticket":"luizomf/omskills#34","status":"done"}',
            "interactive",
            f"{ticket} outcome rejected (status); root available.",
        ),
        (
            '{"ticket":"luizomf/omskills#35","status":"delivered"}',
            "interactive",
            f"{ticket} outcome rejected (identity); root available.",
        ),
        (
            '{"ticket":"luizomf/omskills#34","status":"delivered","next":"#35"}',
            "print",
            f"{ticket} outcome rejected (shape); print settled; no pong pending.",
        ),
        (
            'prefix {"ticket":"luizomf/omskills#34","status":"delivered"}',
            "interactive",
            f"{ticket} outcome rejected (syntax); root available.",
        ),
    ]
    for message, mode, expected in scenarios:
        assert terminal_report(message, ticket, mode) == expected

    assert dispatch_report(ticket, 7, "interactive") == (
        "luizomf/omskills#34 dispatched (#7); root available; outcome pending."
    )
    assert dispatch_report(ticket, 7, "print") is None


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
        "use the skill loader to read and follow the installed `caveman` skill",
        "That composition read is the root's sole file read",
        "`<owner>/<repository>#<positive-integer>`",
        "only ASCII letters, digits, `.`, `_`, or `-`",
        "explicitly states Mission authorization",
        "performs no tracker, repository, or remote discovery",
        "only `ticket`, `coordinator`, `state`, and `outcome`",
        "`PI_PROVIDER`, `PI_MODEL`, and `PI_REASONING_LEVEL`",
        "retain none of their values in dispatcher state",
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

    staged_routing = {
        ROOT / "CONTEXT.md": "Its active tracer accepts one exact",
        ROOT / "skills/productivity/writing-great-skills/SKILL.md": (
            "supply that same one exact identity to the active `dispatch-tickets`"
        ),
        ROOT / "skills/productivity/write-a-skill/SKILL.md": (
            "route that same one exact identity to `dispatch-tickets`"
        ),
        ROOT / "skills/engineering/triage/SKILL.md": (
            "supplies that same one exact identity to `dispatch-tickets`"
        ),
        ROOT / "skills/engineering/to-tickets/SKILL.md": (
            "supply that same one exact identity to the active `dispatch-tickets`"
        ),
    }
    for path, fragment in staged_routing.items():
        require(path.read_text(), fragment)

    check_reference_scenarios()
    print("dispatch-tickets contract and reference scenarios ok")


if __name__ == "__main__":
    main()
