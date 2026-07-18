---
name: prompt-comprehension-audits
description: Blind-audit whether a fresh agent reconstructs a prompt's intended execution contract before costly or autonomous work.
---

# Audit Prompt Comprehension

Test whether a fresh agent can reconstruct the intended contract from source material. The audit is read-only unless the user requested prompt edits.

## Keep the audit blind

- Establish the accepted intent or spec used for comparison. When none exists, assess self-sufficiency and label inferred intent.
- Spawn a new auditor identity for each audit pass with `fork_turns: "none"`.
- Supply the prompt and its explicitly required source artifacts. Include the accepted intent only when comparison requires it.
- Ask the auditor to reconstruct mission, inputs, outputs, authority, sequence, success conditions, fallbacks, side effects, ambiguities, and likely shortcuts, citing source evidence for material defects.
- Keep the auditor read-only and non-delegating. Consume its consolidated report rather than scratch work.

Fresh identity is central to the test: success should come from the prompt and supplied artifacts, not earlier conversation or the coordinator's diagnosis.

## Adjudicate once

Compare the report with the prompt, accepted intent, and cited evidence. Classify each material finding as a real defect, intentional flexibility, or auditor error. Resolve routine wording and ownership gaps autonomously.

A defect is something capable of changing execution: contradictory ownership, missing required input or output, ambiguous authority, broken handoff, unsafe side effect, unclear completion or fallback state, prompt/spec mismatch, or a likely shortcut that defeats the task. Style, optional detail, implementation freedom, and preferences remain outside the result unless they plausibly change behavior.

For multi-prompt workflows, concentrate on seams: shared field names, artifact paths, stage order, blocker semantics, ownership, and final side effects.

One clean auditor is the normal budget. Use a second fresh auditor only when a material disagreement remains after inspecting the cited sources; give it the disputed sources and question, then adjudicate the result. This is a tie-break, not a voting loop.

## Resolve and report

When edits are in scope, apply the smallest changes that remove real defects while preserving useful implementation judgment. Otherwise return a compact `PASS` or `DIVERGENCE` with evidence-backed findings and their disposition.

Completion means every reported material defect has a disposition and every in-scope real defect is resolved. Static comprehension establishes prompt clarity; runtime behavior, tool availability, artifact quality, and deployment remain separate evidence surfaces.
