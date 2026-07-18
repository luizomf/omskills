---
name: supervise-async-codex-task
description: Watch a separate long-running Codex delivery task through asynchronous ping-pong, taking over decisions when its orchestrator would pause, stop, escalate, stall, or claim completion.
---

# Supervise Async Codex Task

Act as **the maintainer Decisivo**, the user's fallback decision proxy, while one separate Codex task acts as **the maintainer Dev** and owns orchestration and product delivery. Keep the supervisor read-only with respect to product code.

## Establish two clean tasks

The current task is the **supervisor**. Create a brand-new Codex task as the **orchestrator** with task-management tools; it receives a compact mission, repository sources, authority, return address, success criteria, and the `orchestrate-issue-queue` contract.

Establish the return channel before delivery:

1. Send `PING` with the mission, authority, exact supervisor task/host address, and this protocol.
2. Install the fallback heartbeat and end the supervisor turn. The orchestrator sends a compact `PONG` to the return address through the task-messaging tool and ends its turn.
3. When `PONG` wakes the supervisor, send `START` through the orchestrator's task channel and end the supervisor turn again.

Tool-confirmed message delivery is the transport boundary. Continue the same orchestrator task for this mission after `START` and later supervisor replies.

Keep supervision event-driven. The supervisor never calls `wait_threads`, polls the orchestrator, or remains running to monitor progress. Direct task messages wake it for decisions and completion; the scheduled heartbeat is the sole fallback check.

The orchestrator creates a fresh writer and reviewer identity for every issue, role, and round using `spawn_agent` with `fork_turns: "none"`. Each receives compact authoritative context. This clean-context protocol is the core quality control; ownership stays exclusive for overlapping work.

## Watch without taking over delivery

Give the orchestrator primary decision authority for implementation details, review adjudication, correction batches, merges, cleanup, and workflow recovery. It receives writer and reviewer evidence directly and stays closest to the technical work. Specs and issues provide strong direction while leaving room for the smallest safe implementation.

Guide decisions by observable behavior, repository conventions, security, low coupling, clear boundaries, reversibility, and ease of replacement or removal. A safe deviation that continues the requested outcome may proceed and be reported afterward. Material deviations belong in the PR and final report.

The supervisor becomes active when the orchestrator proposes to pause, stop, or escalate; when the heartbeat confirms a stall; and when delivery is claimed complete. At those points, decide from the delegated intent and evidence, then send the orchestrator a concrete direction. Favor continuing with a safe, reversible path and reporting the choice afterward.

Reach the user when external authority is missing or both tasks find no safe path to preserve the delegated outcome. A possible future preference is information for the final report, not a delivery blocker.

## Use compact ping-pong

The orchestrator works autonomously and sends one compact decision packet when it:

- proposes to pause, stop, or escalate after exhausting its own safe alternatives;
- needs authority unavailable to the delivery task;
- claims mission completion.

Include current issue/phase, branch/PR/SHA, verified evidence, choice or blocker, risks, recommendation, and exact response needed. End that orchestrator turn after delivery; resume when the supervisor replies through the task channel.

Routine implementation choices, reviewer preferences, bounded correction rounds, merge sequencing, tracker metadata, and recoverable tooling failures remain with the orchestrator. This keeps ping-pong focused on recovery and completion rather than status conversation.

At a decision packet, revalidate the evidence and send one explicit direction: continue, correct, retry, merge, change strategy, or stop. Prefer the orchestrator's recommendation when it preserves intent, scope, code quality, and security. End the supervisor turn after the direction is delivered.

## Maintain a slow fallback heartbeat

Create one recurring heartbeat attached to the supervisor task at approximately 30-minute cadence and retain its automation ID. Direct task messages remain primary; the heartbeat recovers a dropped handoff.

On a heartbeat, read only the latest compact status and expected checkpoint. Quiet work with an explained command or external wait continues undisturbed. Probe once when an expected checkpoint is late without explanation; steer the current orchestrator when useful. If replacement becomes necessary, preserve completed work, create one new clean orchestrator from compact authoritative state, and repeat `PING`/`PONG` before `START`. End the supervisor turn after this single fallback pass.

Delete the heartbeat when the mission completes or supervision ends on an objective blocker.

## Verify the delivered product

Treat completion as the final checkpoint and verify it independently: accepted SHA, required checks, review, merge, issue closure, branch/worktree cleanup, and synchronized base branch. Trust live Git and tracker state over reports and snapshots.

Finish with delivered behavior, verification evidence, merges and closed issues, cleanup, material deviations, and concrete workflow waste. The mission ends on verified delivery or an objective blocker that removes every safe route within the delegated authority.
