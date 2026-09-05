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

**Governing authority**:
An accepted durable source that constrains behavior, including Specs, ADRs, workflow and security documentation, and other domain contracts. Authority and impact—not file extension—determine whether a change is behavioral and requires independent review.
_Avoid_: editorial-only documentation, optional background, code-only authority

**Triage role**:
A canonical category or state label applied to a **Ticket** during triage. Category roles are `bug` and `enhancement`; state roles include `needs-triage` and `ready-for-agent`. Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Prompt Audit**:
A terminal sequential evidence workflow for one exact Ticket contract. The current audit coordinator first fixes the reference intent, then one fresh read-only non-delegating interpreter completes its interpretation, then one fresh independent read-only non-delegating reviewer receives the reference intent and completed interpretation—but no hidden coordinator analysis or desired answer. The coordinator adjudicates that evidence, records exactly `PASS`, `FAIL`, or explicit `BYPASS`, and ends. Prompt Audit never dispatches or implements.
_Avoid_: implementation handoff, parallel audit passes, semantic test suite

**Prompt audit status**:
A durable execution-gate result attached to one exact contract in the **Issue tracker**. `PASS` means no material semantic divergence survived audit-coordinator adjudication and the Ticket fits one fresh agent context; `BYPASS` means a maintainer explicitly waived that audit for the exact contract and is never represented as `PASS`; `FAIL` means the audit did not establish equivalent comprehension or context fit. A current `PASS` or `BYPASS` makes the exact Ticket eligible for Unattended execution. It neither selects the Ticket nor grants **Mission authorization**. Prompt Audit is not applicable to Assisted work by default, but the maintainer may request it for complex intent. A material change to outcome, scope, workflow or order, deliverables, acceptance criteria, relations, or completion makes it stale.

**Delivery topology**:
The routing dimension resolved before the first implementation mutation. **Direct delivery** keeps one responsible conversational agent in end-to-end ownership. **Mission topology** coordinates multiple selected **Tickets** or work with real dependency, conflict, integration, shared-resource, or multiple-writer coordination. Topology is independent of **Maintainer availability**; several edits in one request do not become several Tickets merely because they touch several files.
_Avoid_: autonomy level, fixed mode matrix, agent-count preference

**Direct delivery**:
The topology for an untracked request or exactly one selected **Ticket** when no real coordination requires a **Mission**. In Assisted work, the responsible agent owns investigation, implementation, verification, review adjudication, corrections, and delivery; the confirmed conversation is the active contract. Durable tracking is required when that contract must survive the conversation or materially changes existing **Governing authority**. The agent may use bounded non-delegating research or investigation with narrow questions and compact evidence, but retains decisions and implementation.
_Avoid_: unreviewed work, implicit multi-writer coordination, mandatory dispatcher route

**Maintainer availability**:
The delivery dimension that records whether the maintainer remains available for ordinary implementation **Questions**. **Assisted** means available; **Unattended** means execution must continue as an **Unattended Mission** within durable pre-resolved authority or stop at a genuine blocker. Availability is independent of **Delivery topology**, but changing one Direct Assisted item to Unattended establishes a one-Ticket Mission rather than an unattended direct path. Silence never changes availability.
_Avoid_: direct versus Mission topology, inferred absence, fixed mode matrix

**Unattended Mission**:
A **Mission**, including a one-Ticket Mission created when Direct Assisted work changes availability, explicitly authorized to continue without the maintainer participating in ordinary implementation decisions. Its durable Ticket contracts, resolved relations, execution gates, and stopping conditions must support safe progress while the maintainer is absent.
_Avoid_: Assisted work, unattended direct delivery, every Mission

**Delivery mode gate**:
The adaptive gate before the first implementation mutation. Read-only inspection, investigation, and reproduction may precede it. The responsible agent asks only for a topology or availability dimension that remains materially unresolved; an explicit semantic choice satisfies that dimension without magic wording, caller ancestry, role labels, or redundant confirmation.
_Avoid_: fixed questionnaire, provenance check, post-mutation confirmation

