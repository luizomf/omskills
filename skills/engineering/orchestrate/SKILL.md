---
name: orchestrate
description: Orchestrate one authorized Ticket or fixed Ticket queue through an isolated writer, isolated reviewer, coordinator-owned correction, and fresh-context continuation.
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

Fix the **Mission envelope** from accepted user direction: exact authorized Ticket identities, scope, deferrals, queue, and completion boundary. When the user supplies a query or queue source, resolve its current Ticket identities once and freeze that snapshot before delivery. Authorization is non-transitive; newly discovered work and later queue additions remain outside this run.

Read the repository instructions, live tracker state, complete Ticket, governing sources, dependency and conflict edges, base branch, and relevant code. Select one open, `ready-for-agent`, authorized, unblocked Ticket from the fixed queue. Live state wins over handoffs and snapshots.

Locate the newest applicable `Prompt Audit` status for that Ticket:

- `PASS` — proceed when no material change to the audited execution contract occurred afterward.
- `BYPASS` — proceed only when its basis records explicit maintainer authorization for unaudited orchestration.
- `FAIL` — this Ticket is not authorized; record its basis and continue with the next independent authorized Ticket when one exists, otherwise report the blocked mission.
- Missing or stale — this Ticket is not authorized; record the missing gate and continue with the next independent authorized Ticket when one exists, otherwise report the blocked mission.

Never infer bypass authorization from a general request to implement or orchestrate. When the maintainer explicitly authorizes bypass in the current invocation, post a `Prompt Audit` comment with `Status: BYPASS`, the issue or agent-brief reference, and the authorization basis before continuing.

A current `PASS` or `BYPASS` transfers every in-scope implementation decision to the coordinator. Resolve choices from the accepted sources and repository evidence without opening another user decision gate. If required behavior cannot be determined or external authority is unavailable, mark that Ticket blocked and continue with the next independent authorized Ticket when one exists; otherwise report the blocked mission. Never widen the Ticket or invent adjacent work.

This step is complete when the coordinator has one exact Ticket with a current `PASS` or `BYPASS`, fixed scope and deferrals, acceptance criteria, an exact base fixed point, and an executable writer assignment.

## 2. Dispatch one writer

Start exactly one fresh isolated writer for the whole Ticket. Give it a self-contained prompt with the repository and workspace paths, complete Ticket and governing sources, fixed scope and deferrals, acceptance criteria, repository instructions, expected verification, and required result fields.

Require the writer to implement the Ticket, perform its local iteration and relevant tests, leave the result at an exact candidate commit, and report changed files, verification, deviations, and concerns. The writer must perform the work directly without reviewing, selecting another Ticket, spawning, or delegating.

This step is complete when the writer has returned one implementation result at an exact candidate commit.

## 3. Establish the review candidate

Inspect the writer result against every acceptance criterion and applicable repository rule. Resolve missing or incorrect in-scope implementation directly, run the checks needed to make the candidate reviewable, and commit any coordinator corrections. Do not return the issue to the writer.

This step is complete when one candidate commit at `HEAD` accounts for the full issue and is ready for an independent read-only review.

## 4. Review the candidate

Use `code-review` with the base fixed point from step 1 while the candidate commit is at `HEAD`; the review range is `git diff <base-fixed-point>...HEAD`. Give it the complete issue and governing sources, repository instructions, and commands needed to inspect the full diff. The orchestration coordinator is the review root; `code-review` owns the isolated-reviewer contract, complete read-only pass, evidence requirements, and finding adjudication. Do not reproduce or weaken that policy here.

This step is complete when `code-review` has returned one adjudicated report for the candidate commit at `HEAD` against the base fixed point.

## 5. Correct and integrate

Apply every surviving in-scope correction directly, without another writer or reviewer. Record out-of-scope review findings without creating or implementing follow-up Tickets. Run repository-required verification and complete the repository's commit, push, integration, tracker, and cleanup workflow.

Review limits bound delegated review, not coordinator authority. Continue through source-resolved divergences and handle blocked or unauthorized Tickets as step 1 defines, without opening an interactive decision loop.

This step is complete when the Ticket is delivered at a durable verified state, required tracker and integration work is complete, and the repository state is safe for continuation.

## 6. Continue in a fresh coordinator context

Only an already-authorized next Ticket inside the fixed Mission envelope continues through `wormhole`. The continuation state must identify this `orchestrate` `SKILL.md` as the governing contract, cite the completed Ticket and durable state, identify the fixed queue and next authorized Ticket or selection rule, and require the fresh coordinator to read this skill completely before acting. With no next authorized Ticket, report completion.

This step is complete when the fresh coordinator starts the next authorized unit under this contract or the completed mission has been reported.

Example invocation: `Orchestrate every audited issue in the supplied queue, honoring its dependency order.`
