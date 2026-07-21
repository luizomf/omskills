---
name: code-review
description: Review changes from a fixed point against both repository standards and the originating spec. Use for branch, PR, or work-in-progress review.
disable-model-invocation: true
---

# Code Review

Review `git diff <fixed-point>...HEAD` through two lenses in one clean pass:

- **Standards:** repository instructions, conventions, maintainability, and relevant code smells.
- **Spec:** requested behavior, acceptance criteria, omissions, incorrect behavior, and scope creep.

The lenses stay distinct in the report, but one fresh reviewer covers both so it can notice interactions without duplicating repository reads.

## Prepare the review

1. Resolve the fixed point supplied by the user. Ask only when none can be inferred. Confirm the three-dot diff is non-empty and capture `git log <fixed-point>..HEAD --oneline`.
2. Locate the originating issue or spec from commit references, a user-provided path, or matching project docs. If none exists, review observable correctness and state that spec compliance could not be checked.
3. Locate applicable repository instruction and standards files.

## Dispatch one clean reviewer

Use the harness's delegation mechanism to start one fresh, independent reviewer. The reviewer must not inherit the parent conversation; baseline system and project instructions are acceptable, but conversational turns, coordinator analysis, and desired answers must not carry over. If the harness cannot guarantee this isolation, stop and report that the review cannot be performed reliably. Give the reviewer a compact, self-contained initial prompt containing:

- repository and fixed point;
- diff and commit commands;
- spec or issue source, when available;
- applicable instruction and standards paths;
- the contract below.

```text
Review the complete diff in read-only mode. Read the supplied repository instructions, standards, and spec. Inspect both Standards and Spec in one pass, including correctness, regressions, tests, security implications, documentation, portability, maintainability, missing requirements, and scope creep. Finish the whole surface even after finding a blocker. Report only concrete findings with file/line and evidence; separate blockers from non-blocking observations and keep Standards and Spec labels. Do not edit, push, approve, merge, spawn, or delegate.
```

The reviewer may use code smells as heuristics, never automatic violations. Repository rules and the actual spec override generic preferences. Skip formatter or linter findings already enforced by passing tooling.

## Adjudicate and report

The root verifies every finding against the diff and its cited source. Reject invented requirements, speculative hardening, stylistic preferences, and findings contradicted by repository conventions. Make routine judgment calls without adding another reviewer.

Report blockers first, ordered by severity, with Standards or Spec labels. Then list non-blocking observations and a short verdict. If no concrete finding survives adjudication, report a pass and any verification limits.

If evidence leaves a material technical disagreement, the root chooses the smallest safe interpretation that preserves requested behavior, quality, and security. Do not dispatch another reviewer, create a voting loop, or return the judgment to the user.
