# Omskills

A personal collection of agent skills adapted for the maintainer's Codex workflow. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-omskills`.

## Language

**Issue tracker**:
The tool that hosts a repo's specs, tickets, and issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-spec`, `to-tickets`, `triage`, `code-review`, and `wayfinder` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Ticket**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, issue, investigation, or slice produced by `to-tickets`.
_Avoid_: backlog item

**Spec**:
A durable planning document describing a problem and its solution, published to the **Issue tracker** by `to-spec`. A **Spec** is broken down into **Tickets**.
_Avoid_: PRD (use only when quoting external systems that call them PRDs)

**Triage role**:
A canonical state-machine label applied to a **Ticket** during triage (e.g. `needs-triage`, `ready-for-agent`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

## Relationships

- An **Issue tracker** holds many **Specs** and **Tickets**
- A **Spec** is broken down into many **Tickets**
- A **Ticket** carries one **Triage role** at a time

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "issue" remains acceptable when the underlying tracker calls a work item an issue, but the skill vocabulary now uses **Ticket** for implementation slices and **Spec** for durable planning documents.