**Mission authorization**:
Explicit user or invoker direction that selects one Ticket or supplies one finite, non-empty, pre-resolved **Mission plan**. It is required for an **Unattended Mission** and authorizes execution there without ordinary interactive decisions; when Mission topology is used, it supplies the plan regardless of maintainer availability. Readiness and a valid **Prompt audit status** are eligibility gates, not selection. Authorization is non-transitive: findings and newly imagined work outside the selected identities are reported, not converted into implementation.
_Avoid_: ready-work query, discovery request, open-ended mandate

**Mission plan**:
The invoker-supplied execution topology for a Mission: fully qualified unique Ticket identities, ordered sequential phases, declared compatible parallel groups, blockers, and conflicts, all resolved before dispatch. A one-Ticket Mission is a one-item plan. The **Ticket dispatcher** validates and freezes this topology without discovering or semantically scheduling work.
_Avoid_: dispatcher-built queue, dynamic work graph, child-proposed next work

**Mission envelope**:
The authority boundary established by **Mission authorization**: the exact frozen **Mission plan**, scope, deferrals, and completion boundary for one coordinated run. When used, the **Ticket dispatcher** alone owns its compact mechanical routing state and outcomes. Each fresh **Ticket coordinator** receives exactly one Ticket identity and resolves that Ticket's governing sources and applicable live execution gate.
_Avoid_: adjacent-work authorization, child-selected work

**Ticket dispatcher**:
The minimal root policy role implemented by the user-only `dispatch-tickets` skill. It provides thin mechanical dispatch for long finite multi-Ticket Missions, without being the exclusive caller of `orchestrate` **Ticket coordinators**. It accepts one explicitly authorized **Mission plan**, validates and freezes the supplied topology, and owns only compact mechanical routing state, active coordinator identities and native session references, matching cancellation intent, and **Ticket outcomes**. It starts one fresh coordinator for each identity runnable under the frozen topology; declared compatible groups may run in parallel, while phases, audit passes, and Ticket internals remain sequential. A phase advances only after every identity in its active group returns matching `delivered`; every other or invalid transition stops the Mission. The dispatcher may forward an explicitly targeted instruction literally to one active coordinator, but it cannot add, remove, replace, or reorder work; untargeted conversation remains at the root. It never queries the tracker, discovers or expands work, resolves a query, introduces a resolver role, inspects implementation context, semantically schedules work, or resolves blockers.
_Avoid_: Ticket coordinator, implementation worker, query resolver, semantic supervisor

**One-Ticket convenience entry**:
The user-only `implement` skill. It accepts exactly one explicitly authorized Ticket and, in the same root invocation, composes that identity unchanged as a one-item **Mission plan** through `dispatch-tickets`. It never creates a coordinator, invokes `orchestrate`, or owns implementation, review, or delivery.
_Avoid_: same-context implementation by `implement`, root coordinator, orchestrate alias

**Ticket coordinator**:
The fresh isolated agent running `orchestrate` for exactly one explicitly authorized Ticket in the managed Mission route. A human/invoker or context-rich parent may dispatch it directly for smaller work. It validates the selected Ticket's explicit authorization, live execution gate when applicable, scope, required repository setup and actual execution capabilities, not its parent's role or provenance; it neither inspects ancestors nor rejects a `role=user` prompt or missing dispatcher/depth assertion. It reads every governing source, owns writer and reviewer delegation, performs surviving corrections and verification, completes delivery and tracker obligations, and returns one compact **Ticket outcome**. Missing required repository setup during a headless Ticket run produces a blocker; the coordinator does not open interactive setup through the dispatcher.
_Avoid_: Ticket dispatcher, sequence owner, leaf writer, leaf reviewer

**Ticket outcome**:
The single-line JSON terminal envelope returned as a **Ticket coordinator**'s final assistant message. Matching `delivered` is the only result that satisfies the selected Ticket and, in Mission topology, its identity in the frozen **Mission plan**; `blocked`, `failed`, or `cancelled` stop that delivery. It contains only the Ticket identity, status, an essential durable reference when available, and one short blocker when applicable; detailed evidence remains in the tracker, repository, and coordinator session. A missing, malformed, mismatched, duplicate, truncated, wrong-path, or unexpected outcome fails closed.
_Avoid_: implementation report, review summary, diff, handoff transcript

