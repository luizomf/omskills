---
name: grill-with-docs
description: Stress-test a repository plan or design through bounded Question rounds while updating domain terms and durable architecture decisions.
---

# Grill With Docs

Resolve a plan or design's decision tree with the user. Keep the tree internal: do not render or persist it.

Before the first round and after every user response:

1. Validate every answer the user actually provided against glossary terms, repository evidence, earlier answers, stated constraints, edge cases, error behavior, and omitted constraints. Surface conflicts before treating an answer as settled.
2. Settle only the Questions the user answered. Never infer an answer for an omitted Question; keep it eligible for a later recomputed frontier. Persist every confirmed domain term or approved durable decision before moving on, under the recording gates below.
3. Investigate discoverable facts when they are needed using whatever workspace tools, authoritative sources, or isolated assistance the active harness provides. Do not ask the user to discover them or require a particular skill invocation, command spelling, or harness-specific worker API. If a fact remains unresolved, defer only the Questions that depend on it.
4. Recompute the current frontier. A Question is eligible only when all its decision and fact prerequisites are settled. Select no more than three mutually independent eligible Questions; answering one must not determine, invalidate, or change the options of another.
5. Present only that frontier and wait for the user's response.

Use this shape for every visible Question:

```markdown
### Q<number> — <short title>

<question text or options>

**Recommendation:** <concise recommended answer, with repository evidence or a trade-off>
```

Keep each identifier unchanged and unambiguous while its round is visible; identifiers need not be global across rounds. The user makes each decision; do not treat a recommendation as approval.

Do not enact the resulting plan or start implementation. Artifact writes are limited to the confirmed recording and routing rules below.

## Use repository domain language

Read the applicable `CONTEXT.md`, `CONTEXT-MAP.md`, and ADRs when they exist. Their absence requires no user action.

During the interview:

- identify any use of a term that conflicts with the glossary;
- propose one canonical term when multiple words refer to the same concept or one word refers to multiple concepts;
- use concrete scenarios to determine which side of a domain boundary owns behavior; and
- verify claims about current behavior against the code and report contradictions.

## Record resolved decisions

When a domain term's meaning, ownership, or distinction is confirmed, update the applicable `CONTEXT.md` in the same turn. If no applicable file exists, create it when the resolved term defines shared domain meaning, ownership, or distinction that later work must use. Include domain definitions and relationships, not implementation plans, tasks, or session notes. Follow [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Offer an ADR only when all three conditions hold:

1. reversing the decision would require migration, compatibility work, coordinated changes across multiple callers or stored artifacts, or another concrete cost identified during the interview;
2. the result would surprise a future reader unless the rationale were recorded; and
3. the decision is the result of a genuine trade-off.

Create an accepted ADR only after the user approves both the decision and recording it. Follow [ADR-FORMAT.md](./ADR-FORMAT.md).

These domain and ADR writes remain inline interview behavior under their own gates. They do not authorize completion routing or implementation.

## Complete the grill

Begin completion only when the recomputed Question frontier is genuinely empty because no unresolved Question or unresolved fact could materially change the plan. An empty frontier caused by an unresolved prerequisite is not completion.

For implementation-bound work, include known dependencies, conflicts, shared resources outside Git, exclusive candidates for every Ticket, and delivery/integration decisions in the shared understanding. Distinguish parallel branch artifacts from combined-target delivery, durable exact predecessor inputs and retention through all consumers. Leave complete phases and a preplanned ordinary integration Ticket blocked by every parallel member to `to-tickets` during breakdown approval.

Use these two gates in order:

1. **Confirm the shared understanding.** Consolidate the established decisions, constraints, exclusions, relevant evidence, and any unresolved Questions, including why the unresolved Questions do not block completion. Ask the user to confirm or correct that complete understanding, then wait. Do not recommend a destination yet. If the user corrects it, update the decision tree, resume grilling when needed, and repeat this gate until the user explicitly confirms the revised understanding.
2. **Confirm the destination separately.** Only after the user explicitly confirms the shared understanding, recommend exactly one destination from the criteria below and give a concise reason. Mention alternatives only when they are materially relevant to safe continuation. Ask the user to confirm that destination in a separate prompt, then wait. Never combine the two confirmations or route work before this second confirmation.

Choose the recommendation by these criteria:

- **Conversation only:** nothing needs to survive beyond the current conversation.
- **Scratchpad:** temporary, clean-context continuation is needed, but the result does not yet warrant durable planning authority.
- **New Spec:** durable behavior or workflow planning is needed and no existing Spec or Ticket already governs the result.
- **Existing Spec or Ticket update:** an existing tracked item already governs the result; update it instead of creating a duplicate.
- **Domain language:** confirmed shared meaning, ownership, or distinction qualifies for `CONTEXT.md` under the inline recording rule above.
- **ADR:** the decision passes all three ADR conditions above and the user separately approves recording it.

Destination confirmation does not replace the domain or ADR recording gates.

## Route the confirmed destination

Only after the user separately confirms the destination, take the corresponding action:

- For conversation-only completion, finish with the confirmed summary and write no new artifact.
- Write a confirmed Scratchpad directly under the safety and content contract below.
- Route a new Spec through `to-spec`; do not create a Spec under this skill's own authority.
- Route an existing Spec or Ticket update through the configured issue-tracker skill or invoking tracker workflow that owns that operation. Update the governing item instead of creating a duplicate.
- Apply a domain-language or ADR destination only under the recording gates above. Inline updates already required during the interview remain valid and are not delayed until completion.

None of these routes starts implementation. A destination confirmation, Scratchpad, Spec, tracked-item update, domain document, or ADR does not bypass existing Prompt Audit, readiness, implementation, review, PR, or handoff authority.

### Scratchpad contract

Before writing, confirm that Git ignores `.scratch/`. If it does not, add `.scratch/` to the repository's ignore rules and confirm the rule takes effect before creating the file. If the directory cannot be made ignored, do not write the Scratchpad.

Write the Scratchpad only at `.scratch/<topic-slug>/grill.md`, using a topic slug derived from the confirmed objective. Make it self-contained for an agent with no access to the prior conversation and include these sections:

```markdown
# Grill continuation: <topic>

> This Scratchpad is temporary continuation context. It carries no implementation authority.

## Objective and scope

## Established decisions

## Constraints and exclusions

## Unresolved Questions

## Evidence pointers

## Recommended next destination
```

Record concise conclusions and useful paths or URLs, not a full conversation transcript or turn-by-turn decision history. Never stage or commit the Scratchpad. It may be removed after its accepted content is incorporated into a durable artifact; preserve it while unresolved continuation context still depends on it.
