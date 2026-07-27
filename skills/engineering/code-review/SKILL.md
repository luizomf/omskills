---
name: code-review
description: Review changes from a fixed point against both repository standards and the originating spec. Use for branch, PR, or work-in-progress review.
---

# Code Review

Read the configured issue tracker and domain-document locations. If either configuration is unavailable, run `setup-omskills` first.

Review `git diff <fixed-point>...HEAD` once against two separately reported criteria sets:

- **Standards:** applicable repository instructions and conventions, maintainability, and relevant code smells.
- **Spec:** requested behavior, acceptance criteria, omissions, incorrect behavior, and changes outside the requested scope.

## Prepare

1. Use the fixed point supplied by the user. If none was supplied, infer one and ask the user only when none can be inferred.
2. Run `git diff <fixed-point>...HEAD`. If it is empty, stop and report that there are no changes to review. Otherwise, capture `git log <fixed-point>..HEAD --oneline`.
3. Locate the originating issue or specification from user-provided paths, commit references, or project documentation that names the changed behavior. If none is found, review observable correctness and report that specification compliance was not verified.
4. Locate every repository instruction or standards file that applies to a changed path.

## Dispatch one isolated reviewer

Use the harness's delegation mechanism to start exactly one reviewer. The reviewer may receive baseline system and project instructions, but must not receive parent conversational turns, coordinator analysis, or a requested verdict. If the harness cannot enforce that isolation, stop and report that this review cannot be performed under the required isolation.

Provide a self-contained prompt containing:

- repository path and fixed point;
- exact diff and commit-log commands;
- issue or specification source, when found;
- paths to applicable instruction and standards files;
- this contract:

```text
Review the complete diff in read-only mode. Read the supplied repository instructions, standards, and specification. Inspect Standards and Spec in one pass, including correctness, regressions, tests, security, documentation, portability, maintainability, missing requirements, and scope changes. Inspect every changed file even after finding a blocker. Report only concrete findings with file/line and evidence. Separate blockers from non-blocking observations and label each finding Standards or Spec. Do not edit, push, approve, merge, spawn, or delegate.
```

Treat code smells as investigation prompts, not violations. Repository rules and the originating specification take precedence over generic preferences. Omit formatter and linter findings when passing tooling already enforces them.

## Adjudicate and report

The root must verify each reported finding against the diff and its cited source. Reject invented requirements, speculative hardening, style preferences, and claims contradicted by repository conventions.

Report blockers first, ordered by severity, and label each finding **Standards** or **Spec**. Then list non-blocking observations and a short verdict. If no concrete finding survives adjudication, report a pass and any verification limits.

When evidence supports incompatible interpretations, choose the smallest safe interpretation that preserves requested behavior, quality, and security. Do not dispatch another reviewer, create a vote, or ask the user to adjudicate the review.
