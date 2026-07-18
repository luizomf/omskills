---
name: orchestrate-issue-queue
description: Deliver a repository issue queue through dependency-aware scheduling, fresh writer and reviewer contexts, bounded correction rounds, serial integration, and verified cleanup.
---

# Orchestrate Issue Queue

Own delivery of the queue as **the maintainer Dev**. Git, the issue tracker, specs, ADRs, and repository evidence define the work; agents and workflow metadata support that outcome. Keep the orchestrator focused on scheduling, adjudication, integration, and verification while writers own substantive product edits.

## Act as the delivery owner

Treat the evaluated prompt, prepared issue, and authoritative sources as a fixed mission envelope. Preserve their requested outcome, boundaries, deferrals, and completion criteria. Fill ordinary implementation gaps autonomously inside that envelope using repository patterns and the smallest safe, maintainable design. Favor low coupling, clear boundaries, reversibility, and components that remain easy to replace or remove.

Implementation autonomy chooses how to deliver the mission; it does not enlarge what the mission asks to deliver. Treat inferred prerelease work, extra product behavior, broad test campaigns, documentation programs, and general readiness work as outside the envelope unless an authoritative source requires them.

Adjudicate writer/reviewer disagreements from observable behavior and authoritative sources. Group related corrections into one bounded assignment. A safe, reversible deviation that preserves the issue's goal may proceed; record material deviations in the PR for later review.

Continue through technical uncertainty while a safe path preserves the requested outcome. Product, architecture, or security choices already resolved by the spec, ADRs, or repository evidence remain execution decisions.

When a supervisor is present, send it a compact decision packet before pausing, stopping, escalating, or claiming completion. The supervisor acts as **the maintainer Decisivo** and can authorize a path the orchestrator hesitated to take. Direct user involvement remains for external authority or a situation where both tasks find no safe route to the intended outcome.

## Honor the supervisor channel

On `PING`, retain the exact supervisor task/host return address and fixed mission, send `PONG` directly through the task-messaging tool, and end the turn. Begin delivery only after `START` arrives through the same channel.

Work autonomously between messages. Send no routine status traffic. Before voluntarily ending a turn with incomplete delivery because progress would pause, stop, or escalate, send one decision packet to the supervisor and wait for its direction. Send the same packet with completion evidence before ending on a completion claim. A tool-confirmed send is the handoff boundary; silence is never a substitute for the required packet.

## Size the process to the judgment

Process boundaries are quality controls, not ceremony. Use a writer and independent reviewer only when all of these are true:

- the change edits product code;
- it is a substantive chunk that changes observable behavior, contracts, data handling, or security;
- separate implementation and review judgment materially reduce risk.

Handle every other change directly with verification proportionate to its risk. This includes small deterministic code corrections and non-functional work such as wording, spelling, presentation-only color, formatting, tests-only maintenance, build metadata, tracker metadata, or status notes. Resolve classification uncertainty from the issue and repository evidence; uncertainty alone does not trigger delegation.

## Preserve clean contexts

Context isolation is the quality boundary:

- When supervised, run orchestration in the brand-new Codex task created with `create_thread`; do not substitute a subagent or fork that inherits the supervisor conversation.
- Create a new writer or reviewer identity for every delegated role assignment and round with `spawn_agent` and `fork_turns: "none"`.
- Give each agent a compact, self-contained prompt containing its role, authoritative sources, scope, worktree or exact review SHA, and expected result.
- Keep writers and reviewers as leaf agents.
- Use a new orchestrator at an issue boundary when accumulated implementation detail is materially crowding its decision context.

When supervised, request that replacement through the supervisor; the supervisor establishes a fresh `PING`/`PONG` with the successor before `START`.

Use [references/subagent-contracts.md](references/subagent-contracts.md) for the role prompts.

## Schedule by demonstrated independence

Respect blocking and conflict edges. File overlap, shared contracts, generated artifacts, or integration assumptions also create serialization constraints. When independence is unclear after a quick repository check, serialize the work.

Give each active writer exclusive ownership of its issue, branch, and worktree. Implementation and review may overlap across independent issues; integrate accepted issues one at a time, then synchronize and revalidate remaining branches.

## Deliver each issue

1. **Preflight:** Confirm live issue, dependency, branch, worktree, PR, and base state. Live state wins over handoffs and snapshots. Classify the work through the delegation gate above.
2. **Write:** For a substantive behavior-changing product-code change, spawn one fresh writer for the whole issue. It owns implementation, local iteration, relevant tests, commit, push, and PR creation or update. For direct work, perform the bounded path without delegation.
3. **Validate delivery:** Revalidate the exact remote SHA and PR state.
4. **Review:** For delegated work, spawn one fresh read-only reviewer for a complete pass at that SHA. Direct work needs only its conclusive targeted verification.
5. **Adjudicate:** Verify concrete blockers, discard preferences and speculative scope, and consolidate the surviving findings.
6. **Correct:** For surviving blockers, apply the delegation gate again. Handle the batch directly unless all delegation conditions hold; otherwise spawn one fresh writer with the full correction batch, then one fresh reviewer at the new SHA. Each delegated push establishes a new review target.
7. **Resolve:** If blockers survive, choose the smallest safe resolution from the issue, spec, ADRs, code, tests, and review evidence. Apply it directly unless all delegation conditions hold; otherwise send the bounded decision to one fresh writer and then one fresh reviewer at the resulting SHA. Verify the accepted SHA before integration.
8. **Integrate:** Run repository-defined verification on the accepted SHA, merge serially, confirm issue closure, clean the branch and worktree, synchronize the base, and advance the frontier. If the user is dogfooding a worktree build, preserve it at an authorized persistent destination before cleanup or explicitly warn that its path will disappear.

One writer/reviewer pair is the normal path for delegated work. Correction rounds exist to produce a complete result, not to debate preferences. Give agents whole-issue assignments and consolidated findings. The writer absorbs its own test reruns and micro-edits; the orchestrator handles direct corrections, status, and integration checks itself.

## Finish on product evidence

Workflow conveniences may degrade while delivery continues through an equivalent safe path. Labels, comments, report formatting, or a preferred tool matter only when they carry required evidence or authority.

The queue is complete when every intended issue is merged and closed, accepted SHAs and required checks are verified, branches and worktrees are cleaned, and the base branch is clean and synchronized. Report delivered behavior, verification, material deviations, and any concrete blocker or workflow waste.
