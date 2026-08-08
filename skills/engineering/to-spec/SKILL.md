---
name: to-spec
description: Synthesize the current conversation and repository context into a spec, then publish it to the configured issue tracker without a requirements interview.
---

# To Spec

Produce a complete **Spec** from information already established in the conversation and repository. Do not conduct a requirements interview. The only user confirmation in this process is the caller-visible test-seam check in step 3.

Read the configured Issue tracker and triage-label vocabulary. If either is unavailable, run `setup-omskills` first.

## Process

### 1. Gather the established contract

Read the accepted conversation decisions and every referenced issue, plan, prototype, domain document, ADR, and repository instruction. Make an internal inventory of every established requirement, decision, success case, failure case, edge case, and out-of-scope boundary. Do not fill gaps with plausible requirements or preferred implementation details.

### 2. Inspect the affected area

If the repository has not already been inspected in this context, inspect the current implementation and applicable tests. Use the project's domain glossary terms throughout the Spec and preserve applicable ADR decisions.

### 3. Confirm the caller-visible test seam

Identify the **caller-visible test seam** or seams through which tests will verify the feature: interfaces shared by production callers and behavior tests. Prefer an existing test seam closest to the externally observable behavior that can exercise all specified behavior. When a new seam is needed, place it as close to that behavior as possible and minimize the number of seams.

Show the proposed caller-visible test seams and wait for the user to confirm them. This is the process's only confirmation gate.

### 4. Write and check the complete Spec

Write the Spec with the template below. Before publication, compare it with the source inventory from step 1: it must preserve every established requirement and decision, include every established boundary and the confirmed caller-visible test seam, and introduce nothing unstated.

<spec-template>

## Problem Statement

<the established problem from the user's perspective>

## Solution

<the established solution from the user's perspective>

## User Stories

<an extensive numbered list covering every established aspect of the feature; include each distinct actor goal or user-visible outcome, with established success, failure, and edge outcomes as separate stories when they produce different user-visible results; include no unstated requirements>

1. As an <actor>, I want <feature>, so that <benefit>.

<user-story-example>
1. As a mobile bank customer, I want to see the balance on my accounts, so that I can make informed spending decisions.
</user-story-example>

## Implementation Decisions

<a bullet list of the implementation decisions already established, including applicable modules and interfaces, technical clarifications, architecture, schema changes, contracts, and interactions>

Do not include file paths or code snippets. Exception: when prototype output contains a state machine, reducer, schema, type shape, or other snippet that encodes an established decision more precisely than prose can, include only its decision-bearing parts and identify it as prototype output.

## Testing Decisions

- **Test rule:** assert behavior observable through the confirmed caller-visible test seam, not implementation details.
- **Confirmed caller-visible test seam:** <the user-confirmed production-caller interface or interfaces>
- **Modules:** <the modules exercised through that seam>
- **Prior art:** <existing repository tests that provide the pattern to follow>

## Out of Scope

<the source-supported boundaries of what is out of scope>

## Further Notes

<remaining established information that does not fit another section, or "None">

</spec-template>

### 5. Publish as a planning artifact and audit it

Publish the complete Spec as one artifact in the configured Issue tracker. Give it no configured state-role label: in particular, do not apply `ready-for-agent`, `ready-for-human`, or another implementation-readiness state. Non-state metadata may follow the configured tracker policy, but a Spec remains a planning artifact.

After the complete published body is stable, run `prompt-comprehension-audits` against that exact Spec and record the result using the configured tracker comment operation. The Spec may authorize Ticket publication or code only when its newest applicable Prompt Audit status is a current `PASS` or explicit maintainer-authorized `BYPASS`. A missing, stale, or `FAIL` status stops the handoff before either transition. Never infer bypass, and do not add another user-confirmation gate for the audit. A later material edit to the Spec makes the prior status stale and requires a new audit before handoff.

Publishing is complete when the planning artifact contains every established requirement and decision without invention, uses the confirmed caller-visible test seam, has no configured state-role label, and has a recorded current `PASS` or explicit maintainer-authorized `BYPASS` for its complete contract.
