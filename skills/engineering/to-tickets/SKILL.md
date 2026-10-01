---
name: to-tickets
description:
  Break a plan, spec, or conversation into tracer-bullet tickets with explicit
  blocking and conflict edges, then publish them to the configured tracker.
---

# To Tickets

Create **tracer-bullet tickets** with two scheduling relations:

- A **blocking edge** means the blocked ticket cannot start or integrate until
  the blocker is complete.
- A **conflict edge** means two otherwise unblocked tickets should not have
  active writers concurrently because they materially overlap in files,
  contracts, artifacts, or integration assumptions.

Read the configured issue tracker and triage-label vocabulary. If either
configuration is unavailable, follow
[setup-omskills](../setup-omskills/SKILL.md) and its scoped authorization gate
before continuing, including in headless runs. Respect read-only roles and
return unresolved prerequisites to the responsible caller.

## Process

### 1. Gather source context

Use the plan, spec, or conversation already in context. If the user provides a
path, issue number, or URL, read its complete body and comments before drafting
tickets.

### 2. Inspect the repository when needed

If the repository's current implementation has not already been inspected in
this context, inspect the affected area. Use terms from the project domain
glossary in ticket titles and bodies, and preserve applicable ADR decisions.

### 3. Draft vertical slices

Each tracer-bullet Ticket must:

- deliver one behavior through every layer that behavior affects;
- be independently demonstrable or verifiable after completion;
- fit one fresh agent context with room to understand, implement, and verify it;
  and
- identify its category role as `bug` or `enhancement` from the accepted source.

Keep every requirement durable in the Ticket or explicitly incorporated tracker
artifacts; planning and audit conversations carry no hidden requirements. Do not
split cohesive work just to manufacture parallelism or invent serial
dependencies.

Assign every ticket its actual blocking and conflict edges. A ticket with no
blockers enters the frontier. It is eligible for concurrent work only when
repository evidence shows no material conflict with active tickets.

#### Wide-refactor exception

Use **expand–contract** instead of vertical slices when one mechanical change,
such as renaming a column or retyping a shared symbol, has a whole-codebase
blast radius and no partial vertical slice can keep CI passing:

1. **Expand:** add the new form beside the old form without breaking current
   callers.
2. **Migrate:** move callers in batches sized by blast radius, such as one
   package or directory per ticket. Each migration ticket is blocked by
   expansion, and the old form remains available so each batch can pass CI
   independently.
3. **Contract:** remove the old form only after every migration ticket is
   complete; block contraction on all migration tickets.

If no migration batch can pass CI independently, retain this sequence on an
integration branch and block a final integrate-and-verify ticket on all batches.
In that case, the requirement to leave CI passing applies to the final ticket
rather than each batch.

### 4. Obtain breakdown approval

Present a numbered draft. For each ticket, include:

- **Title:** one line naming the delivered behavior;
- **Blocked by:** every ticket that must complete first, or none;
- **Conflicts with:** every conflicting ticket and its shared surface, or none;
  and
- **What it delivers:** the end-to-end behavior that becomes demonstrable or
  verifiable.

Before requesting approval, identify Mission topology whenever the breakdown
selects multiple Tickets; record their dependency, conflict, integration, and
shared-resource needs. Record maintainer availability independently when the
source resolves it; otherwise leave that dimension for the adaptive pre-mutation
gate rather than inferring absence from Mission topology.

Show the proposed order, blockers, conflicts, and shared resources outside Git.
Distinguish priority order from required sequence or phase barriers so execution
can continue independent work around a local blocker. Prefer serial delivery.
Propose parallel groups when their benefit, repository/contract independence,
shared-resource compatibility, actual runtime capacity, and integration
boundaries are established. Preserve explicitly required topology during
execution; resolve an unavailable prerequisite rather than silently changing it.

Every implementation Ticket in a multi-Ticket Mission, including integration
Tickets, requires an exclusive worktree and branch established by its technical
owner before implementation. Read
[the worktree policy](../orchestrate/WORKTREES.md) when planning candidate
locations and cleanup. Before reading relative links, run
`cd '<loaded-skill-directory>' && pwd -P` with this loaded file's directory to
obtain the physical base, then resolve links against that printed directory.
Resolve the source symlink before applying `..`; read linked files even when
their skills are absent from the discovery list. For planning, use that shared
policy without invoking the coordinator.

Declare every delivery boundary in the approved breakdown:

- Parallel members deliver verified, committed, pushed branch artifacts, not
  implicit shared-target merges or group completion.
- Each parallel group includes a preplanned ordinary integration Ticket blocked
  by every member. Identify every predecessor, intended base/target and
  combination requirements. Require durable tracker evidence of each produced
  artifact's repository, remote branch and exact full commit SHA before
  integration starts; exact outputs are recorded at predecessor delivery, not
  guessed during planning. The integration Ticket combines those verified inputs
  in its own candidate, reviews and verifies the complete combined state, and
  records input-to-result commits before dependent work advances.
