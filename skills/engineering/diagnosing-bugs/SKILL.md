---
name: diagnosing-bugs
description: Reproduction-first diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

# Diagnosing Bugs

Prefer reproduction before a fix. Use these phases as a feedback loop, not a rigid waterfall: a falsifiable hypothesis or targeted instrumentation may be needed to obtain the first reproduction. State what the evidence establishes and what remains uncertain.

When exploring the codebase, read `CONTEXT.md` if it exists and follow ADRs that apply to the affected modules.

Read-only inspection and reproduction may begin immediately. Before creating a harness or test, adding instrumentation, applying a fix, or making any other implementation mutation, pass the adaptive Delivery mode gate. Honor topology and maintainer availability already established semantically; ask only for a materially unresolved dimension. An untracked request or exactly one selected Ticket may remain with the conversational responsible agent as Direct Assisted work without mandatory readiness, Prompt Audit, dispatcher, separate Ticket coordinator, or writer.

## Phase 1 — Establish the symptom and feedback loop

Identify the expected behavior, observed failure, relevant environment, and available evidence. Prefer one command that reaches the actual bug path and distinguishes the reported symptom from unrelated failures.

Choose the smallest useful approach:

1. An existing unit, integration, or end-to-end test at a seam that reaches the bug.
2. A CLI fixture, HTTP request, browser interaction, or replay of a captured event/log.
3. A throwaway harness containing the minimum callers and dependencies needed to reach the failure.
4. A property/fuzz run, concurrency workload, or differential comparison with recorded inputs and conditions.
5. A timing harness, profiler, query plan, or bounded `git bisect` investigation when history and evidence make it useful.
6. A [`scripts/hitl-loop.template.sh`](scripts/hitl-loop.template.sh) record when a human action is unavoidable.

Assert the symptom, not merely process success. Reduce avoidable setup and control time, random seeds, and external dependencies where practical without removing the behavior under investigation.

For intermittent bugs, record attempts or exposure, observed failures, conditions, and reproduction rate. Choose a bounded workload proportionate to the observed frequency, cost, and operational risk; no fixed number of attempts or minimum failure rate determines whether investigation may continue. Non-recurrence alone does not disprove a rare failure.

If a reliable loop is unavailable, use captured evidence and an explicit falsifiable hypothesis to design a discriminating probe under phases 3–4. Ask for missing artifacts or access only when they are genuinely needed. Production instrumentation requires appropriate authorization; do not infer it from permission to debug locally. If neither evidence nor authorized investigation can advance the question, report the concrete blocker instead of inventing a cause.

This phase is complete when the symptom and environment are identified and either a runnable feedback loop has an observed result, or the evidence gap and next authorized discriminating probe are explicit. Record commands, outcomes, and limitations; do not label an unobserved reproduction as successful.

## Phase 2 — Reproduce and minimise

Use the feedback loop or captured evidence to distinguish the original symptom from nearby failures. Preserve the exact error, output difference, or timing for comparison.

Remove inputs, callers, configuration, data, and steps one at a time when doing so preserves the relevant failure path. Re-run after each meaningful reduction and restore a removed part when evidence shows it was necessary. For rare failures, account for exposure and uncertainty rather than treating one passing run as proof that a reduction removed the bug.

This phase is complete when the smallest currently supported reproduction or evidence packet is identified, with any remaining minimisation limits stated. Return to hypotheses or instrumentation when more evidence is needed; exhaustive minimisation is not a prerequisite for a useful probe.

## Phase 3 — Form and test hypotheses

State the evidence-backed candidate cause and its falsifiable prediction:

> If <X> is the cause, then <changing Y> will remove the symptom or <observing Z> will distinguish it from the alternatives.

One strong hypothesis is enough to begin. Add and rank alternatives when the evidence supports them or a failed probe leaves competing explanations; do not manufacture a quota. A maintainer-supplied hypothesis is a candidate to test, not a confirmed cause.

Show the current hypothesis and planned probe concisely. Continue within established authorization without a ceremonial approval gate; ask only when the probe's scope or risk needs a new decision.

This phase is complete when each hypothesis being tested has a discriminating prediction and an authorized probe. Revise or discard it when observations contradict it.

## Phase 4 — Instrument and compare

Map each probe to its prediction and change one causal variable at a time where practical. Prefer a debugger, REPL, focused trace, profiler, or logs at the relevant boundary over broad logging. Mark temporary instrumentation so it can be found and removed, for example with a unique `[DEBUG-a4f2]` tag.

Preserve useful error context without capturing secrets or unnecessary user data. Record when instrumentation may change timing or mask the failure. Compare before and after under equivalent conditions.

For a performance regression, record a numerical baseline before claiming improvement. Use history or bisect when it helps isolate the regression; neither is mandatory when the relevant cause can be tested directly.

This phase is complete when the probe has an observed result that supports, contradicts, or narrows the hypothesis. An inconclusive result returns to investigation; it is not evidence of a fix.

## Phase 5 — Fix and regression evidence

Apply the smallest correction supported by the investigation. Prefer a regression test before the fix when an available seam reaches the bug pattern through its actual callers; a test that omits the faulty ordering or coordination is not that regression test.

When a valid seam exists:

1. Convert the reproduction into a test and capture its failure on the original symptom.
2. Apply the fix and capture the passing result.
3. Run relevant existing checks and the original, unminimised scenario.

When no faithful automated seam exists, document that limitation and use the strongest available before/after evidence. Do not fabricate a test or weaken a valid one to make the candidate pass. A candidate correction with incomplete causal verification remains explicitly provisional.

This phase is complete when the correction and applicable checks have observed results, and any remaining causal or regression-coverage uncertainty is stated.

## Phase 6 — Cleanup and handoff

Before reporting completion:

- Re-run the original scenario or equivalent probe and report the result. For intermittent bugs, include exposure and observed failure counts rather than claiming that non-recurrence proves elimination.
- Report regression-test and repository-check results, or the exact missing evidence.
- Remove owned temporary instrumentation unless retaining it was explicitly authorized; preserve unrelated diagnostics and work.
- Remove throwaway harnesses or keep useful ones in a clearly marked location according to repository retention rules.
- Describe the supported cause and correction in the commit or handoff; separate confirmed evidence from remaining hypotheses.

This phase is complete when the candidate, evidence, cleanup, and remaining limitations are accounted for. A verified fix may be delivered under the repository workflow; unresolved verification must not be reported as confirmed success.

If the investigation exposes a durable architectural problem, explain what would prevent recurrence and recommend `improve-codebase-architecture` when a separate design investigation is useful. Do not automatically launch adjacent work.
