---
name: orchestrate
description: Orchestrate delivery of prepared issues through one isolated writer, one isolated reviewer, coordinator-owned correction, and fresh-context continuation. Use when asked to autonomously deliver an audited issue or issue queue.
---

# Orchestrate

Own delivery inside the fixed mission envelope established by accepted user direction, repository instructions, issues, specifications, documentation, ADRs, and repository evidence. Use the harness's available isolated-subagent mechanism; tool names and transport details belong to the harness.

Read the configured issue tracker and domain-document locations. If either configuration is unavailable, run [`setup-omskills`](../setup-omskills/SKILL.md) first.

The delivery graph is acyclic:

```text
coordinator -> writer -> coordinator -> reviewer -> coordinator
```

Writer and reviewer are single-pass leaf agents. Every result returns only to the coordinator, which owns scope, decisions, corrections, integration, continuation, and completion.

## 1. Establish one work unit

Read the repository instructions, live tracker state, complete issue, governing sources, dependency and conflict edges, base branch, and relevant code. Select one open, authorized, unblocked issue from the supplied prepared queue. Live state wins over handoffs and snapshots.

When the sources leave an in-scope choice whose plausible options do not materially differ in behavior, scope, security, compatibility, cost, or reversibility, choose the smallest safe and reversible option consistent with repository conventions—the option you would recommend if asked—record it, and continue. Ask the user only when a material decision remains unresolved, the required change would leave approved scope, or external authority is required.

This step is complete when the coordinator has one exact issue, fixed scope and deferrals, acceptance criteria, base state, and an executable writer assignment.

## 2. Dispatch one writer

Start exactly one fresh isolated writer for the whole issue. Give it a self-contained prompt with the repository and workspace paths, complete issue and governing sources, fixed scope and deferrals, acceptance criteria, repository instructions, expected verification, and required result fields.

Require the writer to implement the issue, perform its local iteration and relevant tests, leave the result at an exact commit or otherwise fixed diff, and report changed files, verification, deviations, and concerns. The writer must perform the work directly without reviewing, selecting another issue, spawning, or delegating.

This step is complete when the writer has returned one implementation result at an exact reviewable fixed point.

## 3. Establish the review candidate

Inspect the writer result against every acceptance criterion and applicable repository rule. Resolve missing or incorrect in-scope implementation directly, run the checks needed to make the candidate reviewable, and establish the exact fixed point. Do not return the issue to the writer.

This step is complete when one candidate fixed point accounts for the full issue and is ready for an independent read-only review.

## 4. Dispatch one reviewer

Start exactly one different fresh isolated reviewer. Give it the complete issue and governing sources, repository instructions, exact fixed point, and commands needed to inspect the full diff. Keep it read-only and require one complete pass covering correctness, regressions, tests, security, documentation, portability, maintainability, missing requirements, and scope changes.

Require concrete findings with file or verification-path evidence, separated into blockers and non-blocking observations. The reviewer must inspect every changed file and return only to the coordinator without editing, spawning, delegating, or contacting the writer.

This step is complete when the reviewer has returned one complete evidence-backed report for the exact fixed point.

## 5. Adjudicate, correct, and integrate

Verify every finding against the issue, governing sources, diff, code, and tests. Reject preferences, speculative hardening, invented requirements, and scope expansion. Apply all surviving corrections directly, without another writer or reviewer, then run repository-required verification and complete the repository's commit, push, integration, tracker, and cleanup workflow.

Review limits bound delegated review, not coordinator authority. A delegated result is evidence rather than a completion or stop decision. Continue through source-resolved divergences; stop only for the material unresolved conditions from step 1.

This step is complete when the issue is delivered at a durable verified state, required tracker and integration work is complete, and the repository state is safe for continuation.

## 6. Continue in a fresh coordinator context

An already-authorized next work unit continues through [`wormhole`](../../productivity/wormhole/SKILL.md). Its handoff must identify this `orchestrate` `SKILL.md` as the governing contract, cite the completed issue and durable state, identify the queue source and next authorized unit or selection instruction, and require the fresh coordinator to read this skill completely before acting. With no next work unit, report completion.

This step is complete when the fresh coordinator starts the next authorized unit under this contract or the completed mission has been reported.

Example invocation: `Orchestrate every audited issue in the supplied queue, honoring its dependency order.`
