# Omskills

A curated collection of agent skills for structured Codex and coding-agent workflows. Skills are organized into buckets and consumed by per-repository configuration emitted by `/setup-omskills`.

## Language

**Issue tracker**:
The tool that hosts a repo's specs, tickets, and issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, and `wayfinder` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Question**:
A live prompt asking the user to resolve one decision or ambiguity during an interactive workflow. A **Question** is answered in the conversation and may shape a later **Spec** or **Ticket**; it is not itself tracked implementation work.
_Avoid_: issue, ticket, task

**Ticket**:
A single tracked implementation unit inside an **Issue tracker**, sized to fit one fresh agent context with room for verification. A Ticket may be a bug, task, issue, investigation, or slice produced by `to-tickets`; it is not an interactive **Question**.
_Avoid_: backlog item, multi-agent implementation plan, interview question

**Scratchpad**:
A temporary, untracked, self-contained continuation record under an ignored `.scratch/` directory. It lets an agent with clean context recover established decisions, unresolved **Questions**, evidence pointers, and the recommended next action, but it is not a **Spec**, **Ticket**, ADR, or permanent documentation and carries no implementation authority.
_Avoid_: spec, ticket, ADR, permanent documentation, implementation plan

**Spec**:
The durable planning authority describing a problem, intended behavior, constraints, and established design guidance. A **Spec** guides code only through smaller **Tickets** and is never itself an implementation unit.
_Avoid_: PRD (use only when quoting external systems that call them PRDs), implementation ticket

**Triage role**:
A canonical category or state label applied to a **Ticket** during triage. Category roles are `bug` and `enhancement`; state roles include `needs-triage` and `ready-for-agent`. Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Prompt audit status**:
A durable execution-gate result attached to one exact contract in the **Issue tracker**. `PASS` means no semantic divergence survived audit-coordinator adjudication and the Ticket fits one fresh agent context; `BYPASS` means a maintainer explicitly waived that audit for the exact contract; `FAIL` means the audit did not establish equivalent comprehension or context fit. A current `PASS` or `BYPASS` makes the exact Ticket eligible for autonomous execution. It neither selects the Ticket nor grants **Mission authorization**, and a material contract change makes it stale.

**Mission authorization**:
Explicit user or invoker direction that selects one Ticket or supplies an already-resolved ordered list of Ticket identities for autonomous delivery. Readiness and a valid **Prompt audit status** are eligibility gates, not selection. Authorization is non-transitive: findings and newly imagined work outside the selected identities are reported, not converted into implementation.
_Avoid_: ready-work query, discovery request, open-ended mandate

**Mission envelope**:
The authority boundary established by **Mission authorization**: the exact selected Ticket identities, scope, deferrals, and completion boundary for one autonomous run. For a sequence, the **Ticket dispatcher** alone owns its fixed order and cursor. Each fresh **Ticket coordinator** receives one current Ticket identity and resolves that Ticket's governing sources and live execution gate.
_Avoid_: adjacent-work authorization, child-selected work

**Ticket dispatcher**:
The minimal root policy role for the future user-only `dispatch-tickets` skill. It accepts an explicit, already-resolved ordered Ticket identity list supplied by its user or invoker and alone owns that list, its fixed order, cursor, current coordinator identity, dispatch state, and compact **Ticket outcomes**. It starts one fresh **Ticket coordinator** at a time, may forward a relevant user instruction without interpreting implementation content, and remains the user's responsive control surface while asynchronous work runs. It does not query the tracker, discover work, resolve a query, introduce a resolver role, inspect implementation context, or resolve blockers; its initial contract has no heartbeat, stall diagnosis, retry, or skip.
_Avoid_: Ticket coordinator, implementation worker, query resolver, semantic supervisor

**Ticket coordinator**:
The fresh isolated agent running `orchestrate` for exactly one explicitly authorized Ticket. It validates that Ticket's live execution gate and required repository setup, reads every governing source, owns writer and reviewer delegation, performs surviving corrections and verification, completes delivery and tracker obligations, and returns one compact **Ticket outcome**. Missing required repository setup during a headless Ticket run produces a blocker; the coordinator does not open interactive setup through the dispatcher.
_Avoid_: Ticket dispatcher, sequence owner, leaf writer, leaf reviewer

