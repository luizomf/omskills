---
name: prompt-comprehension-audits
description: Check whether clean-context agents understand an issue or execution prompt exactly as intended before costly or autonomous work.
---

# Audit Prompt Comprehension

Test whether a fresh agent's interpretation is semantically equivalent to the intended request.

## Establish the reference intent

Record the accepted intent from the user's request, issue, or authoritative specification, including every explicit boundary and every item deferred to later work.

If no accepted intent exists outside the prompt, use only the prompt's explicit requirements as the reference and report each ambiguity without resolving it. Edit the prompt only when the user requested edits.

## Run two isolated agent passes

Start one fresh, independent agent for the interpreter pass and another for the reviewer pass. Each agent may receive baseline system and project instructions but no parent conversational turns, coordinator analysis, or desired answer. If the harness cannot guarantee these isolation conditions, stop and report that the audit cannot meet its required isolation.

### 1. Run the interpreter pass

Give the interpreter only:

- the original prompt;
- artifacts that the prompt explicitly requires;
- this question: "What do you understand you are being asked to do?"

Require only a reconstruction of the requested outcome, scope boundaries, required actions and order, deliverables, completion point, and ambiguities that could change any of those items. Keep the interpreter read-only and non-delegating.

The interpreter must explain the prompt as written without executing it, revising it, or adding unstated requirements.

### 2. Record the coordinator assessment

Compare the interpreter response with the reference intent. Record only these differences:

- requested work omitted or unrequested work added;
- a scope boundary changed;
- a required action or its order changed;
- a deliverable or completion point changed;
- wording interpreted in a way that changes the outcome, scope, required workflow, deliverables, or completion point.

Do not report missing release work, tests, artifacts, fallbacks, documentation, or implementation details unless the reference intent requires them.

### 3. Run the reviewer pass

After the interpreter finishes, give the reviewer only:

- the original prompt;
- the interpreter's response;
- the reference intent recorded above.

Withhold the coordinator assessment. Keep the reviewer read-only and non-delegating. Require `PASS` or `DIVERGENCE` and quoted or paraphrased evidence for every item added, omitted, or changed. The reviewer must compare semantic meaning and exclude requirements that arise only from its preferred implementation workflow.

### 4. Adjudicate

Decide from the prompt, interpreter response, reviewer judgment, and reference intent; the coordinator, not either delegated agent, owns the result.

Return `PASS` only when the interpreted task has the same outcome, scope, required actions and order, deliverables, and completion point as the reference intent and adds no work. Otherwise, return `DIVERGENCE` with the smallest evidence-backed correction. If prompt edits are authorized, preserve every deferred and out-of-scope boundary.

After changing the prompt, run exactly one new interpreter/reviewer pair against the revised text. If any divergence remains, report it and stop; do not add scope to obtain a pass.

## Audit boundary

The audit evaluates communication of intent only. It does not evaluate implementation readiness, execute the issue, inspect the application, run tests, prepare a release, or establish runtime behavior.
