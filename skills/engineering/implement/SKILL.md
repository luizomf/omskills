---
name: implement
description: "Implement one authorized code unit through clean-context execution and coordinator-owned completion."
---

# Implement

Deliver exactly one repository implementation unit. The invoking agent is the coordinator and owns scope, decisions, corrections, verification, integration, and completion.

## 1. Establish one authorized unit

Read the accepted request and its governing sources. Identify the requested behavior, every acceptance criterion, and one execution contract that fits a single implementation unit. If the request combines independent units or a blocked or conflicting set of Tickets, stop before writer dispatch or code and report that one unit must be selected or decomposed.

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

Use `tdd` when the behavior can be exercised at a test seam already confirmed in the request, specification, issue, Ticket, or conversation. Pass that confirmation through without asking the user to reconfirm it. Run typechecking regularly, single test files regularly, and the full test suite once after implementation is complete.

This step is complete when the coordinator has corrected every source-determined divergence and verified the complete unit against every acceptance criterion.

## 4. Integrate and complete

Integrate the verified unit through the repository's required workflow. Commit only when the user explicitly requested a commit or the repository's recorded workflow says this invocation should commit, and use a conventional commit. Independent code review remains outside this direct path.

This step is complete when the coordinator has integrated the verified result, disclosed any isolation limitation, and reported completion, deviations, unexecuted checks, and concerns.
