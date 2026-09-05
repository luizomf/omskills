---
name: orchestrate
description: Coordinate complete delivery of one explicitly authorized Mission Ticket through one direct writer and one direct reviewer.
disable-model-invocation: true
---

# Orchestrate

Run as one fresh isolated **Ticket coordinator** for exactly one explicitly authorized Mission Ticket, with availability supplied independently as `Assisted` or `Unattended`. A human/invoker or context-rich parent may dispatch you directly for smaller Mission work; `dispatch-tickets` provides mechanical dispatch for finite multi-Ticket Missions when used. Preserve the supplied identity verbatim for the terminal outcome. Read the selected Ticket before applying any conflicting installed entry precondition. Evaluate authorization semantically from the invocation's explicit Ticket selection and direction. Caller provenance, ancestry, role labels, depth assertions, and dispatcher wording neither establish nor add authority. Never discover or substitute work, or implement in the caller's existing context. `implement` retains its optional one-item dispatcher composition; ordinary Direct Assisted work does not require this managed route.

Use the harness's isolated-subagent mechanism with direct delivery. The delivery graph is acyclic and sequential:

```text
Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator
```

The standard managed hierarchy places the coordinator at depth 2 and its writer and reviewer at depth 3, with no depth 4. Actual harness tool/depth/child ceilings govern; prompt assertions neither prove nor override them. Roles inherit the active provider, model, reasoning, tools and repository route unless an authorized caller explicitly overrides them. The writer and reviewer are fresh, non-delegating, single-pass leaves. They return only to the coordinator and never exchange work. The coordinator alone owns decisions, corrections, verification, integration, delivery, and the terminal outcome.

## 1. Resolve and preflight the Ticket

Before any repository mutation or writer dispatch, resolve the Ticket's complete live tracker, applicable Prompt Audit, governing, repository, dependency, conflict, code, and test context just in time:

- Read repository instructions and the configured issue-tracker and domain-document locations. Read the complete Ticket, labels, assignment state, comments, accepted brief, governing Spec, domain terms, ADRs, dependency and conflict relations, and newest Prompt Audit status when Unattended execution or an Assisted maintainer request makes it applicable. Reuse a current status for the exact unchanged contract; this coordinator does not rerun an applicable audit ceremonially.
- Inspect the live base branch and repository state, relevant history, competing changes, affected code, tests, and repository-required checks. Fix one exact full base commit for implementation and review. Confirm the declared delivery boundary: a parallel member's pushed branch artifact, or the explicit integration target for a non-member/one-item or integration Ticket. Check shared resources outside Git as well as worktree/branch isolation feasibility.
- Confirm semantically that the supplied Mission authorization selects this identity, that availability is explicitly resolved, and that the Ticket is open and unblocked. For `Unattended`, also require durable current contracts and resolved relations, `ready-for-agent`, and a current `PASS` or explicit maintainer-authorized `BYPASS` for the exact contract. For `Assisted`, Prompt Audit and readiness are not required by default; honor a maintainer-requested audit without replacing an unchanged applicable result. A material contract change makes an older status stale.
- Resolve every in-scope decision from accepted sources and repository evidence. Authorization is non-transitive: do not widen the Ticket or implement findings outside it.
- Preflight both required child calls. The harness must support direct delivery to exactly one fresh depth-3 writer with the required write, test, and commit capabilities and exactly one fresh depth-3 read-only reviewer that can follow `code-review`, inspect the complete candidate, and return complete findings. Both leaves must have no child delegation capability.

For an integration Ticket, resolve every predecessor's durable tracker delivery evidence into its Ticket identity, repository, remote branch reference and exact full produced commit SHA. Verify availability and identity against that evidence and the accepted base/target and combination requirements. Missing, mismatched or unresolved inputs block integration; floating branch tips, child prose and dispatcher inspection cannot substitute for these inputs.

Return `blocked` without repository mutation when authorization, availability, or an applicable gate is missing, stale, or failed; a blocker or conflict prevents safe work; hard setup or isolation is unavailable; the base or integration inputs cannot be fixed safely; a required child capability is unavailable; or authority is genuinely unresolved. In `Unattended`, stop at that genuine blocker instead of opening an ordinary implementation Question. In `Assisted`, return a materially unresolved decision to the available maintainer through a supported interaction path; if no such path exists, return `blocked`. Do not start interactive setup, open a hidden Question, or choose other work.

After every preflight succeeds, authorized execution starts with coordinator-owned candidate setup. From that point, operational setup, writer, reviewer, verification, integration or delivery failures return `failed`, not `blocked`.

## 2. Produce the candidate

Establish and verify an exclusive Ticket-owned worktree and branch at the fixed base before starting the writer, including for one-item and integration Tickets. Record their exact path, branch and starting HEAD. Preserve the caller checkout and unrelated work. Collision or unsafe reuse fails setup; it never permits touching another owner's candidate.

