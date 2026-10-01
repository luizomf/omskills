---
name: code-review
description:
  Review a committed range or complete work-in-progress candidate against
  repository standards and its governing contract.
---

# Code Review

Read applicable repository instructions and domain documents. Read issue-tracker
configuration only when the review contract is tracked; an untracked direct
request uses its confirmed conversation as the contract and does not require
tracker setup. If required configuration is unavailable, follow
[setup-omskills](../setup-omskills/SKILL.md) and its scoped authorization gate
before review. A read-only reviewer returns the missing prerequisite to its
responsible caller instead of writing setup.

Review exactly one candidate in one of two modes:

- **Committed:** a fixed base commit through `HEAD`.
- **WIP:** the current staged, unstaged, and untracked worktree state.

Honor an explicit mode. Otherwise infer committed mode for a branch, PR, or
supplied fixed point and WIP mode for a worktree request. Ask only when both
remain plausible; never combine them into a partial hybrid.

Review against two separately reported criteria sets:

- **Standards:** applicable repository instructions and conventions,
  maintainability, and relevant code smells.
- **Spec:** the exact Ticket, accepted behavior, acceptance criteria, omissions,
  incorrect behavior, and changes outside scope.

## Adversarial review contract

Challenge the candidate rather than seek confirmation that the author is right.
The normal path is one review followed by author corrections and verification;
perform the complete investigation now instead of relying on a later pass.

- Inspect every candidate path and contract requirement, reading surrounding
  context and tracing affected callers, consumers, tests, and governing sources
  wherever needed to establish correctness. Challenge assumptions, failure and
  boundary cases, regressions, omissions, and contradictory instructions that
  apply to this candidate; passing checks and author claims are evidence to
  examine, not substitutes for inspection.
- Continue across the complete candidate after finding a blocker. Return every
  concrete, supported problem found, including non-blocking ones, without a
  finding quota or a top-findings cutoff. Consolidate duplicates only when all
  affected locations and distinct consequences remain explicit.
- State defects, impact, and severity directly, without sugar-coating, praise
  padding, or downgrading a finding to soften the verdict. Be adversarial toward
  the work, not the author. Evidence determines severity; inventing
  requirements, speculative defects, or stylistic preferences is not adversarial
  review.
- For every finding, identify Standards or Spec, severity/blocking status,
  file/line (or exact artifact section), the violated rule or expected behavior,
  supporting evidence, and consequence. Distinguish evidence gaps from confirmed
  defects. Report relevant discovered problems outside the authorized correction
  scope as findings without expanding the investigation into unrelated work.

The pass is complete only when every candidate path and applicable requirement
has been examined and every supported finding is reported. State coverage and
verification limitations explicitly; an unexamined required area makes the
review incomplete, not clean. A complete pass with no supported findings reports
that result without manufacturing faults or claiming proof of defect-free work.

## Prepare the complete candidate

### Committed mode

1. Use the fixed point supplied by the caller. If none was supplied, infer one
   and ask only when none can be established. Resolve review HEAD to a full SHA.
   For standalone committed review, resolve the base as the merge base of that
   fixed point and review HEAD, preserving the `fixed-point...HEAD` candidate.
   For coordinated review, use the supplied exact full base SHA and verify it is
   an ancestor of review HEAD.
2. In a coordinated Ticket review, verify the supplied candidate path, branch
   and exact HEAD before capture. Use that exclusive candidate, never an
   inherited caller checkout; do not create another workspace. Unexpected
   branch/HEAD drift stops review as incomplete.
3. Capture the complete `git diff <base-sha> <review-sha>` and
   `git log <base-sha>..<review-sha> --oneline` in that candidate. Check that
   its identity/HEAD remains unchanged after capture; report exact path, branch,
   base and review SHAs with any capture limitations.
4. If the diff is empty, stop and report that there are no committed changes to
   review.

### WIP mode

1. Capture staged changes with `git diff --cached`.
2. Capture unstaged changes with `git diff`.
3. Inventory every untracked path and capture its complete content or binary
   status without treating ignored files as candidate work.
4. Report every unreadable or unrepresentable path as a capture limitation. If
   all three parts are empty, stop and report that there is no WIP candidate.

For either mode, locate the current contract and every applicable repository
instruction, governing source, and standard. The contract may be a tracked
Ticket or Spec, or the concise confirmed request for untracked direct work. If
no governing contract exists, review Standards and observable correctness while
stating that contract compliance could not be verified.

## Select the caller-safe review path

This skill requires one isolated review pass; assigning a reviewer name does not
create isolation, read-only behavior, tools, or delivery semantics. Direct code
or behavior changes and changes to Specs, ADRs, workflow, security, or other
governing authority require this fresh independent pass. Purely editorial
documentation may instead be self-reviewed.

