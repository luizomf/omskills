---
name: to-tickets
description: Break a plan, spec, or the current conversation into tracer-bullet tickets with blocking and conflict edges, published to the configured tracker.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into **tickets** — tracer-bullet vertical slices with explicit scheduling edges:

- A **blocking edge** requires another ticket to complete before this one can start or integrate.
- A **conflict edge** means two otherwise unblocked tickets should not have active writers at the same time because they overlap in files, contracts, artifacts, or integration assumptions.

The issue tracker and triage label vocabulary should have been provided to you — use the [`setup-omskills`](../setup-omskills/SKILL.md) skill first if not.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its blocking and conflict edges. A ticket with no blockers enters the frontier. It is eligible for parallel work only when repository evidence also shows no material conflict with active tickets; missing declared dependencies alone does not prove independence.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket — green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on tickets that genuinely gate it?
- Are the conflict edges correct — which unblocked tickets still share a contract, artifact, or integration surface?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker configured by [`setup-omskills`](../setup-omskills/SKILL.md) — the tickets are the same either way, only the shape of the blocking edges changes:

- **Local markdown** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file lists both edge types. Use the per-ticket template below — never combine all tickets into one file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so edges can reference real identifiers. Use native blocking relationships where available; record conflict edges in the issue body unless the tracker has an equivalent native relation. Apply the `ready-for-agent` triage label unless instructed otherwise — the tickets are agent-grabbable by construction.

Do NOT close or modify any parent issue.

Work the **frontier**: tickets whose blockers are all done. Multiple frontier tickets may run concurrently only when their independence is demonstrated and each has exclusive ownership, branch, and worktree.

<local-ticket-template>

# <NN> — <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None — can start immediately".

**Conflicts with:** the numbers/titles of unblocked tickets that must not have active writers concurrently, or "None — independent".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective — not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None — can start immediately".

## Conflicts with

- A reference to each conflicting ticket and the shared surface, or "None — independent".

</issue-template>

In either form, avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

Work each frontier ticket with the [`implement`](../implement/SKILL.md) skill, clearing context between tickets. Parallel writers require exclusive worktrees and demonstrated independence; integrate completed tickets one at a time and revalidate the remaining branches after every merge.
