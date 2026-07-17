---
name: orchestrate-issue-queue
description: Orchestrate repository issues in dependency-aware waves with exclusive worktrees, one fresh writer and reviewer per issue, bounded retry, and serial integration. Use for continuous multi-issue implement-review-merge delivery.
---

# Orchestrate Issue Queue

Coordinate delivery; do not implement or approve changes yourself. Keep Git and the issue tracker authoritative. Run issues concurrently only when their independence is demonstrated, and integrate accepted work one issue at a time.

## Exercise judgment

Treat a detailed issue as the default plan, not an immutable script. The orchestrator owns delivery and may adjust implementation details, tests, acceptance wording, or sequencing when repository evidence shows a better path. Preserve the issue's intent and approximate scope, keep the code simple and maintainable, and never weaken security or documented boundaries merely to make a check pass.

Make engineering decisions autonomously and record material deviations in the PR. When alternatives differ, choose the smallest safe option that best preserves the issue's intent, code quality, maintainability, and security. Do not return tradeoffs or failed reviews to the user for resolution.

Fill small gaps in an issue when the repository sources make the intended result clear and the choice does not expand product scope, weaken a security boundary, create code smell, or revise a durable decision. Escalate only a real product choice, missing authority, owner-only manual gate, or the absence of any safe in-scope path.

## Keep every context clean

- Start the orchestration in a fresh task. Keep its context lean: consume compact agent reports and authoritative PR/issue state, not full transcripts or unfiltered logs. At an issue boundary, hand off the queue state to a fresh orchestrator whenever the current context has accumulated implementation detail.
- Start every writer and reviewer with fresh context. Give them source locations, the issue, the exact SHA when reviewing, and the required outcome—not another agent's conversation.
- Writers and reviewers are leaf agents. They do not spawn or delegate.
- Never reuse an agent for another role, round, or issue.

Use [references/subagent-contracts.md](references/subagent-contracts.md) as compact role prompts.

## Schedule the frontier

- Respect blocking edges. Treat conflict edges and material overlap in files, contracts, artifacts, or integration assumptions as serialization constraints.
- An unblocked issue is only a parallel candidate; missing declared dependencies does not prove independence. When a quick repository check cannot demonstrate independence, serialize it.
- Give every active writer exclusive ownership of its issue, branch, and worktree. Use the operating system temporary directory for disposable reproduction or verification worktrees; use a durable path for implementation that must survive task recovery.
- Implementation and review may overlap across independent issues. Merge accepted issues one at a time, then synchronize and revalidate every remaining branch before accepting it.

## Run the queue

For each issue:

1. **Preflight:** Confirm the issue is open, unowned, unblocked, and has enough acceptance criteria to implement. Confirm its branch and worktree are exclusive and it has no material conflict with active work.
2. **Write:** Dispatch one fresh writer for the whole issue. The writer owns implementation, local iteration, relevant tests, commit, push, and the PR.
3. **Validate delivery:** Revalidate the PR and exact remote SHA. Treat GitHub as authoritative.
4. **Review:** Dispatch one fresh read-only reviewer for the whole issue at that SHA. The reviewer checks the spec, behavior, tests, security implications, documentation, and repository rules in one pass.
5. **Adjudicate:** Verify every blocking finding yourself. Ignore vague, duplicated, or non-reproducible objections.
6. **Retry once:** If blockers remain, dispatch one fresh writer with the issue and adjudicated findings. After its delivery, dispatch one fresh reviewer for the new SHA. Any push invalidates the earlier review.
7. **Resolve:** If the second review still blocks, choose the smallest safe path forward from the available evidence. You may revise non-material issue details when that produces a simpler, correct, maintainable, and secure result. Give the decision, revised constraints, and surviving blockers to a new fresh writer; do not reopen process discussion. Verify the resulting SHA yourself and merge when the issue's intent, checks, and repository rules are satisfied.
8. **Advance:** Confirm the issue closed, clean its branch and worktree, synchronize the remaining work, and dispatch newly eligible frontier issues.

The normal budget per issue is therefore one writer and one reviewer, with one fresh writer/reviewer retry only when needed. The final resolution writer is an escape hatch, not another automatic review loop.

## Whole-issue passes

- The issue is the unit of work. A writer fixes its own local test failures and small omissions before reporting once.
- A reviewer finishes the complete review even after finding a blocker and returns one consolidated report.
- Do not create agents for tests, individual findings, status checks, or micro-edits.
- Run repository-defined verification once on the accepted SHA. Reviewers rerun only focused checks needed to prove a concern.
- Merge only a SHA that was reviewed or directly verified after the escape-hatch decision, passes required checks, and closes the issue.

## Stop conditions

Workflow plumbing degrades before delivery stops. If a preferred skill, tool, subagent, comment, label, report format, or status update fails, preserve completed work and use an equivalent safe path. Keep PR descriptions to intent, material changes, acceptance criteria, verification evidence, and documentation impact—not an execution diary.

Continue autonomously while any safe in-scope path exists. Stop only when missing credentials, permission, required evidence, an unavailable external system, or an irreducible conflict actually removes every safe route to completion. Record that concrete blocker without turning it into an open-ended user decision.

Finish when every queued issue is merged and closed and the base branch is clean and synchronized.
