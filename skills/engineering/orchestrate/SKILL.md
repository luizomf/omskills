---
name: orchestrate
description: Orchestrate delivery of prepared issues through one isolated writer, one isolated reviewer, coordinator-owned correction, and fresh-context continuation. Use when asked to autonomously deliver an audited issue or issue queue.
---

# Orchestrate

Own delivery inside the fixed mission envelope established by accepted user direction, repository instructions, issues, specifications, documentation, ADRs, and repository evidence. Use the harness's available isolated-subagent mechanism; tool names and transport details belong to the harness.

Read the configured issue tracker and domain-document locations. If either configuration is unavailable, run `setup-omskills` first.

The delivery graph is acyclic:

```text
coordinator -> writer -> coordinator -> reviewer -> coordinator
```

Writer and reviewer are single-pass leaf agents. Every result returns only to the coordinator, which owns scope, decisions, corrections, integration, continuation, and completion.

## 1. Establish one work unit

Read the repository instructions, live tracker state, complete issue, governing sources, dependency and conflict edges, base branch, and relevant code. Select one open, authorized, unblocked issue from the supplied prepared queue. Live state wins over handoffs and snapshots.

For each candidate Ticket, read its complete comments, configured native or fallback blockers, and labels. Reject it from selection and writer dispatch when any of these conditions holds:

- the Ticket is closed;
- any configured native or fallback relation identifies an open blocker;
- its newest applicable Prompt Audit status is missing, stale, or `FAIL`; or
- it does not carry exactly one configured category role and exactly the configured `ready-for-agent` state role, with no other configured state role.

A current explicit maintainer-authorized `BYPASS` satisfies the Ticket audit condition; an inferred or unrecorded bypass does not. Recheck every live Ticket invariant immediately before writer dispatch and stop if any changed.

Locate the newest applicable `Prompt Audit` status for that issue:

- `PASS` — proceed when no material change to the audited execution contract occurred afterward.
- `BYPASS` — proceed only when its basis records explicit maintainer authorization for unaudited orchestration.
- `FAIL` — stop and report its basis; a newer applicable `PASS` or `BYPASS` may supersede it.
- Missing or stale — stop and ask the maintainer to run `prompt-comprehension-audits` or explicitly authorize a bypass.

Never infer bypass authorization from a general request to implement or orchestrate. When the maintainer explicitly authorizes bypass in the current invocation, post a `Prompt Audit` comment with `Status: BYPASS`, the issue or agent-brief reference, and the authorization basis before continuing.

When the sources leave an in-scope choice whose plausible options do not materially differ in behavior, scope, security, compatibility, cost, or reversibility, choose the smallest safe and reversible option consistent with repository conventions—the option you would recommend if asked—record it, and continue. Ask the user only when a material decision remains unresolved, the required change would leave approved scope, or external authority is required.

This step is complete when the coordinator has one exact issue with a current `PASS` or `BYPASS`, fixed scope and deferrals, acceptance criteria, an exact base fixed point, and an executable writer assignment.

## 2. Dispatch one writer

Start exactly one fresh isolated writer for the whole issue. Give it a self-contained prompt with the repository and workspace paths, complete issue and governing sources, fixed scope and deferrals, acceptance criteria, repository instructions, expected verification, and required result fields.

Require the writer to implement the issue, perform its local iteration and relevant tests, leave the result at an exact candidate commit, and report changed files, verification, deviations, and concerns. The writer must perform the work directly without reviewing, selecting another issue, spawning, or delegating.

This step is complete when the writer has returned one implementation result at an exact candidate commit.

## 3. Establish the review candidate

Inspect the writer result against every acceptance criterion and applicable repository rule. Resolve missing or incorrect in-scope implementation directly, run the checks needed to make the candidate reviewable, and commit any coordinator corrections. Do not return the issue to the writer.

This step is complete when one candidate commit at `HEAD` accounts for the full issue and is ready for an independent read-only review.

## 4. Review the candidate

Use `code-review` with the base fixed point from step 1 while the candidate commit is at `HEAD`; the review range is `git diff <base-fixed-point>...HEAD`. Give it the complete issue and governing sources, repository instructions, and commands needed to inspect the full diff. The orchestration coordinator is the review root; `code-review` owns the isolated-reviewer contract, complete read-only pass, evidence requirements, and finding adjudication. Do not reproduce or weaken that policy here.

This step is complete when `code-review` has returned one adjudicated report for the candidate commit at `HEAD` against the base fixed point.

## 5. Correct and integrate

Apply every surviving in-scope correction directly, without another writer or reviewer. Run repository-required verification and complete the repository's commit, push, integration, tracker, and cleanup workflow.

Review limits bound delegated review, not coordinator authority. Continue through source-resolved divergences; stop only for the material unresolved conditions from step 1.

This step is complete when the issue is delivered at a durable verified state, required tracker and integration work is complete, and the repository state is safe for continuation.

## 6. Continue in a fresh coordinator context

An already-authorized next work unit continues through `wormhole`. The continuation state must identify this `orchestrate` `SKILL.md` as the governing contract, cite the completed issue and durable state, identify the queue source and next authorized unit or selection instruction, and require the fresh coordinator to read this skill completely before acting. With no next work unit, report completion.

This step is complete when the fresh coordinator starts the next authorized unit under this contract or the completed mission has been reported.

Example invocation: `Orchestrate every audited issue in the supplied queue, honoring its dependency order.`
