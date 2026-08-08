# Omskills

A curated collection of agent skills for structured Codex and coding-agent workflows. Skills are organized into buckets and consumed by per-repository configuration emitted by `/setup-omskills`.

## Language

**Issue tracker**:
The tool that hosts a repo's specs, tickets, and issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, and `wayfinder` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Ticket**:
A single tracked implementation unit inside an **Issue tracker**, sized to fit one fresh agent context with room for verification. A Ticket may be a bug, task, issue, investigation, or slice produced by `to-tickets`.
_Avoid_: backlog item, multi-agent implementation plan

**Spec**:
The durable planning authority describing a problem, intended behavior, constraints, and established design guidance. A **Spec** guides code only through smaller **Tickets** and is never itself an implementation unit.
_Avoid_: PRD (use only when quoting external systems that call them PRDs), implementation ticket

**Triage role**:
A canonical category or state label applied to a **Ticket** during triage. Category roles are `bug` and `enhancement`; state roles include `needs-triage` and `ready-for-agent`. Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Prompt audit status**:
A durable result attached to one exact execution contract in the **Issue tracker**. `PASS` means no semantic divergence survived audit-coordinator adjudication and the Ticket fits one fresh agent context; `BYPASS` means a maintainer explicitly authorized autonomous delivery without a pass; `FAIL` means the audit did not establish equivalent comprehension or context fit. A current `PASS` or `BYPASS` authorizes autonomous implementation of that contract only. A material contract change makes its prior status stale.

**Mission envelope**:
The exact authorized Ticket identities, governing Specs, scope, deferrals, frozen queue, and completion boundary for one autonomous run. If authorization names a query or queue source, its current Ticket identities are resolved once when the run starts and then frozen. Authorization is non-transitive: findings and newly imagined work outside the envelope are reported, not converted into implementation.
_Avoid_: open-ended mandate, adjacent-work authorization

## Relationships

- An **Issue tracker** holds many **Specs** and **Tickets**
- A **Spec** is broken down into many **Tickets** and is never implemented directly
- A triaged **Ticket** carries one category **Triage role** and one state **Triage role**
- A code or behavior-changing **Ticket** becomes `ready-for-agent` only with a current `PASS` or explicit `BYPASS` **Prompt audit status**
- A current `PASS` or `BYPASS` transfers in-scope implementation decisions to the autonomous coordinator; it does not create another user decision gate
- Text or documentation work that cannot change behavior does not require a **Prompt audit status**
- A **Ticket** may retain multiple historical **Prompt audit statuses**, but only its newest applicable status governs that exact contract
- `orchestrate` accepts only Tickets inside the fixed **Mission envelope** with a current `PASS` or `BYPASS`

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "issue" remains acceptable when the underlying tracker calls a work item an issue, but the skill vocabulary now uses **Ticket** for implementation slices and **Spec** for durable planning documents.