**Mission complete**:
The terminal state in Mission topology in which every Ticket selected by the **Mission authorization** is delivered and the Mission's completion boundary is satisfied. It describes the global Mission, not merely the current agent turn or one dispatched worker.
_Avoid_: turn complete, worker accepted, work started

**Safe turn boundary**:
A state in which the current agent turn may end without abandoning authorized work. It exists only after Direct delivery or the Mission is complete, at a genuine blocker, at an explicit user gate, or under an **Accepted continuation mechanism**.
_Avoid_: work started, context restored, intent stated

**Accepted continuation mechanism**:
An acknowledged asynchronous operation whose harness-owned lifecycle documents automatic completion delivery or an owning-session reentry attempt without requiring a delegated agent to understand and execute a separate callback instruction. This contract does not claim that a process, host, network, or owning session cannot fail. A cooperative textual callback or a background process with no automatic return path does not qualify by itself.
_Avoid_: guaranteed wake, worker promise, background activity

**Role inheritance**:
The default route for the standard dispatcher, coordinator, writer, and reviewer roles. They inherit the active provider, model, reasoning level, tools, and repository route unless an authorized caller explicitly overrides them. Role names delimit ownership, not intelligence or capability. The standard managed hierarchy is caller (dispatcher when used) at depth 1, Ticket coordinator at depth 2, and non-delegating writer and reviewer leaves at depth 3; there is no depth 4. Actual tool capabilities and depth/child ceilings are harness-enforced, never established or overridden by role or depth assertions.
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
- A request to work through a wayfinder map authorizes selecting and resolving one in-scope investigation per session without reconfirming established steps. Destination implementation still requires the normal Ticket delivery gates and explicit Mission authorization; map Notes do not bypass them.
- All `.scratch/` artifacts remain local and Git-ignored, with filenames and subdirectories chosen for the work. Prefer the project's durable Issue tracker for project-relevant requirements, decisions, and delivery history. In a local Markdown tracker, triage `Status` and investigation `Lifecycle` are separate fields.
- A **Scratchpad** may preserve temporary planning context and be removed after accepted content reaches a durable artifact, but it carries no implementation authority
- A **Spec** is broken down into many **Tickets** and is never implemented directly
- A triaged **Ticket** carries one category **Triage role** and one state **Triage role**
- The final Ticket Issue is the recoverable implementation contract; conversations and audit transcripts carry no hidden authority
- **Delivery topology** and **Maintainer availability** are resolved independently at the adaptive **Delivery mode gate**, without a fixed matrix or fixed questionnaire
- Direct Assisted work may use an untracked request or exactly one selected **Ticket**; its confirmed conversation is the active contract, with no Ticket, Agent Brief, readiness state, or Prompt Audit required by default unless the contract must survive the conversation
- Direct Assisted work that materially changes existing **Governing authority** updates the applicable Ticket, **Spec**, ADR, workflow, security, or other durable source before delivery
- More than one selected Ticket, or real dependency, conflict, integration, shared-resource, or multiple-writer coordination, requires **Mission topology**
- A code or behavior-changing **Ticket** becomes `ready-for-agent` for Unattended execution only with a current `PASS` or explicit `BYPASS` **Prompt audit status** for its exact contract
- `ready-for-agent` and a current `PASS` or `BYPASS` make a Ticket eligible for Unattended execution; only **Mission authorization** selects it
- **Prompt Audit** is optional on request for Assisted work and remains mandatory for Unattended execution; it gathers interpreter and reviewer evidence sequentially, records its status, and ends without dispatch or implementation
- A **Ticket** may retain multiple historical **Prompt audit statuses**, but only its newest applicable status governs that exact unchanged contract
- A human/invoker or context-rich parent may dispatch one fresh **Ticket coordinator** directly for smaller work; the **Ticket dispatcher** remains the thin route for long finite multi-Ticket Missions, with its mechanical authority boundaries unchanged when used
- The **One-Ticket convenience entry** retains its composition of a one-Ticket selection as a one-item frozen **Mission plan** through the dispatcher in the same root invocation
- The invoker, not the dispatcher, supplies and authorizes every identity, sequential phase, compatible parallel group, blocker, and conflict before dispatch
- Ticket breakdown approval includes complete relations, sequential phases and explicitly compatible parallel groups, accounting for shared resources outside Git. When independence is not established, planning proposes serial work; dispatch never silently serializes an authorized group.
- Every implementation Ticket handled by a **Ticket coordinator**, including one-item and integration Tickets, owns an exclusive worktree and branch established after preflight and before its writer. All candidate work, review, corrections and checks share that path, branch and fixed base, with exact writer, review and final commits.
- Parallel members deliver verified, committed, pushed branch artifacts, not implicit merges to the shared target. Each group has a preplanned ordinary integration Ticket blocked by every member; it identifies predecessors, intended base/target and combination requirements. Other Tickets explicitly state their normal integration target.
- Integration coordinators verify every predecessor's durable tracker evidence, repository/remote branch reference and exact full commit before combining those results in their own candidate. Combined-state review, verification and durable input-to-result evidence precede dependent work.
- Coordinators own candidate disposition. Branch artifacts and recoverable work remain until delivery and all integration consumers no longer need them; cleanup covers only positively identified, safe, no-longer-needed Ticket resources. Unrelated, failed, cancelled, dirty and unintegrated work stays recoverable, with retention reasons recorded.
- An N-member parallel group requires affirmative evidence of the active harness's root concurrency bound and same-batch start support in the current delivery mode. Child-only ceilings do not prove root capacity; unknown or exceeded capacity rejects before any Ticket starts, without splitting, serialization, retries or runtime changes.
- When used, the **Ticket dispatcher** starts one fresh `orchestrate` **Ticket coordinator** per runnable identity according to the frozen topology; parallel coordinators exist only in a declared compatible group, and the next phase waits for the active group to be delivered
- Once a Ticket is selected for Unattended execution, a current `PASS` or `BYPASS` transfers its in-scope implementation decisions to its **Ticket coordinator** without creating another user decision gate
- A **Ticket coordinator** owns complete delivery of exactly one Ticket through the acyclic `Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator` graph
- Writer and reviewer are fresh, isolated, non-delegating, single-pass leaves; the **Ticket coordinator** adjudicates findings, performs surviving corrections directly, verifies, integrates, and decides the one-Ticket outcome
- Standard caller, coordinator, writer, and reviewer roles follow **Role inheritance** and actual harness capability/depth ceilings; direct caller authority does not permit same-context implementation in the managed route, work discovery/substitution, or delegating leaves
- In Direct Assisted work, the responsible conversational agent may implement in its current context; bounded investigation leaves do not share implementation ownership
- Independent Assisted investigations should use available parallel capacity together when independence and capacity are established; routine local inspection stays local when delegation would cost more context than it saves
- Assisted code or behavior changes and changes to Specs, ADRs, workflow, security, or other governing authority receive one fresh independent review. Purely editorial documentation may be self-reviewed. Review receives the concise current contract, governing sources, complete candidate, and verification instructions; material corrections require re-review
- Explicitly targeted steering may reach one active coordinator literally without changing the plan; untargeted conversation remains at the dispatcher root
- Text or documentation work that cannot change behavior does not require a **Prompt audit status**
- Moving from Direct Assisted work to Unattended establishes a one-Ticket **Unattended Mission** and requires a new explicit gate: preserve recoverable current state, establish durable current contracts and resolved relations, obtain a current `PASS` or explicit `BYPASS`, and receive explicit **Mission authorization**. Silence never authorizes the transition
- Once an **Unattended Mission** starts, it completes within the durable contract or stops at a genuine blocker rather than opening ordinary interactive Questions
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
