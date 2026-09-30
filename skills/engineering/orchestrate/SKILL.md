---
name: orchestrate
description:
  Own one selected Ticket from investigation through implementation, independent
  review, and verified delivery. Use when responsible for completing a Mission
  Ticket.
---

# Orchestrate

Be the technical owner of one selected Ticket. Keep investigation,
implementation, tests, debugging, review adjudication, corrections, and delivery
in this conversation. Bring in a fresh independent reviewer for the complete
candidate. The default flow is:

```text
owner: investigate → implement and test → independent reviewer
     → adjudicate and correct → verify and deliver
```

A dispatcher may start you, or an authorized caller may invoke you directly. Use
the established conversation when already responsible for this Ticket; a new
dispatched Ticket starts with a fresh owner. A conversation that conducted its
Prompt Audit hands implementation to a fresh owner. Read the selected Ticket and
resolve authority from the accepted request, rather than caller ancestry or role
labels.

Before reading any relative link, run
`python3 -c 'from pathlib import Path; import sys; print((Path(sys.argv[1]).resolve().parent / sys.argv[2]).resolve())' '<loaded-file-path>' '<relative-link>'`
with this file's actual path and the link, then read the printed path. Pass
resolved skill paths to fresh agents.

## 1. Resolve the contract and candidate

Read repository instructions, configured tracker operations, the complete Ticket
and relevant comments, governing Spec/domain docs/ADRs, dependency results, and
conflicts. Inspect the repository, live base, existing worktrees, affected
code/tests, and shared resources. If required configuration is missing, follow
[setup-omskills](../setup-omskills/SKILL.md) within its scoped authorization.

Establish:

- The selected identity, authorized scope, acceptance criteria, deferrals, and
  delivery boundary.
- `Assisted` or `Unattended` availability from the accepted request. In Assisted
  work, use accepted sources and consult the maintainer for materially
  unresolved decisions. Unattended work requires durable current authority,
  resolved dependencies, `ready-for-agent`, and a current Prompt Audit `PASS` or
  explicit `BYPASS` for the exact contract. Reuse unchanged applicable evidence;
  a material contract change requires updating authority and the applicable
  gate.
- Actual implementation, verification, delivery, and independent-review
  capabilities, including remote environments and ownership where relevant.
- An exclusive Ticket-owned worktree and branch with an exact full base SHA.
  Follow [WORKTREES.md](WORKTREES.md) for location, ownership, safe reuse, and
  cleanup. Record the path, branch, and starting HEAD. On resumption, verify the
  recorded candidate and current state before changing it.

For integration Tickets, verify each predecessor's repository, remote branch,
and exact full produced commit against durable delivery evidence. Establish the
target and combination requirements before combining inputs.

Report a concrete blocker when required authority, dependencies, ownership,
setup, or capabilities are missing. Preserve recoverable work and identify the
decision or evidence needed. The dispatcher can keep independent work moving
while this Ticket remains paused.

This step is complete when the live contract, gates, ownership, fixed base, and
delivery boundary permit implementation, or the specific blocker and recoverable
state have been reported.

## 2. Investigate, implement, and test

Do the technical work yourself in the owned candidate, retaining the reasoning
that connects evidence to changes. Use focused planning for work that benefits
from it and the repository's implementation conventions.

For bugs, follow [diagnosing-bugs](../diagnosing-bugs/SKILL.md): reproduce the
reported failure and establish a faithful regression test where a suitable seam
exists. If automation is impractical, record the limitation and before/after
evidence. Use [tdd](../tdd/SKILL.md) for test-first changes. Bounded research or
design assistance can support your decisions within the task and available
capabilities; you retain candidate ownership and implementation.

Resolve routine decisions from accepted sources. Failing checks and correctable
defects are implementation work: keep investigating, fixing, and verifying while
an in-scope next action is available. Report a blocker only with the concrete
missing prerequisite that prevents that progress. Material user steering updates
the affected contract and applicable gates before the changed implementation.
Keep out-of-scope findings as findings. For integration, combine the verified
predecessor commits and resolve the authorized integration work in this
candidate.

Verify path, branch, and expected HEAD before consequential changes; investigate
unexpected drift rather than silently switching candidates. Run focused checks,
inspect the complete diff from the fixed base, and commit the complete
candidate. Record the exact full review SHA.

