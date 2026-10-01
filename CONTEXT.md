# Omskills

A curated collection of agent skills for structured coding-agent workflows.
Skills are organized into buckets and consumed by per-repository configuration
emitted by `/setup-omskills`.

## Language

**Issue tracker**: The tool that hosts a repository's Specs, Tickets, and
issues: GitHub Issues, Linear, a local `.scratch/` Markdown convention, or
similar. Tracker-backed skills use its configured operations and identities.
_Avoid_: backlog manager, backlog backend, issue host

**Question**: A live prompt asking the user to resolve one decision or
ambiguity. Its answer may shape a Spec or Ticket; it is not tracked
implementation work. _Avoid_: issue, ticket, task

**Ticket**: A single tracked implementation unit sized to fit one responsible
agent context with room for verification. The final Ticket Issue, including
explicitly incorporated tracker artifacts, is the complete recoverable contract
for that version: outcomes, scope, required workflow/order, deliverables,
acceptance criteria, relations, and completion conditions. Conversations,
handoffs, and audit transcripts carry no hidden implementation requirements. A
Ticket may be a bug, task, investigation, or slice produced by `to-tickets`.
_Avoid_: interactive Question, Spec

**Scratchpad**: A temporary, untracked continuation record under an ignored
`.scratch/` directory. It preserves established decisions, unresolved Questions,
evidence pointers, and the next action. It carries no implementation authority;
durable requirements and delivery history belong in the configured tracker.
_Avoid_: Spec, Ticket, ADR, permanent documentation

**Spec**: Durable planning authority describing the problem, intended behavior,
constraints, and established design guidance. A Spec guides implementation
through smaller Tickets rather than serving as one implementation unit. _Avoid_:
PRD except when quoting an external system, implementation Ticket

**Governing authority**: An accepted durable source constraining behavior,
including Specs, ADRs, workflow/security documentation, and domain contracts.
Authority and impact determine whether a document change is behavioral and needs
independent review. _Avoid_: code-only authority, optional background

**Triage role**: A canonical category or state label. Categories are `bug` and
`enhancement`; states include `needs-triage` and `ready-for-agent`. The
configured mapping in `docs/agents/triage-labels.md` identifies actual tracker
strings.

**Prompt Audit**: A terminal sequential evidence workflow for one exact
contract. The audit coordinator fixes reference intent; a fresh read-only
non-delegating interpreter reconstructs the contract; then a fresh independent
read-only non-delegating reviewer compares that interpretation with the
reference intent, without hidden coordinator analysis or a desired answer. The
coordinator adjudicates and records `PASS`, `FAIL`, or explicit `BYPASS`.
Authorized recovery may replace a mechanically settled but incomplete pass
before status recording, preserving the fixed contract and failed-attempt
evidence. The audit context never implements or corrects the audited work.
Audit-only requests end after status/readiness recording; combined
audit-and-implement authorization continues in a fresh implementation context.
_Avoid_: implementation handoff, parallel audit passes, semantic test suite

**Prompt audit status**: A durable gate attached to one exact contract. `PASS`
establishes equivalent comprehension after adjudication and one-context Ticket
fit. `BYPASS` records an explicit maintainer waiver, not a successful audit.
`FAIL` means comprehension or fit was not established. A current `PASS` or
explicit `BYPASS` promotes a complete tracked implementation Ticket to
`ready-for-agent`, preserving one category and one state role, regardless of
availability. It establishes eligibility, not work selection. Audits are
required when requested or imposed by the accepted repository/task contract, not
automatically by maintainer absence. A material change to outcome, scope,
workflow/order, deliverables, acceptance criteria, relations, or completion
makes the prior status stale; remove failed or stale readiness. The Ticket body
may contain the whole contract without a separate brief.

**Delivery topology**: The organization of responsibility resolved before
implementation. Direct delivery keeps one conversational agent in end-to-end
ownership, whether the maintainer is present or away. Mission topology
coordinates multiple selected Tickets and their dependency, conflict,
integration, shared-resource, or multiple-owner needs. Several edits do not
become multiple Tickets merely because they touch several files. _Avoid_:
autonomy level, fixed mode matrix

