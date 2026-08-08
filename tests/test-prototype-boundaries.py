#!/usr/bin/env python3
"""Deterministic prompt-action and source-graph checks for prototype boundaries.

This repository distributes prompts rather than a host application. The UI fixture is
therefore the closest dependency-free equivalent of a production module graph and
route manifest: production entries are traversed exactly as build entries would be,
and prototype-only source-set modules must remain absent from that closure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = json.loads(
    (ROOT / "tests/fixtures/prototype-boundaries.json").read_text()
)
PROTOTYPE = (ROOT / "skills/engineering/prototype/SKILL.md").read_text()
UI = (ROOT / "skills/engineering/prototype/UI.md").read_text()
LOGIC = (ROOT / "skills/engineering/prototype/LOGIC.md").read_text()
WAYFINDER = (ROOT / "skills/engineering/wayfinder/SKILL.md").read_text()

PROTOTYPE_ACTIONS = {
    "create_throwaway_artifact",
    "run_throwaway_artifact",
    "record_decision",
}
PROMOTION_ACTIONS = {
    "edit_production",
    "implement_behavior_anew",
    "add_production_tests",
    "disconnect_ui_prototype",
    "verify_production_exclusion",
}
REPOSITORY_ACTIONS = {"write_tracker", "create_commit", "create_branch"}
AUTHORIZING_AUDITS = {"PASS", "BYPASS"}
REQUIRED_UI_ROLES = {
    "variant-subtree",
    "url-variant-selection",
    "switcher",
    "keyboard-controls",
    "throwaway-route",
    "route-registration",
}


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


def allowed_actions(case: dict[str, Any]) -> list[str]:
    authorized = set(case["contract_authorizations"])
    planning_only = (
        case["mode"] == "wayfinder"
        and not case["wayfinder_execution_authorized"]
    )
    execution_contract_authorized = (
        case["prompt_audit_status"] in AUTHORIZING_AUDITS
    )
    promotion_authorized = (
        execution_contract_authorized
        and case["mode"] == "promotion"
        and case["separate_promotion_unit"]
    )
    allowed: list[str] = []

    if not execution_contract_authorized:
        return allowed
    if case["mode"] == "promotion" and not promotion_authorized:
        return allowed

    for action in case["requested_actions"]:
        if action not in authorized or action == "copy_prototype_code":
            continue
        if action in PROTOTYPE_ACTIONS:
            allowed.append(action)
        elif action in PROMOTION_ACTIONS:
            if promotion_authorized and not planning_only:
                allowed.append(action)
        elif action in REPOSITORY_ACTIONS:
            if not planning_only:
                allowed.append(action)
        else:
            raise AssertionError(f"unknown fixture action: {action}")
    return allowed


def module_closure(graph: dict[str, Any], entries: list[str]) -> set[str]:
    modules = graph["modules"]
    pending = list(entries)
    visited: set[str] = set()
    while pending:
        module = pending.pop()
        expect(module in modules, f"source graph references missing module {module!r}")
        if module in visited:
            continue
        visited.add(module)
        pending.extend(modules[module]["imports"])
    return visited


def check_prompt_action_cases() -> None:
    observed_ids = set()
    for case in FIXTURE["prompt_action_cases"]:
        observed_ids.add(case["id"])
        expect(case["prompt"].strip(), f"prompt-action case {case['id']} has no prompt")
        expect(
            allowed_actions(case) == case["expected_allowed"],
            f"wrong authorized actions for {case['id']}",
        )

    for required in (
        "prototype-only-autonomous",
        "unaudited-prototype-stops",
        "separately-audited-promotion",
        "wayfinder-planning-only-composition",
    ):
        expect(required in observed_ids, f"missing prompt-action case {required!r}")


def check_ui_production_exclusion() -> None:
    graph = FIXTURE["ui_source_graph"]
    modules = graph["modules"]
    production = graph["production_build"]
    prototype = graph["prototype_build"]
    production_modules = module_closure(graph, production["entries"])
    prototype_modules = module_closure(graph, prototype["entries"])
    prototype_only_modules = {
        name
        for name, module in modules.items()
        if module["source_set"] == "prototype"
    }
    prototype_roles = {
        modules[name]["role"] for name in prototype_only_modules
    }

    expect(
        production_modules == set(production["expected_modules"]),
        "production module closure drifted",
    )
    expect(
        production_modules.isdisjoint(prototype_only_modules),
        "prototype-only module entered the production build graph",
    )
    expect(
        prototype_only_modules.issubset(prototype_modules),
        "prototype build fixture does not exercise its complete subtree",
    )
    expect(
        REQUIRED_UI_ROLES.issubset(prototype_roles),
        "UI fixture omits required prototype-only machinery",
    )
    expect(
        all(
            route["entry"] in production_modules
            and route["entry"] not in prototype_only_modules
            for route in production["route_manifest"]
        ),
        "prototype route or registration entered the production route manifest",
    )
    expect(
        all(
            route["entry"] in prototype_modules
            for route in prototype["route_manifest"]
        ),
        "prototype route manifest is disconnected from its source graph",
    )
    expect(
        all("runtime_condition" not in modules[name] for name in prototype_only_modules),
        "fixture models runtime disabling instead of source/build exclusion",
    )


def check_documented_contract() -> None:
    for phrase in (
        "current Prompt Audit `PASS` or explicit maintainer-authorized `BYPASS`",
        "missing, stale, or `FAIL` status stops before prototype creation or execution",
        "autonomously authorizes",
        "accepted question and repository scope",
        "production behavior changes",
        "tracker writes",
        "commits",
        "branch creation",
        "current execution contract already authorizes",
        "Do not ask for separate confirmation",
        "Production promotion is a separate repository implementation unit with its own current Prompt Audit",
        "implement the validated behavior anew",
        "do not copy prototype code directly",
        "add applicable tests",
        "production build, route manifest, bundle/module graph, or closest deterministic equivalent",
    ):
        expect(phrase in PROTOTYPE, f"prototype contract omits {phrase!r}")

    for phrase in (
        "source/build boundary",
        "production module and route graph",
        "standalone prototype-only harness or entrypoint",
        "variant components and subtrees",
        "URL variant-selection logic",
        "switcher",
        "keyboard controls",
        "throwaway route and route registration",
        "`NODE_ENV !== 'production'`",
        "insufficient",
        "remove or disconnect",
    ):
        expect(phrase in UI, f"UI prototype contract omits {phrase!r}")

    for phrase in (
        "prototype remains throwaway",
        "Do not lift or copy its source into production",
    ):
        expect(phrase in LOGIC, f"logic prototype contract omits {phrase!r}")

    for phrase in (
        "non-production and decision-bearing",
        "do not promote it or perform destination work",
    ):
        expect(phrase in WAYFINDER, f"Wayfinder composition omits {phrase!r}")

    expect(
        "Apply any validated decision to production code" not in PROTOTYPE,
        "prototype capture still auto-promotes production code",
    )
    expect(
        "Commit the prototype to a throwaway branch" not in PROTOTYPE,
        "prototype capture still auto-creates a branch",
    )
    expect(
        "gate on `process.env.NODE_ENV !== 'production'`" not in UI,
        "UI guidance still relies on runtime-only exclusion",
    )


def main() -> None:
    check_prompt_action_cases()
    check_ui_production_exclusion()
    check_documented_contract()
    print("prototype boundary tests ok")


if __name__ == "__main__":
    main()
