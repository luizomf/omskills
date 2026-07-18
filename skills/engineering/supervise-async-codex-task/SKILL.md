---
name: supervise-async-codex-task
description: Supervise a separate long-running Codex task through asynchronous ping-pong with a slow heartbeat fallback, acting as the user's autonomous decision proxy while an orchestrator delivers specified issues.
---

# Supervise Async Codex Task

Act as the user's decision proxy in the current task. Create and steer one separate Codex task that owns orchestration and delivery. Keep the supervisor task read-only with respect to project code.

## Use two Codex tasks

The current task is the **supervisor**. The separate task is the **orchestrator**. Create a brand-new Codex task for the orchestrator with task-management tools; a collaboration subagent is not the orchestrator and does not satisfy this contract.

"Separate" and "clean" mean a newly created task identity with no prior conversation. Never resume, fork, repurpose, or send a follow-up mission to an existing or previously used task, even if it is idle, appears unrelated, or can be given a clean prompt. Continuing the newly created orchestrator after its own `PONG` or a later decision checkpoint is the only allowed resumption because those turns belong to the same mission.

Before dispatch, resolve the supervisor task's concrete return address. Put the supervisor task ID and host ID, when needed, in the orchestrator's initial prompt. If no concrete return address is available, do not dispatch the mission.

Establish the channel before work begins:

1. The supervisor's initial prompt is `PING`: mission, authority, return address, and protocol.
2. The orchestrator's first action is to call the Codex task-messaging tool, such as `send_message_to_thread`, with that exact return address and a compact `PONG` containing its task identity and readiness.
3. A message is delivered only when the tool call reports success. Printing `PONG` or a decision packet as the orchestrator's final response does not deliver it.
4. After a successful `PONG`, end the orchestrator turn. Begin work only when the supervisor replies `START` through the orchestrator's task channel.

Then use this ping-pong protocol:

1. Work until a supervisory decision checkpoint.
2. Call the task-messaging tool with the supervisor's exact return address and one compact decision packet containing current issue and phase, branch/PR/SHA, verified evidence, blocker or choice, risks, recommendation, and the exact response needed.
3. End the orchestrator turn. Do not poll or wait for the supervisor inside that turn.
4. Resume only when the supervisor sends the decision back to the orchestrator task.

Treat the tool's successful delivery result as the completion criterion for every `PONG` and decision packet. The orchestrator's local final response may acknowledge delivery, but it is never the transport. Address every decision, blocker, manual gate, and pending action to the supervisor task, never to the user or the maintainer. Only the supervisor may determine that external owner authority is required.

Decision checkpoints include scope or acceptance deviations, reviewer adjudication, retry strategy, blockers, workflow fallback, merge or continue/stop choices, and claimed completion. Planned mechanical work between checkpoints remains with the orchestrator.

After creating the orchestrator or returning a decision, end the supervisor turn. The orchestrator's next decision packet wakes the supervisor through the task messaging channel. This is asynchronous ping-pong, not a blocking monitor loop.

## Install a slow fallback heartbeat

After dispatch, create one recurring heartbeat attached to the supervisor task with an approximately 30-minute cadence. Use the Codex automation tool, reuse an existing heartbeat for the same mission instead of duplicating it, and retain its automation ID in the supervisor's compact state. Direct task messages remain the primary loop; the heartbeat exists only to recover a dropped hot-potato handoff.

On each heartbeat wake:

1. Read only the orchestrator's latest compact status and expected checkpoint.
2. If it is working or waiting on an explained command or external system, do not interrupt it. Leave the heartbeat active for its next scheduled wake and end the supervisor turn.
3. If a decision packet is pending, process it normally. If the expected checkpoint is late without explanation, apply the stall-recovery rules below.
4. If the defined mission is complete, verify completion, delete the heartbeat by its stored automation ID, and finish. Also delete it whenever supervision terminates on an objective blocker so no orphaned heartbeat remains.

Never create another heartbeat merely because the existing one woke. If completion arrives through direct task messaging before the next wake, delete the heartbeat during that completion pass.

## Establish the mission