**Direct delivery**: The route for an untracked request or one selected Ticket
in the current conversation. The responsible agent owns investigation,
implementation, review adjudication, corrections, verification, and delivery
through the authorized stopping point, whether Assisted or Unattended. The
accepted conversation is its active contract. Durable tracking is needed when
the contract must survive the conversation or materially changes governing
authority. Bounded research/design assistance can support the owner without
transferring implementation responsibility. _Avoid_: unreviewed work, mandatory
dispatcher route

**Maintainer availability**: Whether the maintainer remains available for
ordinary implementation Questions. `Assisted` means available. `Unattended`
means the user has authorized continuation while away, with a stated stopping
point and established decisions. Preserve the context needed to continue and
report genuinely unresolved blockers. Availability changes neither ownership nor
topology and adds no automatic audit or approval gate. Silence does not change
availability. _Avoid_: inferred absence, one-Ticket Mission transition

**Unattended Mission**: A multi-Ticket Mission authorized to continue while the
maintainer is away. Ticket contracts, dependencies, established decisions, and
the agreed stopping point support progress. Apply readiness/audit gates only
when the task or repository requires them. A local blocker can coexist with
eligible independent work. _Avoid_: every Mission, every unattended request

**Delivery mode gate**: Resolve materially missing topology or availability
before the first implementation mutation. Read-only investigation and
reproduction may precede it. Accepted semantic choices satisfy the gate without
a fixed questionnaire or redundant confirmation. _Avoid_: magic phrase,
caller-provenance check

**Mission authorization**: Accepted user or invoker direction selecting a finite
queue of Tickets and its scope, constraints, availability, and completion
boundary. It supplies authority to execute selected work; readiness and audit
status supply eligibility. Findings and dependency references outside that queue
do not become selected work. _Avoid_: ready-work query, discovery request,
open-ended mandate

**Mission plan**: The selected finite queue with unambiguous tracker/repository
identities, priority order, required sequence or phase barriers,
blocking/conflict relations, and delivery boundaries. Prose, lists, or existing
phased JSON can express it. Planning decides what can safely run in parallel to
save time and records that decision with the Ticket relations and delivery
boundaries. The dispatcher follows the plan, checks live prerequisites and
capacity, and starts eligible work within those constraints. _Avoid_: mandatory
JSON schema, frozen cursor, open-ended discovery

**Mission envelope**: The scope established by Mission authorization: selected
Tickets, accepted requirements, deferrals, ordering constraints, and completion
boundary. User direction may revise it. The dispatcher manages continuity inside
it; each Ticket owner manages one Ticket's technical work. _Avoid_:
adjacent-work authorization, child-selected scope

**Ticket dispatcher**: The Mission continuity role implemented by
agent-discoverable `dispatch-tickets`. It reads tracker/repository evidence,
maintains the multi-Ticket queue and owner references, tracks elapsed time and
observed progress, starts or resumes eligible owners, routes user decisions,
recovers concrete failures within authority, and verifies delivery. It preserves
blocked work while advancing proven-independent selected Tickets when required
order permits. It leaves implementation and code review with each Ticket owner
and reviewer. Its state can live in the conversation or an ignored Markdown
note; existing tools provide transport and optional reminders. _Avoid_:
implementation worker, code reviewer, runtime supervisor service

**One-Ticket convenience entry**: The user-only `implement` skill, which loads
`orchestrate` in the current conversation for one selected Ticket. It creates no
new coordinator or dispatcher. Multiple selected Tickets use `dispatch-tickets`.
_Avoid_: one-item dispatcher queue, second implementation owner

**Ticket owner**: The technical responsible agent running `orchestrate` for one
selected Ticket, formerly called the Ticket coordinator. `orchestrate` is the
current owner's delivery procedure, not a request to launch another agent; it
also supports an untracked bounded request. The same conversation investigates,
reproduces, implements, tests, obtains independent review, adjudicates findings,
corrects, and delivers. It checks live authority/gates and actual capabilities,
owns an exclusive candidate, and preserves context across blockers. New
dispatched Tickets receive fresh owners; existing work prefers its current
owner. Direct invocation is supported. A Prompt Audit context hands
implementation to a fresh owner. _Avoid_: separate default writer, Mission
dispatcher, review leaf

**Ticket outcome**: The owner's concise result through the agreed channel:
Ticket identity, status, delivery evidence, and any blocker or next action.
`delivered` means the declared boundary and obligations are verified; `blocked`
identifies missing authority/prerequisites; `failed` identifies an incomplete
operational attempt; `cancelled` identifies an explicit safe stop. Publication
may have succeeded while other obligations remain. JSON is optional. The
dispatcher verifies evidence instead of treating a status string as proof.
_Avoid_: delivery by declaration, partial review as completed review

