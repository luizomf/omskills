---
name: diagnosing-bugs
description: Reproduction-first diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

# Diagnosing Bugs

A discipline for hard bugs. Complete these phases in order, and skip a phase only when explicitly justified.

When exploring the codebase, read `CONTEXT.md` if it exists and follow ADRs that apply to the affected modules.

## Phase 1 — Build a feedback loop

Create one command that executes the bug's code path and returns a pass/fail verdict for the exact symptom reported by the user.

Try these methods in roughly this order:

1. A failing unit, integration, or end-to-end test at a seam that reaches the bug.
2. A curl or HTTP script against a running development server.
3. A CLI command with fixture input that compares stdout with a known-good result.
4. A Playwright or Puppeteer script that asserts on the DOM, console, or network.
5. A replay of a captured request, payload, or event log through the isolated code path.
6. A throwaway harness containing the minimum service set and dependencies required to call the bug path.
7. For intermittent wrong output, a property or fuzz loop over 1,000 random inputs.
8. When the regression is bounded by two commits, datasets, or versions, a harness compatible with `git bisect run`.
9. A differential loop that compares the same input across the old and new versions or two configurations.
10. When a human action is unavoidable, a `scripts/hitl-loop.template.sh` script that records the human action and resulting output.

After the command exists:

- assert the reported symptom rather than only checking for process success;
- reduce setup and unrelated initialization until a run takes seconds, not minutes;
- pin time and random seeds and isolate filesystem and network dependencies when they affect the verdict;
- make the command unattended, except for the structured human step in the HITL script.

For a non-deterministic bug, run the trigger 100 times under recorded conditions. Use parallel execution, load, narrower timing windows, or injected delays to raise the reproduction rate. Continue until the reproduction rate is high enough to debug against; one reproduction per 100 is insufficient.

If no method produces a loop, stop. Report every method attempted and request one of:

- access to an environment that reproduces the bug;
- a captured HAR file, log dump, core dump, or timestamped screen recording;
- permission to add temporary production instrumentation.

Do not generate hypotheses before a feedback-loop command exists.

### Phase 1 completion

Phase 1 is complete only when you report one command, its output from at least one completed run, and evidence that it:

- [ ] executes the actual bug path and fails on the user's reported symptom;
- [ ] returns the same verdict on every deterministic run, or reproduces at a pinned rate high enough to debug against for a non-deterministic bug;
- [ ] completes in seconds, not minutes;
- [ ] runs unattended, except through `scripts/hitl-loop.template.sh`.

Do not begin Phase 2 until all four conditions hold.

## Phase 2 — Reproduce and minimise

Run the Phase 1 command and confirm that:

- [ ] it produces the user's reported failure rather than a different nearby failure;
- [ ] it reproduces on at least two runs, or at the recorded rate for a non-deterministic bug;
- [ ] the exact error, output difference, or timing is captured for comparison after the fix.

Then remove inputs, callers, configuration, data, and steps one at a time. Re-run the command after each removal. Restore an element when its removal changes the verdict to green.

Phase 2 is complete when the failure still reproduces and removing any remaining element makes the command green. Do not begin Phase 3 before both conditions hold.

## Phase 3 — Hypothesise

Before testing any cause, write and rank 3–5 hypotheses. For each hypothesis, state its testable prediction in this format:

> If <X> is the cause, then <changing Y> will remove the symptom or <changing Z> will increase it.

Discard or revise any hypothesis without a falsifiable prediction. Show the ranked list to the user before testing. If the user is unavailable, proceed without waiting and retain the stated ranking.

## Phase 4 — Instrument

Map each probe to one Phase 3 prediction and change one variable per probe.

Prefer tools in this order:

1. A debugger or REPL when the environment supports the required observation.
2. Logs only at boundaries that distinguish the ranked hypotheses.

Do not emit broad logs for later filtering. Prefix every temporary debug log with a unique tag such as `[DEBUG-a4f2]`.

For a performance regression, establish a numerical baseline with a timing harness, profiler, or query plan, then bisect. Do not apply a performance fix before recording the baseline.

## Phase 5 — Fix and regression test

Write the regression test before the fix only when an available seam reproduces the bug pattern as it occurs at the call site. A seam is not valid when it omits required callers or call-chain behavior.

If no such seam exists, document that limitation and carry it into Phase 6. Do not add a test at a seam that cannot reproduce the pattern.

If a valid seam exists, in order:

1. Convert the minimised reproduction into a test at that seam.
2. Run it and capture the failing result.
3. Apply the fix.
4. Run the test and capture the passing result.
5. Run the Phase 1 command against the original, unminimised scenario.

## Phase 6 — Cleanup and post-mortem

Before reporting completion:

- [ ] Re-run the Phase 1 command and confirm that the original symptom is absent.
- [ ] Confirm that the regression test passes, or document the missing valid seam.
- [ ] Search for every `[DEBUG-...]` prefix created during diagnosis and remove all matching instrumentation.
- [ ] Remove throwaway prototypes created during diagnosis or move them to a location whose path marks them as debug artifacts.
- [ ] State the confirmed hypothesis in any commit or PR message produced for the fix.

After the fix, ask what would have prevented the bug. If prevention requires an architectural change, such as adding a valid test seam or removing demonstrated caller coupling, pass those findings to [`improve-codebase-architecture`](../improve-codebase-architecture/SKILL.md). Make this recommendation only after the fix is complete.
