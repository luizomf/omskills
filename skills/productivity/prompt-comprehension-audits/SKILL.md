---
name: prompt-comprehension-audits
description: Audit whether a clean agent understands a prompt as intended. Use before costly or autonomous runs, or when prompt clarity, ownership, handoffs, and likely shortcuts need blind verification.
---

# Audit Prompt Comprehension

Check whether a fresh agent reconstructs the intended contract from the prompt. This is a read-only audit unless the user explicitly asks for edits or execution.

## Keep the experiment clean

- Keep the root as coordinator and decision-maker.
- Dispatch one auditor with clean context (`fork_turns: "none"`). Supply the prompt, its explicitly required dependencies, and—only when comparison is required—the accepted intent or spec.
- Supply source artifacts, not the root's diagnosis, conversation, or desired answer.
- Instruct the auditor to inspect only supplied sources, make no changes, take no external actions, and not delegate.
- Keep the root context lean: consume the consolidated report, not the auditor's scratch work or unfiltered logs.

## Run the audit

1. **Establish intent:** Identify the accepted intent or spec against which the prompt will be judged. If none exists, audit only self-sufficiency and label inferred intent.
2. **Dispatch one clean auditor:** Ask it to reconstruct the mission, inputs, outputs, authority, sequence, success conditions, fallbacks, side effects, ambiguities, and likely shortcuts. Require source evidence for every defect.
3. **Adjudicate:** Compare the report with the prompt and accepted intent. The root owns the result and rejects invented requirements, weak citations, stylistic preferences, and confusion caused only by the auditor's summary.
4. **Decide:** Mark each material finding as real, intentional flexibility, or auditor error. Make routine judgment calls autonomously.
5. **Resolve:** If edits were requested, make the smallest prompt change that removes each real defect while preserving useful flexibility. Otherwise report the findings succinctly.

The normal budget is one clean auditor. Dispatch one different clean auditor only when a material disagreement remains after the root inspects the cited evidence. Give it the disputed sources and question, not the first auditor's conclusion. The root then decides; do not create a voting loop or third judge.

## What counts as a defect

A defect can change execution: contradictory ownership, missing input or output, ambiguous authority, broken handoff, unsafe side effect, unclear success or fallback state, prompt/spec mismatch, or a likely shortcut that defeats the task.

Style, optional detail, and intentionally delegated judgment are not defects unless they plausibly change behavior. Repeated clean-agent confusion is evidence, not automatic proof.

For multi-prompt workflows, also check shared field names, artifact paths, stage order, blocker semantics, and ownership of final side effects. Report only inconsistent seams.

## Report

Return a compact result:

- `PASS`, or `DIVERGENCE`;
- evidence-backed material findings;
- the root's disposition for each;
- minimal recommended or applied changes.

State the audit boundary when relevant: static comprehension review does not prove runtime behavior, tool availability, artifact quality, or deployment correctness.