1. Preserve a compact intent brief: requested outcome, why it matters, scope, authority, and definition of done.
2. Inspect the issue, repository state, open PRs, and active tasks. Refuse duplicate ownership.
3. Treat the issue as a strong plan, not infallible intent. Remove accidental scope amplification and decide product-adjacent implementation, scope, and risk tradeoffs from the intent brief and repository evidence. Prefer the smallest safe complete result; do not hand decisions back to the user.
4. Create one new clean orchestrator task. Give it the intent brief, issues, repository instructions, authority, return address, decision checkpoints, stop conditions, and the `orchestrate-issue-queue` contract. Do not select an existing task discovered during inspection. This skill's ping-pong protocol overrides that contract wherever it grants the orchestrator final decision authority.

The orchestrator creates one new clean writer and one new clean reviewer per issue. Require every internal collaboration-subagent creation to call `spawn_agent` with `fork_turns: "none"` and a compact self-contained role prompt; this does not apply to the orchestrator task created with task-management tools. It may run demonstrably independent issues concurrently in exclusive worktrees, but never creates competing writers for the same or conflicting work. It may create one additional new writer and one additional new reviewer when the supervisor confirms adjudicated blockers; neither retry role may reuse an earlier agent. If that still fails, it returns a decision packet so the supervisor can choose a different safe strategy and send it to one newly spawned clean writer. Do not create multiple review axes, agents for individual findings, or unbounded retry loops.

## Maintain compact state

Use decision packets and compact task status as the durable state. Track only, per active issue:

- current issue and phase;
- active role;
- branch, PR, and exact SHA;
- last verified evidence;
- next expected checkpoint;
- blockers or external waits.

Read only new task output. Do not reread full conversations, ingest raw logs, or rescan Git/GitHub when nothing changed. Let task messages drive the loop; do not keep the supervisor running merely to wait. Never use a subagent to monitor the orchestrator or duplicate it because it is slow.

## Recover stalls

Quiet work is not automatically stalled. On a later user, event, or scheduled wake, treat it as a stall only when an expected checkpoint is late, no command or external wait explains it, and one compact probe receives no useful progress evidence.

On a confirmed stall, first steer the current orchestrator within its existing mission. If replacement is necessary, stop the stale operation and create one brand-new orchestrator task with no prior conversation; pass only compact authoritative state and source locations. Never repurpose another existing task or agent as the replacement. Preserve completed work, change strategy when needed, and do not broaden scope or start competing writers.

## Decide for the user

Treat a detailed spec plus issue as roughly 90% of the decision. Own the remaining execution gap. When the orchestrator supplies a reasonable recommendation that preserves intent and approximate scope, accept it by default and continue.

Do not waive a security failure, code smell, durable architectural decision, or material product ambiguity under this default. Require a bounded correction or choose another safe path. Reach the user only when missing external authority or a genuine product choice exceeds the intent already delegated to the supervisor.

At every decision packet:

1. Revalidate and deduplicate the evidence.
2. Separate requirements and real security boundaries from reviewer overreach, speculative hardening, and agent-created scope.
3. Choose the smallest safe path that preserves the intent: accept the result, simplify it, revise non-material issue details, or send a bounded correction to a new clean writer.
4. Send one explicit instruction back to the orchestrator: continue, correct, retry, merge, replace strategy, or stop. Record material deviations in the PR.

Treat failures in preferred tools, skills, subagents, tracker metadata, or reporting as workflow degradation. Preserve completed work, select an equivalent safe path, and continue unless the failure removes required evidence, authority, or every safe route to completion.

If no safe path preserves the intended outcome or external authority is missing, record the concrete blocker and stop. Exhaust safe alternatives first, and do not turn technical uncertainty or reviewer disagreement into a user question.

## Verify completion

Treat completion as a decision checkpoint. Do not trust the claim alone. Confirm the accepted SHA, required checks, review, merge, issue closure, cleanup, and synchronized base branch. Finish only after verified completion or an objective external blocker.

Afterward, report concrete workflow waste observed during the run. Change a skill only when the user requested it or the evidence supports a small, low-risk instruction fix; never launch an expensive test run merely to validate prompt wording.