- An interactive responsible agent, including a Ticket owner, may use the active
  harness's documented asynchronous delivery or
  [tmux-worker](../../productivity/tmux-worker/SKILL.md) for a visible isolated
  reviewer; follow its result-channel and editor-safety rules. An asynchronous
  caller resumes adjudication only after the matching completion notification;
  after acceptance it does not wait, sleep, or poll.
- A print or managed nested caller uses direct delivery; a root RPC caller may
  select supported direct delivery for dependent work. Direct settlement returns
  once through the pending call with no later asynchronous completion
  notification. A root Ticket owner uses the documented asynchronous path when
  direct settlement is unavailable: retain the review identity and candidate,
  end the turn after acceptance, and resume adjudication only from its matching
  completion notification, without waiting or polling.
- A designated reviewer is already the fresh review leaf, regardless of absolute
  depth: it performs the supplied one-pass contract directly with inherited
  non-delegating tools, returns complete findings to its responsible caller, and
  skips the dispatch and adjudication sections below. The implementation owner
  uses the caller path to obtain that independent review.

Before launch, require a fresh isolated conversation with no parent transcript
or prior child turns. Preflight the read-only tools and providers needed to
inspect the complete candidate, and, where the harness exposes lineage controls,
inherit the existing depth ceiling and set the child's direct-child ceiling to
zero or remove delegation capability. An over-depth or capability mismatch must
reject before launch or prompt acceptance. Do not retry it as though a review
occurred.

Choose a complete result-recovery channel before dispatch. Prefer the full
terminal response plus the harness's native session reference. If terminal text
is bounded, read the complete assistant message from that session before
adjudication. A harness without an adequate result or inspectable native session
may instead use one predeclared findings artifact outside the candidate
worktree; writing that artifact is the only allowed write. Require a completed
outcome through the selected transport as well as complete findings: for managed
calls, verify mechanical completion; for visible workers, verify the agreed
terminal report/event and complete artifact. A failed, interrupted, cancelled,
or missing reviewer outcome is incomplete even when partial findings exist. If
complete decision-bearing findings cannot be recovered, report the review as
incomplete rather than inferring a verdict.

## Dispatch one isolated reviewer

Read [model-routing](../../productivity/model-routing/SKILL.md) before selecting
the reviewer's model/effort. Before reading relative links, run
`cd '<loaded-skill-directory>' && pwd -P` with this loaded file's directory to
obtain the physical base, then resolve links against that printed directory.
Resolve the source symlink before applying `..`; read linked files even when
their skills are absent from the discovery list. Select for the candidate's
remaining uncertainty and impact, respecting explicit user routes and required
review independence; being a reviewer does not itself require the parent's
model.

Start exactly one fresh, read-only, non-delegating reviewer. Supply the selected
mode, candidate path and branch, exact base/review SHAs for committed mode (or
complete staged/unstaged/untracked capture for WIP), complete candidate or exact
read-only commands that reproduce it there, a concise current contract,
applicable governing sources and repository instructions, verification
instructions and results, the selected result channel, this skill's resolved
path, and this contract. Do not supply the parent transcript by default:

```text
Read the supplied code-review skill and apply its Adversarial review contract directly to every candidate path against Standards and Spec. This is the single planned review before author corrections: complete the investigation and return every supported finding, not only blockers or a top-findings summary. Report coverage and limitations as well as the full findings. Do not edit the candidate, push, approve, merge, spawn, delegate, recursively invoke code-review, invent requirements, or expand the reviewed scope. If and only if a findings artifact path was supplied, write the complete result there and report that exact path.
```

## Adjudicate and report

Verify every reported finding against the candidate and cited authority only
after the reviewer has settled and the complete selected result channel has been
recovered. Reject speculative hardening, style preferences, invented
requirements, and claims contradicted by repository conventions.

Treat review as a one-way handoff, not an approval loop. The reviewer delivers
all supported findings in one completed pass. The author owns resolution:
validate every finding against the contract and evidence, fix confirmed in-scope
problems, and justify rejected or deferred findings, including non-blocking and
out-of-scope ones. Continue implementation, debugging, and verification as
needed; do not send corrections back for reviewer approval or launch another
review of those corrections. Completion depends on the accepted requirements and
verification evidence, not reviewer agreement or finding count.

A finding is work to resolve, not by itself a reason to stop. A
delivery-blocking defect requires correction before delivery; it does not make
the Ticket `blocked` while the owner can resolve it within scope and available
authority. Resolve routine technical decisions from accepted sources. Only a
genuinely missing decision, dependency, permission, or capability that prevents
further in-scope progress follows the caller's blocker path. Findings outside
the accepted work remain findings rather than new implementation scope.

Record the reviewed and final candidate states and the corrections between them,
rather than implying the reviewer inspected later changes. An incomplete attempt
does not satisfy the independent-review requirement; recover it under the
caller's existing recovery authority, not as a review/correction loop.

Report the selected mode, coverage and capture/verification limitations, all
findings ordered by severity with their dispositions and correction evidence,
and a short verdict. Keep the verdict concise without truncating the findings.
