#!/usr/bin/env python3
"""Compact state and metrics for adaptive Codex task supervision."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
INTERVALS = {
    "quick": 180,
    "normal": 600,
    "heavy": 1200,
    "external": 1800,
    "stalled": 180,
    "terminal": 0,
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_root(override: Path | None) -> Path:
    if override is not None:
        return override.expanduser().resolve()
    base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    return base / "codex/supervise-async-codex-task"


def run_dir(run_id: str, override: Path | None) -> Path:
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise SystemExit(f"Invalid run id: {run_id!r}")
    return state_root(override) / run_id


@contextmanager
def locked(run_id: str, override: Path | None, create: bool = False) -> Iterator[Path]:
    directory = run_dir(run_id, override)
    if create:
        directory.mkdir(parents=True, exist_ok=False)
    if not directory.is_dir():
        raise SystemExit(f"Unknown run: {run_id}")
    lock_path = directory / ".lock"
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield directory


def load(directory: Path) -> dict[str, Any]:
    return json.loads((directory / "state.json").read_text(encoding="utf-8"))


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def append_event(directory: Path, event: str, metadata: dict[str, Any]) -> None:
    record = {"timestamp": now(), "event": event, **metadata}
    with (directory / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def fingerprint(observation: dict[str, str]) -> str:
    encoded = json.dumps(observation, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def init_run(args: argparse.Namespace) -> None:
    with locked(args.run_id, args.state_root, create=True) as directory:
        created_at = now()
        state = {
            "schema_version": 1,
            "run_id": args.run_id,
            "status": "active",
            "executor_thread": args.executor_thread,
            "repository": args.repository,
            "objective": args.objective,
            "automation_id": args.automation_id,
            "created_at": created_at,
            "updated_at": created_at,
            "last_fingerprint": None,
            "last_observation": None,
            "metrics": {
                "observations": 0,
                "unchanged_observations": 0,
                "full_reads": 0,
                "interventions": 0,
                "phase_transitions": 0,
            },
            "improvements": [],
        }
        atomic_write(directory / "state.json", state)
        append_event(directory, "initialized", {"executor_thread": args.executor_thread})
    print(json.dumps({"run_id": args.run_id, "status": "active"}))


def observe(args: argparse.Namespace) -> None:
    observation = {
        "phase": args.phase,
        "executor_status": args.executor_status,
        "executor_updated_at": args.executor_updated_at,
        "event_sequence": args.event_sequence,
        "sha": args.sha,
        "active_role": args.active_role,
        "activity_class": args.activity_class,
    }
    current_fingerprint = fingerprint(observation)
    with locked(args.run_id, args.state_root) as directory:
        state = load(directory)
        changed = current_fingerprint != state["last_fingerprint"]
        previous_phase = (state.get("last_observation") or {}).get("phase")
        metrics = state["metrics"]
        metrics["observations"] += 1
        if not changed:
            metrics["unchanged_observations"] += 1
        if changed and previous_phase and previous_phase != args.phase:
            metrics["phase_transitions"] += 1
        metrics["full_reads"] += int(args.full_read)
        metrics["interventions"] += int(args.intervention)
        state["last_fingerprint"] = current_fingerprint
        state["last_observation"] = observation
        state["updated_at"] = now()
        if args.activity_class == "terminal":
            state["status"] = args.executor_status
        atomic_write(directory / "state.json", state)
        if changed:
            append_event(
                directory,
                "observation_changed",
                {
                    "phase": args.phase,
                    "executor_status": args.executor_status,
                    "event_sequence": args.event_sequence,
                    "sha": args.sha,
                    "activity_class": args.activity_class,
                },
            )
    result = {
        "changed": changed,
        "recommended_interval_seconds": INTERVALS[args.activity_class],
        "should_read_details": changed,
    }
    print(json.dumps(result, sort_keys=True))


def record_improvement(args: argparse.Namespace) -> None:
    improvement = {
        "timestamp": now(),
        "skill": args.skill,
        "summary": args.summary,
        "evidence": args.evidence,
        "risk": args.risk,
    }
    with locked(args.run_id, args.state_root) as directory:
        state = load(directory)
        state["improvements"].append(improvement)
        state["updated_at"] = now()
        atomic_write(directory / "state.json", state)
        append_event(directory, "improvement_recorded", {"skill": args.skill, "risk": args.risk})
    print(json.dumps({"recorded": True, "skill": args.skill}))


def finish(args: argparse.Namespace) -> None:
    with locked(args.run_id, args.state_root) as directory:
        state = load(directory)
        state["status"] = args.outcome
        state["updated_at"] = now()
        state["summary"] = args.summary
        atomic_write(directory / "state.json", state)
        append_event(directory, "finished", {"outcome": args.outcome})
    print(json.dumps({"status": args.outcome}))


def show(args: argparse.Namespace) -> None:
    with locked(args.run_id, args.state_root) as directory:
        print(json.dumps(load(directory), indent=2, sort_keys=True))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    root.add_argument("--state-root", type=Path)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init")
    init.add_argument("run_id")
    init.add_argument("--executor-thread", required=True)
    init.add_argument("--repository", required=True)
    init.add_argument("--objective", required=True)
    init.add_argument("--automation-id", required=True)
    init.set_defaults(function=init_run)

    observation = commands.add_parser("observe")
    observation.add_argument("run_id")
    observation.add_argument("--phase", required=True)
    observation.add_argument("--executor-status", required=True)
    observation.add_argument("--executor-updated-at", default="")
    observation.add_argument("--event-sequence", default="")
    observation.add_argument("--sha", default="")
    observation.add_argument("--active-role", default="")
    observation.add_argument("--activity-class", choices=INTERVALS, required=True)
    observation.add_argument("--full-read", action="store_true")
    observation.add_argument("--intervention", action="store_true")
    observation.set_defaults(function=observe)

    improvement = commands.add_parser("record-improvement")
    improvement.add_argument("run_id")
    improvement.add_argument("--skill", required=True)
    improvement.add_argument("--summary", required=True)
    improvement.add_argument("--evidence", required=True)
    improvement.add_argument("--risk", choices=("low", "policy"), required=True)
    improvement.set_defaults(function=record_improvement)

    finished = commands.add_parser("finish")
    finished.add_argument("run_id")
    finished.add_argument("--outcome", choices=("complete", "blocked"), required=True)
    finished.add_argument("--summary", required=True)
    finished.set_defaults(function=finish)

    display = commands.add_parser("show")
    display.add_argument("run_id")
    display.set_defaults(function=show)
    return root


def main() -> None:
    args = parser().parse_args()
    args.function(args)


if __name__ == "__main__":
    main()
