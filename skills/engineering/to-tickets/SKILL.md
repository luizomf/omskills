---
name: to-tickets
description: Break a plan, spec, or conversation into tracer-bullet tickets with explicit blocking and conflict edges, then publish them to the configured tracker.
---

# To Tickets

Create **tracer-bullet Tickets** with two scheduling relations:

- A **blocking edge** means the blocked Ticket cannot start or integrate until the blocker is complete.
- A **conflict edge** records a direct write-conflict between otherwise unblocked Tickets. It means they must not have active writers concurrently because they share a file, contract, artifact, or integration surface.

Read the configured Issue tracker and triage-label vocabulary. If either is unavailable, run `setup-omskills` first.

## Process

### 1. Gather source context

Use the plan, Spec, or conversation already in context. If the user provides a path, issue number, or URL, read its complete body and comments before drafting Tickets.

#### Establish a publishable parent Spec

A plan or conversation may supply the source context, but it is not itself a publishable parent identity. When the source is not already a durable Spec in the configured Issue tracker, run `to-spec` from that established context first. Resume this process only with the resulting complete Spec, its configured tracker identity or path, and its current authorizing Prompt Audit status. Do not invent a source identity or publish parentless implementation Tickets.

#### Validate the source Prompt Audit

Locate the parent Spec's newest applicable Prompt Audit status before accepting it for breakdown:

- a current `PASS` authorizes the breakdown;
- `BYPASS` authorizes it only when the status records explicit maintainer authorization for that source contract; and
- a missing, stale, or `FAIL` status stops before Ticket drafting or publication and reports the choices to run `prompt-comprehension-audits` or obtain an explicit maintainer-authorized bypass.

Never infer bypass from a request to create Tickets. A material source-contract change makes an older status stale.

### 2. Inspect the repository when needed

If the repository's current implementation has not already been inspected in this context, inspect the affected area. Use terms from the project domain glossary in Ticket titles and bodies, and preserve applicable ADR decisions.

Identify prefactoring that would make later slices smaller. Fold ordinary prefactoring into the first behavior slice that needs it rather than publishing a standalone prefactor Ticket.

### 3. Draft vertical slices

Each tracer-bullet Ticket must:

- deliver one user-visible behavior through every layer that behavior affects, such as schema, API, UI, and tests;
- be independently demonstrable or verifiable after completion; and
- fit one fresh agent context with room to understand, implement, and verify the behavior.

Assign every real blocking edge and every direct write-conflict edge. For each conflict, name the shared file, contract, artifact, or integration surface. A Ticket with no blockers enters the frontier. It is eligible for concurrent work only when repository evidence shows no direct conflict with active Tickets.

#### Wide-refactor exception

Use **expand–contract** instead of vertical slices only when one mechanical change, such as renaming a column or retyping a shared symbol, has a whole-codebase blast radius and no partial vertical slice can keep CI passing:

1. **Expand:** add the new form beside the old form without breaking current callers.
2. **Migrate:** move callers in batches sized by blast radius, such as one package or directory per Ticket. Each migration Ticket is blocked by expansion, and the old form remains available so each batch can pass CI independently.
3. **Contract:** remove the old form only after every migration Ticket is complete; block contraction on all migration Tickets.

If no migration batch can pass CI independently, retain this sequence on an integration branch and block a final integrate-and-verify Ticket on all batches. In that case, the requirement to leave CI passing applies to the final Ticket rather than each batch.

Do not use this exception to justify ordinary standalone prefactoring.

### 4. Obtain breakdown approval

Present a numbered draft. The number becomes part of the Ticket's stable Planning identity for duplicate-free publication and resume. For each Ticket, include:

- **Title:** one line naming the delivered behavior;
- **Category:** exactly one configured category role, `bug` or `enhancement`;
- **Blocked by:** every Ticket that must complete first, or none;
- **Conflicts with:** every direct write-conflict plus its shared file, contract, artifact, or integration surface, or none; and
- **What it delivers:** the end-to-end behavior that becomes demonstrable or verifiable.

Ask the user to identify:

- any Ticket that does not fit one fresh context or cannot be verified independently;
- any blocking edge that does not gate start or integration, and any missing blocker;
- any conflict edge without a direct shared surface, and any missing conflict; and
- Tickets to merge or split.

Revise and repeat until the user approves the breakdown. Do not publish before approval. This is the established breakdown-approval gate; do not add another publication confirmation.

### 5. Publish transactionally and resumably

