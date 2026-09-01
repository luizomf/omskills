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
A single tracked implementation unit inside an **Issue tracker**, sized to fit one fresh agent context with room for verification. The final Ticket Issue, including any explicitly incorporated tracker artifact, is the complete recoverable implementation contract for that exact version: it contains or identifies every accepted outcome, scope boundary, required workflow or order, deliverable, acceptance criterion, relation, and completion condition. Conversations, handoffs, and audit transcripts may explain the contract but contain no secret implementation requirement. A Ticket may be a bug, task, issue, investigation, or slice produced by `to-tickets`; it is not an interactive **Question**.
_Avoid_: backlog item, multi-agent implementation plan, interview question

**Scratchpad**:
A temporary, untracked, self-contained continuation record under an ignored `.scratch/` directory. It lets an agent with clean context recover established decisions, unresolved **Questions**, evidence pointers, and the recommended next action, but it is not a **Spec**, **Ticket**, ADR, or permanent documentation and carries no implementation authority.
_Avoid_: spec, ticket, ADR, permanent documentation, implementation plan

**Spec**:
The durable planning authority describing a problem, intended behavior, constraints, and established design guidance. A **Spec** guides code only through smaller **Tickets** and is never itself an implementation unit.
_Avoid_: PRD (use only when quoting external systems that call them PRDs), implementation ticket

**Triage role**:
A canonical category or state label applied to a **Ticket** during triage. Category roles are `bug` and `enhancement`; state roles include `needs-triage` and `ready-for-agent`. Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Prompt Audit**:
A terminal sequential evidence workflow for one exact Ticket contract. The current audit coordinator first fixes the reference intent, then one fresh read-only non-delegating interpreter completes its interpretation, then one fresh independent read-only non-delegating reviewer receives the reference intent and completed interpretation—but no hidden coordinator analysis or desired answer. The coordinator adjudicates that evidence, records exactly `PASS`, `FAIL`, or explicit `BYPASS`, and ends. Prompt Audit never dispatches or implements.
_Avoid_: implementation handoff, parallel audit passes, semantic test suite

**Prompt audit status**:
A durable execution-gate result attached to one exact contract in the **Issue tracker**. `PASS` means no material semantic divergence survived audit-coordinator adjudication and the Ticket fits one fresh agent context; `BYPASS` means a maintainer explicitly waived that audit for the exact contract and is never represented as `PASS`; `FAIL` means the audit did not establish equivalent comprehension or context fit. A current `PASS` or `BYPASS` makes the exact Ticket eligible for autonomous execution. It neither selects the Ticket nor grants **Mission authorization**. A material change to outcome, scope, workflow or order, deliverables, acceptance criteria, relations, or completion makes it stale.

**Mission authorization**:
Explicit user or invoker direction that selects one Ticket or supplies one finite, non-empty, pre-resolved **Mission plan** for autonomous delivery. Readiness and a valid **Prompt audit status** are eligibility gates, not selection. Authorization is non-transitive: findings and newly imagined work outside the selected identities are reported, not converted into implementation.
_Avoid_: ready-work query, discovery request, open-ended mandate

**Mission plan**:
The invoker-supplied execution topology for a Mission: fully qualified unique Ticket identities, ordered sequential phases, declared compatible parallel groups, blockers, and conflicts, all resolved before dispatch. A one-Ticket Mission is a one-item plan. The **Ticket dispatcher** validates and freezes this topology without discovering or semantically scheduling work.
_Avoid_: dispatcher-built queue, dynamic work graph, child-proposed next work

**Mission envelope**:
The authority boundary established by **Mission authorization**: the exact frozen **Mission plan**, scope, deferrals, and completion boundary for one autonomous run. The **Ticket dispatcher** alone owns its compact mechanical routing state and outcomes. Each fresh **Ticket coordinator** receives exactly one Ticket identity and resolves that Ticket's governing sources and live execution gate.
_Avoid_: adjacent-work authorization, child-selected work

