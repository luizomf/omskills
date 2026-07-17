---
name: orchestrate-issue-queue
description: Orchestrate an ordered queue of repository issues with one fresh writer, one fresh reviewer, one retry, and sequential integration. Use for multi-issue implement-review-merge work that must preserve clean contexts and exact-SHA review.
---

# Orchestrate Issue Queue

Coordinate the queue; do not implement or approve changes yourself. Process one issue at a time and keep Git and the issue tracker authoritative.

## Exercise judgment

Treat a detailed issue as the default plan, not an immutable script. The orchestrator owns delivery and may adjust implementation details, tests, acceptance wording, or sequencing when repository evidence shows a better path. Preserve the issue's intent and approximate scope, keep the code simple and maintainable, and never weaken security or documented boundaries merely to make a check pass.

Make engineering decisions autonomously and record material deviations in the PR. When alternatives differ, choose the smallest safe option that best preserves the issue's intent, code quality, maintainability, and security. Do not return tradeoffs or failed reviews to the user for resolution.

## Keep every context clean

- Start the orchestration in a fresh task. Keep its context lean: consume compact agent reports and authoritative PR/issue state, not full transcripts or unfiltered logs. At an issue boundary, hand off the queue state to a fresh orchestrator whenever the current context has accumulated implementation detail.
- Start every writer and reviewer with fresh context. Give them source locations, the issue, the exact SHA when reviewing, and the required outcome—not another agent's conversation.
- Writers and reviewers are leaf agents. They do not spawn or delegate.
- Never reuse an agent for another role, round, or issue.

Use [references/subagent-contracts.md](references/subagent-contracts.md) as compact role prompts.

## Run the queue

For each issue:

1. **Preflight:** Confirm the issue is open, unowned, unblocked, and has enough acceptance criteria to implement. Confirm the base branch and worktree are safe.
2. **Write:** Dispatch one fresh writer for the whole issue. The writer owns implementation, local iteration, relevant tests, commit, push, and the PR.
3. **Validate delivery:** Revalidate the PR and exact remote SHA. Treat GitHub as authoritative.
4. **Review:** Dispatch one fresh read-only reviewer for the whole issue at that SHA. The reviewer checks the spec, behavior, tests, security implications, documentation, and repository rules in one pass.
5. **Adjudicate:** Verify every blocking finding yourself. Ignore vague, duplicated, or non-reproducible objections.
6. **Retry once:** If blockers remain, dispatch one fresh writer with the issue and adjudicated findings. After its delivery, dispatch one fresh reviewer for the new SHA. Any push invalidates the earlier review.
7. **Resolve:** If the second review still blocks, choose the smallest safe path forward from the available evidence. You may revise non-material issue details when that produces a simpler, correct, maintainable, and secure result. Give the decision, revised constraints, and surviving blockers to a new fresh writer; do not reopen process discussion. Verify the resulting SHA yourself and merge when the issue's intent, checks, and repository rules are satisfied.
8. **Advance:** Confirm the issue closed, then start the next issue with new agents.

The normal budget per issue is therefore one writer and one reviewer, with one fresh writer/reviewer retry only when needed. The final resolution writer is an escape hatch, not another automatic review loop.

## Whole-issue passes

- The issue is the unit of work. A writer fixes its own local test failures and small omissions before reporting once.
- A reviewer finishes the complete review even after finding a blocker and returns one consolidated report.
- Do not create agents for tests, individual findings, status checks, or micro-edits.
- Run repository-defined verification once on the accepted SHA. Reviewers rerun only focused checks needed to prove a concern.
- Merge only a SHA that was reviewed or directly verified after the escape-hatch decision, passes required checks, and closes the issue.

## Stop conditions

Continue autonomously while any safe in-scope path exists. A missing credential, permission, unavailable external system, or irreducible conflict with the requested outcome may make completion objectively impossible; record that concrete blocker and stop without turning it into an open-ended user decision.

Finish when every queued issue is merged and closed and the base branch is clean and synchronized.
