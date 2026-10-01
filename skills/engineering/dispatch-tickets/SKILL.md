---
name: dispatch-tickets
description:
  Coordinate a multi-issue Mission by tracking dependencies, responsible agents,
  blockers, and verified deliveries. Use when asked to carry a selected queue of
  multiple Tickets through completion.
---

# Dispatch Tickets

Supervise a Mission of multiple selected Tickets on the user's behalf. Each
[orchestrate](../orchestrate/SKILL.md) owner handles one Ticket's technical
work; you maintain the authorized queue, track progress and elapsed time,
support its responsible agent, and verify delivery. Read tracker and repository
evidence for those decisions. Implementation and code review stay with the
Ticket owner and its independent reviewer.

For an untracked request or only one selected Ticket, follow
[orchestrate](../orchestrate/SKILL.md) in the current conversation instead of
launching a dispatcher or another owner. The maintainer's absence does not
change that route. Once a multi-Ticket Mission is underway, keep supervising it
through its agreed boundary even when only one Ticket remains.

Use the environment's existing subagents or
[tmux-worker](../../productivity/tmux-worker/SKILL.md). This is an agent
workflow described in Markdown, with ordinary notes when useful; it needs no
coordination code or runtime service.

Before reading any relative link, run
`python3 -c 'from pathlib import Path; import sys; print((Path(sys.argv[1]).resolve().parent / sys.argv[2]).resolve())' '<loaded-file-path>' '<relative-link>'`
with this file's actual path and the link, then read the printed path. Resolve
pointers before passing them to a fresh agent. Read
[model-routing](../../productivity/model-routing/SKILL.md) before
model-selectable launches; apply explicit routes and the active harness's
authorization and inheritance rules.

## 1. Establish the Mission

Resolve from the request and accepted sources:

- The finite set of selected Tickets, repository/tracker identities, scope, and
  completion boundary. A list, prose plan, or existing phased JSON plan can
  supply them. Several files or subtasks inside one request do not by themselves
  make a multi-Ticket Mission.
- Required order, blocking and conflict relations, shared resources, and each
  Ticket's delivery target. Distinguish a suggested priority order from a
  required sequence or phase barrier. Preserve explicitly required order;
  otherwise choose among eligible Tickets in priority order.
- The authorized stopping point and maintainer availability: `Assisted` for
  ordinary Questions, or `Unattended` for continuing within established
  decisions while the maintainer is away. Reuse those choices from the request.
  Absence alone does not require an audit or another approval.
- Existing owners, conversations, candidates, completed deliveries, and the
  permitted recovery scope. Check ongoing work before starting another owner.

Read the configured tracker operations and repository instructions. If required
configuration is missing, follow [setup-omskills](../setup-omskills/SKILL.md)
within its setup authorization. Read selected Tickets and their relations to
determine eligibility. Follow external references as dependency evidence without
adding them to the selected work. The Ticket owner rechecks its complete
contract and applicable execution gates before implementation.

Prefer serial execution. Parallel work requires established independence,
compatible shared resources, actual available capacity, and an agreed
integration boundary. Preserve an accepted parallel plan's requirements; resolve
unavailable capacity rather than silently changing a required topology. Planning
through [to-tickets](../to-tickets/SKILL.md) supplies branch-artifact and
integration boundaries when needed.

Keep a concise Mission record: selected Tickets, order/relations, owner and
conversation reference, candidate location, start time, last observed progress,
next check or action, blockers, and delivery evidence. Use the current
conversation or an ignored local Markdown note as appropriate. Durable
requirements and delivery history belong in the configured tracker; private
operational notes remain private.

This step is complete when the selected queue, availability, constraints, and
current ownership are known, or a specific missing decision prevents safe
dispatch.

## 2. Start or resume the next eligible owner

Check live dependency delivery, conflicts, existing ownership, and capacity
before each start. A closed issue or a ready label alone does not establish
delivery or authorization. Apply readiness or Prompt Audit gates when required
by the accepted task or repository, not merely because the maintainer is away.

For a new Ticket, start one fresh responsible conversation with the resolved
`orchestrate` path. Supply:

- Ticket identity, repository/workspace, accepted scope and governing-source
  pointers;
- availability, relevant user decisions and routing instructions;
- dependency results and changes already integrated that affect this Ticket;
- delivery boundary, required checks, shared-resource ownership, and any
  existing candidate;
- the chosen result channel and evidence expected at delivery or a blocker.

The owner investigates, implements, tests, obtains independent review,
adjudicates, corrects, and delivers. Give it the capabilities to do that work
and obtain its reviewer within actual harness limits. A role name is not a
capability grant.

For a paused Ticket, prefer the same conversation and candidate. Send the
resolved blocker, accepted decisions, and relevant intervening deliveries.
Revalidate affected contracts and gates before resuming implementation. Keep one
active owner for each candidate.

Honor the transport's delivery contract. Managed direct calls return through the
pending call; after asynchronous acceptance, retain the owner/session identity
and release the turn for its completion event. Unknown acceptance calls for
evidence recovery, not a duplicate start. For visible workers, agree on a result
artifact or supported event through `tmux-worker`, preserving the user's editor
and the worker conversation.

