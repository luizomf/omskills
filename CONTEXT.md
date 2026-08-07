# Omskills

A curated collection of agent skills for structured Codex and coding-agent workflows. Skills are organized into buckets and consumed by per-repository configuration emitted by `/setup-omskills`.

## Language

**Issue tracker**:
The tool that hosts a repo's specs, tickets, and issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, and `wayfinder` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Ticket**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, issue, investigation, or slice produced by `to-tickets`.
_Avoid_: backlog item

**Spec**:
A durable planning document describing a problem and its solution, published to the **Issue tracker** by `to-spec`. A **Spec** is broken down into **Tickets**.
_Avoid_: PRD (use only when quoting external systems that call them PRDs)

**Triage role**:
A canonical category or state label applied to a **Ticket** during triage. Category roles are `bug` and `enhancement`; state roles include `needs-triage` and `ready-for-agent`. Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Execution contract**:
An accepted prompt or authoritative artifact that may authorize autonomous work, including writer dispatch or repository code.

**Prompt audit status**:
A result recorded for an **Execution contract**, durably in the **Issue tracker** when the contract is tracked. `PASS` means no semantic divergence survived audit-coordinator adjudication and any repository implementation unit satisfied the applicable tracer-bullet fit check; `BYPASS` means a maintainer explicitly authorized autonomous delivery without a pass; `FAIL` means the audit did not establish equivalent clean-context comprehension or implementation-unit fit. A status becomes stale after a material change to the requested outcome, scope, required workflow, deliverables, acceptance criteria, or completion point.

## Relationships

- An **Issue tracker** holds many **Specs** and **Tickets**
- A **Spec** is broken down into many **Tickets**
- A triaged **Ticket** carries one category **Triage role** and one state **Triage role**
- A **Ticket** may retain multiple historical **Prompt audit statuses**, but only its newest applicable status governs autonomous delivery
- An **Execution contract** may authorize writer dispatch or code only with a current `PASS` or explicit maintainer-authorized `BYPASS` **Prompt audit status**
- A missing, stale, or `FAIL` **Prompt audit status** stops the execution contract before writer dispatch or code
- The fixed interpreter, reviewer, and confirmation prompts inside the prompt-audit protocol are read-only protocol mechanics and do not recursively require a **Prompt audit status**

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "issue" remains acceptable when the underlying tracker calls a work item an issue, but the skill vocabulary now uses **Ticket** for implementation slices and **Spec** for durable planning documents.
