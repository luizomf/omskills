---
name: to-spec
description: Synthesize the current conversation and repository context into a spec, then publish it to the configured issue tracker without a requirements interview.
---

# To Spec

Produce a spec, also called a PRD, from information already established in the conversation and repository. Do not conduct a requirements interview. The only user confirmation in this process is the testing-seam check in step 2.

Read the configured issue tracker and triage-label vocabulary. If either is unavailable, run [`setup-omskills`](../setup-omskills/SKILL.md) first.

## Process

1. If the repository has not already been inspected in this context, inspect the current implementation in the affected area. Use the project's domain glossary terms throughout the spec and preserve applicable ADR decisions.

2. Identify the seam or seams through which tests will verify the feature. Prefer an existing seam. Choose the seam closest to the feature's externally observable behavior that can exercise all specified behavior. When a new seam is needed, place it as close to that behavior as possible. Minimize the number of seams; use one when one seam can cover all specified behavior. Show the proposed seams and wait for the user to confirm them.

3. Write the spec with the template below and publish it as one issue in the configured tracker. Apply `ready-for-agent`; do not perform additional triage.

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

- **Test rule:** assert behavior observable through the confirmed seam, not implementation details.
- **Modules:** <the modules exercised through that seam>
- **Prior art:** <existing repository tests that provide the pattern to follow>

## Out of Scope

<the source-supported boundaries of what is out of scope>

## Further Notes

<remaining established information that does not fit another section, or "None">

</spec-template>

Publishing is complete when the issue contains every established requirement and decision, introduces no new requirement, uses the confirmed testing seams, and has `ready-for-agent`.
