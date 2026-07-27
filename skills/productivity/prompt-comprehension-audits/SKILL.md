---
name: prompt-comprehension-audits
description: Check whether clean-context agents understand an issue or execution prompt exactly as intended before costly or autonomous work.
---

# Audit Prompt Comprehension

Test whether a fresh agent's interpretation is semantically equivalent to the intended request. The interpreter and reviewer provide advisory evidence; the audit coordinator owns the final status.

## Establish the reference intent

Before delegation, record the complete accepted intent from the original execution prompt, accepted user direction, accepted conversation decisions, and every applicable authoritative issue, specification, document, ADR, and repository rule. Include every explicit boundary and every item deferred to later work.

If no accepted intent exists beyond the execution prompt, use only its explicit requirements as the reference. Record ambiguities that could materially change the outcome, scope, required workflow, deliverables, or completion point; do not infer adjacent work.

When the maintainer explicitly authorizes the invoking autonomous workflow to proceed without a comprehension audit, skip the agent passes, choose `BYPASS`, and record the status as specified below.

## Run two isolated agent passes

Start one fresh, independent agent for the interpreter pass and another for the reviewer pass. Each agent may receive baseline system and project instructions but no parent conversational turns, coordinator analysis, or desired answer. If the harness cannot guarantee these isolation conditions, choose `FAIL`, report that the audit cannot meet its required isolation, and stop after recording the status as specified below.

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

Treat a difference as semantic only when it changes the understood outcome, scope, required workflow, deliverables, or completion point. Do not fail an audit merely because an interpretation compresses or omits an enumeration while preserving its governing boundary.

When the reference sources leave an in-scope choice whose plausible options do not materially differ in behavior, scope, security, compatibility, cost, or reversibility, select the smallest safe and reversible option consistent with repository conventions—the option you would recommend if asked. Record the choice in the reference intent and execution prompt when needed, then continue.

If no semantic divergence survives adjudication, choose `PASS`.

For each semantic divergence, consult the complete reference intent:

- If it determines one safe meaning and the prompt is already clear, record the coordinator adjudication and continue without editing.
- If it determines the meaning but the execution prompt or an authoritative request artifact permits the wrong reading, minimally clarify the execution prompt and each affected authoritative artifact. Within accepted scope, the coordinator may edit any such artifact needed to express already-established intent. Preserve approved scope and deferred work; do not create acceptance criteria.
- If a material decision remains unresolved, the required change would leave approved scope, or external authority is required, choose `FAIL`, report the unresolved decision to the user, and stop after recording the status.

After adjudicating every divergence, choose `PASS` when none remains and no artifact repair requires confirmation.

After repairing an execution prompt or authoritative request artifact, use exactly one fresh clean-context confirmation reviewer. Give it only the revised prompt or request artifact and the authoritative sources that artifact explicitly requires or cites; withhold the conversation, previous responses, coordinator analysis, and a desired answer. Require it to reconstruct the requested outcome, scope boundaries, required workflow, deliverables, and completion point, then report `PASS` or `DIVERGENCE` with evidence about whether the request is self-contained and aligned with the supplied sources.

The coordinator adjudicates the confirmation once. If no concrete divergence survives, choose `PASS`. If a concrete remaining defect is resolved by the reference intent, apply one final minimal correction and choose `PASS` without another reviewer. Apply the escalation rule above only when a material decision remains unresolved. Exhausting the isolated-review budget transfers the result to coordinator adjudication; it is not a reason to stop or start a reviewer loop.

## Record the prompt audit status

Choose exactly one status:

- `PASS` — no semantic divergence survives audit-coordinator adjudication.
- `BYPASS` — the maintainer explicitly authorizes the invoking autonomous workflow to proceed without `PASS`. Never infer this authorization or represent a bypass as a pass.
- `FAIL` — the audit cannot establish equivalent clean-context comprehension, including when required isolation cannot be completed or a material divergence remains unresolved.

When the execution contract is a tracked issue or an agent brief on one, post a new comment without editing prior audit history:

```markdown
## Prompt Audit

**Status:** PASS | BYPASS | FAIL
**Contract:** <issue or agent-brief reference>
**Basis:** <concise evidence or explicit maintainer authorization>
```

For an untracked prompt, report the same fields to the invoking workflow. A newer status supersedes an older one only when it applies to the same execution contract. A material change to the requested outcome, scope, required workflow, deliverables, acceptance criteria, or completion point makes the prior status stale.

Resume the invoking workflow after `PASS` or `BYPASS`. Stop after `FAIL`.

## Audit boundary

The audit evaluates communication of intent only. It does not implement the issue, inspect runtime readiness, run tests, prepare a release, or establish runtime behavior.
