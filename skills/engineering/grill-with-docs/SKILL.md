---
name: grill-with-docs
description: Stress-test a repository plan or design while maintaining its domain glossary and durable architectural decisions.
disable-model-invocation: true
---

# Grill With Docs

Interview the user until you share a precise understanding of the subject. Walk the decision tree one branch at a time, resolving dependencies before the decisions that depend on them.

- Ask exactly one question at a time and wait for the answer.
- With each question, give your recommended answer and briefly explain why.
- Inspect the repository for discoverable facts instead of asking the user. Decisions remain theirs: present each one and wait for confirmation.
- Challenge assumptions, vague terms, contradictions, edge cases, and omitted constraints.
- Do not enact the resulting plan.

## Use the repository's domain language

Read the relevant `CONTEXT.md`, `CONTEXT-MAP.md`, and ADRs when they exist. Proceed silently when they do not.

During the interview:

- Call out conflicts with the existing glossary.
- Propose precise canonical terms for vague or overloaded language.
- Test domain boundaries with concrete scenarios.
- Check claims about current behavior against the code and surface contradictions.

## Record decisions as they resolve

Update the appropriate `CONTEXT.md` immediately when a domain term is resolved. Create it lazily when the first term warrants one. Keep it strictly implementation-free: it is a concise glossary, not a spec or scratch pad. Follow [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Offer an ADR only when the decision is all three:

1. costly to reverse;
2. surprising without its rationale; and
3. the result of a genuine trade-off.

Create an accepted ADR only after the user agrees. Follow [ADR-FORMAT.md](./ADR-FORMAT.md).

Stop when no material ambiguity remains and the user confirms the shared understanding.
