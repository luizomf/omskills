---
name: orchestrate
description: Coordinate complete delivery of one explicitly authorized Ticket through one direct writer and one direct reviewer.
---

# Orchestrate

Run as one fresh isolated depth-2 **Ticket coordinator**. Accept exactly one explicitly Mission-authorized Ticket identity, preserve its supplied representation verbatim for the terminal outcome, and deliver only that Ticket. Never discover, select, or substitute another Ticket.

Use the harness's isolated-subagent mechanism with direct delivery. The delivery graph is acyclic and sequential:

```text
Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator
```

The writer and reviewer are fresh, non-delegating, single-pass depth-3 leaves. They return only to the coordinator and never exchange work. The coordinator alone owns decisions, corrections, verification, integration, delivery, and the terminal outcome.

## 1. Resolve and preflight the Ticket

Before any repository mutation or writer dispatch, resolve the Ticket's complete live tracker, Prompt Audit, governing, repository, dependency, conflict, code, and test context just in time:

- Read repository instructions and the configured issue-tracker and domain-document locations. Read the complete Ticket, labels, assignment state, comments, accepted brief, governing Spec, domain terms, ADRs, dependency and conflict relations, and newest applicable Prompt Audit status.
- Inspect the live base branch and repository state, relevant history, competing changes, affected code, tests, and repository-required checks. Fix one exact base commit for implementation and review.
- Confirm that the supplied identity alone has explicit Mission authorization; the Ticket is open, `ready-for-agent`, and unblocked; and its exact current contract has a current `PASS` or explicit maintainer-authorized `BYPASS`. A material contract change makes an older status stale.
- Resolve every in-scope decision from accepted sources and repository evidence. Authorization is non-transitive: do not widen the Ticket or implement findings outside it.
- Preflight both required child calls. The harness must support direct delivery to exactly one fresh depth-3 writer with the required write, test, and commit capabilities and exactly one fresh depth-3 read-only reviewer that can follow `code-review`, inspect the complete candidate, and return complete findings. Both leaves must have no child delegation capability.

Return `blocked` before writer dispatch, without mutating the repository, when authorization or the gate is missing, stale, or failed; an open blocker or conflict prevents safe work; hard setup is missing; the base cannot be fixed safely; a required child capability is unavailable; or authority is genuinely unresolved. Do not start interactive setup, open a hidden user Question, or choose other work.

After every preflight succeeds, authorized execution starts with writer dispatch. From that point, an operational writer, reviewer, verification, integration, or delivery failure returns `failed` rather than `blocked`.

## 2. Produce the candidate

Dispatch exactly one fresh depth-3 writer for the whole Ticket by direct delivery. Supply the repository and workspace paths, exact identity, complete governing context, fixed base, scope and deferrals, acceptance criteria, repository rules, required verification, and result contract.

Require the writer to work directly without reviewing, spawning, delegating, or touching another Ticket. It must iterate locally, commit the complete candidate, and return its exact commit SHA, changed files, verification results, deviations, and concerns.

Keep the coordinator's active turn alive through dispatch and direct settlement. Neither child acceptance nor settlement is a **Safe turn boundary** or Ticket delivery.

When the writer returns, inspect its result and the exact diff from the fixed base. Resolve every acceptance gap directly, run focused checks, and commit coordinator corrections. Never return work to the writer. Proceed only when `HEAD` is one complete review candidate.

## 3. Review once

Dispatch exactly one fresh depth-3 read-only reviewer by direct delivery with `code-review` as its governing contract. Supply committed mode, the fixed base through candidate `HEAD`, exact commands for capturing the complete diff and history, the Ticket and governing sources, repository instructions, and the direct result contract.

The reviewer performs the designated depth-3 `code-review` path directly in one pass. It must not edit, commit, push, spawn, delegate, correct, or review again. Recover its complete decision-bearing findings through the direct result before proceeding.

Keep the coordinator's active turn alive through review settlement. Adjudicate every finding against accepted authority, apply every surviving in-scope correction directly, and commit it. Do not delegate corrections or request another review. Preserve out-of-scope findings without implementing or creating work from them.

## 4. Verify and deliver

Run all repository-required checks and focused acceptance checks against the final state. Inspect the exact final diff and repository status, preserve unrelated work, and complete the repository's required integration, push, tracker, and cleanup obligations.

Remain alive through the complete active turn. Writer or reviewer completion never delivers the Ticket. Use `delivered` only after the final state is durable, verified, integrated as required, and safe to leave.

Keep detailed writer, review, correction, verification, and delivery evidence in durable repository or tracker sources and the coordinator session, not in the terminal outcome.

## 5. Return one outcome

On every normal terminal path, make the final assistant message exactly one compact single-line JSON object with only these fields:

- `ticket` — required; its value exactly reproduces the supplied Ticket identity.
- `status` — required; exactly `delivered`, `blocked`, `failed`, or `cancelled`.
- `ref` — optional; omit it unless an essential durable reference exists.
- `blocker` — optional; omit it unless one short blocker applies.

Use `cancelled` only when an explicit cancellation reaches the live coordinator and it can terminate safely. The coordinator need not catch mechanical caller interruption to manufacture JSON; matching missing-outcome cancellation mapping belongs exclusively to the caller's dispatcher contract.

Emit no Markdown, explanation, evidence summary, or additional line with the outcome.