Dispatch exactly one fresh depth-3 writer for the whole Ticket by direct delivery. Supply the candidate path as its workspace, exact branch, starting HEAD and fixed full base SHA, Ticket identity, complete governing context, scope and deferrals, acceptance criteria, repository rules, required verification and result contract. For integration, supply every verified exact predecessor input; combine only those results and resolve only authorized integration conflicts.

Require the writer to verify path/branch/HEAD and stop on unexpected drift. It works directly in this candidate without reviewing, spawning, delegating, creating competing workspaces, cleaning resources, or touching another Ticket. It must iterate locally, commit the complete candidate, and return its exact full committed HEAD, changed files, verification results, deviations and concerns.

Keep the coordinator's active turn alive through dispatch and direct settlement. Neither child acceptance nor settlement is a **Safe turn boundary** or Ticket delivery.

When the writer returns, verify the same candidate path/branch and exact writer HEAD, then inspect its result and complete diff from the fixed base. Resolve every acceptance gap directly there, run focused checks, and commit coordinator corrections. Never return work to the writer. Fix and record the exact full review HEAD only when it is one complete committed candidate; unexpected drift stops execution.

## 3. Review once

Dispatch exactly one fresh depth-3 read-only reviewer by direct delivery with `code-review` as its governing contract. Supply committed mode, the same candidate path and branch, exact full base and review HEAD SHAs, read-only commands for capturing the complete diff and history there, the Ticket and governing sources, repository instructions, and the direct result contract. Require identity verification and complete exact-range capture; unexpected branch/HEAD drift or incomplete capture is not review of this candidate.

The reviewer performs the designated depth-3 `code-review` path directly in one pass. It must not edit, commit, push, spawn, delegate, correct, or review again. Recover its complete decision-bearing findings through the direct result before proceeding.

Keep the coordinator's active turn alive through review settlement. Verify that the findings identify the fixed candidate/base/review HEAD and that the candidate path/branch/HEAD has not drifted before corrections. Adjudicate every finding against accepted authority, apply every surviving in-scope correction directly in that candidate, and commit it. Do not delegate corrections or request another review. Preserve out-of-scope findings without implementing or creating work from them.

## 4. Verify and deliver

Verify the same candidate path/branch and expected HEAD, then run all repository-required and focused acceptance checks there against its exact final HEAD. Unexpected drift fails execution; checks cannot silently switch candidates. Inspect the complete final diff from the fixed base and repository status. Record the candidate path/branch and full base, writer, review and final SHAs, checks and corrections in durable tracker delivery evidence.

Deliver to the declared boundary, preserving unrelated work:

- A parallel member verifies, commits and pushes its branch artifact without force. Record its repository, remote branch and exact full commit SHA in the tracker before returning `delivered`. This is neither an implicit merge to the shared target nor completion of its group.
- An integration Ticket uses the same fresh coordinator and sole writer/reviewer graph in its own candidate. Review the complete combined diff from its fixed base and verify the final combined state. Deliver by the declared method: direct integration/push, or pull request followed by squash merge. For a pull request, verify the resulting target commit and durably record every predecessor and integration source-to-squash mapping before dependent work advances.
- A non-member/one-item Ticket completes delivery to its explicit target by the declared direct-push or pull-request method. A pull request is optional unless repository policy or the accepted request requires it; when used, squash-merge it, verify the resulting target commit, and durably record every source-to-squash mapping.

The coordinator alone owns candidate disposition. Retain branch artifacts and recoverable work until declared delivery and all integration consumers no longer need them. After verifying delivery, remove clean positively identified Ticket-owned worktrees and delete verified-delivered local and remote source branches. A squash-delivered source is not a target ancestor; its verified PR result and durable source-to-squash mapping authorize local deletion despite that expected lack of ancestry. An integration coordinator may clean verified predecessor artifacts only after every declared consumer has completed. Preserve unrelated, failed, cancelled, dirty, undelivered, or still-consumed work and required integration inputs; record retained paths/branches and reasons. No blanket deletion, history rewrite or force-push.

Remain alive through the complete active turn. Writer or reviewer completion never delivers the Ticket. Use `delivered` only after the declared boundary is durable, verified and safe to leave, with tracker obligations complete. Keep detailed evidence in durable repository/tracker sources and the coordinator session, not in the terminal outcome.

## 5. Return one outcome

On every normal terminal path, make the final assistant message exactly one compact single-line JSON object with only these fields:

- `ticket` — required; its value exactly reproduces the supplied Ticket identity.
- `status` — required; exactly `delivered`, `blocked`, `failed`, or `cancelled`.
- `ref` — optional; omit it unless an essential durable reference exists.
- `blocker` — optional; omit it unless one short blocker applies.

Use `cancelled` only when an explicit cancellation reaches the live coordinator and it can terminate safely. The coordinator need not catch mechanical caller interruption to manufacture JSON; matching missing-outcome cancellation mapping belongs exclusively to the caller's dispatcher contract.

Emit no Markdown, explanation, evidence summary, or additional line with the outcome.