**Ticket outcome**:
The single-line JSON terminal envelope returned as a **Ticket coordinator**'s final assistant message. `delivered` allows the dispatcher to advance its cursor; `blocked`, `failed`, or `cancelled` stops the sequence. It contains only the Ticket identity, status, an essential durable reference when available, and one short blocker when applicable; detailed evidence remains in the tracker, repository, and coordinator session. A missing, malformed, or mismatched outcome fails closed.
_Avoid_: implementation report, review summary, diff, handoff transcript

**Mission complete**:
The terminal state in which every Ticket selected by the **Mission authorization** is delivered and the Mission's completion boundary is satisfied. It describes the global mission, not merely the current agent turn or one dispatched worker.
_Avoid_: turn complete, worker accepted, work started

**Safe turn boundary**:
A state in which the current agent turn may end without abandoning authorized work. It exists only after **Mission complete**, at a genuine blocker, at an explicit user gate, or under an **Accepted continuation mechanism**.
_Avoid_: work started, context restored, intent stated

**Accepted continuation mechanism**:
An acknowledged asynchronous operation whose harness-owned lifecycle documents automatic completion delivery or an owning-session reentry attempt without requiring a delegated agent to understand and execute a separate callback instruction. This contract does not claim that a process, host, network, or owning session cannot fail. A cooperative textual callback or a background process with no automatic return path does not qualify by itself.
_Avoid_: guaranteed wake, worker promise, background activity

## Relationships

- An **Issue tracker** holds many **Specs** and **Tickets**
- A **Question** is resolved in a live interaction and may inform a later **Scratchpad**, **Spec**, or **Ticket**
- A **Scratchpad** may preserve temporary planning context and be removed after accepted content reaches a durable artifact, but it carries no implementation authority
- A **Spec** is broken down into many **Tickets** and is never implemented directly
- A triaged **Ticket** carries one category **Triage role** and one state **Triage role**
- A code or behavior-changing **Ticket** becomes `ready-for-agent` only with a current `PASS` or explicit `BYPASS` **Prompt audit status**
- `ready-for-agent` and a current `PASS` or `BYPASS` make a Ticket eligible; only **Mission authorization** selects it for execution
- Once a Ticket is selected, a current `PASS` or `BYPASS` transfers its in-scope implementation decisions to the **Ticket coordinator** without creating another user decision gate
- Text or documentation work that cannot change behavior does not require a **Prompt audit status**
- A **Ticket** may retain multiple historical **Prompt audit statuses**, but only its newest applicable status governs that exact contract
- The **Ticket dispatcher** is the only sequence owner: it receives the already-resolved ordered identity list, advances its cursor only after a matching `delivered` **Ticket outcome**, and never accepts child-selected `next` work
- A **Ticket coordinator** owns complete delivery of one Ticket through the acyclic `Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator` graph
- Writer and reviewer are fresh, isolated, single-pass leaves; the **Ticket coordinator** adjudicates findings, performs surviving corrections directly, verifies, integrates, and decides the one-Ticket outcome
- The dispatcher does not inspect or mediate missing setup; a headless **Ticket coordinator** returns a blocker when required repository configuration is unavailable
- An interactive dispatcher turn may end after the harness accepts its asynchronous coordinator dispatch as an **Accepted continuation mechanism**; **Mission complete** still requires a matching `delivered` outcome for every selected identity
- The dispatcher/coordinator managed subagent lineage does not depend on `wormhole` or `tmux-worker`; both remain available as generic optional interactive transports outside that lineage
- `wormhole` transfers an interactive conversation to a fresh context and derives no work or implementation authority from the transfer; its definitive callback remains the source of truth for origin retirement
- A `wormhole` handoff's recorded authorized immediate action, explicit user gate, or absence of authorized action selects the continuation branch
- `tmux-worker` owns only visible tmux transport and lifecycle; its caller owns task meaning, artifacts, completion, post-callback decisions, and whether a turn may end
- A cooperative `tmux-worker` callback is a transport event, not an **Accepted continuation mechanism** by itself, and cannot justify ending an unattended autonomous turn
- The serialized detailed rewrite of `orchestrate` remains owned by Ticket #40. Until that rewrite, its queue, `next`, handoff, `wormhole`, watchdog, retry, and skip clauses are deferred execution text rather than this migrated governing architecture

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "issue" remains acceptable when the underlying tracker calls a work item an issue, but the skill vocabulary now uses **Ticket** for implementation slices and **Spec** for durable planning documents.
- "Router Skill" in skill-authoring guidance names a user-only skill-selection aid, never the canonical **Ticket dispatcher**.
