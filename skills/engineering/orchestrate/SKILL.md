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

At every coordinator entry or wake, keep the current turn live until the mission is complete, genuinely blocked with no independent authorized Ticket runnable, waiting at an explicit user gate already recorded in the Mission envelope, or protected by an **Accepted continuation mechanism**. Completing or preparing a numbered step is not by itself permission to end the turn.

## 1. Establish one work unit

Fix the **Mission envelope** from accepted user direction: exact authorized Ticket identities, scope, deferrals, queue, and completion boundary. When the user supplies a query or queue source, resolve its current Ticket identities once and freeze that snapshot before delivery. Authorization is non-transitive; newly discovered work and later queue additions remain outside this run.

Initial authorization is all-or-nothing. Before selecting a work unit or dispatching a writer, read the repository instructions, live tracker state, every supplied Ticket and its governing sources, and the dependency and conflict edges. Locate the newest applicable `Prompt Audit` status for every Ticket in the frozen queue:

- `PASS` — valid when no material change to the audited execution contract occurred afterward.
- `BYPASS` — valid only when its basis records explicit maintainer authorization for unaudited orchestration.
- `FAIL` — invalid unless a newer applicable `PASS` or `BYPASS` supersedes it.
- Missing or stale — invalid.

If any supplied Ticket lacks a current valid gate, report the entire mission blocked before work selection or writer dispatch. Do not filter that Ticket out or begin an authorized subset. Never infer bypass authorization from a general request to implement or orchestrate. When the maintainer explicitly authorizes bypass in the current invocation, post a `Prompt Audit` comment with `Status: BYPASS`, the issue or agent-brief reference, and the authorization basis before continuing.

Once that complete check succeeds, the mission has started. Before each work unit, including after a fresh-context continuation, re-read live tracker and gate state. A gate that has since become stale or invalid blocks only that Ticket; a dependency or other live blocker likewise blocks only the affected work. Continue with the next independent authorized Ticket when one exists, and report the mission blocked only when unfinished mission work remains with no independent authorized Ticket runnable. From the remaining fixed queue, select one open, `ready-for-agent`, authorized, unblocked Ticket, then read its base branch and relevant code. Live state wins over handoffs and snapshots.

A current `PASS` or `BYPASS` transfers every in-scope implementation decision to the coordinator. Resolve ordinary uncertainty, preferences, and source-resolved choices without opening another user decision gate. If required behavior cannot be determined or external authority is unavailable, mark that Ticket blocked and apply the same independent-work rule. Never widen the Ticket or invent adjacent work.

This step is complete when initial authorization has succeeded and the coordinator has one exact Ticket with a current `PASS` or `BYPASS`, fixed scope and deferrals, acceptance criteria, an exact base fixed point, and an executable writer assignment.

## 2. Dispatch one writer

Start exactly one fresh isolated writer for the whole Ticket. Give it a self-contained prompt with the repository and workspace paths, complete Ticket and governing sources, fixed scope and deferrals, acceptance criteria, repository instructions, expected verification, and required result fields.

Keep the coordinator turn live through preparation and dispatch. Reading, validation, selection, planning, claiming, and statements of intent do not establish a **Safe turn boundary**. For a runnable Ticket, the first boundary exists only after the harness acknowledges acceptance of the isolated writer as an **Accepted continuation mechanism**. A rejected or unacknowledged dispatch creates no boundary and must be handled as an actual blocker rather than reported as started work.

Require the writer to implement the Ticket, perform its local iteration and relevant tests, leave the result at an exact candidate commit, and report changed files, verification, deviations, and concerns. The writer must perform the work directly without reviewing, selecting another Ticket, spawning, or delegating. Writer acceptance permits a local turn boundary; it does not complete this step, deliver the Ticket, or make the mission complete. The writer's return resumes the same coordinator.

This step is complete when the writer has returned one implementation result at an exact candidate commit.

## 3. Establish the review candidate

Inspect the writer result against every acceptance criterion and applicable repository rule. Resolve missing or incorrect in-scope implementation directly, run the checks needed to make the candidate reviewable, and commit any coordinator corrections. Do not return the issue to the writer.

This step is complete when one candidate commit at `HEAD` accounts for the full issue and is ready for an independent read-only review.

## 4. Review the candidate

Use `code-review` with the base fixed point from step 1 while the candidate commit is at `HEAD`; the review range is `git diff <base-fixed-point>...HEAD`. Give it the complete issue and governing sources, repository instructions, and commands needed to inspect the full diff. The orchestration coordinator is the review root; `code-review` owns the isolated-reviewer contract, complete read-only pass, evidence requirements, and finding adjudication. Do not reproduce or weaken that policy here.

This step is complete when `code-review` has returned one adjudicated report for the candidate commit at `HEAD` against the base fixed point.

## 5. Correct and integrate

Apply every surviving in-scope correction directly, without another writer or reviewer. Record out-of-scope review findings without creating or implementing follow-up Tickets. Run repository-required verification and complete the repository's commit, push, integration, tracker, and cleanup workflow.

Review limits bound delegated review, not coordinator authority. Continue through source-resolved divergences and handle blocked or unauthorized Tickets as step 1 defines, without opening an interactive decision loop. On the final Ticket, writer acceptance is still only a local **Safe turn boundary**: the mission continues across every later wake and through writer return, review, coordinator correction, verification, integration, tracker obligations, and cleanup before **Mission complete** is reported.

This step is complete when the Ticket is delivered at a durable verified state, required tracker and integration work is complete, and the repository state is safe for continuation.

## 6. Continue in a fresh coordinator context

After durable delivery, inspect only the frozen Mission envelope. An independent next Ticket that remains authorized and runnable continues through `wormhole`. The continuation state must identify this `orchestrate` `SKILL.md` as the governing contract, cite the completed Ticket and durable state, identify the fixed queue and next Ticket or selection rule, record that initial authorization succeeded, and require the fresh coordinator to read this skill completely before acting.

The fresh coordinator applies step 1's later live-state rule; it does not repeat initial authorization semantics against a gate that changed after mission start. For a runnable next Ticket, the concrete first **Safe turn boundary** supplied to `wormhole` is the writer acceptance defined in step 2. Restoration, reading, validation, selection, planning, claiming, and intent remain preparation.

Report **Mission complete** only when every Ticket in the envelope has reached its required durable outcome and all final integration, tracker, and cleanup obligations are complete. If unfinished work remains and no independent authorized Ticket is runnable, report the mission blocked. Wait for user input only at an explicit gate already recorded in the Mission envelope; never manufacture one from an audited in-scope choice.

This step is complete when `wormhole` confirms the fresh coordinator's first boundary, or when the coordinator has established and reported the envelope's explicit-gate, blocked, or durable terminal-completion outcome.

Example invocation: `Orchestrate every audited issue in the supplied queue, honoring its dependency order.`
