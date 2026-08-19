---
name: to-spec
description: Synthesize the current conversation and repository context into a spec, then publish it to the configured issue tracker without a requirements interview.
---

# To Spec

Produce a new or updated Spec from information already established in the conversation, repository, or a supplied Scratchpad. Do not conduct a requirements interview, invent decisions, or treat the Spec as an implementation unit.

Read the configured issue tracker. If it is unavailable, run `setup-omskills` first.

A supplied Scratchpad is source context, not implementation authority. Read it completely. Preserve its explicit established decisions, constraints, exclusions, unresolved Questions, and evidence pointers without treating an unresolved Question or recommendation as a decision. Do not fill gaps from an imagined prior conversation.

## Process

1. Gather all supplied source context. When a Scratchpad is supplied, distinguish its established content from its unresolved Questions before synthesis.

2. If the repository has not already been inspected in this context, inspect the current implementation in the affected area. Use the project's domain glossary terms throughout the Spec and preserve applicable ADR decisions.

3. Search the configured issue tracker by domain concept and cited relationships for an existing Spec that already governs the result. If one exists, read its complete body and comments and update it instead of creating a duplicate. Preserve accepted content outside the synthesized change.

4. Record test seams, interfaces, architecture hints, and other implementation guidance only when the supplied context or repository has already established them. Mark missing implementation decisions as unresolved rather than inventing them or interviewing the user during synthesis.

5. Write the Spec with the template below. Update the governing Spec found in step 3, or publish one new planning issue when none exists. Add no implementation-readiness state: `to-tickets` must first decompose the Spec into independently auditable Tickets.

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

## Testing Guidance

- **Established test seams:** <caller-visible seams already established, or "Not yet established">
- **Observable behavior:** <the outcomes later Tickets must preserve and verify>
- **Prior art:** <existing repository tests already identified, or "None identified">

## Out of Scope

<the source-supported boundaries of what is out of scope>

## Further Notes

<remaining established information that does not fit another section, or "None">

</spec-template>

6. After the new or updated Spec durably incorporates every accepted Scratchpad item that should survive, the supplied Scratchpad file may be removed. Preserve it when unresolved continuation context still depends on it; never delete it before checking the durable artifact.

Publishing is complete when the new or updated Spec contains every established requirement and decision, introduces no new requirement, identifies unresolved implementation details honestly, preserves unrelated accepted content, and carries no implementation-readiness state.
