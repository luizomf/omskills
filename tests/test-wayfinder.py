#!/usr/bin/env python3
"""Deterministic disposable-map checks for the Wayfinder contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = json.loads((ROOT / "tests/fixtures/wayfinder.json").read_text())
WAYFINDER = (ROOT / "skills/engineering/wayfinder/SKILL.md").read_text()
SETUP = ROOT / "skills/engineering/setup-omskills"


TRANSITIONS = {
    "valid-frontier continuation",
    "blocked, claimed, or unresolved-fog handoff",
    "route-clear planning completion",
    "destination completion",
}
UNSAFE_PUBLIC_MARKERS = {
    "credential value:",
    "credential path:",
    "vault name:",
    "private filesystem location:",
    "private network location:",
    "secret identifier:",
    "private session identifier:",
}
UNSAFE_PUBLIC_PATTERNS = (
    r"(?:^|\s)/(?:users|home|private)(?:/|\b)",
    r"\b(?:localhost|127\.0\.0\.1|10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2})\b",
    r"\b(?:sk|ghp|glpat)-[a-z0-9_-]+\b",
    r"\bvault://",
    r"\bsecret[-_ ](?:id|identifier)\s*[:=]",
    r"\bsession[-_ ](?:id|identifier)\s*[:=]",
)


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


def public_safe(text: str) -> bool:
    lowered = text.lower()
    return not any(
        marker in lowered for marker in UNSAFE_PUBLIC_MARKERS
    ) and not any(re.search(pattern, lowered) for pattern in UNSAFE_PUBLIC_PATTERNS)


def provision_labels(
    case: dict[str, Any], managed: list[str]
) -> tuple[str, list[str], list[str]]:
    initial_inventory = list(case["initial_inventory"])
    reinventory = list(case["reinventory"])
    events = [
        f"inventory:{','.join(initial_inventory)}",
        f"reinventory:{','.join(reinventory)}",
    ]
    created: list[str] = []
    for label in managed:
        if label in reinventory:
            continue
        events.append(f"configured-create:{label}")
        if not case["create_results"].get(label, False):
            return (
                f"STOP: configured label creation failed for {label}",
                created,
                events,
            )
        created.append(label)

    events.append("verify")
    final_inventory = list(case["final_inventory"])
    if not all(label in final_inventory for label in managed):
        return "STOP: final Wayfinder label verification failed", created, events
    return "ready", created, events


def distinct_preclaims_are_safe(case: dict[str, Any]) -> bool:
    allocated = list(map(int, case["allocated_tickets"]))
    return len(allocated) >= 2 and len(allocated) == len(set(allocated))


def tracker_preflight(case: dict[str, Any]) -> str:
    tracker = case["configured"]
    if tracker is None:
        result = case["setup_result"]
        if result != "success":
            return f"STOP: tracker setup {result}"
        tracker = case["setup_selected"]
    if tracker is None:
        return "STOP: no Issue tracker selected"
    if not case["required_capabilities"]:
        return "STOP: required tracker capability unavailable"
    return str(tracker)


def by_number(children: list[dict[str, Any]], number: int) -> dict[str, Any] | None:
    return next((child for child in children if child["number"] == number), None)


def select_and_claim(case: dict[str, Any]) -> tuple[int | None, str]:
    if int(case["resolved_count"]) >= 1:
        return None, "session already resolved one Ticket"

    children = case["children"]
    distinct_preclaim = case["distinct_preclaim"]
    capabilities = set(case["documented_capabilities"])

    if case["atomic_requested"] and "atomic_claim" not in capabilities:
        return None, "atomic claim is undocumented"

    if case["mode"] == "named":
        candidate = by_number(children, int(case["named"]))
        if candidate is None:
            return None, "not an actual child"
    else:
        if case["concurrent_shared_identity"]:
            if distinct_preclaim is not None:
                candidate = by_number(children, int(distinct_preclaim))
                if candidate is None:
                    return None, "preclaim is not an actual child"
            elif case["atomic_requested"] and "atomic_claim" in capabilities:
                candidate = next(
                    (
                        child
                        for child in children
                        if child["state"] == "open"
                        and not child["blocked"]
                        and not child["assignees"]
                    ),
                    None,
                )
            else:
                return None, "concurrent automatic selection has no safe claim"
        else:
            candidate = next(
                (
                    child
                    for child in children
                    if child["state"] == "open"
                    and not child["blocked"]
                    and not child["assignees"]
                ),
                None,
            )
        if candidate is None:
            return None, "frontier is empty"

    number = int(candidate["number"])
    if candidate["state"] != "open":
        return None, "candidate is closed"
    if candidate["blocked"]:
        return None, "candidate is blocked"
    if candidate["assignees"]:
        if distinct_preclaim == number:
            return number, "selected"
        return None, "assignee is not session evidence"

    if case["concurrent_shared_identity"] and distinct_preclaim != number:
        if not (case["atomic_requested"] and "atomic_claim" in capabilities):
            return None, "concurrent candidate lacks distinct ownership"
    if "claim" not in capabilities:
        return None, "claim capability unavailable"
    if case["claim_result"] != "success":
        return None, "claim failed"

    reread = by_number(case["post_claim_children"], number)
    if reread is None:
        return None, "child scope changed after claim"
    if reread["state"] != "open":
        return None, "open state changed after claim"
    if reread["blocked"]:
        return None, "blocker state changed after claim"
    if reread["assignees"] != [case["claim_assignee"]]:
        return None, "ownership changed after claim"
    return number, "selected"


def reconcile_map(data: dict[str, Any]) -> dict[str, Any]:
    resolved = data["resolved"]
    actions = [
        f"answer:{resolved['number']}",
        f"close:{resolved['number']}",
        f"index:{resolved['number']}",
    ]
    decisions = [int(resolved["number"])]

    new_numbers = {int(ticket["number"]) for ticket in data["new_tickets"]}
    for ticket in data["new_tickets"]:
        actions.append(f"create:{ticket['number']}")
    for ticket in data["new_tickets"]:
        for blocker in ticket["blocked_by"]:
            expect(int(blocker) in new_numbers, "fixture blocker was not created first")
            actions.append(f"block:{ticket['number']}<-{blocker}")

    for ticket in data["invalidated"]:
        expect(ticket["action"] in {"update", "close"}, "invalid invalidation action")
        actions.append(f"{ticket['action']}:{ticket['number']}")

    out_of_scope: list[str] = []
    for ticket in data["out_of_scope_tickets"]:
        actions.extend(
            [f"close:{ticket['number']}", f"out-of-scope:{ticket['number']}"]
        )
        out_of_scope.append(f"ticket:{ticket['number']}")

    seen_fog: set[str] = set()
    remaining_fog: list[str] = []
    for item in data["fog"]:
        identifier = str(item["id"])
        expect(identifier not in seen_fog, f"fog item inspected twice: {identifier}")
        seen_fog.add(identifier)
        disposition = item["disposition"]
        expect(
            disposition in {"remain", "graduate", "resolved", "out-of-scope"},
            f"fog item has no supported disposition: {identifier}",
        )
        if disposition == "remain":
            remaining_fog.append(identifier)
        elif disposition == "graduate":
            expect(
                set(map(int, item["tickets"])).issubset(new_numbers),
                f"graduated fog has missing Ticket: {identifier}",
            )
        elif disposition == "out-of-scope":
            out_of_scope.append(f"fog:{identifier}")

    return {
        "actions": actions,
        "decisions": decisions,
        "remaining_fog": remaining_fog,
        "out_of_scope": out_of_scope,
        "inspected_fog": sorted(seen_fog),
    }


def execution_authorized(notes: str) -> bool:
    return re.search(r"(?mi)^Execution authorized:\s*\S", notes) is not None


def completion_transition(case: dict[str, Any]) -> dict[str, Any]:
    frontier = [
        child
        for child in case["open_children"]
        if not child["blocked"] and not child["claimed"]
    ]
    if frontier:
        transition = "valid-frontier continuation"
        actions = ["comment-map", "handoff"]
    elif case["open_children"] or case["fog"]:
        transition = "blocked, claimed, or unresolved-fog handoff"
        actions = ["comment-map", "handoff"]
    elif case["execution_authorized"] and case["destination_reached"]:
        transition = "destination completion"
        actions = ["comment-map", "close-map"]
    elif case["execution_authorized"] and not case["destination_reached"]:
        transition = "blocked, claimed, or unresolved-fog handoff"
        actions = ["comment-map", "handoff"]
    elif case["route_clear"] and case["handoff"]:
        transition = "route-clear planning completion"
        actions = ["comment-map", "handoff", "close-map"]
    else:
        transition = "blocked, claimed, or unresolved-fog handoff"
        actions = ["comment-map", "handoff"]

    comment = (
        "## Wayfinder transition\n\n"
        f"**Transition:** {transition}\n"
        f"**State:** {case['state']}\n"
        f"**Handoff:** {case['handoff']}"
    )
    return {"transition": transition, "actions": actions, "comments": [comment]}


def check_fixed_labels_and_tracker_preflight() -> None:
    managed = FIXTURE["labels"]["managed"]
    table_labels = re.findall(r"(?m)^\| `(wayfinder:[^`]+)` \|", WAYFINDER)
    expect(table_labels == managed, "Wayfinder does not own the exact five-label inventory")
    for case in FIXTURE["label_provisioning_cases"]:
        status, created, events = provision_labels(case, managed)
        expect(status == case["expected_status"], f"wrong label status for {case['id']}")
        expect(created == case["expected_created"], f"wrong created labels for {case['id']}")
        expect(
            events[0].startswith("inventory:")
            and events[1].startswith("reinventory:"),
            f"creation preceded re-inventory for {case['id']}",
        )
        reinventory = set(case["reinventory"])
        expect(
            all(label not in reinventory for label in created),
            f"existing label was recreated for {case['id']}",
        )
        if status == "ready":
            expect(events[-1] == "verify", f"final inventory was not verified for {case['id']}")
            expect(
                reinventory.issubset(set(case["final_inventory"])),
                f"unrelated label was removed for {case['id']}",
            )
    expect(
        FIXTURE["labels"]["local_types"]
        == ["research", "prototype", "grilling", "task"],
        "local type fields drifted",
    )

    setup_skill = (SETUP / "SKILL.md").read_text()
    expect(
        not all(label in setup_skill for label in managed),
        "setup gained a reverse inventory of Wayfinder consumer labels",
    )
    for case in FIXTURE["tracker_preflight"]:
        expect(
            tracker_preflight(case) == case["expected"],
            f"wrong tracker preflight result for {case['id']}",
        )
    failed_with_local = next(
        case
        for case in FIXTURE["tracker_preflight"]
        if case["id"] == "failed-setup-does-not-fallback"
    )
    expect(
        failed_with_local["local_available"]
        and tracker_preflight(failed_with_local).startswith("STOP:"),
        "failed hosted setup fell back to local Markdown",
    )


def check_selection_and_claims() -> None:
    for case in FIXTURE["selection_cases"]:
        selected, reason = select_and_claim(case)
        expect(selected == case["expected"], f"wrong selection for {case['id']}")
        expect(reason == case["expected_reason"], f"wrong stop reason for {case['id']}: {reason}")
    for case in FIXTURE["concurrent_preclaim_cases"]:
        expect(
            distinct_preclaims_are_safe(case) == case["expected_safe"],
            f"wrong concurrent preclaim result for {case['id']}",
        )


def check_reconciliation() -> None:
    data = FIXTURE["reconciliation"]
    result = reconcile_map(data)
    expect(result["actions"] == data["expected_actions"], "map reconciliation order is wrong")
    expect(result["decisions"] == data["expected_decisions"], "decision index is wrong")
    expect(result["remaining_fog"] == data["expected_remaining_fog"], "fog reconciliation is wrong")
    expect(result["out_of_scope"] == data["expected_out_of_scope"], "out-of-scope reconciliation is wrong")
    expect(
        len(result["inspected_fog"]) == len(data["fog"]),
        "not every fog item was inspected exactly once",
    )
    create_positions = [
        result["actions"].index(action)
        for action in result["actions"]
        if action.startswith("create:")
    ]
    blocker_positions = [
        result["actions"].index(action)
        for action in result["actions"]
        if action.startswith("block:")
    ]
    expect(max(create_positions) < min(blocker_positions), "blocker edge preceded child creation")
    expect(204 not in result["decisions"], "out-of-scope Ticket became a decision")


def check_public_output_and_plan_default() -> None:
    public = FIXTURE["public_output"]
    expect(all(public_safe(text) for text in public["safe"]), "safe fixture output was rejected")
    expect(all(not public_safe(text) for text in public["unsafe"]), "unsafe fixture output reached the tracker")
    expect(
        set(public["allowed_task_fields"])
        == {"capability availability", "access requirements", "public URLs", "result facts"},
        "Task public fields are not exact",
    )
    for case in FIXTURE["plan_cases"]:
        expect(
            execution_authorized(case["notes"]) == case["execution_authorized"],
            f"wrong plan/execute interpretation for {case['id']}",
        )
    expect(not FIXTURE["prototype_result"]["production"], "Wayfinder prototype became production work")
    expect(FIXTURE["prototype_result"]["decision_bearing"], "Wayfinder prototype lost its decision")


def check_completion_transitions() -> None:
    observed: set[str] = set()
    for case in FIXTURE["transition_cases"]:
        result = completion_transition(case)
        observed.add(result["transition"])
        expect(
            result["transition"] == case["expected_transition"],
            f"wrong completion transition for {case['id']}",
        )
        expect(result["actions"] == case["expected_actions"], f"wrong transition actions for {case['id']}")
        expect(len(result["comments"]) == 1, f"transition was not recorded exactly once for {case['id']}")
        expect(public_safe(result["comments"][0]), f"transition comment is not public-safe for {case['id']}")
        if result["transition"] == "destination completion":
            expect(case["execution_authorized"] and case["destination_reached"], "destination completed without authority or result")
        if result["transition"] == "route-clear planning completion":
            expect(not case["execution_authorized"], "planning completion executed the destination")
            expect(result["actions"].index("handoff") < result["actions"].index("close-map"), "planning map closed before destination handoff")

    expect(observed == TRANSITIONS, "fixtures do not exercise all four completion transitions")
    for case_id in (
        "empty-frontier-blocked-child",
        "empty-frontier-claimed-child",
        "empty-frontier-unresolved-fog",
        "empty-frontier-unmet-destination",
    ):
        case = next(case for case in FIXTURE["transition_cases"] if case["id"] == case_id)
        transition = completion_transition(case)["transition"]
        expect(transition not in {"route-clear planning completion", "destination completion"}, f"empty non-complete map completed: {case_id}")


def check_documented_contract() -> None:
    github = (SETUP / "issue-tracker-github.md").read_text()
    gitlab = (SETUP / "issue-tracker-gitlab.md").read_text()
    local = (SETUP / "issue-tracker-local.md").read_text()
    current = (ROOT / "docs/agents/issue-tracker.md").read_text()

    for phrase in (
        "The configuration is a hard dependency",
        "Never switch to local Markdown or another tracker",
        "A capability exists only when the selected configuration documents it",
        "immediately re-read child scope, open state, blockers, and ownership",
        "assignee identity alone is never session evidence",
        "distinct preclaim",
        "explicitly documents as atomic",
        "Resolve at most one Ticket",
        "non-production and decision-bearing",
        "every item in **Not yet specified**",
        "exactly one public-safe comment on the authoritative map",
        "Missing execution authorization never permits destination completion",
    ):
        expect(phrase in WAYFINDER, f"Wayfinder contract omits {phrase!r}")
    for phrase in (
        "credential values or paths",
        "vault names",
        "private filesystem or network locations",
        "secret identifiers",
        "private session identifiers",
    ):
        expect(phrase in WAYFINDER, f"public tracker boundary omits {phrase!r}")
    expect("If no tracker is available after that, use local markdown" not in WAYFINDER, "local Markdown fallback remains")

    answer = WAYFINDER.index("post the public-safe answer")
    close = WAYFINDER.index("and close it", answer)
    index = WAYFINDER.index("Update the map's **Decisions so far**", close)
    reconcile = WAYFINDER.index("Reconcile the complete resulting map state", index)
    transition = WAYFINDER.index("record one completion transition", reconcile)
    expect(answer < close < index < reconcile < transition, "post-resolution order is not deterministic")

    for name, document in (("GitHub", github), ("GitLab", gitlab), ("current GitHub", current)):
        for phrase in (
            "Inventory labels",
            "Create one approved missing label",
            "## Wayfinding operations",
            "**Claim:**",
            "**Resolve:**",
            "**Comment:**",
            "**Close:**",
        ):
            expect(phrase in document, f"{name} configuration omits {phrase!r}")
    expect("Type: research|prototype|grilling|task" in local, "local tracker type field is missing")
    expect("No hosted label operation applies" in local, "local tracker can invent hosted labels")
    expect("configured `map.md` identity when local Markdown is selected" in WAYFINDER, "Wayfinder requires a hosted map label for local Markdown")
    expect("apply `wayfinder:map` only when" in WAYFINDER, "Wayfinder applies a map label unconditionally")
    expect("## Comments" in local and "Closing an item" in local, "local comments or closure are missing")


def main() -> None:
    check_fixed_labels_and_tracker_preflight()
    check_selection_and_claims()
    check_reconciliation()
    check_public_output_and_plan_default()
    check_completion_transitions()
    check_documented_contract()
    print("wayfinder tests ok")


if __name__ == "__main__":
    main()
