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
- **Blocked by:** every ticket that must complete first, or none; and
- **What it delivers:** the end-to-end behavior that becomes demonstrable or verifiable.

Ask the user to identify:

- any ticket that does not fit one fresh context or cannot be verified independently;
- any blocking edge that does not gate start or integration, and any missing blocker;
- any conflict edge without a shared surface, and any missing conflict; and
- tickets to merge or split.

Revise and repeat until the user approves the breakdown. Do not publish before approval.

### 5. Publish to the configured tracker

Create every approved Ticket identity first with exactly one category role and the `needs-triage` state. After every identity exists, add parent links, blocking edges, and conflict edges in a second pass so all relations use real identifiers.

- **Local markdown:** write every Ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, then record both edge types.
- **GitHub, GitLab, or another issue tracker:** create every issue first, then add the tracker's native parent and blocking relations where available and record conflicts in its configured representation.

Do not apply `ready-for-agent`, close or modify the parent Spec, run Prompt Audits, or begin implementation. Ticket publication and readiness are separate phases.

<local-ticket-template>

# <NN> — <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work from the user's perspective>

**Blocked by:** <ticket numbers/titles, or "None — can start immediately">

**Conflicts with:** <ticket numbers/titles, or "None — independent">

**Category:** bug | enhancement

**Status:** needs-triage

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

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- <each blocking ticket reference, or "None — can start immediately">

## Conflicts with

- <each conflicting ticket reference plus the shared surface, or "None — independent">

</issue-template>

Describe behavior and acceptance criteria without file paths, layer-by-layer implementation lists, or code snippets. Exception: when prototype output contains a state machine, reducer, schema, type shape, or other snippet that encodes an established decision more precisely than prose can, include only its decision-bearing parts and identify it as prototype output.

The publish step is complete when every approved Ticket exists separately with one category and `needs-triage`, and every parent, blocking, and conflict relation is recorded.

## Next-phase handoff

Ticket creation never authorizes implementation. Triage verifies and stabilizes each Ticket and its Agent Brief; `prompt-comprehension-audits` then checks semantic comprehension and one-context fit. Only a current `PASS` or explicit maintainer `BYPASS` transitions that exact Ticket to `ready-for-agent`, making it eligible without selecting it. Explicit Mission authorization is a separate later phase: route one selected Ticket directly to its coordinator contract, `orchestrate`, or supply that same one exact identity to the active `dispatch-tickets` when a responsive root is required. Ordered-sequence dispatch remains unavailable until its separate sequence contract is delivered. Neither route discovers ready work or derives authorization from a query.