- Non-member Tickets and individually selected Tickets state their integration
  target and direct-push or pull-request delivery method explicitly. A pull
  request is optional unless repository policy or the accepted request requires
  one; every used pull request is squash-merged.
- Require a durable source-to-squash mapping for every pull request, including
  non-member and individually selected Ticket delivery. Make verified
  owner-managed cleanup under the shared worktree policy part of completion,
  assigning declared predecessor cleanup to the integration owner after the
  final consumer completes.

For example, a compatible group A/B/C delivers three branch artifacts; the next
phase is integration I, blocked by A, B and C; dependent D is blocked by I. I is
an ordinary authorized Ticket, not a dispatcher integration action. These
decisions are part of breakdown approval, not another user gate.

Ask the user to identify:

- any ticket that does not fit one fresh context or cannot be verified
  independently;
- any blocking edge that does not gate start or integration, and any missing
  blocker;
- any conflict edge without a shared surface, and any missing conflict; and
- tickets to merge or split.

Revise and repeat until the user approves the breakdown. Do not publish before
approval.

### 5. Publish to the configured tracker

Create every approved Ticket identity first with exactly one category role and
the `needs-triage` state. After every identity exists, add parent links,
blocking edges, and conflict edges in a second pass so all relations use real
identifiers.

- **Local markdown:** follow the configured tracker's ignore and lifecycle
  rules. Write one file per Ticket at a chosen `.scratch/` path, then record
  both edge types using those paths.
- **GitHub, GitLab, or another issue tracker:** create every issue first, then
  add the tracker's native parent and blocking relations where available and
  record conflicts in its configured representation.

Do not apply `ready-for-agent`, close or modify the parent Spec, run Prompt
Audits, or begin implementation. Ticket publication and readiness are separate
phases.

<local-ticket-template>

# <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work from the
user's perspective>

**Blocked by:** <linked Ticket paths, or "None">

**Conflicts with:** <linked Ticket paths and shared surfaces, or "None">

**Delivery:** <branch artifact or explicit integration target plus direct-push
or pull-request method; every PR includes a durable source-to-squash mapping;
integration also includes all predecessor identities, base/target, combination
requirements, durable exact-input evidence obligations, and post-delivery
cleanup>

**Category:** bug | enhancement

**Status:** needs-triage

**Lifecycle:** open

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

<parent Spec reference when one exists; otherwise omit this section>

## Category

`bug` | `enhancement`

## What to build

<the end-to-end behavior this ticket makes work from the user's perspective>

## Delivery

<branch artifact or explicit integration target plus direct-push or pull-request
method; every PR includes a durable source-to-squash mapping; integration also
includes all predecessor identities, base/target, combination requirements,
durable exact-input evidence obligations, and post-delivery cleanup>

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- <each blocking ticket reference, or "None">

## Conflicts with

- <each conflicting ticket reference plus the shared surface, or "None">

</issue-template>

Describe behavior and acceptance criteria without incidental file paths,
layer-by-layer implementation lists, or code snippets. Preserve exact
repository/remote branch references and candidate or delivery identities when
they define required handoffs. Exception: when prototype output contains a state
machine, reducer, schema, type shape, or other snippet that encodes an
established decision more precisely than prose can, include only its
decision-bearing parts and identify it as prototype output.

The publish step is complete when every approved Ticket exists separately with
one category and `needs-triage`, and every parent, blocking, and conflict
relation is recorded.

## Next-phase handoff

Ticket creation never authorizes implementation. Triage verifies and stabilizes
the complete Ticket contract; a separate Agent Brief is unnecessary when the
body is complete. Requested `prompt-comprehension-audits` checks comprehension
and one-context fit; current `PASS` or explicit maintainer `BYPASS` applies
`ready-for-agent` regardless of availability, without selecting work. Remove
failed or materially stale readiness. Reuse an unchanged applicable audit;
maintainer absence alone does not require one.

Explicit authorization may accompany the audit request; after PASS, delivery
proceeds in a fresh implementation context, separate from the audit coordinator.
Audit-only requests stop after status/readiness recording. For a Mission, pass
the selected finite queue, relations, required order, delivery boundaries, and
established availability to [dispatch-tickets](../dispatch-tickets/SKILL.md). It
checks live state, starts or resumes Ticket owners, preserves blocked work while
advancing eligible independent Tickets, and verifies delivery. For one selected
Ticket, [implement](../implement/SKILL.md) loads
[orchestrate](../orchestrate/SKILL.md) in the current conversation, whether the
maintainer stays or authorizes work while away. It adds no dispatcher or owner
handoff. Pass resolved skill paths when launching owners for a multi-Ticket
Mission. Every route preserves the accepted scope, applicable gates, exclusive
ownership, independent review, and delivery evidence; readiness alone does not
select work.