This step is complete when the candidate covers every acceptance criterion,
relevant checks have results, and the complete committed candidate is ready for
independent review, or a blocker/failure has a recoverable handoff.

## 3. Review and adjudicate

Follow [code-review](../code-review/SKILL.md) for one fresh independent
adversarial review of the complete candidate. Use the environment's isolated
subagent mechanism or [tmux-worker](../../productivity/tmux-worker/SKILL.md),
preserving that transport's result and editor-safety rules. Read
[model-routing](../../productivity/model-routing/SKILL.md) before a
model-selectable launch and follow active harness authorization and inheritance.

Give the reviewer the resolved review-skill path, candidate path and branch,
exact full base/review SHAs, governing contract, applicable repository
instructions, verification results, and a complete result channel. The reviewer
applies code-review's adversarial contract read-only and returns every supported
finding, including non-blocking problems, in this single planned pass; you
remain the implementation owner.

For managed calls, use the harness's actual direct/asynchronous delivery path.
After asynchronous acceptance, retain the review identity and release the turn;
adjudicate after its matching completed result arrives. Unknown acceptance
requires evidence recovery before another launch. For visible workers, agree on
the result artifact/event before starting. Recover complete findings and a
completed review outcome; interrupted or partial review does not count as
completed review.

Apply code-review's one-way handoff: adjudicate every finding, correct confirmed
in-scope problems, and verify the final result yourself. Keep resolving failures
without returning corrections for reviewer approval or another review. Record
the reviewed and final SHAs honestly, including what changed after review.

This step is complete when the independent pass is complete, every finding has
an evidence-based disposition, and confirmed in-scope problems have verified
corrections.

## 4. Verify and deliver

Check the candidate identity and final HEAD. Run repository-required checks and
focused acceptance verification against the final state; reuse results only
where relevant inputs are unchanged. Inspect the complete final diff and status.
Record the base, reviewed, and final SHAs, checks, findings/dispositions, and
any verification limitations in durable delivery evidence.

Complete the declared delivery method:

- **Branch artifact:** push the verified branch and record repository, remote
  reference, and exact full commit. Preserve it for its integration consumer.
- **Target delivery:** integrate by the agreed direct-push or pull-request
  method. A PR is optional unless required by the repository or request. When
  used, squash-merge it, verify the resulting target commit and content
  equivalence, and record the source-to-squash mapping.
- **Integration Ticket:** review and verify the complete combined state from its
  fixed base, deliver to the target, and record exact predecessor-to-result
  mappings before dependent work proceeds.

Complete tracker obligations and verified cleanup under
[WORKTREES.md](WORKTREES.md), retaining protected artifacts with explicit
reasons. Protect private environment details, credentials, logs, and
continuation notes; publish only appropriate delivery evidence.

If an operation fails, inspect what actually completed before attempting
recovery within the task's authority. Preserve the candidate and evidence. A
successful push with outstanding review, verification, tracker, or cleanup work
is partial delivery, not completion.

This step is complete when the declared boundary is durable and verified,
required tracker updates and eligible cleanup are complete, or the precise
remaining obligation and recovery state have been reported.

## 5. Report the outcome and preserve continuity

Return a concise report through the agreed channel with Ticket identity, status,
evidence references, and any blocker or next action. Use `delivered` for
verified completion, `blocked` for a missing decision/prerequisite, `failed` for
an incomplete operational attempt, and `cancelled` for an explicit safe stop.
Identify any publication that succeeded despite an incomplete overall outcome.
JSON is optional when useful to the caller; evidence establishes delivery.

For blocked, failed, or cancelled work, retain the conversation and candidate,
branch/worktree, HEAD and dirty changes, completed checks, current hypothesis,
and recommended next step. Prefer resuming this same owner when the blocker
clears. Before any replacement writes, establish that prior candidate-writing
activity has stopped and transfer the recoverable state. Silence alone does not
establish failure or permission for concurrent ownership.

This step is complete when the caller can verify delivery or resume the
outstanding work without reconstructing its state from scratch.

## Example

For a selected regression Ticket, reproduce the failure in the owned worktree,
add a faithful failing test, implement the fix, and run the relevant checks.
Commit candidate A and obtain independent review of base → A. Adjudicate the
findings, commit correction B, and verify the final state. Record A as reviewed
and B as final, with correction evidence. Complete the agreed push or PR
delivery, tracker updates, and cleanup; return those references to the
dispatcher.
