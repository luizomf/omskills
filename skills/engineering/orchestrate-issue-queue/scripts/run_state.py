#!/usr/bin/env python3
"""Maintain a safe issue-queue snapshot and append-only diagnostic log."""

from __future__ import annotations

import argparse
import copy
import fcntl
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator


SCHEMA_VERSION = 2
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SAFE_TEXT_PATTERN = re.compile(r"^[^\x00-\x1f\x7f]{1,500}$")
SHA_PATTERN = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
REVIEW_ROLES = {
    "single": ("reviewer",),
    "dual": ("adversarial", "standards-spec"),
}


class StateError(Exception):
    """Report a rejected orchestration state transition."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_state_root() -> Path:
    base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return base / "codex" / "orchestrate-issue-queue"


def validate_run_id(run_id: str) -> str:
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise StateError(
            f'Invalid run id "{run_id}". Use 1-128 letters, digits, dots, underscores, or hyphens.'
        )
    return run_id


def validate_text(value: str, field: str) -> str:
    if not SAFE_TEXT_PATTERN.fullmatch(value):
        raise StateError(f'Invalid {field} "{value}". Use 1-500 printable characters on one line.')
    return value


def validate_sha(value: str) -> str:
    if not SHA_PATTERN.fullmatch(value):
        raise StateError(
            f'Invalid remote SHA "{value}". Expected a full 40- or 64-character hexadecimal commit id.'
        )
    return value.lower()


def integer_between(minimum: int, maximum: int) -> Callable[[str], int]:
    def parse(value: str) -> int:
        try:
            number = int(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError(f'Expected an integer, received "{value}".') from error
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(
                f'Expected an integer from {minimum} through {maximum}, received "{value}".'
            )
        return number

    return parse


def run_directory(state_root: Path, run_id: str) -> Path:
    validate_run_id(run_id)
    root = state_root.expanduser().resolve()
    target = (root / run_id).resolve()
    if target.parent != root:
        raise StateError(f'Run path "{target}" escapes state root "{root}".')
    return target


@contextmanager
def locked_run(run_dir: Path) -> Iterator[None]:
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / ".lock").open("a", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        yield


def read_state(run_dir: Path) -> dict[str, Any]:
    state_path = run_dir / "state.json"
    if not state_path.exists():
        raise StateError(f'Run state not found at "{state_path}".')
    with state_path.open(encoding="utf-8") as state_file:
        state = json.load(state_file)
    if state.get("schema_version") != SCHEMA_VERSION:
        raise StateError(
            f'Unsupported schema version "{state.get("schema_version")}". Expected {SCHEMA_VERSION}.'
        )
    return state


def write_state(run_dir: Path, state: dict[str, Any]) -> None:
    state_path = run_dir / "state.json"
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix="state.", suffix=".tmp", dir=run_dir
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as temporary_file:
            json.dump(state, temporary_file, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_name, state_path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def last_event_sequence(run_dir: Path) -> int:
    events_path = run_dir / "events.jsonl"
    if not events_path.exists():
        return 0
    last_line = ""
    with events_path.open(encoding="utf-8") as events_file:
        for line in events_file:
            if line.strip():
                last_line = line
    if not last_line:
        return 0
    return int(json.loads(last_line)["sequence"])


def append_event(
    run_dir: Path,
    state: dict[str, Any],
    event_name: str,
    metadata: dict[str, Any] | None = None,
) -> int:
    sequence = max(state.get("event_sequence", 0), last_event_sequence(run_dir)) + 1
    event: dict[str, Any] = {
        "sequence": sequence,
        "timestamp": utc_now(),
        "run_id": state["run_id"],
        "event": event_name,
    }
    if state.get("active_issue") is not None:
        event["active_issue"] = state["active_issue"]
    if metadata:
        event.update({key: value for key, value in metadata.items() if value is not None})
    with (run_dir / "events.jsonl").open("a", encoding="utf-8") as events_file:
        events_file.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        events_file.flush()
        os.fsync(events_file.fileno())
    return sequence


def find_issue(state: dict[str, Any], issue_id: str) -> dict[str, Any]:
    for issue in state["queue"]:
        if issue["id"] == issue_id:
            return issue
    raise StateError(f'Issue "{issue_id}" is not part of run "{state["run_id"]}".')


def require_active_issue(state: dict[str, Any], issue_id: str) -> dict[str, Any]:
    if state["status"] != "active":
        raise StateError(f'Run status is "{state["status"]}", not "active".')
    if state["active_issue"] != issue_id:
        raise StateError(
            f'Issue "{issue_id}" is not active. Current active issue: "{state["active_issue"]}".'
        )
    issue = find_issue(state, issue_id)
    if issue["status"] != "active":
        raise StateError(f'Issue "{issue_id}" status is "{issue["status"]}", not "active".')
    return issue


def current_review_round(issue: dict[str, Any]) -> dict[str, Any]:
    if not issue["review_rounds"]:
        raise StateError(f'Issue "{issue["id"]}" has no review round.')
    return issue["review_rounds"][-1]


def required_roles(state: dict[str, Any]) -> tuple[str, ...]:
    return REVIEW_ROLES[state["review_policy"]]


def mutate(
    state_root: Path,
    run_id: str,
    mutation: Callable[[dict[str, Any]], tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    run_dir = run_directory(state_root, run_id)
    with locked_run(run_dir):
        state = read_state(run_dir)
        candidate = copy.deepcopy(state)
        try:
            event_name, metadata = mutation(candidate)
        except StateError as error:
            requested_operation = (
                mutation.__qualname__.split(".<locals>", 1)[0]
                .removeprefix("command_")
                .replace("_", "-")
            )
            append_event(
                run_dir,
                state,
                "transition_rejected",
                {
                    "reason": str(error),
                    "requested_run_id": run_id,
                    "requested_operation": requested_operation,
                },
            )
            raise
        candidate["updated_at"] = utc_now()
        candidate["event_sequence"] = append_event(
            run_dir, candidate, event_name, metadata
        )
        write_state(run_dir, candidate)
        return candidate


def new_issue(issue_id: str, active: bool) -> dict[str, Any]:
    return {
        "id": issue_id,
        "status": "active" if active else "pending",
        "phase": "preflight" if active else "queued",
        "branch": None,
        "pr": None,
        "remote_sha": None,
        "review_rounds": [],
        "review_status": None,
        "verification": None,
        "active_writer": None,
        "writer_agents": [],
        "reviewer_agents": [],
        "correction_attempts": 0,
        "awaiting": None,
        "next_action": "perform_preflight" if active else "wait_for_predecessor",
        "merged": False,
        "closed": False,
    }


def command_init(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = run_directory(args.state_root, args.run_id)
    issue_ids = [validate_text(issue, "issue id") for issue in args.issues]
    if len(set(issue_ids)) != len(issue_ids):
        raise StateError("Issue queue contains duplicate identifiers.")
    validate_text(args.repository, "repository")
    if not args.goal.strip():
        raise StateError("Goal must not be empty.")
    with locked_run(run_dir):
        if (run_dir / "state.json").exists():
            raise StateError(f'Run "{args.run_id}" already exists at "{run_dir}".')
        now = utc_now()
        state = {
            "schema_version": SCHEMA_VERSION,
            "run_id": args.run_id,
            "repository": args.repository,
            "goal": args.goal,
            "status": "active",
            "goal_status": "none",
            "goal_pause_reason": None,
            "review_policy": args.review_policy,
            "max_correction_attempts": args.max_corrections,
            "active_issue": issue_ids[0],
            "queue": [new_issue(issue_id, index == 0) for index, issue_id in enumerate(issue_ids)],
            "created_at": now,
            "updated_at": now,
            "event_sequence": 0,
        }
        state["event_sequence"] = append_event(
            run_dir,
            state,
            "run_initialized",
            {
                "repository": args.repository,
                "issue_count": len(issue_ids),
                "review_policy": args.review_policy,
                "max_correction_attempts": args.max_corrections,
            },
        )
        write_state(run_dir, state)
        return state


def command_dispatch_implementation(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "preflight" or issue["next_action"] != "dispatch_implementer":
            raise StateError(
                f'Issue "{args.issue}" cannot dispatch implementation from phase '
                f'"{issue["phase"]}" with next action "{issue["next_action"]}".'
            )
        agent_id = validate_text(args.agent_id, "agent id")
        if agent_id in issue["writer_agents"] or agent_id in issue["reviewer_agents"]:
            raise StateError(f'Agent "{agent_id}" is not fresh for issue "{args.issue}".')
        issue["writer_agents"].append(agent_id)
        issue.update(
            phase="implementing",
            awaiting="implementer",
            next_action="wait_for_implementation",
            active_writer=agent_id,
        )
        return "implementation_dispatched", {
            "issue": args.issue,
            "phase": issue["phase"],
            "agent_id": agent_id,
        }

    return mutate(args.state_root, args.run_id, change)


def command_record_preflight(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "preflight" or issue["next_action"] != "perform_preflight":
            raise StateError(
                f'Issue "{args.issue}" cannot record preflight from phase '
                f'"{issue["phase"]}" with next action "{issue["next_action"]}".'
            )
        issue["next_action"] = "dispatch_implementer"
        return "preflight_completed", {
            "issue": args.issue,
            "phase": issue["phase"],
            "next_action": issue["next_action"],
        }

    return mutate(args.state_root, args.run_id, change)


def command_deliver(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        previous_phase = issue["phase"]
        if previous_phase not in {"implementing", "correcting"}:
            raise StateError(
                f'Issue "{args.issue}" cannot deliver from phase "{previous_phase}".'
            )
        agent_id = validate_text(args.agent_id, "agent id")
        if agent_id != issue["active_writer"]:
            raise StateError(
                f'Delivery agent "{agent_id}" differs from active writer "{issue["active_writer"]}".'
            )
        sha = validate_sha(args.sha)
        if args.branch:
            issue["branch"] = validate_text(args.branch, "branch")
        if args.pr:
            issue["pr"] = validate_text(args.pr, "PR")
        if not issue["branch"] or not issue["pr"]:
            raise StateError(
                f'Issue "{args.issue}" needs both branch and PR before review.'
            )
        issue["remote_sha"] = sha
        issue["phase"] = "reviewing"
        issue["review_status"] = "pending"
        issue["verification"] = None
        issue["active_writer"] = None
        issue["awaiting"] = "reviewer_dispatch"
        issue["next_action"] = "dispatch_reviewers"
        issue["review_rounds"].append(
            {
                "round": len(issue["review_rounds"]) + 1,
                "sha": sha,
                "required_roles": list(required_roles(state)),
                "dispatches": {},
                "results": {},
                "status": "pending",
            }
        )
        event_name = (
            "implementation_delivered"
            if previous_phase == "implementing"
            else "correction_delivered"
        )
        return event_name, {
            "issue": args.issue,
            "phase": issue["phase"],
            "branch": issue["branch"],
            "pr": issue["pr"],
            "remote_sha": sha,
            "review_round": len(issue["review_rounds"]),
            "agent_id": agent_id,
        }

    return mutate(args.state_root, args.run_id, change)


def command_dispatch_review(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "reviewing":
            raise StateError(f'Issue "{args.issue}" is not in review.')
        sha = validate_sha(args.sha)
        if sha != issue["remote_sha"]:
            raise StateError(
                f'Reviewer dispatch SHA "{sha}" differs from current remote SHA "{issue["remote_sha"]}".'
            )
        roles = required_roles(state)
        if args.role not in roles:
            raise StateError(
                f'Review role "{args.role}" is invalid for policy "{state["review_policy"]}". '
                f'Expected one of: {", ".join(roles)}.'
            )
        agent_id = validate_text(args.agent_id, "agent id")
        if agent_id in issue["writer_agents"] or agent_id in issue["reviewer_agents"]:
            raise StateError(f'Agent "{agent_id}" is not a fresh reviewer for issue "{args.issue}".')
        review_round = current_review_round(issue)
        if args.role in review_round["dispatches"]:
            raise StateError(f'Review role "{args.role}" was already dispatched for SHA "{sha}".')
        review_round["dispatches"][args.role] = {
            "agent_id": agent_id,
            "dispatched_at": utc_now(),
        }
        issue["reviewer_agents"].append(agent_id)
        missing_dispatches = [role for role in roles if role not in review_round["dispatches"]]
        if missing_dispatches:
            issue["awaiting"] = "reviewer_dispatch"
            issue["next_action"] = "dispatch_reviewers"
        else:
            issue["awaiting"] = "reviews"
            issue["next_action"] = "wait_for_reviews"
        return "reviewer_dispatched", {
            "issue": args.issue,
            "phase": issue["phase"],
            "reviewed_sha": sha,
            "review_round": review_round["round"],
            "role": args.role,
            "agent_id": agent_id,
            "missing_dispatches": missing_dispatches,
            "next_action": issue["next_action"],
        }

    return mutate(args.state_root, args.run_id, change)


def command_record_review(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "reviewing":
            raise StateError(f'Issue "{args.issue}" is not in review.')
        sha = validate_sha(args.sha)
        if sha != issue["remote_sha"]:
            raise StateError(
                f'Review SHA "{sha}" differs from current remote SHA "{issue["remote_sha"]}".'
            )
        roles = required_roles(state)
        if args.role not in roles:
            raise StateError(
                f'Review role "{args.role}" is invalid for policy "{state["review_policy"]}". '
                f'Expected one of: {", ".join(roles)}.'
            )
        if args.outcome == "passed" and args.blocking_findings:
            raise StateError("A passed review cannot contain blocking findings.")
        if args.outcome == "blocked" and args.blocking_findings < 1:
            raise StateError("A blocked review must contain at least one blocking finding.")
        review_round = current_review_round(issue)
        if review_round["sha"] != sha:
            raise StateError(
                f'Review round SHA "{review_round["sha"]}" differs from submitted SHA "{sha}".'
            )
        missing_dispatches = [role for role in roles if role not in review_round["dispatches"]]
        if missing_dispatches:
            raise StateError(
                "Cannot record reviews before all required roles are dispatched: "
                + ", ".join(missing_dispatches)
                + "."
            )
        dispatched_agent = review_round["dispatches"][args.role]["agent_id"]
        agent_id = validate_text(args.agent_id, "agent id")
        if agent_id != dispatched_agent:
            raise StateError(
                f'Review result agent "{agent_id}" differs from dispatched agent "{dispatched_agent}".'
            )
        if args.role in review_round["results"]:
            raise StateError(
                f'Role "{args.role}" already recorded a result for SHA "{sha}".'
            )
        review_round["results"][args.role] = {
            "outcome": args.outcome,
            "blocking_findings": args.blocking_findings,
            "agent_id": agent_id,
            "recorded_at": utc_now(),
        }
        missing_roles = [role for role in roles if role not in review_round["results"]]
        if missing_roles:
            issue["awaiting"] = "reviews"
            issue["next_action"] = "wait_for_reviews"
        else:
            outcomes = [result["outcome"] for result in review_round["results"].values()]
            if all(outcome == "passed" for outcome in outcomes):
                review_round["status"] = "passed"
                issue["review_status"] = "passed"
                issue["awaiting"] = None
                issue["next_action"] = "verify_current_sha"
            else:
                review_round["status"] = "blocked"
                issue["review_status"] = "blocked"
                if issue["correction_attempts"] >= state["max_correction_attempts"]:
                    issue["awaiting"] = "human_decision"
                    issue["next_action"] = "request_human_decision"
                    state["goal_status"] = "paused"
                    state["goal_pause_reason"] = "automatic correction limit reached"
                else:
                    issue["awaiting"] = None
                    issue["next_action"] = "dispatch_corrector"
        return "review_recorded", {
            "issue": args.issue,
            "phase": issue["phase"],
            "reviewed_sha": sha,
            "review_round": review_round["round"],
            "role": args.role,
            "outcome": args.outcome,
            "blocking_findings": args.blocking_findings,
            "missing_roles": missing_roles,
            "round_status": review_round["status"],
            "next_action": issue["next_action"],
        }

    return mutate(args.state_root, args.run_id, change)


def command_record_verification(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "reviewing" or issue["review_status"] != "passed":
            raise StateError(f'Issue "{args.issue}" has not passed its current review barrier.')
        sha = validate_sha(args.sha)
        if sha != issue["remote_sha"]:
            raise StateError(
                f'Verification SHA "{sha}" differs from current remote SHA "{issue["remote_sha"]}".'
            )
        checks = [validate_text(check, "check name") for check in args.checks]
        if len(set(checks)) != len(checks):
            raise StateError("Verification contains duplicate check names.")
        issue["verification"] = {
            "sha": sha,
            "outcome": args.outcome,
            "checks": checks,
            "recorded_at": utc_now(),
        }
        if args.outcome == "passed":
            issue["awaiting"] = None
            issue["next_action"] = "adjudicate_and_merge"
        elif issue["correction_attempts"] >= state["max_correction_attempts"]:
            issue["awaiting"] = "human_decision"
            issue["next_action"] = "request_human_decision"
            state["goal_status"] = "paused"
            state["goal_pause_reason"] = "automatic correction limit reached"
        else:
            issue["awaiting"] = None
            issue["next_action"] = "dispatch_corrector"
        return "verification_recorded", {
            "issue": args.issue,
            "phase": issue["phase"],
            "verified_sha": sha,
            "outcome": args.outcome,
            "checks": checks,
            "next_action": issue["next_action"],
        }

    return mutate(args.state_root, args.run_id, change)


def command_dispatch_correction(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "reviewing" or issue["next_action"] != "dispatch_corrector":
            raise StateError(
                f'Issue "{args.issue}" is not ready to dispatch a corrector; '
                f'next action is "{issue["next_action"]}".'
            )
        if issue["correction_attempts"] >= state["max_correction_attempts"]:
            raise StateError(
                f'Issue "{args.issue}" exhausted its {state["max_correction_attempts"]} '
                "automatic correction attempts."
            )
        agent_id = validate_text(args.agent_id, "agent id")
        if agent_id in issue["writer_agents"] or agent_id in issue["reviewer_agents"]:
            raise StateError(f'Agent "{agent_id}" is not fresh for issue "{args.issue}".')
        issue["writer_agents"].append(agent_id)
        issue["correction_attempts"] += 1
        issue["phase"] = "correcting"
        issue["awaiting"] = "corrector"
        issue["next_action"] = "wait_for_correction"
        issue["active_writer"] = agent_id
        return "correction_dispatched", {
            "issue": args.issue,
            "phase": issue["phase"],
            "attempt": issue["correction_attempts"],
            "agent_id": agent_id,
        }

    return mutate(args.state_root, args.run_id, change)


def command_mark_merged(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        if issue["phase"] != "reviewing" or issue["review_status"] != "passed":
            raise StateError(f'Issue "{args.issue}" has not passed its current review barrier.')
        sha = validate_sha(args.sha)
        if sha != issue["remote_sha"]:
            raise StateError(
                f'Merge SHA "{sha}" differs from reviewed remote SHA "{issue["remote_sha"]}".'
            )
        review_round = current_review_round(issue)
        if review_round["sha"] != sha or review_round["status"] != "passed":
            raise StateError(f'SHA "{sha}" does not have a passing review round.')
        verification = issue["verification"]
        if not verification or verification["sha"] != sha or verification["outcome"] != "passed":
            raise StateError(f'SHA "{sha}" does not have passing repository verification.')
        if not args.issue_closed:
            raise StateError(f'Issue "{args.issue}" closure was not confirmed.')
        issue.update(
            status="done",
            phase="done",
            awaiting=None,
            next_action="none",
            merged=True,
            closed=True,
        )
        next_issue = next(
            (queued_issue for queued_issue in state["queue"] if queued_issue["status"] == "pending"),
            None,
        )
        if next_issue:
            next_issue.update(
                status="active",
                phase="preflight",
                next_action="perform_preflight",
            )
            state["active_issue"] = next_issue["id"]
        else:
            state["active_issue"] = None
            state["status"] = "complete"
            state["goal_status"] = "none"
            state["goal_pause_reason"] = None
        return "issue_merged", {
            "issue": args.issue,
            "active_issue": args.issue,
            "active_issue_after": state["active_issue"],
            "phase": issue["phase"],
            "merged_sha": sha,
            "next_issue": state["active_issue"],
            "run_status": state["status"],
        }

    return mutate(args.state_root, args.run_id, change)


def command_goal_pause(args: argparse.Namespace) -> dict[str, Any]:
    reason = validate_text(args.reason, "pause reason")

    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if state["status"] != "active":
            raise StateError(f'Cannot pause Goal mode for run status "{state["status"]}".')
        state["goal_status"] = "paused"
        state["goal_pause_reason"] = reason
        return "goal_paused", {"reason": reason, "issue": state["active_issue"]}

    return mutate(args.state_root, args.run_id, change)


def command_goal_resume(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if state["status"] != "active":
            raise StateError(f'Cannot resume Goal mode for run status "{state["status"]}".')
        issue = find_issue(state, state["active_issue"])
        if issue["awaiting"] == "human_decision":
            raise StateError("Human authorization is required before Goal mode can resume.")
        state["goal_status"] = "active"
        state["goal_pause_reason"] = None
        return "goal_resumed", {
            "issue": state["active_issue"],
            "next_action": issue["next_action"],
        }

    return mutate(args.state_root, args.run_id, change)


def command_authorize_correction(args: argparse.Namespace) -> dict[str, Any]:
    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = find_issue(state, args.issue)
        waiting_for_decision = (
            state["status"] == "active"
            and state["active_issue"] == args.issue
            and issue["status"] == "active"
            and issue["awaiting"] == "human_decision"
        )
        resumable_blocked_run = (
            state["status"] == "blocked"
            and state["active_issue"] == args.issue
            and issue["status"] == "blocked"
            and issue["phase"] == "blocked"
            and issue["next_action"] == "human_intervention_required"
            and issue["review_status"] == "blocked"
            and issue["active_writer"] is None
        )
        if not waiting_for_decision and not resumable_blocked_run:
            raise StateError(f'Issue "{args.issue}" is not waiting for human correction authorization.')
        if resumable_blocked_run:
            state["status"] = "active"
            issue["status"] = "active"
            issue["phase"] = "reviewing"
        state["max_correction_attempts"] += args.additional_attempts
        issue["awaiting"] = None
        issue["next_action"] = "dispatch_corrector"
        return "additional_correction_authorized", {
            "issue": args.issue,
            "additional_attempts": args.additional_attempts,
            "max_correction_attempts": state["max_correction_attempts"],
            "resumed_blocked_run": resumable_blocked_run,
        }

    return mutate(args.state_root, args.run_id, change)


def command_block_run(args: argparse.Namespace) -> dict[str, Any]:
    reason = validate_text(args.reason, "block reason")

    def change(state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        issue = require_active_issue(state, args.issue)
        issue.update(
            status="blocked",
            phase="blocked",
            awaiting=None,
            next_action="human_intervention_required",
        )
        state["status"] = "blocked"
        state["goal_status"] = "none"
        state["goal_pause_reason"] = None
        return "run_blocked", {"issue": args.issue, "phase": "blocked", "reason": reason}

    return mutate(args.state_root, args.run_id, change)


def command_show(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = run_directory(args.state_root, args.run_id)
    with locked_run(run_dir):
        return read_state(run_dir)


def summarize_state(state: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "run_id": state["run_id"],
        "status": state["status"],
        "goal_status": state["goal_status"],
        "active_issue": state["active_issue"],
        "event_sequence": state["event_sequence"],
    }
    if state["active_issue"] is not None:
        issue = find_issue(state, state["active_issue"])
        summary["active_issue_state"] = {
            "phase": issue["phase"],
            "awaiting": issue["awaiting"],
            "next_action": issue["next_action"],
            "remote_sha": issue["remote_sha"],
        }
    return summary


def add_run_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("run_id")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root", type=Path, default=default_state_root())
    parser.add_argument(
        "--full-state",
        action="store_true",
        help="Print the complete snapshot after a mutation; show always prints it.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Create a new queue run")
    add_run_argument(init)
    init.add_argument("--repository", required=True)
    init.add_argument("--goal", required=True)
    init.add_argument("--issues", nargs="+", required=True)
    init.add_argument("--review-policy", choices=tuple(REVIEW_ROLES), default="single")
    init.add_argument(
        "--max-corrections",
        type=integer_between(0, 100),
        metavar="0..100",
        default=1,
    )
    init.set_defaults(action=command_init)

    dispatch = commands.add_parser("dispatch-implementation")
    add_run_argument(dispatch)
    dispatch.add_argument("issue")
    dispatch.add_argument("--agent-id", required=True)
    dispatch.set_defaults(action=command_dispatch_implementation)

    preflight = commands.add_parser("record-preflight")
    add_run_argument(preflight)
    preflight.add_argument("issue")
    preflight.set_defaults(action=command_record_preflight)

    deliver = commands.add_parser("deliver")
    add_run_argument(deliver)
    deliver.add_argument("issue")
    deliver.add_argument("--branch")
    deliver.add_argument("--pr")
    deliver.add_argument("--sha", required=True)
    deliver.add_argument("--agent-id", required=True)
    deliver.set_defaults(action=command_deliver)

    dispatch_review = commands.add_parser("dispatch-review")
    add_run_argument(dispatch_review)
    dispatch_review.add_argument("issue")
    dispatch_review.add_argument("--sha", required=True)
    dispatch_review.add_argument("--role", required=True)
    dispatch_review.add_argument("--agent-id", required=True)
    dispatch_review.set_defaults(action=command_dispatch_review)

    review = commands.add_parser("record-review")
    add_run_argument(review)
    review.add_argument("issue")
    review.add_argument("--sha", required=True)
    review.add_argument("--role", required=True)
    review.add_argument("--outcome", choices=("passed", "blocked"), required=True)
    review.add_argument("--blocking-findings", type=int, default=0)
    review.add_argument("--agent-id", required=True)
    review.set_defaults(action=command_record_review)

    verification = commands.add_parser("record-verification")
    add_run_argument(verification)
    verification.add_argument("issue")
    verification.add_argument("--sha", required=True)
    verification.add_argument("--outcome", choices=("passed", "failed"), required=True)
    verification.add_argument("--checks", nargs="+", required=True)
    verification.set_defaults(action=command_record_verification)

    correction = commands.add_parser("dispatch-correction")
    add_run_argument(correction)
    correction.add_argument("issue")
    correction.add_argument("--agent-id", required=True)
    correction.set_defaults(action=command_dispatch_correction)

    merged = commands.add_parser("mark-merged")
    add_run_argument(merged)
    merged.add_argument("issue")
    merged.add_argument("--sha", required=True)
    merged.add_argument("--issue-closed", action="store_true")
    merged.set_defaults(action=command_mark_merged)

    pause = commands.add_parser("goal-pause")
    add_run_argument(pause)
    pause.add_argument("--reason", required=True)
    pause.set_defaults(action=command_goal_pause)

    resume = commands.add_parser("goal-resume")
    add_run_argument(resume)
    resume.set_defaults(action=command_goal_resume)

    authorize = commands.add_parser("authorize-correction")
    add_run_argument(authorize)
    authorize.add_argument("issue")
    authorize.add_argument(
        "--additional-attempts",
        type=integer_between(1, 100),
        metavar="1..100",
        default=1,
    )
    authorize.set_defaults(action=command_authorize_correction)

    block = commands.add_parser("block-run")
    add_run_argument(block)
    block.add_argument("issue")
    block.add_argument("--reason", required=True)
    block.set_defaults(action=command_block_run)

    show = commands.add_parser("show")
    add_run_argument(show)
    show.set_defaults(action=command_show)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        state = args.action(args)
    except (StateError, json.JSONDecodeError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    output = state if args.command == "show" or args.full_state else summarize_state(state)
    json.dump(output, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