**Ticket dispatcher**:
The minimal root policy role implemented by the user-only `dispatch-tickets` skill. It is the only root contract that creates `orchestrate` **Ticket coordinators**. It accepts one explicitly authorized Ticket or **Mission plan**, validates and freezes the supplied topology, and owns only compact mechanical routing state, active coordinator identities and native session references, matching cancellation intent, and **Ticket outcomes**. It starts one fresh coordinator for each identity runnable under the frozen topology; declared compatible groups may run in parallel, while phases, audit passes, and Ticket internals remain sequential. A phase advances only after every identity in its active group returns matching `delivered`; every other or invalid transition stops the Mission. The dispatcher may forward an explicitly targeted instruction literally to one active coordinator, but it cannot add, remove, replace, or reorder work; untargeted conversation remains at the root. It never queries the tracker, discovers or expands work, resolves a query, introduces a resolver role, inspects implementation context, semantically schedules work, or resolves blockers.
_Avoid_: Ticket coordinator, implementation worker, query resolver, semantic supervisor

**One-Ticket convenience entry**:
The user-only `implement` skill. It accepts exactly one explicitly authorized Ticket and, in the same root invocation, composes that identity unchanged as a one-item **Mission plan** through `dispatch-tickets`. It never creates a coordinator, invokes `orchestrate`, or owns implementation, review, or delivery.
_Avoid_: direct implementation path, root coordinator, orchestrate alias

**Ticket coordinator**:
The fresh isolated agent running `orchestrate` for exactly one explicitly authorized Ticket. It validates that Ticket's live execution gate and required repository setup, reads every governing source, owns writer and reviewer delegation, performs surviving corrections and verification, completes delivery and tracker obligations, and returns one compact **Ticket outcome**. Missing required repository setup during a headless Ticket run produces a blocker; the coordinator does not open interactive setup through the dispatcher.
_Avoid_: Ticket dispatcher, sequence owner, leaf writer, leaf reviewer

**Ticket outcome**:
The single-line JSON terminal envelope returned as a **Ticket coordinator**'s final assistant message. Matching `delivered` is the only result that satisfies an identity in the frozen **Mission plan**; `blocked`, `failed`, or `cancelled` stop the Mission. It contains only the Ticket identity, status, an essential durable reference when available, and one short blocker when applicable; detailed evidence remains in the tracker, repository, and coordinator session. A missing, malformed, mismatched, duplicate, truncated, wrong-path, or unexpected outcome fails closed.
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

**Role inheritance**:
The default route for the standard dispatcher, coordinator, writer, and reviewer roles. They inherit the active provider, model, reasoning level, tools, and repository route unless an authorized caller explicitly overrides them. Role names delimit ownership, not intelligence or capability. The managed hierarchy remains dispatcher at depth 1, Ticket coordinator at depth 2, and non-delegating writer and reviewer leaves at depth 3; there is no depth 4.
_Avoid_: reduced-intelligence role, implicit capability downgrade, delegating leaf

**Mission observer**:
An external, bounded observation role with no implementation authority and no ownership of dispatcher or Mission state. It permits at most one payload-free heartbeat at a time and one bounded inspection of visible tmux plus durable repository and tracker evidence. Healthy progress is silent except for scheduling the next single heartbeat. Intervention is limited to concrete failure or blockage, an abandoned human gate, or an invalid or stopped dispatch transition; Mission completion or terminal stop schedules no further heartbeat. It provides no daemon, recurring cron or poller, persistent Mission state, takeover, or survival guarantee.
_Avoid_: monitor daemon, Mission supervisor, dispatcher watchdog

**Workflow evidence policy**:
The rule that phrase, regex, snapshot, injected-wording, and test-only semantic state models do not prove prompt meaning. Tests remain appropriate for real executable code and deterministic mechanical or structural invariants. Prose meaning uses sequential clean-context **Prompt Audit** and bounded real workflow evidence; redundant semantic assertions and frameworks are deleted rather than replaced.
_Avoid_: prompt wording test, regex comprehension proof, duplicate prose implementation

## Relationships

