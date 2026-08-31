#!/usr/bin/env python3
"""Regression checks for the Prompt Audit-to-orchestration context boundary."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTEXT = (ROOT / "CONTEXT.md").read_text()
PROMPT_AUDIT = (
    ROOT / "skills/productivity/prompt-comprehension-audits/SKILL.md"
).read_text()
IMPLEMENT = (ROOT / "skills/engineering/implement/SKILL.md").read_text()
ORCHESTRATE = (ROOT / "skills/engineering/orchestrate/SKILL.md").read_text()
DISPATCH = (ROOT / "skills/engineering/dispatch-tickets/SKILL.md").read_text()
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
        "Prompt Audit and Ticket implementation are separate context units",
        "every accepted decision needed for delivery is durable in the audited Ticket or Agent Brief",
        "the audit conversation is not an implementation handoff",
        "then ends without implementation",
        "exactly one explicitly Mission-authorized, context-fit Ticket with a current `PASS` or `BYPASS`",
        "one fresh isolated **Ticket coordinator** running `orchestrate`",
        "An already-resolved ordered list of such authorized identities routes to the **Ticket dispatcher**",
        "starts one fresh coordinator per Ticket",
    )
    assert "prompt-comprehension-audits` owns the canonical" not in CONTEXT
    assert "Prompt Audit and Ticket implementation are separate context units" not in PROMPT_AUDIT


def validate_prompt_audit_completion(text: str) -> None:
    completion = section(text, "## Complete the audit context", "## Audit boundary")
    require(
        completion,
        "prompt-comprehension-audits completion route",
        "complete the current invocation through exactly one terminal branch",
        "`FAIL`",
        "stop before dispatch",
        "without Mission authorization",
        "report eligibility and stop before dispatch",
        "with explicit Mission authorization for this exact Ticket",
        "one fresh isolated context running installed `orchestrate`",
        "without another user intervention",
        "The current audit invocation performs no Ticket implementation",
    )
    bullets = [line for line in completion.splitlines() if line.startswith("- ")]
    assert len(bullets) == 3, "Prompt Audit must expose exactly three terminal branches"
    assert bullets[0].startswith("- `FAIL`")
    assert bullets[1].startswith("- `PASS` or `BYPASS` without Mission authorization")
    assert bullets[2].startswith(
        "- `PASS` or `BYPASS` with explicit Mission authorization for this exact Ticket"
    )
    implementation_lines = [
        line.strip()
        for line in completion.splitlines()
        if "implement" in line.lower()
    ]
    assert implementation_lines == [
        "The branch selection is the audit's terminal action. "
        "The current audit invocation performs no Ticket implementation. "
        "Every other audit returns its recorded status and ends."
    ], "Prompt Audit completion contains an implementation continuation"


def check_prompt_audit_completion_route() -> None:
    validate_prompt_audit_completion(PROMPT_AUDIT)
    assert "resume implementation" not in PROMPT_AUDIT.lower()
    completion = section(
        PROMPT_AUDIT,
        "## Complete the audit context",
        "## Audit boundary",
    )
    assert "dispatch-tickets" not in completion, (
        "one-Ticket Prompt Audit completion must route directly to orchestrate"
    )

    contradictory = PROMPT_AUDIT.replace(
        "## Audit boundary",
        "After PASS, implement the Ticket in this audit conversation.\n\n"
        "## Audit boundary",
        1,
    )
    try:
        validate_prompt_audit_completion(contradictory)
    except AssertionError:
        pass
    else:
        raise AssertionError("same-context audit-to-implementation regression was accepted")


def check_durable_fit_gate() -> None:
    require(
        PROMPT_AUDIT,
        "prompt-comprehension-audits durable contract",
        "make every accepted decision and boundary required for delivery durable in the final Ticket or Agent Brief",
        "the audit conversation is not an implementation handoff",
        "a fresh `orchestrate` Ticket coordinator can recover the complete execution contract from the Issue tracker",
    )
    require(
        PROMPT_AUDIT,
        "prompt-comprehension-audits fit gate",
        "Treat any semantic `PASS` or explicit `BYPASS` above as provisional",
        "one repository code or behavior-changing Ticket",
        "fit in one fresh agent context with room to understand the relevant behavior, implement the end-to-end change, and verify it",
        "choose `FAIL` and report that decomposition is required before autonomous delivery",
    )


def check_entry_point_pointers() -> None:
    require(
        IMPLEMENT,
        "skills/engineering/implement/SKILL.md",
        "load and follow installed `orchestrate` as the complete delivery contract",
        "fresh isolated Ticket coordinator",
        "only a routing pointer and performs no Ticket implementation",
        "this skill adds no alternate execution path",
    )
    require(
        ORCHESTRATE,
        "skills/engineering/orchestrate/SKILL.md",
        "Run as one fresh isolated depth-2 **Ticket coordinator**",
        "Accept exactly one explicitly Mission-authorized Ticket identity",
    )
    require(
        DISPATCH,
        "skills/engineering/dispatch-tickets/SKILL.md",
        "supplies one non-empty ordered list of unique identities",
        "performs no tracker, repository, or remote discovery",
        "every start creates a clean coordinator conversation",
        "stop before every remaining Ticket",
    )

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


if __name__ == "__main__":
    check_canonical_domain_boundary()
    check_prompt_audit_completion_route()
    check_durable_fit_gate()
    check_entry_point_pointers()
    print("Prompt Audit routing boundary ok")
