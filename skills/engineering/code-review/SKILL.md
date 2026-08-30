---
name: code-review
description: Review a committed range or complete work-in-progress candidate against repository standards and its governing contract.
---

# Code Review

Read the configured issue tracker and domain-document locations. If either configuration is unavailable during an interactive invocation, run `setup-omskills` first and wait for its confirmed output. During a headless Ticket run, return a missing-setup blocker to the Ticket coordinator instead; never route setup through a Ticket dispatcher.

Review exactly one candidate in one of two modes:

- **Committed:** a fixed base commit through `HEAD`.
- **WIP:** the current staged, unstaged, and untracked worktree state.

Honor an explicit mode. Otherwise infer committed mode for a branch, PR, or supplied fixed point and WIP mode for a worktree request. Ask only when both remain plausible; never combine them into a partial hybrid.

Review against two separately reported criteria sets:

- **Standards:** applicable repository instructions and conventions, maintainability, and relevant code smells.
- **Spec:** the exact Ticket, accepted behavior, acceptance criteria, omissions, incorrect behavior, and changes outside scope.

## Prepare the complete candidate

### Committed mode

1. Use the fixed point supplied by the user. If none was supplied, infer one and ask only when none can be established.
2. Capture the complete `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`.
3. If the diff is empty, stop and report that there are no committed changes to review.

### WIP mode

1. Capture staged changes with `git diff --cached`.
2. Capture unstaged changes with `git diff`.
3. Inventory every untracked path and capture its complete content or binary status without treating ignored files as candidate work.
4. Report every unreadable or unrepresentable path as a capture limitation. If all three parts are empty, stop and report that there is no WIP candidate.

For either mode, locate the governing Ticket or specification and every repository instruction or standard applicable to the candidate. If no governing contract exists, review Standards and observable correctness while stating that Spec compliance could not be verified.

## Dispatch one isolated reviewer

Start exactly one clean, read-only reviewer. Supply the selected mode, complete candidate, governing contract, applicable repository instructions, and this contract:

```text
Review every supplied candidate path in one pass against Standards and Spec. Report only concrete findings with file/line and evidence. Separate blockers from non-blocking observations and label each finding Standards or Spec. Treat capture limitations explicitly. Do not edit, push, approve, merge, spawn, delegate, invent requirements, or expand the reviewed scope.
```

## Adjudicate and report

Verify every reported finding against the candidate and cited authority. Reject speculative hardening, style preferences, invented requirements, and claims contradicted by repository conventions.

Inside a Ticket with a current Prompt Audit `PASS` or explicit `BYPASS`, adjudicate all in-scope findings from the accepted sources without opening another user decision gate. If the sources cannot determine required behavior, report that Ticket as blocked rather than guessing or widening it. Findings outside the Ticket remain findings and never authorize new work.

Report the selected mode, capture limitations, blockers ordered by severity, non-blocking observations, and a short verdict. Do not dispatch another reviewer or create a correction/re-review loop.
