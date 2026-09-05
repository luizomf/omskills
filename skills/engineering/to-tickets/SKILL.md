---
name: to-tickets
description: Break a plan, spec, or conversation into tracer-bullet tickets with explicit blocking and conflict edges, then publish them to the configured tracker.
---

# To Tickets

Create **tracer-bullet tickets** with two scheduling relations:

- A **blocking edge** means the blocked ticket cannot start or integrate until the blocker is complete.
- A **conflict edge** means two otherwise unblocked tickets should not have active writers concurrently because they materially overlap in files, contracts, artifacts, or integration assumptions.

Read the configured issue tracker and triage-label vocabulary. If either configuration is unavailable during an interactive invocation, run `setup-omskills` first and wait for its confirmed output. During a headless Ticket run, return a missing-setup blocker to the Ticket coordinator instead; never route setup through a Ticket dispatcher.

## Process

### 1. Gather source context

Use the plan, spec, or conversation already in context. If the user provides a path, issue number, or URL, read its complete body and comments before drafting tickets.

### 2. Inspect the repository when needed

If the repository's current implementation has not already been inspected in this context, inspect the affected area. Use terms from the project domain glossary in ticket titles and bodies, and preserve applicable ADR decisions.

### 3. Draft vertical slices

Each tracer-bullet Ticket must:

- deliver one behavior through every layer that behavior affects;
- be independently demonstrable or verifiable after completion;
- fit one fresh agent context with room to understand, implement, and verify it; and
- identify its category role as `bug` or `enhancement` from the accepted source.

Assign every ticket its blocking and conflict edges. A ticket with no blockers enters the frontier. It is eligible for concurrent work only when repository evidence shows no material conflict with active tickets.

#### Wide-refactor exception

Use **expand–contract** instead of vertical slices when one mechanical change, such as renaming a column or retyping a shared symbol, has a whole-codebase blast radius and no partial vertical slice can keep CI passing:

1. **Expand:** add the new form beside the old form without breaking current callers.
2. **Migrate:** move callers in batches sized by blast radius, such as one package or directory per ticket. Each migration ticket is blocked by expansion, and the old form remains available so each batch can pass CI independently.
3. **Contract:** remove the old form only after every migration ticket is complete; block contraction on all migration tickets.

If no migration batch can pass CI independently, retain this sequence on an integration branch and block a final integrate-and-verify ticket on all batches. In that case, the requirement to leave CI passing applies to the final ticket rather than each batch.

### 4. Obtain breakdown approval

Present a numbered draft. For each ticket, include:

- **Title:** one line naming the delivered behavior;
- **Blocked by:** every ticket that must complete first, or none;
- **Conflicts with:** every conflicting ticket and its shared surface, or none; and
- **What it delivers:** the end-to-end behavior that becomes demonstrable or verifiable.

Before requesting approval, identify Mission topology whenever the breakdown selects multiple Tickets or establishes real dependency, conflict, integration, shared-resource, or multiple-writer coordination. Record maintainer availability independently when the source resolves it; otherwise leave that dimension for the adaptive pre-mutation gate rather than inferring absence from Mission topology.

Show complete sequential phases, compatible parallel groups, blockers and conflicts, including shared resources outside Git. For every same-frontier group, inspect repository overlap, governing contracts, integration assumptions, and external resources and affirmatively identify all work proven safe to run in parallel. Do not default proven-independent Tickets to serial execution. When independence is unknown, a conflict exists, or capacity is unsupported, propose serial phases and state that reason explicitly; never relabel or silently serialize an authorized parallel group. Parallel N requires affirmative evidence of sufficient active ROOT capacity and same-batch start support in the applicable transport mode; child-only limits and unknown bounds are insufficient and fail the parallel proposal closed.

Every implementation Ticket handled by a Ticket coordinator, including a one-item or integration Ticket, requires an exclusive worktree and branch established by its coordinator after preflight and before its writer.

Declare every delivery boundary in the approved breakdown:

- Parallel members deliver verified, committed, pushed branch artifacts, not implicit shared-target merges or group completion.
- Each parallel group includes a preplanned ordinary integration Ticket blocked by every member. Identify every predecessor, intended base/target and combination requirements. Require durable tracker evidence of each produced artifact's repository, remote branch and exact full commit SHA before integration starts; exact outputs are recorded at predecessor delivery, not guessed during planning. The integration Ticket combines those verified inputs in its own candidate, reviews and verifies the complete combined state, and records input-to-result commits before dependent work advances.
- Non-member/one-item Tickets state their normal integration target and direct-push or pull-request delivery method explicitly. A pull request is optional unless repository policy or the accepted request requires one; every used pull request is squash-merged.
- Retain artifacts and recoverable work until declared delivery and all integration consumers no longer need them. For every pull request, require a durable source-to-squash mapping, including non-member and one-item delivery. After verifying the target result and required mappings, coordinator-owned cleanup removes clean owned worktrees and deletes verified-delivered local and remote source branches; expected lack of ancestry after squash does not prevent deletion. Preserve unrelated, failed, cancelled, dirty, undelivered, or still-consumed work and record retention reasons.

For example, a compatible group A/B/C delivers three branch artifacts; the next phase is integration I, blocked by A, B and C; dependent D is blocked by I. I is an ordinary audited, authorized Ticket, not a dispatcher integration action. These decisions are part of breakdown approval, not another user gate.

Ask the user to identify:

- any ticket that does not fit one fresh context or cannot be verified independently;
- any blocking edge that does not gate start or integration, and any missing blocker;
- any conflict edge without a shared surface, and any missing conflict; and
- tickets to merge or split.

Revise and repeat until the user approves the breakdown. Do not publish before approval.

### 5. Publish to the configured tracker

Create every approved Ticket identity first with exactly one category role and the `needs-triage` state. After every identity exists, add parent links, blocking edges, and conflict edges in a second pass so all relations use real identifiers.

- **Local markdown:** follow the configured tracker's ignore and lifecycle rules. Write one file per Ticket at a chosen `.scratch/` path, then record both edge types using those paths.
- **GitHub, GitLab, or another issue tracker:** create every issue first, then add the tracker's native parent and blocking relations where available and record conflicts in its configured representation.

Do not apply `ready-for-agent`, close or modify the parent Spec, run Prompt Audits, or begin implementation. Ticket publication and readiness are separate phases.

<local-ticket-template>

# <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work from the user's perspective>

**Blocked by:** <linked Ticket paths, or "None">

**Conflicts with:** <linked Ticket paths and shared surfaces, or "None">

**Delivery:** <branch artifact or explicit integration target plus direct-push or pull-request method; every PR includes a durable source-to-squash mapping; integration also includes all predecessor identities, base/target, combination requirements, durable exact-input evidence obligations, and post-delivery cleanup>

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

<branch artifact or explicit integration target plus direct-push or pull-request method; every PR includes a durable source-to-squash mapping; integration also includes all predecessor identities, base/target, combination requirements, durable exact-input evidence obligations, and post-delivery cleanup>

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- <each blocking ticket reference, or "None">

## Conflicts with

- <each conflicting ticket reference plus the shared surface, or "None">

</issue-template>

Describe behavior and acceptance criteria without incidental file paths, layer-by-layer implementation lists, or code snippets. Preserve exact repository/remote branch references and candidate or delivery identities when they define required handoffs. Exception: when prototype output contains a state machine, reducer, schema, type shape, or other snippet that encodes an established decision more precisely than prose can, include only its decision-bearing parts and identify it as prototype output.

The publish step is complete when every approved Ticket exists separately with one category and `needs-triage`, and every parent, blocking, and conflict relation is recorded.

## Next-phase handoff

Ticket creation never authorizes implementation. Triage verifies and stabilizes each Ticket and its Agent Brief. For Unattended execution, `prompt-comprehension-audits` checks semantic comprehension and one-context fit; only a current `PASS` or explicit maintainer `BYPASS` transitions that exact unchanged Ticket to `ready-for-agent`, making it eligible without selecting it. Reuse an unchanged applicable audit. Prompt Audit is optional when requested for Assisted work and is not its default gate.

Explicit Mission authorization is a separate later phase whenever Mission topology is selected: supply one finite pre-resolved Mission plan and independently resolved availability to `dispatch-tickets`, or use `implement` to compose exactly one selected Ticket as that dispatcher's optional one-item Mission plan. For smaller Mission work, a human/invoker or context-rich parent may directly dispatch one fresh isolated `orchestrate` coordinator for the explicitly selected Ticket. Every route evaluates selection and authority semantically and checks actual capabilities; caller provenance, ancestry, role/depth assertions, and dispatcher wording neither establish nor add authority. When used, the dispatcher remains mechanical with frozen topology; no route discovers ready work or derives authorization from a query. Ordinary Direct Assisted work does not require these Mission entries.