- An **Issue tracker** holds many **Specs** and **Tickets**
- A **Question** is resolved in a live interaction and may inform a later **Scratchpad**, **Spec**, or **Ticket**
- A **Scratchpad** may preserve temporary planning context and be removed after accepted content reaches a durable artifact, but it carries no implementation authority
- A **Spec** is broken down into many **Tickets** and is never implemented directly
- A triaged **Ticket** carries one category **Triage role** and one state **Triage role**
- The final Ticket Issue is the recoverable implementation contract; conversations and audit transcripts carry no hidden authority
- A code or behavior-changing **Ticket** becomes `ready-for-agent` only with a current `PASS` or explicit `BYPASS` **Prompt audit status** for its exact contract
- `ready-for-agent` and a current `PASS` or `BYPASS` make a Ticket eligible; only **Mission authorization** selects it for execution
- **Prompt Audit** gathers interpreter and reviewer evidence sequentially, records its status, and ends without dispatch or implementation
- A **Ticket** may retain multiple historical **Prompt audit statuses**, but only its newest applicable status governs that exact unchanged contract
- Every autonomous one-Ticket or multi-Ticket Mission enters through the **Ticket dispatcher**; the **One-Ticket convenience entry** composes a one-Ticket selection as a one-item frozen **Mission plan** in the same root invocation
- The invoker, not the dispatcher, supplies and authorizes every identity, sequential phase, compatible parallel group, blocker, and conflict before dispatch
- The **Ticket dispatcher** alone starts one fresh `orchestrate` **Ticket coordinator** per runnable identity according to the frozen topology; parallel coordinators exist only in a declared compatible group, and the next phase waits for the active group to be delivered
- Once a Ticket is selected, a current `PASS` or `BYPASS` transfers its in-scope implementation decisions to its **Ticket coordinator** without creating another user decision gate
- A **Ticket coordinator** owns complete delivery of exactly one Ticket through the acyclic `Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator` graph
- Writer and reviewer are fresh, isolated, non-delegating, single-pass leaves; the **Ticket coordinator** adjudicates findings, performs surviving corrections directly, verifies, integrates, and decides the one-Ticket outcome
- Standard dispatcher, coordinator, writer, and reviewer roles follow **Role inheritance** and the depth-1/depth-2/depth-3 hierarchy
- Explicitly targeted steering may reach one active coordinator literally without changing the plan; untargeted conversation remains at the dispatcher root
- Text or documentation work that cannot change behavior does not require a **Prompt audit status**
- The dispatcher does not inspect or mediate missing setup; a headless **Ticket coordinator** returns a blocker when required repository configuration is unavailable
- An interactive dispatcher turn may end after the harness accepts its asynchronous coordinator dispatch as an **Accepted continuation mechanism**; **Mission complete** still requires a matching `delivered` outcome for every selected identity
- A **Mission observer** is separate from implementation and routing, and bounded observation never becomes persistent workflow state or a continuation guarantee
- The **Workflow evidence policy** separates deterministic executable checks from clean-context evidence about prose meaning
- The dispatcher/coordinator managed subagent lineage does not depend on `wormhole` or `tmux-worker`; both remain available as generic optional interactive transports outside that lineage
- `wormhole` transfers an interactive conversation to a fresh context and derives no work or implementation authority from the transfer; its definitive callback remains the source of truth for origin retirement
- A `wormhole` handoff's recorded authorized immediate action, explicit user gate, or absence of authorized action selects the continuation branch
- `tmux-worker` owns only visible tmux transport and lifecycle; its caller owns task meaning, artifacts, completion, post-callback decisions, and whether a turn may end
- A cooperative `tmux-worker` callback is a transport event, not an **Accepted continuation mechanism** by itself, and cannot justify ending an unattended autonomous turn

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "issue" remains acceptable when the underlying tracker calls a work item an issue, but the skill vocabulary now uses **Ticket** for implementation slices and **Spec** for durable planning documents.
- "Router Skill" in skill-authoring guidance names a user-only skill-selection aid, never the canonical **Ticket dispatcher**.
