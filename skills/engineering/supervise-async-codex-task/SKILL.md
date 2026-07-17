---
name: supervise-async-codex-task
description: Supervise a separate long-running Codex task through an asynchronous ping-pong protocol, acting as the user's autonomous decision proxy while an orchestrator delivers specified issues.
---

# Supervise Async Codex Task

Act as the user's decision proxy in the current task. Create and steer one separate Codex task that owns orchestration and delivery. Keep the supervisor task read-only with respect to project code.

## Use two Codex tasks

The current task is the **supervisor**. The separate task is the **orchestrator**. Create or resume it with Codex task-management tools; a collaboration subagent is not the orchestrator and does not satisfy this contract.

Before dispatch, capture the supervisor task's return address. Give the orchestrator that task ID, its host when needed, and this ping-pong protocol:

1. Work until a supervisory decision checkpoint.
2. Send the supervisor one compact decision packet containing current issue and phase, branch/PR/SHA, verified evidence, blocker or choice, risks, recommendation, and the exact response needed.
3. End the orchestrator turn. Do not poll or wait for the supervisor inside that turn.
4. Resume only when the supervisor sends the decision back to the orchestrator task.

Decision checkpoints include scope or acceptance deviations, reviewer adjudication, retry strategy, blockers, workflow fallback, merge or continue/stop choices, and claimed completion. Planned mechanical work between checkpoints remains with the orchestrator.

After creating the orchestrator or returning a decision, end the supervisor turn. The orchestrator's next decision packet wakes the supervisor through the task messaging channel. This is asynchronous ping-pong, not a blocking monitor loop.

## Establish the mission

1. Preserve a compact intent brief: requested outcome, why it matters, scope, authority, and definition of done.
2. Inspect the issue, repository state, open PRs, and active tasks. Refuse duplicate ownership.
3. Treat the issue as a strong plan, not infallible intent. Remove accidental scope amplification and decide product-adjacent implementation, scope, and risk tradeoffs from the intent brief and repository evidence. Prefer the smallest safe complete result; do not hand decisions back to the user.
4. Create or resume one clean orchestrator task. Give it the intent brief, issues, repository instructions, authority, return address, decision checkpoints, stop conditions, and the `orchestrate-issue-queue` contract. This skill's ping-pong protocol overrides that contract wherever it grants the orchestrator final decision authority.

The orchestrator uses one fresh writer and one fresh reviewer per issue. It may run demonstrably independent issues concurrently in exclusive worktrees, but never creates competing writers for the same or conflicting work. It may repeat a writer/reviewer pair once when the supervisor confirms adjudicated blockers. If that still fails, it returns a decision packet so the supervisor can choose a different safe strategy and send it to one new clean writer. Do not create multiple review axes, agents for individual findings, or unbounded retry loops.

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

On a confirmed stall, steer or stop the stale operation within existing authority. Preserve completed work, change strategy when needed, and continue with the same orchestrator or one clean replacement. Do not broaden scope or start competing writers.

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
