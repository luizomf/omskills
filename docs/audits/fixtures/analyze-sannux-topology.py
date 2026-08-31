#!/usr/bin/env python3
"""Emit public-safe topology counts from the disposable Sannux session tree."""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
records: list[dict[str, object]] = []
for path in sorted(root.rglob("*.jsonl")):
    raw = path.read_text()
    entries = [json.loads(line) for line in raw.splitlines() if line]
    user_texts: list[str] = []
    calls: list[tuple[str | None, object]] = []
    for entry in entries:
        message = entry.get("message") if entry.get("type") == "message" else None
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if message.get("role") == "user":
            if isinstance(content, str):
                user_texts.append(content)
            elif isinstance(content, list):
                user_texts.append(
                    "".join(
                        item.get("text", "")
                        for item in content
                        if isinstance(item, dict) and item.get("type") == "text"
                    )
                )
        if message.get("role") == "assistant" and isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "toolCall":
                    calls.append((item.get("name"), item.get("arguments", {})))

    initial = user_texts[0] if user_texts else ""
    if "Mission authorization" in initial and "dispatch-tickets" in initial:
        role = "root"
    elif initial.startswith("Repository: daily-paper"):
        role = "coordinator"
    elif "read-only reviewer" in initial.lower() or "code-review" in initial.lower():
        role = "reviewer"
    elif "writer" in initial.lower():
        role = "writer"
    else:
        role = "unknown"
    starts = [arguments for name, arguments in calls if name == "subagent_start"]
    records.append(
        {
            "role": role,
            "starts": len(starts),
            "direct_starts": sum(
                isinstance(arguments, dict) and arguments.get("delivery") == "direct"
                for arguments in starts
            ),
            "has_pong": "[PONG subagent" in raw,
        }
    )

counts = {
    role: sum(record["role"] == role for record in records)
    for role in ("root", "coordinator", "writer", "reviewer", "unknown")
}
assert len(records) == 7, records
assert counts == {
    "root": 1,
    "coordinator": 2,
    "writer": 2,
    "reviewer": 2,
    "unknown": 0,
}, counts
root_record = next(record for record in records if record["role"] == "root")
assert root_record["starts"] == root_record["direct_starts"] == 2
for record in records:
    if record["role"] == "coordinator":
        assert record["starts"] == record["direct_starts"] == 2
    elif record["role"] in {"writer", "reviewer"}:
        assert record["starts"] == 0
assert not any(record["has_pong"] for record in records)

print("session_files=7")
print("root_sessions=1")
print("coordinator_sessions=2")
print("writer_sessions=2")
print("reviewer_sessions=2")
print("root_direct_starts=2")
print("coordinator_direct_starts=4")
print("leaf_starts=0")
print("pong_markers=0")
