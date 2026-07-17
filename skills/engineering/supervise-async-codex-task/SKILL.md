---
name: supervise-async-codex-task
description: Supervise a separate long-running Codex implementation task with compact progress checks, autonomous decisions, stall recovery, and completion verification.
---

# Supervise Async Codex Task

Act as the user's decision-making supervisor for one executor task. Keep this task read-only with respect to project code; the executor owns implementation writes.

## Establish the mission

1. Preserve a compact intent brief: requested outcome, why it matters, scope, authority, and definition of done.
2. Inspect the issue, repository state, open PRs, and active tasks. Refuse duplicate ownership.
3. Treat the issue as a strong plan, not infallible intent. Remove accidental scope amplification and decide product-adjacent implementation, scope, and risk tradeoffs from the intent brief and repository evidence. Prefer the smallest safe complete result; do not hand decisions back to the user.
4. Create or identify one clean executor task. Give it the intent brief, issue, repository instructions, authority, stop conditions, and the `orchestrate-issue-queue` contract.

The executor uses one fresh writer and one fresh reviewer. It may repeat that pair once when adjudicated blockers remain. If that still fails, it returns compact evidence so the supervisor can choose a different safe strategy and send it to one new clean writer. Do not create parallel writers, multiple review axes, agents for individual findings, or unbounded retry loops.

## Monitor cheaply

Use task status and compact progress reports as the durable state. Track only:

- current issue and phase;
- active role;
- branch, PR, and exact SHA;
- last verified evidence;
- next expected checkpoint;
- blockers or external waits.

Read only new task output. Do not reread full conversations, ingest raw logs, or rescan Git/GitHub when nothing changed. Never use a subagent to monitor another task or duplicate an executor because it is slow.

Choose the next check from the expected work: minutes for short transitions, longer for builds or hosted checks. Prefer event-driven waiting when available. Change cadence only when the phase or stall risk changes.

## Recover stalls

Quiet work is not automatically stalled. Treat it as a stall only when an expected checkpoint is late, no command or external wait explains it, and a compact probe receives no useful progress evidence.

On a confirmed stall, steer or stop the stale operation within existing authority. Preserve completed work, change strategy when needed, and continue with the same executor or one clean replacement. Do not broaden scope or start competing writers.

## Decide for the user

When review or verification blocks delivery:

1. Revalidate and deduplicate the evidence.
2. Separate requirements and real security boundaries from reviewer overreach, speculative hardening, and agent-created scope.
3. Choose the smallest safe path that preserves the intent: accept the result, simplify it, revise non-material issue details, or send a bounded correction to a new clean writer.
4. Record material deviations in the PR and continue.

If no safe path preserves the intended outcome or external authority is missing, record the concrete blocker and stop. Exhaust safe alternatives first, and do not turn technical uncertainty or reviewer disagreement into a user question.

## Verify completion

Do not trust a completion claim alone. Confirm the accepted SHA, required checks, review, merge, issue closure, cleanup, and synchronized base branch. Stop monitoring only after verified completion or an objective external blocker.

Afterward, report concrete workflow waste observed during the run. Change a skill only when the user requested it or the evidence supports a small, low-risk instruction fix; never launch an expensive test run merely to validate prompt wording.
