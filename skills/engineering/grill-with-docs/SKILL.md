---
name: grill-with-docs
description: Stress-test a repository plan or design one decision question at a time while updating domain terms and durable architecture decisions.
---

# Grill With Docs

Resolve a plan or design's decision tree with the user. Resolve prerequisites before dependent decisions, and do not enact the resulting plan.

Maintain an exhaustive material-decision inventory throughout the interview. Include every decision that could change the outcome, scope, behavior, ownership, constraints, deliverables, or completion point; record its prerequisites and mark it `unresolved`, `resolved`, or `explicitly deferred`. Only the user can explicitly defer an item.

## Start the interview

Read the applicable `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, plan, and repository evidence. Their absence requires no user action. Build the initial material-decision inventory, remove questions answered by discoverable facts, and order unresolved items by prerequisite.

Inspect the evidence for the first unresolved item, then ask exactly one decision question and wait. Include one recommended answer and the repository evidence or trade-off that supports it. The user makes the decision; the recommendation is not approval.

This step is complete when the exhaustive initial inventory exists and exactly one evidence-backed question with a recommendation is awaiting an answer.

## Process every reply

On each user reply, perform this order before asking anything else:

1. Validate the previous answer against glossary terms, repository evidence, earlier answers, stated constraints, edge cases, error behavior, and omitted constraints. Report contradictions and keep the affected item unresolved until they are reconciled.
2. Persist every accepted part of the previous answer under the domain and ADR rules below. Complete applicable updates in the same turn before moving to a dependent item.
3. Refresh the complete material-decision inventory. Add newly exposed material items, preserve prerequisites, and mark an item resolved or explicitly deferred only when the validated answer supports that state.
4. Inspect repository evidence for the next prerequisite-ready unresolved item. Do not ask the user for discoverable facts.
5. Ask exactly one next question and wait. Include one recommended answer and the evidence or trade-off supporting it. If every material item is resolved or explicitly deferred, ask instead for final confirmation of the shared understanding, with the recommendation to confirm only when the recorded inventory is accurate.

Surface a conflict through the one next question before moving to a dependent decision. This step is complete for a reply when the prior answer has been validated and persisted, the exhaustive inventory is current, and exactly one evidence-backed next question with a recommendation is awaiting an answer, or the validated final confirmation permits completion.

## Use repository domain language

During the interview:

- identify any use of a term that conflicts with the glossary;
- propose one canonical term when multiple words refer to the same concept or one word refers to multiple concepts;
- use concrete scenarios to determine which side of a domain boundary owns behavior; and
- verify claims about current behavior against the code and report contradictions.

## Persist resolved decisions

When a domain term's meaning, ownership, or distinction is confirmed, update the applicable `CONTEXT.md` in the same turn. If no applicable file exists, create it when the resolved term defines shared domain meaning, ownership, or distinction that later work must use. Include domain definitions and relationships, not implementation plans, tasks, or session notes. Follow [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Offer an ADR only when all three conditions hold:

1. reversing the decision would require migration, compatibility work, coordinated changes across multiple callers or stored artifacts, or another concrete cost identified during the interview;
2. the result would surprise a future reader unless the rationale were recorded; and
3. the decision is the result of a genuine trade-off.

Create an accepted ADR only after the user approves both the decision and recording it. Follow [ADR-FORMAT.md](./ADR-FORMAT.md). Treat required recording approval as an unresolved inventory item and ask it through the same one-question order.

## Finish

Stop only after every material inventory item is resolved or explicitly deferred, all required persistence is complete, and the user has confirmed the shared understanding. If no document, Ticket, issue, or plan has been generated, provide a detailed handoff to the user.
