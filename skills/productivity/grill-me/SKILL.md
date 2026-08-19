---
name: grill-me
description: Stress-test any plan, idea, or design through bounded rounds of independent decision Questions.
---

# Grill Me

Stress-test the plan by maintaining an internal decision tree of unresolved decisions, their prerequisites, and relevant facts. Keep the tree internal: do not render or persist it.

Before the first round and after every user response:

1. Update the tree from settled decisions and known constraints. Validate every answer the user actually provided against available evidence, earlier answers, stated constraints, boundary cases, and missing assumptions. Surface conflicts before treating an answer as settled.
2. Settle only the Questions the user answered. Never infer an answer for an omitted Question; keep it eligible for a later recomputed frontier.
3. Investigate discoverable facts when they are needed using whatever workspace tools, authoritative sources, or isolated assistance the active harness provides. Do not ask the user to discover them or require a particular skill invocation, command spelling, or harness-specific worker API. If a fact remains unresolved, defer only the Questions that depend on it.
4. Recompute the current frontier. A Question is eligible only when all its decision and fact prerequisites are settled. Select no more than three mutually independent eligible Questions; answering one must not determine, invalidate, or change the options of another.
5. Present only that frontier and wait for the user's response.

Use this shape for every visible Question:

```markdown
### Q<number> — <short title>

<question text or options>

**Recommendation:** <concise recommended answer, with supporting evidence or trade-off>
```

Keep each identifier unchanged and unambiguous while its round is visible; identifiers need not be global across rounds. The recommendation informs the user's decision and does not settle it.

Question assumptions, undefined or multiply defined terms, contradictions, boundary cases, and missing constraints when they could change the outcome or scope. Keep the session read-only and do not execute the resulting plan.

Stop only when no unresolved Question or unresolved fact could change the outcome or scope and the user confirms the resulting understanding. An empty frontier caused by an unresolved prerequisite is not completion.

If no document, ticket, issue, or plan has been generated, provide a detailed handoff to the user.


