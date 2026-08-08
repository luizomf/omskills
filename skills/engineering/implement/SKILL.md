---
name: implement
description: "Implement one authorized code unit through clean-context execution and coordinator-owned completion."
---

# Implement

Deliver exactly one repository implementation unit. The invoking agent is the coordinator and owns scope, decisions, corrections, verification, integration, and completion.

## 1. Establish one authorized unit

Read the accepted request and its governing sources. Identify the requested behavior, every acceptance criterion, and one execution contract that fits a single implementation unit. If the request combines independent units or a blocked or conflicting set of Tickets, stop before writer dispatch or code and report that one unit must be selected or decomposed.

When the unit is a tracked Ticket, fetch its live state, complete comments, configured native or fallback blockers, and configured triage-role metadata. Reject it before writer dispatch or code when any of these conditions holds:

- the Ticket is closed;
- any configured native or fallback relation identifies an open blocker;
- its newest applicable Prompt Audit status is missing, stale, or `FAIL`; or
- it does not carry exactly one configured category role and exactly the configured `ready-for-agent` state role, with no other configured state role.

A current explicit maintainer-authorized `BYPASS` satisfies the Ticket audit condition; an inferred or unrecorded bypass does not. Recheck these live Ticket invariants immediately before writer dispatch and stop if any changed.

Locate the newest applicable `Prompt Audit` status for the exact execution contract:

- `PASS` authorizes code only while it is current.
- `BYPASS` authorizes code only when a maintainer explicitly granted it for this contract.
- `FAIL`, a missing status, or a stale status stops the workflow before writer dispatch or code. Report the choices to run `prompt-comprehension-audits` or obtain an explicit maintainer-authorized bypass.

A material change to the requested outcome, scope, required workflow, deliverables, acceptance criteria, or completion point makes an earlier status stale. Never infer bypass from a general implementation request. If the maintainer explicitly authorizes bypass in the current invocation, record it through `prompt-comprehension-audits` before continuing.

Resolve source-determined in-scope choices with the smallest safe and reversible option consistent with repository conventions. Ask the user only when a material decision remains unresolved, the required change would leave accepted scope, or external authority is required.

This step is complete when exactly one implementation unit has fixed scope and acceptance criteria under a current `PASS` or explicit maintainer-authorized `BYPASS`.

## 2. Execute once in clean context

When the harness provides clean writer isolation, start exactly one isolated writer for the whole unit. Give it the applicable execution contract, governing sources, fixed scope, acceptance criteria, repository instructions, and expected verification. The assignment must remain covered by the current Prompt Audit status.

The writer implements and locally verifies the unit in one pass, then returns the implementation and evidence to the coordinator. It is a leaf: it does not review, spawn, delegate, or perform a correction round.

When clean writer isolation is unavailable, the coordinator implements the already-authorized unit directly and discloses the limitation in the result. Continue without adding a user-confirmation gate, reviewer pass, or delegated correction loop.

This step is complete when one implementation result and its verification evidence have returned to the coordinator or have been produced directly by the coordinator.

## 3. Adjudicate and verify

Inspect the complete result against every acceptance criterion and governing repository rule. Apply all surviving in-scope corrections directly; never return corrections to the writer.

Use `tdd` when the behavior can be exercised at a test seam already confirmed in the request, specification, issue, Ticket, or conversation. Pass that confirmation through without asking the user to reconfirm it.

Discover verification only from the target repository's instructions, changed-unit documentation, test layout, scripts, and configured automation. Classify each discovered check for this implementation unit before running it. Run only checks the target repository defines and that apply to the changed unit; do not invent or assume typechecking, a single-test convention, or one conventional full suite. A repository-required complete suite remains applicable when its own instructions require it.

Report every discovered check considered, its exact command when one exists, and exactly one status: `passed`, `failed`, `skipped`, `unavailable`, or `inapplicable`. Give the reason for every status other than `passed`; never hide a failing applicable check behind a skip or omit a required check. A required applicable failure blocks a successful completion claim.

This step is complete when the coordinator has corrected every source-determined divergence, verified the complete unit against every acceptance criterion, and recorded the complete repository-applicable check report.

## 4. Integrate and complete

Integrate the verified unit through the repository's required workflow. Commit only when the user explicitly requested a commit or the repository's recorded workflow says this invocation should commit, and use a conventional commit. Independent code review remains outside this direct path.

This step is complete when the coordinator has integrated the verified result, disclosed any isolation limitation, and reported completion, deviations, every check status (including unavailable, inapplicable, skipped, or failing checks), and concerns.
