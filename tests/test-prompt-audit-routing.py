#!/usr/bin/env python3
"""Regression checks for the Prompt Audit-to-orchestration context boundary."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTEXT = (ROOT / "CONTEXT.md").read_text()
PROMPT_AUDIT = (
    ROOT / "skills/productivity/prompt-comprehension-audits/SKILL.md"
).read_text()
README = (ROOT / "README.md").read_text()


def require(text: str, source: str, *fragments: str) -> None:
    for fragment in fragments:
        assert fragment in text, f"{source} missing contract fragment: {fragment}"


def section(text: str, start: str, end: str) -> str:
    assert start in text, f"missing section: {start}"
    body = text.split(start, 1)[1]
    assert end in body, f"missing section boundary after {start}: {end}"
    return body.split(end, 1)[0]


def check_canonical_domain_boundary() -> None:
    require(
        CONTEXT,
        "CONTEXT.md",
        "Prompt Audit and implementation are separate context units",
        "records its status and ends without implementation",
        "eligible Mission-authorized delivery begins only in one fresh isolated **Ticket coordinator** running `orchestrate`",
    )


def check_prompt_audit_completion_route() -> None:
    completion = section(
        PROMPT_AUDIT,
        "## Complete the audit context",
        "## Audit boundary",
    )
    require(
        completion,
        "prompt-comprehension-audits completion route",
        "The audit conversation performs no implementation",
        "`FAIL`",
        "ends without dispatch",
        "without Mission authorization",
        "reports eligibility and ends without dispatch",
        "with explicit Mission authorization for this one Ticket",
        "exactly one fresh isolated context running installed `orchestrate`",
        "without another user intervention",
    )
    assert "resume implementation" not in PROMPT_AUDIT.lower(), (
        "Prompt Audit still permits same-context implementation continuation"
    )
    assert "dispatch-tickets" not in completion, (
        "one-Ticket Prompt Audit completion must route directly to orchestrate"
    )
    require(
        PROMPT_AUDIT,
        "prompt-comprehension-audits fit gate",
        "Treat any semantic `PASS` or explicit `BYPASS` above as provisional",
        "fit in one fresh agent context with room to understand the relevant code, implement the end-to-end behavior, and verify it",
        "choose `FAIL` and report that decomposition is required before autonomous delivery",
    )


def check_entry_point_pointers() -> None:
    assert "Want to implement one explicitly selected, audited Ticket directly" not in README
    scenarios = (
        ("### New Empty Project", "### Existing Project Without These Skills"),
        ("### Existing Project Without These Skills", "### Project Already Using These Skills"),
        ("### Project Already Using These Skills", "## Local Quickstart"),
    )
    for start, end in scenarios:
        scenario = section(README, start, end)
        require(scenario, start, "Mission-authorize", "`/orchestrate`")
        assert "`/implement`" not in scenario, (
            f"README scenario routes around the fresh coordinator: {start}"
        )

    pointers = {
        "skills/engineering/triage/SKILL.md": (
            "routes one Mission-authorized Ticket directly to `orchestrate`",
            "ordered list of Mission-authorized identities to `dispatch-tickets`",
        ),
        "skills/engineering/to-tickets/SKILL.md": (
            "route one selected Ticket directly to its coordinator contract, `orchestrate`",
            "ordered list of Mission-authorized identities to the active `dispatch-tickets`",
        ),
        "skills/productivity/write-a-skill/SKILL.md": (
            "route one selected Ticket directly to `orchestrate`",
            "ordered list of Mission-authorized identities to `dispatch-tickets`",
        ),
        "skills/productivity/writing-great-skills/SKILL.md": (
            "Route one explicitly Mission-authorized Ticket directly to `orchestrate`",
            "ordered list of Mission-authorized identities to the active `dispatch-tickets`",
        ),
    }
    for relative, fragments in pointers.items():
        text = (ROOT / relative).read_text()
        require(text, relative, *fragments)

    for relative in (
        "skills/productivity/wormhole/SKILL.md",
        "skills/productivity/tmux-worker/SKILL.md",
    ):
        text = (ROOT / relative).read_text()
        assert "dispatch-tickets" not in text, (
            f"optional transport must not become a dispatcher route: {relative}"
        )


if __name__ == "__main__":
    check_canonical_domain_boundary()
    check_prompt_audit_completion_route()
    check_entry_point_pointers()
    print("Prompt Audit routing boundary ok")
