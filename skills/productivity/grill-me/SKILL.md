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

Question assumptions, undefined or multiply defined terms, contradictions, boundary cases, and missing constraints when they could change the outcome or scope. Keep the session stateless and read-only: do not write or modify repository artifacts, invoke a writing workflow, or execute the resulting plan.

## Complete the grill

Begin completion only when the recomputed Question frontier is genuinely empty because no unresolved Question or unresolved fact could change the outcome or scope. An empty frontier caused by an unresolved prerequisite is not completion. Completion never starts implementation.

For implementation-bound work, include known dependencies, conflicts, shared resources outside Git, exclusive candidates for every Ticket, and delivery/integration decisions in the shared understanding. Distinguish parallel branch artifacts from combined-target delivery, durable exact predecessor inputs and retention through all consumers. Leave complete phases and a preplanned ordinary integration Ticket blocked by every parallel member to `to-tickets` during breakdown approval.

Use these two gates in order:

1. **Confirm the shared understanding.** Consolidate the established decisions, constraints, exclusions, relevant evidence, and any unresolved Questions, including why the unresolved Questions do not block completion. Ask the user to confirm or correct that complete understanding, then wait. Do not recommend a destination yet. If the user corrects it, update the decision tree, resume grilling when needed, and repeat this gate until the user explicitly confirms the revised understanding.
2. **Confirm the destination separately.** Only after the user explicitly confirms the shared understanding, recommend exactly one destination from the criteria below and give a concise reason. Mention alternatives only when they are materially relevant to safe continuation. Ask the user to confirm that destination in a separate prompt, then wait. Never combine the two confirmations or route work before this second confirmation.

Choose the recommendation by these criteria:

- **Conversation only:** nothing needs to survive beyond the current conversation.
- **Scratchpad:** temporary, clean-context continuation is needed, but the result does not yet warrant durable planning authority.
- **New Spec:** durable behavior or workflow planning is needed and no existing Spec or Ticket already governs the result.
- **Existing Spec or Ticket update:** an existing tracked item already governs the result; update it instead of recommending a duplicate.
- **Domain language or ADR:** shared domain meaning belongs in `CONTEXT.md`, or a durable decision belongs in an ADR, only when the destination satisfies that artifact's existing recording gate.

After the user confirms the destination, report the confirmed recommendation and a concise continuation summary in the conversation only. `grill-me` never carries out the route: it never writes a Scratchpad, Spec, tracked-item update, domain document, ADR, or any other repository artifact. It never starts implementation, resolves the later Delivery mode gate, or bypasses the implementation, proportionate review, repository delivery, or route-specific readiness, Prompt Audit, and authorization rules.


