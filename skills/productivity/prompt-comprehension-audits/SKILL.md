---
name: prompt-comprehension-audits
description: Check whether clean-context agents understand an issue or execution prompt exactly as intended before costly or autonomous work.
---

# Audit Prompt Comprehension

Test semantic comprehension without executing the prompt or turning it into a more complete plan. The question is narrow: did a fresh agent understand exactly what the user asked?

## Establish the reference intent

State the accepted intent from the user's request, issue, or authoritative spec. Preserve its explicit boundaries, including work the user deferred or left for later.

When no accepted intent exists outside the prompt, report the interpretation and ambiguities without inventing the missing intent. Prompt edits remain read-only unless the user requested them.

## Run two clean passes

Use a new agent identity for each pass. Explicitly call `spawn_agent` with `fork_turns: "none"`; the default fork may copy the parent conversation and invalidate the audit. Never reuse an existing agent or continue the first agent for the second pass.

### 1. Ask a clean interpreter

Give the first agent only:

- the original prompt;
- artifacts the prompt explicitly requires;
- this question: "What do you understand you are being asked to do?"

Withhold the surrounding conversation, accepted intent, coordinator diagnosis, and desired answer. Require a compact reconstruction of the requested outcome, scope boundaries, deliverables, completion point, and material ambiguities. Keep the agent read-only and non-delegating.

The interpreter explains the prompt as written. It does not execute it, improve the task, or supply requirements that the prompt did not state.

### 2. Make the coordinator assessment

Compare the interpreter response with the accepted intent. Record only behavioral differences: work omitted, work added, a boundary changed, a deliverable misunderstood, or wording that permits materially different executions.

Missing release preparation, tests, artifacts, fallbacks, documentation, or implementation detail is not a defect unless the accepted intent requires it. The audit measures fidelity to the request, not readiness or completeness for implementation.

### 3. Ask a clean reviewer

After the interpreter finishes, always call `spawn_agent` again with `fork_turns: "none"` for a different reviewer. Give it:

- the original prompt;
- the interpreter's response;
- the accepted intent or authoritative spec.

Withhold the coordinator assessment. Keep the reviewer read-only, non-delegating, and focused on semantic equivalence. Require `PASS` or `DIVERGENCE`, with evidence for any work added, omitted, or changed. The reviewer must reject requirements that come from its idea of a complete workflow rather than the accepted intent.

### 4. Adjudicate

Use the prompt, interpreter response, reviewer judgment, and accepted intent to decide. The agents advise; the coordinator owns the result.

Return `PASS` only when the interpreted task is materially equivalent to the accepted intent and adds no work. Otherwise return `DIVERGENCE` with the smallest evidence-backed correction. When prompt edits are in scope, change only wording needed to restore that equivalence and preserve every deferred or out-of-scope boundary.

If the prompt changes, run one new interpreter/reviewer pair against the revised prompt. Stop with the remaining divergence instead of broadening the task to make it look complete.

## Audit boundary

This audit answers whether the prompt communicates the intended request. It does not validate implementation readiness, execute the issue, inspect the application, run tests, prepare a release, or prove runtime behavior.
