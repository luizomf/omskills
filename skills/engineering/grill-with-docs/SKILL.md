---
name: grill-with-docs
description: Stress-test a repository plan or design one decision question at a time while updating domain terms and durable architecture decisions.
---

# Grill With Docs

Resolve a plan or design's decision tree with the user. Resolve prerequisites before dependent decisions.

For each turn:

1. Validate the user's previous answer, when one exists, against glossary terms, repository evidence, earlier answers, stated constraints, edge cases, error behavior, and omitted constraints. Persist every confirmed domain term or approved durable decision before moving on, and surface any conflict first.
2. Inspect the repository for facts that can answer the next question. Do not ask the user for discoverable facts.
3. Ask exactly one unresolved decision question and wait for the answer.
4. Include one recommended answer and the repository evidence or trade-off that supports it. The user makes the decision; do not treat the recommendation as approval.

Do not enact the resulting plan.

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

Stop when no material ambiguity remains and the user confirms the shared understanding.

If no document, ticket, issue, or plan has been generated, provide a detailed handoff to the user.