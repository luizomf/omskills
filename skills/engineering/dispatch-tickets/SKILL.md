---
name: dispatch-tickets
description:
  Coordinate a multi-issue Mission by tracking dependencies, responsible agents,
  blockers, and verified deliveries. Use when asked to carry a selected queue of
  Tickets through completion.
---

# Dispatch Tickets

Own the continuity of a Mission. Each [orchestrate](../orchestrate/SKILL.md)
agent owns one Ticket's technical work; you maintain the authorized queue,
choose the next eligible work, support its responsible agent, and verify
delivery. Read tracker and repository evidence for those decisions.
Implementation and code review stay with the Ticket owner and its independent
reviewer.

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
  supply them; one selected Ticket is also valid.
- Required order, blocking and conflict relations, shared resources, and each
  Ticket's delivery target. Distinguish a suggested priority order from a
  required sequence or phase barrier. Preserve explicitly required order;
  otherwise choose among eligible Tickets in priority order.
- Maintainer availability: `Assisted` for ordinary Questions, or `Unattended`
  for decisions within durable authority. Use the meaning already established in
  the request; ask only about material missing choices.
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
conversation reference, candidate location, current state, blocker or next
action, and delivery evidence. Use the current conversation or an ignored local
Markdown note as appropriate. Durable requirements and delivery history belong
in the configured tracker; private operational notes remain private.

This step is complete when the selected queue, availability, constraints, and
current ownership are known, or a specific missing decision prevents safe
dispatch.

## 2. Start or resume the next eligible owner

Check live dependency delivery, conflicts, existing ownership, and capacity
before each start. A closed issue or a ready label alone does not establish
delivery or authorization. For Unattended work, require the current readiness
and Prompt Audit `PASS` or explicit `BYPASS` for the exact contract; ordinary
Assisted work does not require them by default.

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

- **Progress:** keep the current owner working. Quiet output and elapsed time
  alone do not establish a stall.
- **User steering:** forward it to the relevant active or paused owner, or
  retain it for the selected future Tickets. Owners resolve technical details
  and durably record material contract changes. Ask only when the recipient or
  decision is genuinely ambiguous.
- **Blocked Ticket:** record the missing decision or dependency and preserve the
  owner, candidate, evidence, and next step. Continue another selected Ticket
  when its independence is established and required order permits it. If all
  remaining work is blocked, report what is needed to resume.
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

Reminders are optional when authorized and useful. Use the existing scheduler's
payload-free reminder with a self-contained reentry instruction identifying this
Mission, known owners, evidence to inspect, and the next decision. Follow its
acceptance, wake, cancellation, and untrusted-output rules. Inspect once per
wake, then choose the next action; cancel outstanding reminders when their
purpose ends. A cooperative tmux callback alone is not an automatic continuation
mechanism. State the supported continuation path honestly when releasing an
unattended turn.

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

Report compactly: delivered work, active owner, blocked work and required
decisions, next eligible work, and evidence references. Mission completion
requires every currently selected Ticket and the overall completion boundary to
be verified; report partial completion explicitly otherwise.

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
