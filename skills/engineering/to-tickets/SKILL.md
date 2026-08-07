---
name: to-tickets
description: Break a plan, spec, or conversation into tracer-bullet tickets with explicit blocking and conflict edges, then publish them to the configured tracker.
---

# To Tickets

Create **tracer-bullet tickets** with two scheduling relations:

- A **blocking edge** means the blocked ticket cannot start or integrate until the blocker is complete.
- A **conflict edge** means two otherwise unblocked tickets should not have active writers concurrently because they materially overlap in files, contracts, artifacts, or integration assumptions.

Read the configured issue tracker and triage-label vocabulary. If either is unavailable, run `setup-omskills` first.

## Process

### 1. Gather source context

Use the plan, spec, or conversation already in context. If the user provides a path, issue number, or URL, read its complete body and comments before drafting tickets.

### 2. Inspect the repository when needed

If the repository's current implementation has not already been inspected in this context, inspect the affected area. Use terms from the project domain glossary in ticket titles and bodies, and preserve applicable ADR decisions.

Identify opportunities to prefactor the code so later tickets can make smaller changes. Schedule any such prefactoring before the tickets it enables.

### 3. Draft vertical slices

Each tracer-bullet ticket must:

- deliver one user-visible behavior through every layer that behavior affects, such as schema, API, UI, and tests;
- be independently demonstrable or verifiable after completion; and
- fit one fresh agent context window.

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

Publish one artifact per approved ticket in blocker-first dependency order:

- **Local markdown:** write each ticket to `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`. Record both edge types.
- **GitHub, Linear, or another issue tracker:** create one issue per ticket so relationships use real identifiers. Use native blocking relations when available. Record conflicts in the issue body unless the tracker provides an equivalent native relation. Apply `ready-for-agent` unless instructed otherwise.

Do not close or modify a parent issue.

<local-ticket-template>

# <NN> — <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work from the user's perspective>

**Blocked by:** <ticket numbers/titles, or "None — can start immediately">

**Conflicts with:** <ticket numbers/titles, or "None — independent">

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

<parent issue reference when the source was an existing issue; otherwise omit this section>

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

The publish step is complete when every approved ticket exists separately, every blocking and conflict edge is recorded, and every non-overridden ticket has `ready-for-agent`.

## Next-phase handoff

Ticket creation does not require implementation. When execution begins later, work frontier tickets whose blockers are complete and use `implement` with a fresh context for each ticket. Concurrent tickets require demonstrated independence plus exclusive owners, branches, and worktrees. Integrate completed tickets one at a time, then revalidate every remaining branch after each merge.
