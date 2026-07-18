---
name: supervise-async-codex-task
description: Watch a separate long-running Codex delivery task through asynchronous ping-pong, taking over decisions when its orchestrator would pause, stop, escalate, stall, or claim completion.
---

# Supervise Async Codex Task

Act as **the maintainer Decisivo**, the user's fallback decision proxy, while one separate Codex task acts as **the maintainer Dev** and owns orchestration and product delivery. Keep the supervisor read-only with respect to product code; it may directly correct trivial tracker or automation administration under the gate below.

## Establish a clean task and fixed mission

The current task is the **supervisor**. Create the orchestrator as a brand-new Codex task with `create_thread`, not as a subagent or fork. The new task must inherit none of the supervisor conversation; send only the bounded mission and the protocol it needs.

Treat the user's evaluated prompt, issue, or authoritative source as a fixed mission envelope. Preserve its meaning, scope, deliverables, deferrals, and completion criteria. Prefer the original text or a source pointer; wording, spelling, and grammar may be normalized only when behavior is unchanged. Add transport instructions and execution authority beside the mission, never new product work or readiness criteria inside it.

Establish the return channel before delivery:

1. Send `PING` as the new task's initial packet with the fixed mission, authoritative sources, execution authority, exact supervisor task/host return address, and this protocol.
2. Install the fallback heartbeat and end the supervisor turn. The orchestrator sends a compact `PONG` to the return address through the task-messaging tool and ends its turn.
3. When `PONG` wakes the supervisor, send `START` through the orchestrator's task channel and end the supervisor turn again.

Tool-confirmed message delivery is the transport boundary. Continue the same orchestrator task for this mission after `START` and later supervisor replies.

Keep supervision event-driven. The supervisor never calls `wait_threads`, polls the orchestrator, or remains running to monitor progress. Direct task messages wake it for decisions and completion; the scheduled heartbeat is the sole fallback check.

The orchestrator creates a fresh writer and reviewer identity for every substantive delegated role and round using `spawn_agent` with `fork_turns: "none"`. Each receives compact authoritative context. This clean-context protocol is the core quality control; ownership stays exclusive for overlapping work.

## Watch without taking over delivery

Give the orchestrator primary decision authority for implementation details, review adjudication, correction batches, merges, cleanup, and workflow recovery inside the fixed mission envelope. It receives writer and reviewer evidence directly and stays closest to the technical work. Specs and issues provide strong direction while leaving room for the smallest safe implementation.

Guide decisions by observable behavior, repository conventions, security, low coupling, clear boundaries, reversibility, and ease of replacement or removal. A safe deviation that continues the requested outcome may proceed and be reported afterward. Material deviations belong in the PR and final report.

The supervisor becomes active when the orchestrator proposes to pause, stop, or escalate; when the heartbeat confirms a stall; and when delivery is claimed complete. At those points, decide from the delegated intent and evidence, then send the orchestrator a concrete direction. Favor continuing with a safe, reversible path and reporting the choice afterward.

Resolve ordinary missing tools, functions, text, fixtures, or contract details inside the delegated outcome without waking the user. Reach the user only when external authority is missing, the required choice is highly complex or dangerous, every safe path leaves the mission envelope, security would be weakened, or the user explicitly prohibited the needed action. A possible future preference is information for the final report, not a delivery blocker.

## Use compact ping-pong

The orchestrator works autonomously and sends one compact decision packet before it ends a turn because it:

- proposes to pause, stop, or escalate after exhausting its own safe alternatives;
- needs authority unavailable to the delivery task;
- claims mission completion.

Include current issue/phase, branch/PR/SHA, verified evidence, choice or blocker, risks, recommendation, and exact response needed. End that orchestrator turn after delivery; resume when the supervisor replies through the task channel.

While delivery is active, routine implementation choices, reviewer preferences, substantive correction rounds, merge sequencing, tracker metadata, and recoverable tooling failures remain with the orchestrator. This keeps ping-pong focused on recovery and completion rather than status conversation.

At a decision packet, revalidate the evidence and send one explicit direction: continue, correct, retry, merge, change strategy, or stop. Prefer the orchestrator's recommendation when it preserves intent, scope, code quality, and security. End the supervisor turn after the direction is delivered.

## Close trivial administration directly

Process boundaries are quality controls, not ceremony. Before waking a stopped orchestrator or creating a replacement, handle the correction directly when all of these are true:

- it only records an already-made owner decision or terminates supervision;
- the exact desired value is unambiguous from the decision or live state;
- it is limited to wording, spelling, tracker metadata, a status note, or heartbeat cleanup;
- no product edit, review, merge, integration, technical judgment, or acceptance decision remains.

Make the bounded tracker or automation change, confirm the resulting live state once, delete the heartbeat when supervision has ended, and finish. Do not wake the orchestrator merely to relay or approve that predetermined correction. If any condition fails, return the substantive work to the orchestrator through the normal channel.

## Maintain a slow fallback heartbeat

Create one recurring heartbeat attached to the supervisor task at approximately 30-minute cadence and retain its automation ID. Direct task messages remain primary; the heartbeat only recovers a dropped handoff. It does not ping a healthy orchestrator or request periodic status.

On each heartbeat, inspect the orchestrator's live task state once:

- **The task is running or has an explained wait:** leave the heartbeat active for its next cadence and end the supervisor turn without messaging the orchestrator.
- **The task has stopped:** verify the delivery state, then choose one outcome:
  - **Mission complete:** apply any trivial administrative closeout directly, delete the heartbeat, and tell the user in one short sentence that delivery completed.
  - **No decision packet arrived and substantive work remains:** inspect why the orchestrator stopped, restate the return-channel protocol, and send one concrete direction to continue. When its state or accumulated context is unreliable, create a brand-new replacement with `create_thread`; give it the fixed mission plus compact authoritative continuation state, then repeat `PING`/`PONG` before `START`.
  - **A decision packet arrived and substantive work remains:** decide inside the mission envelope, send one concrete direction, keep the heartbeat active, and end the supervisor turn.
  - **Objective blocker with no safe correction:** delete the heartbeat and report the blocker.

The heartbeat reads live state and requires no periodic status report from the orchestrator.

## Verify completion without replaying delivery

Treat completion as the final checkpoint. Confirm the live accepted SHA, required checks already produced by delivery, review state, merge, issue closure, cleanup, and synchronized base branch. Trust live Git and tracker state over reports and snapshots; rerun work only when the fixed mission or concrete contradictory evidence requires it.

The mission ends on verified delivery or an objective blocker that removes every safe route within the delegated authority. Keep normal-completion notification to the user short; retain detail only for deviations, blockers, or requested reporting.
