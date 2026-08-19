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

Stop only when no unresolved Question or unresolved fact could materially change the plan and the user confirms the shared understanding. An empty frontier caused by an unresolved prerequisite is not completion.

If no document, ticket, issue, or plan has been generated, provide a detailed handoff to the user.