Treat the approved source identity plus each approved draft number as that Ticket's stable **Planning identity**. Before mutating the tracker, use its configured identity-discovery operation across every artifact that can contain one of those exact identities. Do not limit discovery to already-parented children: an interrupted attempt may have created an identity without completing its parent relation. Match only the exact Planning identity marker, never a title or incidental reference. Reconcile one existing match in place, create a missing identity, and stop on multiple matches or an identity collision. Never create a replacement merely because an earlier attempt is incomplete.

Do not mutate the audited source Spec merely to maintain a fallback identity index. The exact Planning identity marker is the resume key. If an unavoidable material source-contract edit occurs, its prior audit becomes stale and publication stops until that exact revised source receives a new authorizing audit.

Maintain a publication ledger of every approved identity, parent, blocker, conflict, final contract, Prompt Audit status, and readiness transition. Run the phases in this order.

#### Phase A — identities and parents

1. Create or reconcile every approved Ticket identity with its complete behavior and acceptance criteria, using symbolic approved-draft references until all real identifiers exist.
2. Give every Ticket exactly one configured category role and the configured `needs-triage` state role. Remove any other configured category or state roles from a reconciled identity. No Ticket starts ready.
3. Create or reconcile every parent relationship to the source Spec. Prefer the configured native parent relation. Use the configured documented fallback only when that native relation is unavailable.
4. Verify that all approved identities and parents exist before adding any identifier-dependent blocker or conflict relation.

#### Phase B — final contracts and relations

1. Replace symbolic references with the reconciled identifiers and write each final Ticket contract.
2. Create or reconcile every blocking edge. Prefer the configured native blocker relation; use its documented body or file fallback only when the native relation is unavailable.
3. Create or reconcile every direct write-conflict edge on both endpoints, using a native equivalent when configured or the Ticket contract otherwise. Include the shared file, contract, artifact, or integration surface.
4. Re-read every final contract and configured relation. Do not audit a Ticket until its identity, parent, complete body, blockers, and conflicts are final.

#### Phase C — audit and readiness

For each final Ticket, run `prompt-comprehension-audits` against that exact complete contract and append the status without rewriting audit history.

- On a current `PASS` or explicit maintainer-authorized `BYPASS`, remove `needs-triage` and every other configured state role, apply the configured `ready-for-agent` state role, and verify that exactly one configured category role and exactly the configured `ready-for-agent` state role remain.
- On a missing, stale, or `FAIL` status, keep or restore exactly one configured category role plus the configured `needs-triage` state role, remove `ready-for-agent` and every other configured state role, and report that the Ticket is non-ready.
- A material edit after audit makes that status stale and requires the non-ready state until a new audit authorizes readiness.

Do not report publication success until every approved identity, parent, blocker, direct conflict, current authorizing audit, and exact readiness invariant has been re-read and verified. On interruption, unavailable native capability without its configured fallback, failed audit, or any partial result, report success as false and list the exact completed and missing artifacts from the ledger. Resume from Phase A by reconciling approved identities and relations; never duplicate them.

### Tracker artifact shapes

Follow the configured Issue tracker operations for native relations, fallbacks, comments, and labels.

<local-ticket-template>

# <NN> — <Ticket title>

Planning identity: <source identity>/ticket-<NN>
Parent: <source Spec path>
Category: <configured bug|enhancement role>
Status: needs-triage
Author: <configured author identity>
Created: <ISO 8601 timestamp>
Updated: <ISO 8601 timestamp>

What to build: <the end-to-end behavior this Ticket makes work from the user's perspective>

Blocked by: <Ticket Planning identities/numbers/titles, or "None — can start immediately">

Conflicts with: <each conflicting Ticket and shared surface, or "None — independent">

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Planning identity

<source identity>/ticket-<NN>

## Parent

<parent issue reference>

## What to build

<the end-to-end behavior this Ticket makes work from the user's perspective>

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- <each blocking Ticket reference, or "None — can start immediately">

## Conflicts with

- <each conflicting Ticket reference plus its shared file, contract, artifact, or integration surface, or "None — independent">

</issue-template>

Describe behavior and acceptance criteria without layer-by-layer implementation lists or code snippets. File paths are allowed only where needed to identify a direct conflict surface. Prototype output may include only the decision-bearing part of a state machine, reducer, schema, type shape, or similar artifact, identified as prototype output.

## Next-phase handoff

Ticket creation does not require implementation. When execution begins later, `implement` and `orchestrate` must fetch live Ticket state and reject a Ticket that is closed, has an open blocker, has a missing, stale, or `FAIL` Prompt Audit status, or lacks exactly one configured category role plus exactly the configured `ready-for-agent` state role. Concurrent Tickets additionally require demonstrated independence and exclusive owners, branches, and worktrees. Integrate completed Tickets one at a time, then revalidate every remaining branch after each merge.
