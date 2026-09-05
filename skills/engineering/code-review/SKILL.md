---
name: code-review
description: Review a committed range or complete work-in-progress candidate against repository standards and its governing contract.
---

# Code Review

Read applicable repository instructions and domain documents. Read issue-tracker configuration only when the review contract is tracked; an untracked Direct Assisted request uses its confirmed conversation as the contract and does not require tracker setup. If required configuration is unavailable during an interactive tracked invocation, run `setup-omskills` first and wait for its confirmed output. During a headless Ticket run, return a missing-setup blocker to the Ticket coordinator instead; never route setup through a Ticket dispatcher.

Review exactly one candidate in one of two modes:

- **Committed:** a fixed base commit through `HEAD`.
- **WIP:** the current staged, unstaged, and untracked worktree state.

Honor an explicit mode. Otherwise infer committed mode for a branch, PR, or supplied fixed point and WIP mode for a worktree request. Ask only when both remain plausible; never combine them into a partial hybrid.

Review against two separately reported criteria sets:

- **Standards:** applicable repository instructions and conventions, maintainability, and relevant code smells.
- **Spec:** the exact Ticket, accepted behavior, acceptance criteria, omissions, incorrect behavior, and changes outside scope.

## Prepare the complete candidate

### Committed mode

1. Use the fixed point supplied by the caller. If none was supplied, infer one and ask only when none can be established. Resolve review HEAD to a full SHA. For standalone committed review, resolve the base as the merge base of that fixed point and review HEAD, preserving the `fixed-point...HEAD` candidate. For coordinated review, use the supplied exact full base SHA and verify it is an ancestor of review HEAD.
2. In a coordinated Ticket review, verify the supplied candidate path, branch and exact HEAD before capture. Use that exclusive candidate, never an inherited caller checkout; do not create another workspace. Unexpected branch/HEAD drift stops review as incomplete.
3. Capture the complete `git diff <base-sha> <review-sha>` and `git log <base-sha>..<review-sha> --oneline` in that candidate. Check that its identity/HEAD remains unchanged after capture; report exact path, branch, base and review SHAs with any capture limitations.
4. If the diff is empty, stop and report that there are no committed changes to review.

### WIP mode

1. Capture staged changes with `git diff --cached`.
2. Capture unstaged changes with `git diff`.
3. Inventory every untracked path and capture its complete content or binary status without treating ignored files as candidate work.
4. Report every unreadable or unrepresentable path as a capture limitation. If all three parts are empty, stop and report that there is no WIP candidate.

For either mode, locate the current contract and every applicable repository instruction, governing source, and standard. The contract may be a tracked Ticket or Spec, or the concise confirmed request for untracked Direct Assisted work. If no governing contract exists, review Standards and observable correctness while stating that contract compliance could not be verified.

## Select the caller-safe review path

This skill requires one isolated review pass; assigning a reviewer name does not create isolation, read-only behavior, tools, or delivery semantics. Direct Assisted code or behavior changes and changes to Specs, ADRs, workflow, security, or other governing authority require this fresh independent pass. Purely editorial documentation may instead be self-reviewed.

- A root interactive Direct Assisted caller remains the responsible agent and may use the active harness's documented asynchronous delivery or a documented visible isolated-worker transport. An asynchronous caller resumes adjudication only after the one deterministic completion notification; after acceptance it does not wait, sleep, or poll.
- A print caller and a depth-2 Ticket coordinator that depends on the findings use direct delivery. Direct settlement returns once through the pending call and produces no later asynchronous completion notification.
- A designated depth-3 reviewer is already the one fresh review leaf: it performs the supplied one-pass contract directly with inherited non-delegating tools, returns complete findings to the Ticket coordinator, and skips the dispatch and adjudication sections below. A depth-3 writer does not self-review or invoke this helper; it consumes coordinator-supplied evidence or returns a blocker. Neither role requests a depth-4 reviewer.

Before launch, require a fresh isolated conversation with no parent transcript or prior child turns. Preflight the read-only tools and providers needed to inspect the complete candidate, and, where the harness exposes lineage controls, set the child's maximum delegation depth to its assigned depth and its direct-child ceiling to zero. An over-depth or capability mismatch must reject before launch or prompt acceptance. Do not retry it as though a review occurred.

Choose a complete result-recovery channel before dispatch. Prefer the full terminal response plus the harness's native session reference. If terminal text is bounded, read the complete assistant message from that session before adjudication. A harness without an adequate result or inspectable native session may instead use one predeclared findings artifact outside the candidate worktree; writing that artifact is the only allowed write. Require a mechanically completed outcome as well as complete findings: a failed, interrupted, cancelled, or missing reviewer outcome is incomplete even when its native session retains partial text. If complete decision-bearing findings cannot be recovered, report the review as incomplete rather than inferring a verdict.

## Dispatch one isolated reviewer

Start exactly one fresh, read-only, non-delegating reviewer. Supply the selected mode, candidate path and branch, exact base/review SHAs for committed mode (or complete staged/unstaged/untracked capture for WIP), complete candidate or exact read-only commands that reproduce it there, a concise current contract, applicable governing sources and repository instructions, verification instructions and results, the selected result channel, and this contract. Do not supply the parent transcript by default:

```text
Review every supplied candidate path in one pass against Standards and Spec. Perform the review directly and return all decision-bearing findings, not a lossy summary. Report only concrete findings with file/line and evidence. Separate blockers from non-blocking observations and label each finding Standards or Spec. Treat capture limitations explicitly. Do not edit the candidate, push, approve, merge, spawn, delegate, invoke code-review, invent requirements, or expand the reviewed scope. If and only if a findings artifact path was supplied, write the complete result there and report that exact path.
```

## Adjudicate and report

Verify every reported finding against the candidate and cited authority only after the reviewer has settled and the complete selected result channel has been recovered. Reject speculative hardening, style preferences, invented requirements, and claims contradicted by repository conventions.

In Direct Assisted work, the responsible agent adjudicates all findings, resolves any materially source-undetermined Question with the available maintainer, and performs surviving in-scope corrections directly. Dispatch a fresh re-review only when those corrections materially change the candidate; minor corrections receive direct verification instead.

Inside a Mission-authorized Ticket with a current Prompt Audit `PASS` or explicit `BYPASS`, the Ticket coordinator adjudicates all in-scope findings from the accepted sources, performs surviving corrections directly, and opens no other user decision gate. If the sources cannot determine required behavior, report the unresolved authority rather than guessing or widening it; the Ticket coordinator applies its preflight `blocked` versus operational setup/execution `failed` boundary. Findings outside the Ticket remain findings and never authorize new work. The managed single-pass route never dispatches another reviewer or creates a correction/re-review loop.

Report the selected mode, capture limitations, blockers ordered by severity, non-blocking observations, and a short verdict.