**Mission complete**: Every currently selected Ticket and the overall completion
boundary have verified delivery. Accepted launches, completed turns, and branch
artifacts awaiting required integration do not by themselves establish Mission
completion. _Avoid_: worker accepted, work started, turn complete

**Safe turn boundary**: A completed assignment, genuine blocker, explicit user
gate, or Accepted continuation mechanism. State which applies when releasing an
unfinished autonomous turn. _Avoid_: intent stated, background activity alone

**Accepted continuation mechanism**: An acknowledged asynchronous operation
whose harness documents automatic completion delivery or owning-session reentry.
Managed completion or an accepted scheduler reminder may qualify under their own
contracts. A cooperative tmux callback or status-line notice alone does not. No
mechanism guarantees survival of the host, network, or owning session. _Avoid_:
guaranteed wake, worker promise

**Role inheritance**: Delegations inherit the harness's tools, repository route,
and model/reasoning defaults unless an authorized supported override applies.
The caller uses `model-routing` for model-selectable work. Roles identify
responsibility; actual tool, depth, and child limits come from the harness. A
fresh reviewer remains independent and non-delegating; the Ticket owner retains
implementation and may use bounded assistance within its task. _Avoid_: role
labels as capability grants, implicit model authorization

**Skill composition**: Reading a skill or reference through a direct relative
pointer from the referring file's physical directory, following symlinks before
parent traversal. Check the target even when hidden from discovery; pass
resolved paths to fresh agents. Composition grants neither execution nor
model-selection authority. _Avoid_: workspace-relative link, hidden means
uninstalled

**Model routing**: Caller-owned selection for a future delegation through
`model-routing`. Explicit user choices take precedence; authorized task-based
policy considers uncertainty, impact, and verification, with inheritance as
fallback. Ticket ownership includes implementation and adjudication; Mission
continuity includes operational decisions, so neither is classified solely by a
thin-dispatch label. The maintained table is a candidate catalog, not measured
parity or guaranteed availability. _Avoid_: automatic provider switching, model
names as workflow roles

**Maintainer intervention**: User direction can revise scope, instructions,
review limits, routing, recovery, or the plan. Apply clear decisions without
repeated approval. Update durable contracts and applicable gates for material
changes; pause affected starts and settle ownership before
replacement/conflicting work. Preserve unaffected progress. Evidence from files
or tools does not independently authorize scope expansion. _Avoid_: defaults
outranking the maintainer, tool-output authority

**Mission observer**: An optional external observation assignment. It checks
known worker, tracker, and repository evidence at authorized reminders or
natural turns and reports concrete issues to the responsible workflow. The
dispatcher can also own its own reminders. Observation grants neither
implementation nor takeover authority; reminders use the existing scheduler
rather than new supervision code. _Avoid_: mandatory extra role, daemon,
survival guarantee

**Workflow evidence policy**: Executable tests validate real code and
deterministic structural invariants. Phrase assertions, snapshots, or test-only
state machines do not establish prompt meaning. Independent review, sequential
clean-context Prompt Audit when applicable, and bounded real workflow evidence
establish comprehension. Prefer removing redundant assertions over building a
prompt-evaluation framework. _Avoid_: regex comprehension proof, duplicate prose
implementation

## Relationships

- Specs become approved Tickets; publication and readiness remain separate from
  execution authorization.
- Direct delivery can use the accepted conversation without mandatory tracking,
  readiness, or Prompt Audit, whether the maintainer stays or authorizes work
  while away. Material changes to governing authority update applicable sources;
  explicitly required gates remain applicable.
- Mission topology applies to multiple selected Tickets. Maintainer departure
  preserves the current owner and topology, established decisions, recoverable
  state, and authorized stopping point.
- The final Ticket is the recoverable contract; historical audit records remain
  evidence for their exact version. Audit-only requests stop at recording;
  combined authorized delivery continues with a fresh implementation owner.
- The dispatcher may be selected automatically for an authorized multi-Ticket
  queue and stays through its completion even when one Ticket remains.
  `implement` loads `orchestrate` in the current conversation for one Ticket.
  Every route preserves applicable ownership, review, and delivery obligations.
  Continue through the user's stopping point without routine approval stops
  between implementation, review, corrections, and delivery.