This step is complete when the eligible Ticket has one known owner and result
path, or its launch/resumption has a concrete unresolved outcome recorded.

## 3. Maintain continuity

On a result, user message, or authorized reminder, inspect the evidence needed
for the next decision:

- **Progress and elapsed time:** compare time spent with the task, last observed
  progress, and any agreed checkpoint. When progress is unclear or a checkpoint
  is missed, inspect the known owner and available evidence, or request a
  focused update through its supported channel. Support the same owner with
  clarification or authorized recovery. Quiet output or elapsed time alone does
  not prove a stall or authorize replacement.
- **User steering:** forward it to the relevant active or paused owner, or
  retain it for the selected future Tickets. Owners resolve technical details
  and durably record material contract changes. Ask only when the recipient or
  decision is genuinely ambiguous.
- **Correctable findings or failing checks:** keep resolution with the same
  owner; these are work to finish, not by themselves a blocked Ticket. Return
  premature stop reports to that owner with the available in-scope next action,
  without starting a reviewer-approval loop.
- **Blocked Ticket:** require a concrete missing decision, dependency,
  permission, or capability that prevents further in-scope progress. Preserve
  the owner, candidate, evidence, and next step. Continue other eligible
  selected Tickets when required order and dependencies permit; a local blocker
  does not end the Mission. If no remaining Ticket has an eligible next action,
  report what is needed to resume.
- **Concrete failure:** inspect the known conversation, transport outcome,
  candidate state, and available evidence. Prefer recovering the current owner.
  Before replacement within the Mission's recovery authority, confirm the
  previous owner and any candidate-writing activity have stopped; preserve
  branch/worktree, HEAD, dirty changes, checks, current hypothesis, and next
  action. Transfer those facts to the replacement. Uncertain ownership remains
  unresolved until evidence settles it.
- **Plan change or cancellation:** apply clear user direction, pause affected
  starts, and route the change to affected owners. Settle prior ownership before
  replacement or conflicting work, preserving unaffected progress and delivered
  evidence.

A delivery operation may have succeeded before its result was lost. Inspect the
target and tracker before choosing a recovery action. Recover missing evidence
or remaining obligations rather than repeating already completed implementation
or publication.

Use the existing scheduler for a later progress check when supervision needs a
wake beyond worker completion. Choose timing from the task and any
user-requested checkpoint, not a fixed universal timeout. A payload-free
reminder carries this Mission, known owners, last progress, evidence to inspect,
and the next decision. Follow the scheduler's acceptance, wake, cancellation,
and untrusted-output rules. Inspect once per wake, then act or schedule the next
useful check; cancel outstanding reminders when their purpose ends. If no
automatic reentry is available, state that limitation rather than promise
continuous monitoring. A cooperative tmux callback alone is not an automatic
continuation mechanism.

This step is complete when each observed event has a next action or recorded
blocker, current ownership remains unambiguous, and independent eligible work
can proceed within the Mission's constraints.

## 4. Verify delivery and advance

Treat an owner's report as a pointer to evidence. Verify the selected Ticket's
declared boundary against the actual tracker and repository:

- issue/PR state and the relevant delivery record;
- exact reviewed and final candidate commits, completed independent review,
  adjudication, and required check results for the final state;
- the pushed branch artifact or resulting target commit, including
  source-to-squash mapping and content equivalence when squash delivery is used;
- required tracker updates, cleanup, and any protected retained artifacts or
  downstream consumers.

This is delivery verification, not a second code review. Follow the evidence far
enough to establish the claimed result; return gaps to the same owner. A JSON
status, callback, closed issue, or successful merge alone cannot satisfy the
whole boundary. An interrupted review remains incomplete even if partial
findings exist.

Record verified delivery and pass relevant integrated changes to subsequent
owners. Parallel branch artifacts remain inputs until their planned integration
Ticket verifies the combined state. Advance dependents only when their required
delivery boundary is satisfied.

Continue through the user's agreed stopping point; owner completion, review
findings, or a progress report do not introduce approval stops. Report
compactly: delivered work, active owner, blocked work and required decisions,
next eligible work, and evidence references. Mission completion requires every
currently selected Ticket and the overall completion boundary to be verified;
report partial completion explicitly otherwise.

This step is complete when the delivery claim is verified or its exact gap is
recorded, and the next eligible owner is selected or the Mission has reached
completion or a genuine stopping point.

## Example

The user authorizes #10, #11, and #12, with #12 blocked by #10 and #11
independent. The list is priority order rather than a required sequence. #10
reaches an unresolved product decision. Preserve its conversation and worktree,
record the Question, and dispatch #11. After #11's target, checks, review,
tracker state, and cleanup are verified, record its delivery. When the user
resolves #10, resume its original owner with that decision and any relevant
changes from #11. Verify #10's delivery before starting #12.

If the user instead required strict #10 → #11 → #12 execution, retain that order
and report #10's blocker.
