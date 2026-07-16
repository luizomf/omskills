---
name: prompt-comprehension-audits
description: Audit an agent prompt without author bias through a clean-context interpreter, an independent reviewer, and root-agent adjudication. Use before expensive, scheduled, autonomous, or side-effecting runs; when validating prompt clarity, contracts, handoffs, likely shortcuts, or prompt/spec alignment; or when an apparently correct prompt needs blind verification.
---

# Audit prompt comprehension

Test whether fresh Codex agents reconstruct the intended contract from the prompt. For a static audit, analyze the workflow without executing it.

## Preserve the experiment

- Keep the root agent as coordinator and final adjudicator.
- Spawn the interpreter and reviewer as separate subagents with `fork_turns: "none"`. Do not reuse an agent for both roles.
- Treat clean context as conversation isolation, not filesystem isolation: all Codex agents share the workspace. Give each subagent only named inputs and instruct it to ignore unrelated workspace files.
- Pass source artifacts, not the root agent's diagnosis or desired answer.
- Keep static audits read-only. The audit request authorizes analysis and subagent delegation, not execution, publication, prompt edits, or other side effects.
- Run each reviewer only after its matching interpreter finishes. Parallelize different prompt pairs only when context and concurrency limits make that safe.

## Audit each prompt

### 1. Dispatch a clean interpreter

Spawn a subagent with `fork_turns: "none"`. Provide only:

- the prompt under test;
- dependencies the prompt explicitly requires it to read;
- a request to reconstruct the contract without executing it.

Do not provide the spec, historical prompts, surrounding conversation, root assessment, or intended interpretation. Instruct the interpreter to inspect only the supplied content and explicitly named dependency paths, perform no writes or external actions, and return:

1. mission;
2. inputs and outputs;
3. authority and ownership;
4. sequence and decision points;
5. success, fallback, and blocker states;
6. allowed side effects;
7. ambiguities;
8. likely shortcuts or unsafe interpretations.

Require line citations when the source has stable line numbers; otherwise require short exact excerpts for every ambiguity or risk claim. The interpreter is complete when every category has an evidence-backed answer or is marked unspecified.

### 2. Make the root assessment

Compare the interpreter's reconstruction against, in order:

1. the current spec or accepted intent, which is authoritative;
2. current role and orchestration contracts;
3. the matching historical prompt, only when checking whether useful behavior was accidentally lost.

History is evidence, not authority. A newer intentional decision overrides it. Record candidate divergences before reading the independent review; do not edit the prompt yet. This step is complete when each material contract element is classified as aligned, ambiguous, contradictory, or omitted.

### 3. Dispatch a clean reviewer

After the interpreter returns, spawn a different subagent with `fork_turns: "none"`. Provide:

- the original prompt;
- the interpreter response;
- the current spec or accepted intent;
- the matching historical role only when preservation matters.

Withhold the root assessment to avoid anchoring. Instruct the reviewer to inspect only supplied content, perform no side effects or further delegation, and return `PASS` or `DIVERGENCE` with evidence. Require it to classify findings as:

- interpreter error or omission;
- real prompt ambiguity;
- prompt/spec contradiction;
- historical regression;
- intentionally flexible judgment;
- plausible model shortcut.

The reviewer owns comparison with the spec; the interpreter was intentionally denied it. Require the reviewer to:

- trace ownership across roles before declaring a missing guard;
- verify each claimed requirement against the cited spec text;
- reject invented requirements and mismatched citations;
- distinguish similarly named actions performed at different workflow stages;
- distinguish a prompt defect from an interpreter summary omission.

The review is complete when every claimed divergence identifies the source evidence, affected behavior, and responsible layer.

### 4. Adjudicate at the root

Compare the root assessment with the reviewer. Agreement on material behavior supports a pass. Disagreement triggers evidence inspection, not automatic prompt editing: the interpreter, reviewer, spec, history, or root assessment may be wrong.

Repeated independent confusion about the same structure is evidence of a clarity defect even when the author's intent seems obvious. Before accepting a missing-path or missing-dependency finding, trace the full handoff seam: one role may produce an intermediate artifact that another promotes, or consume a path supplied by the orchestrator.

Finish the audit matrix before proposing changes. Edit prompts only when the user requested edits or approves the evidence-backed changes. Adjudication is complete when every finding has a disposition and every material recommendation traces to evidence.

## Report the matrix

Use one row per prompt:

| Prompt | Interpreter | Reviewer | Root assessment | Result | Evidence | Recommended change |
|---|---|---|---|---|---|---|

Leave `Recommended change` empty for clean passes. Keep optional stylistic observations out of failure results. For a single prompt, the final response can be the durable record. For a multi-prompt or unattended audit, update a matrix file incrementally only when workspace writes are within the user's requested scope; otherwise return it in the response.

## Check workflow seams

After adjudicating all prompt pairs, mechanically compare the prompts for:

- status vocabularies and handoff fields;
- artifact paths and stage ordering;
- optional-stage degradation and blocker semantics;
- ownership of final side effects;
- one-pass or no-loop guarantees.

Verify environment and API claims against their actual primary interface before accepting them. The seam check is complete when every cross-prompt field and transition is either consistent or represented as a matrix finding.

## Bound the conclusion

A static audit provides strong evidence about prompt self-sufficiency, contract comprehension, ownership, fallbacks, wording-induced shortcuts, spec alignment, and preserved historical behavior. It does not prove tool use, source or artifact quality, build correctness, deployment, or behavior on large real inputs. State this boundary in the result when it matters.

## Dynamic clean-room branch

Use this branch only when the user has authorized actual execution and its side effects:

1. Spawn a clean-context executor with only the prompt and explicit dependencies to perform the bounded task.
2. Spawn a separate clean-context reviewer with the prompt, result, accepted intent, and narrowly relevant history.
3. Adjudicate both outputs at the root.

Reviewer disagreement is evidence to inspect, never permission to rewrite, publish, retry indefinitely, or expand scope. Preserve the semantic prompt when comparing runtimes; adapt only invocation, tool, and handoff mechanics.

## Control cost and context

- Use one interpreter and one reviewer per prompt; add a third clean judge only for unresolved material disagreement.
- Keep outputs structured and bounded. For more than three prompts, process pairs sequentially or in small batches and retain only the compact matrix plus artifact paths in root context.
- Respect available collaboration slots; sequential interpreter/reviewer pairs are the safe default.
- Use a persistent goal only when the runtime demonstrably stops early, not merely because the audit is long.
- For cross-harness evaluation, repeat the same bounded task and record elapsed time, context growth, interventions, retries, completion, delivery, independently reviewed quality, and handoff survival on the target surface.
