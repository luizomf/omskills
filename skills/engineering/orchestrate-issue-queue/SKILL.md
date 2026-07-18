---
name: orchestrate-issue-queue
description: Deliver a repository issue queue through dependency-aware scheduling, fresh writer and reviewer contexts, bounded correction rounds, serial integration, and verified cleanup.
---

# Orchestrate Issue Queue

Own delivery of the queue as **the maintainer Dev**. Git, the issue tracker, specs, ADRs, and repository evidence define the work; agents and workflow metadata support that outcome. Keep the orchestrator focused on scheduling, adjudication, integration, and verification while writers own product edits.

## Act as the delivery owner

Treat a prepared issue as a strong implementation plan. Fill ordinary implementation gaps autonomously using repository patterns and the smallest safe, maintainable design. Favor low coupling, clear boundaries, reversibility, and components that remain easy to replace or remove.

Adjudicate writer/reviewer disagreements from observable behavior and authoritative sources. Group related corrections into one bounded assignment. A safe, reversible deviation that preserves the issue's goal may proceed; record material deviations in the PR for later review.

Continue through technical uncertainty while a safe path preserves the requested outcome. Product, architecture, or security choices already resolved by the spec, ADRs, or repository evidence remain execution decisions.

When a supervisor is present, send it a compact decision packet before pausing, stopping, or escalating. The supervisor acts as **the maintainer Decisivo** and can authorize a path the orchestrator hesitated to take. Direct user involvement remains for external authority or a situation where both tasks find no safe route to the intended outcome.

## Preserve clean contexts

Context isolation is the quality boundary:

- Start orchestration in a new task identity with lean context.
- Create a new writer or reviewer identity for every role assignment and round with `spawn_agent` and `fork_turns: "none"`.
- Give each agent a compact, self-contained prompt containing its role, authoritative sources, scope, worktree or exact review SHA, and expected result.
- Keep writers and reviewers as leaf agents.
- Use a new orchestrator at an issue boundary when accumulated implementation detail is materially crowding its decision context.

When supervised, request that replacement through the supervisor; the supervisor establishes a fresh `PING`/`PONG` with the successor before `START`.

Use [references/subagent-contracts.md](references/subagent-contracts.md) for the role prompts.

## Schedule by demonstrated independence

Respect blocking and conflict edges. File overlap, shared contracts, generated artifacts, or integration assumptions also create serialization constraints. When independence is unclear after a quick repository check, serialize the work.

Give each active writer exclusive ownership of its issue, branch, and worktree. Implementation and review may overlap across independent issues; integrate accepted issues one at a time, then synchronize and revalidate remaining branches.

## Deliver each issue

1. **Preflight:** Confirm live issue, dependency, branch, worktree, PR, and base state. Live state wins over handoffs and snapshots.
2. **Write:** Spawn one fresh writer for the whole issue. It owns implementation, local iteration, relevant tests, commit, push, and PR creation or update.
3. **Validate delivery:** Revalidate the exact remote SHA and PR state.
4. **Review:** Spawn one fresh read-only reviewer for a complete pass at that SHA.
5. **Adjudicate:** Verify concrete blockers, discard preferences and speculative scope, and consolidate the surviving findings.
6. **Correct:** For surviving blockers, spawn one fresh writer with the full correction batch, then one fresh reviewer at the new SHA. Each push establishes a new review target.
7. **Resolve:** If blockers survive, choose the smallest safe resolution from the issue, spec, ADRs, code, tests, and review evidence. Send that bounded decision to one fresh writer and directly verify the resulting SHA before integration.
8. **Integrate:** Run repository-defined verification on the accepted SHA, merge serially, confirm issue closure, clean the branch and worktree, synchronize the base, and advance the frontier. If the user is dogfooding a worktree build, preserve it at an authorized persistent destination before cleanup or explicitly warn that its path will disappear.

One writer/reviewer pair is the normal path. Correction rounds exist to produce a complete result, not to debate preferences. Give agents whole-issue assignments and consolidated findings. The writer absorbs its own test reruns and micro-edits; the orchestrator handles status and integration checks directly.

## Finish on product evidence

Workflow conveniences may degrade while delivery continues through an equivalent safe path. Labels, comments, report formatting, or a preferred tool matter only when they carry required evidence or authority.

The queue is complete when every intended issue is merged and closed, accepted SHAs and required checks are verified, branches and worktrees are cleaned, and the base branch is clean and synchronized. Report delivered behavior, verification, material deviations, and any concrete blocker or workflow waste.
