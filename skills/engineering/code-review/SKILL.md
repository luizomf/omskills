---
name: code-review
description: Review changes from a fixed point against both repository standards and the originating spec. Use for branch, PR, or work-in-progress review.
---

# Code Review

Read the configured issue tracker and domain-document locations. If either configuration is unavailable, run `setup-omskills` first.

Review exactly one selected candidate against two separately reported criteria sets:

- **Standards:** applicable repository instructions and conventions, maintainability, and relevant code smells.
- **Spec:** accepted behavior, acceptance criteria, omissions, incorrect behavior, and changes outside the accepted scope.

## 1. Select the mode and authority

Select exactly one mode from the request and name it in all subsequent work:

- **Committed mode** reviews a committed branch, pull request, or fixed-point-to-`HEAD` candidate.
- **WIP mode** reviews the current index and worktree candidate, including staged, unstaged, and untracked state. It does not silently fold committed changes into that candidate.

Honor an explicit mode. Otherwise infer committed mode for a supplied base/fixed point or committed branch/PR request and WIP mode for a worktree or work-in-progress request. Ask only when both remain plausible and selecting one would materially change the candidate. Never combine the modes into a partial hybrid review. In committed mode, use the user-supplied base/fixed point when present; otherwise infer the branch or PR base from repository evidence and ask only when no single base can be established.

Locate the accepted behavior in the complete governing Spec, Ticket, issue, or other durable source, and locate every repository instruction or standards file applicable to the candidate paths. If accepted behavior exists only in conversation, reconstruct a self-contained contract with explicit **Outcome**, **Scope**, **Deferrals**, **Acceptance criteria**, and **Completion**. Preserve the accepted meaning; do not add preferred work or expose parent conversation turns, coordinator analysis, or private context.

Compare the authoritative sources before collecting or dispatching the review candidate. If they materially conflict, stop and report the sources, incompatible claims, and decision needed from the owning authority. A material authority conflict is not a source-determined preference and must never receive a silent smallest-safe interpretation.

## 2. Validate untrusted refs

Treat every user-supplied ref, revision, base, or fixed point as untrusted data. Before using one in any Git operation:

1. Reject an empty value, an option-like value beginning with `-`, control characters or whitespace, and shell fragment syntax such as semicolons, ampersands, pipes, backticks, `$()`, or redirections.
2. Pass the value only as one direct process argument with shell execution disabled. Never interpolate it into a command string, evaluate it, or use `eval`.
3. Resolve it with the argument-array equivalent of `git rev-parse --verify --end-of-options '<value>^{commit}'`. Reject a nonzero, missing, ambiguous, or non-commit result.
4. Retain only the resolved commit object ID for subsequent range operations. Resolve `HEAD` to a commit object ID as well so the selected committed candidate is stable.

On any rejection, report the invalid input and stop before candidate collection or isolated reviewer dispatch. Do not fall back to another ref or perform a partial review. Every later Git command uses direct argument arrays and an explicit `--` path boundary; no candidate value or path is shell-evaluated.

## 3. Capture the complete candidate

### Committed mode

After resolving the accepted base and `HEAD`, capture both of these with the resolved object IDs:

- the complete binary-preserving range using the argument-array equivalent of `git diff --no-ext-diff --binary <base-oid>...<head-oid> --`;
- the associated commit log using the argument-array equivalent of `git log --oneline <base-oid>..<head-oid> --`.

The committed candidate is empty when the captured range diff has no bytes. Report `Selected mode: committed` and the empty candidate without dispatching an isolated reviewer, even if the range contains an empty commit.

### WIP mode

Capture all three WIP components separately so staged and unstaged states of the same path remain visible:

- staged: `git diff --no-ext-diff --binary --cached --`;
- unstaged: `git diff --no-ext-diff --binary --`;
- untracked inventory: `git ls-files --others --exclude-standard -z --`.

Parse the untracked inventory as NUL-delimited paths. Create one empty temporary file outside the repository. For every path, record the path in the inventory and capture a binary-preserving patch with the direct-argument equivalent of `git diff --no-index --no-ext-diff --binary -- <empty-temp-file> <path>`. Treat status `0` with no diagnostic as complete empty-file content. Treat status `1` as a successful difference only when Git emits a usable patch and no diagnostic. Any other result—including status `0` with a diagnostic or status `1` with no usable patch or with a diagnostic—is a capture limitation. Retain the raw stdout, exact status, and stderr for that path, and keep the path in the candidate inventory. Remove the temporary file after capture.

Never silently omit a binary or unreadable path. If Git cannot read or represent a candidate path, report the retained status and diagnostic and do not claim complete content coverage for that path. Do not reinterpret ignored files as untracked candidate files.

The WIP candidate is empty only when both tracked diffs have no bytes and the untracked inventory has no paths. Report `Selected mode: WIP` and the empty candidate without dispatching an isolated reviewer.

## 4. Dispatch one isolated reviewer

Use the harness's delegation mechanism to start exactly one reviewer. The reviewer may receive baseline system and project instructions, but must not receive parent conversational turns, coordinator analysis, or a requested verdict. If the harness cannot enforce that isolation, stop and report that this review cannot be performed under the required isolation.

Provide one self-contained assignment containing:

- `Selected mode: committed` or `Selected mode: WIP`;
- repository path and the exact direct-argument Git commands used;
- the complete captured candidate: committed diff and log, or staged diff, unstaged diff, untracked path inventory and per-path patches;
- every capture limitation, including binary or unreadable path limitations;
- every applicable repository instruction and standards source, identified by path and supplied with complete content;
- the complete accepted durable behavior source, or the self-contained conversational contract from step 1; and
- this contract:

```text
Review the complete supplied candidate in read-only mode. Read every supplied repository instruction, standards source, and accepted behavior source. Inspect Standards and Spec in one pass, including correctness, regressions, tests, security, documentation, portability, maintainability, missing requirements, and scope changes. Inspect every candidate path even after finding a blocker. Treat each reported capture limitation as an explicit review limitation; never imply that omitted or unreadable content was inspected. Report only concrete findings with file/line and evidence. Separate blockers from non-blocking observations and label each finding Standards or Spec. Do not edit, push, approve, merge, spawn, or delegate.
```

## 5. Adjudicate and report

The root verifies every reported finding against the complete candidate and its cited authority. Reject invented requirements, speculative hardening, style preferences, and claims contradicted by repository conventions. Treat code smells as investigation prompts, not violations, and omit formatter or linter findings when passing repository tooling already enforces them.

Start the result with **Selected mode: committed** or **Selected mode: WIP**. Report candidate-capture and verification limitations, then blockers ordered by severity, non-blocking observations, and a short verdict. Label every finding **Standards** or **Spec**. If no concrete finding survives, report a pass and every verification limit.

If review evidence reveals a material conflict between authoritative sources, stop adjudication and report the conflicting sources and claims to the owning authority. When no authority conflict exists, resolve ordinary non-material evidence questions with the smallest safe interpretation that preserves accepted behavior, quality, and security. Do not dispatch another reviewer, create a vote, or start a delegated correction or re-review loop.