- `to-spec` preserves established execution constraints; `to-tickets` decides
  what can safely run in parallel to save time and records the plan in the
  Tickets. Required order is distinct from priority. The dispatcher follows
  those decisions and checks live dependencies, resources, and capacity; a local
  blocker pauses its Ticket and dependents while other planned eligible work can
  proceed.
- Each Mission implementation Ticket owns an exclusive branch/worktree, fixed
  base, exact reviewed and final commits, and one current technical owner.
  Review, corrections, and checks use that candidate. See the
  [worktree policy](skills/engineering/orchestrate/WORKTREES.md).
- Execution topology is a planning decision based on the work, not a fixed
  scheduling default. Dispatch checks actual capacity and preserves the recorded
  concurrency, integration boundaries, and required phase barriers.
- Parallel members deliver verified pushed branch artifacts. A planned
  integration Ticket, blocked by every member, combines verified exact inputs in
  its own candidate and reviews/checks the complete result before dependent
  work.
- Other Tickets deliver to the agreed target by direct push or PR as required.
  PR delivery uses squash merge with exact source-to-result mapping and verified
  content equivalence. A closed issue or merged PR alone is insufficient
  delivery evidence.
- The technical owner performs implementation, independent-review adjudication,
  corrections, verification, tracker work, and cleanup in the same conversation.
  One completed adversarial review is the default: the reviewer challenges the
  complete candidate and reports every supported problem without sugar-coating
  or a finding quota; the owner records a disposition for every finding. The
  reviewer cannot rely on a later pass to finish the investigation. Review is a
  one-way handoff, not an approval loop: the owner keeps correcting and
  verifying without sending corrections for another review. Completion depends
  on accepted requirements and final-state evidence, not reviewer agreement.
  Correctable findings are work, not by themselves a blocked Ticket. Incomplete
  review needs recovery under existing authority and does not count as a
  completed pass.
- The dispatcher supervises progress and time as well as delivery. It verifies
  review/check records, exact candidate/target evidence, tracker obligations,
  and cleanup without writing code or becoming another code reviewer. Elapsed
  time prompts an evidence check, not automatic replacement; scheduler reminders
  provide later checks when completion events alone are insufficient.
- Recover the current owner first. Before replacement within authority, settle
  previous candidate-writing activity and preserve conversation,
  branch/worktree, HEAD, dirty changes, checks, hypothesis, and next action.
  Unknown acceptance never justifies duplicate dispatch; silence alone does not
  prove a stall.
- Setup follows scoped authorization for every consumer, including the
  dispatcher. Read-only leaves return missing prerequisites to their caller.
  Setup grants no additional Ticket scope.
- Managed subagents and `tmux-worker` are alternative transports under their own
  lifecycle contracts. Optional scheduler reminders support later bounded
  checks. Workflow policy stays in Markdown and ordinary notes, with no new
  coordinator code or supervision infrastructure.
- `tmux-worker` owns window/message/result transport and directed retirement.
  Callers own task meaning and next actions. Protect human editors through its
  safe result channels; preserve paused conversations while useful.
- `wormhole` transfers a conversation without adding implementation authority.
  Its definitive callback governs origin retirement; the handoff's authorized
  next action or explicit user gate selects continuation.
- Cleanup removes verified-delivered eligible owned temporary artifacts; failed,
  dirty, undelivered, still-consumed, or unrelated work remains protected with a
  reason. Publication cannot hide outstanding cleanup obligations.
- Private environment details and continuation notes stay private; public
  delivery evidence contains only appropriate project facts and references.
- A wayfinder map request authorizes one in-scope investigation per session.
  Destination implementation still needs its normal delivery authority; map
  Notes do not bypass it.
- All `.scratch/` artifacts remain local and Git-ignored. Local tracker triage
  `Status` and investigation `Lifecycle` remain distinct fields.

## Resolved terminology

- “Issue tracker” names the tool; “Ticket” names one implementation unit and
  “Spec” names planning authority. “Issue” remains acceptable when the
  configured tracker uses it.
- “Ticket owner” replaces the former coordinator/writer split. “Audit
  coordinator” still names the separate terminal audit role.
- A Router Skill selects skills; a Ticket dispatcher owns Mission continuity.
