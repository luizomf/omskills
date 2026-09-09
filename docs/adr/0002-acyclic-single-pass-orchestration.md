# Acyclic single-pass Ticket orchestration

## Context

Prompt Audit, Mission dispatch, Ticket delivery, observation, and evidence need one
recoverable architecture. Earlier deliveries established a fresh implementation
context and a serial dispatcher, but left an audit-to-dispatch branch and a
no-parallel limitation. Exclusive dispatcher entry later caused a coordinator
to reject selected work before reading its governing Ticket; caller authority
must be separate from mechanical dispatch ownership. Prompt meaning was also
sometimes modeled through wording assertions rather than clean-context
comprehension.

## Decision

### Independent delivery dimensions and adaptive gate

Delivery topology and maintainer availability are independent dimensions, not a
fixed mode matrix. Topology is either Direct delivery by one responsible
conversational agent or Mission topology for coordinated work. Availability is
Assisted while the maintainer remains available for ordinary implementation
Questions and Unattended when execution must rely on durable pre-resolved
authority and stop at a genuine blocker.

The responsible agent resolves only a materially unknown dimension at an
adaptive Delivery mode gate before the first implementation mutation. Read-only
inspection, investigation, and reproduction may precede the gate. A semantic
statement that already establishes topology or availability is sufficient;
there is no fixed questionnaire, magic wording, caller-ancestry check, or
redundant confirmation.

Direct Assisted delivery applies to an untracked request or exactly one selected
Ticket when no real coordination is required. The confirmed conversation is its
active contract, and the conversational responsible agent owns investigation,
implementation, verification, review adjudication, corrections, and delivery.
No Ticket, Agent Brief, readiness state, or Prompt Audit is required by default.
Durable tracking is required when the active contract must survive the
conversation. If accepted behavior materially changes existing governing
authority, the agent updates the applicable Ticket, Spec, ADR, workflow,
security, or other durable source before delivery.

More than one selected Ticket always requires Mission topology. So does any work
with real dependency, conflict, integration, shared-resource, or multiple-writer
coordination. Several edits in one request do not become
multiple Tickets merely because they touch multiple files. Mission topology does
not imply that the maintainer is absent, and Assisted availability does not
remove its planning, relation, capacity, integration, or delivery boundaries.
An active Mission coordinator must leave untargeted root conversation and
capacity-supported unrelated work responsive rather than monopolizing them by
policy.

Direct Assisted work may delegate bounded non-delegating research or
investigation with narrow questions and compact evidence returns, while the
responsible agent retains decisions and implementation. Independent
investigations should start together when independence and active capacity are
affirmatively established. Routine local inspection stays local when delegation
would cost more context than it saves.

Changing Direct Assisted work to Unattended establishes a one-Ticket Mission
and requires a new explicit gate. Before the transition, preserve recoverable
current state, establish durable current contracts and resolved relations,
obtain a current Prompt Audit `PASS` or explicit maintainer `BYPASS`, and receive
explicit Mission authorization. Silence never changes availability. Once an
Unattended Mission starts, it completes within that authority or stops at a
genuine blocker instead of opening ordinary interactive Questions.

### Ticket contract and execution gate

For tracked work, the final Ticket Issue, including any explicitly incorporated
tracker artifact, is the complete recoverable implementation contract. It
contains or identifies every accepted outcome, scope boundary, required workflow
or order, deliverable, acceptance criterion, relation, and completion condition.
Conversations, handoffs, coordinator analysis, and audit transcripts contain no
secret implementation requirement.

A current Prompt Audit `PASS` or explicit maintainer `BYPASS` for that exact
contract is an Unattended-execution eligibility gate, not Mission selection.
Only explicit Mission authorization selects Unattended work. Prompt Audit is not
applicable to Assisted work by default, though the maintainer may request it for
complex intent. A material change to outcome, scope, workflow or order,
deliverables, acceptance criteria, relations, or completion makes the prior
status stale.

### Terminal sequential Prompt Audit

The current audit coordinator fixes the reference intent from the exact Ticket
contract and governing sources. One fresh read-only non-delegating interpreter
then completes its interpretation. Only after that completion, one fresh
independent read-only non-delegating reviewer receives the reference intent and
the completed interpretation, but not hidden coordinator analysis or a desired
answer. The coordinator adjudicates the evidence, records exactly `PASS`,
`FAIL`, or explicit `BYPASS`, and ends.

`PASS` means no material semantic divergence survives adjudication. `BYPASS` is
an explicit maintainer waiver and is never represented as `PASS`. Prompt Audit
never dispatches or implements. An Assisted-only audit records comprehension
evidence and ends without readiness-label mutation or requiring Unattended
triage artifacts; readiness transition belongs only to an invocation establishing
Unattended eligibility.

Explicit maintainer recovery may replace a mechanically settled but incomplete
pass with a fresh isolated pass before terminal status recording. Preserve the
fixed reference, sequential interpreter/reviewer order and all attempt evidence;
only complete results support adjudication. Replacement does not authorize
semantic verdict shopping, contract edits, or reuse of a prior pass context.
Unknown dispatch acceptance is not proof of settlement. Without authorized
recovery, an incomplete pass records `FAIL`; after terminal status, further audit
work is a separately authorized invocation.

### Frozen Mission plans and mechanical dispatch

When Mission topology is used, Mission authorization supplies one finite,
non-empty, pre-resolved plan. A transition from Direct Assisted work supplies a
one-Ticket Mission plan; this does not require a fixed mode matrix. Before
Mission dispatch, the plan contains
fully qualified unique Ticket identities, ordered sequential phases, declared
compatible parallel groups, blockers, and conflicts. A one-Ticket Mission is a
one-item plan. The dispatcher validates and freezes the supplied topology; it
never discovers, expands, removes, replaces, reorders, or semantically schedules
work.

The dispatcher owns only the frozen topology and compact mechanical routing
state, coordinator references, cancellation intent, and Ticket outcomes when
used. It provides thin dispatch for long finite multi-Ticket Missions, not
exclusive permission to start every coordinator. It starts one fresh
`orchestrate` coordinator for every identity runnable under the frozen topology.
An N-member parallel group requires invoker-declared compatibility, including
shared resources outside Git, and affirmative evidence of the active harness's
root concurrency bound and same-batch start capability in the current delivery
mode. Child-only ceilings or an absent exposed bound do not establish root
capacity. Unknown or unsupported capacity rejects before any Ticket starts;
dispatch never serializes, splits, retries or changes runtime limits to fit it.
The next phase waits until every identity in the active group returns matching
`delivered`; a blocked, failed, cancelled, missing, malformed, mismatched, or
otherwise invalid transition stops new dispatch. Every accepted sibling still
settles and retains its valid outcome, without reviving the stopped Mission.

Explicit user steering is routed by unambiguous scope, not mandatory numeric
IDs: one active coordinator, named Tickets, all active coordinators, or selected
not-yet-started Tickets. The dispatcher forwards the literal instruction to
active targets or retains it with its scope for future start prompts. Clear
requests need no repeated confirmation. Future-only steering leaves accepted
coordinators untouched and does not restart the Mission. Explicit lifecycle
routing updates apply to not-yet-issued starts; referenced routing guidance is
passed to coordinators without root file inspection or guessed model IDs.
Only this compact instruction/routing state is mutable; topology, phase barriers,
settlement, capacity, and outcome contracts remain unchanged. Coordinators own
referenced content, applicable durable contract updates and execution gates;
steering does not silently bypass them. Unrelated conversation stays local.
This maintainer-authorized correction supersedes the earlier single-ID-only
steering and immutable-prompt/start-override restrictions, not the frozen plan.
Authorization remains non-transitive: no child receives later identities or returns `next` work, and
adjacent findings are reported without entering the plan. Mission completion
requires every selected identity to be delivered.

The user-only `implement` skill is only the one-Ticket convenience entry. In the
same root invocation, it composes the selected identity unchanged as a one-item
Mission plan through `dispatch-tickets`. It never invokes `orchestrate`, creates
a coordinator, or owns an independent implementation, review, or delivery path.

### Managed one-Ticket ownership and role inheritance

When Mission topology uses the managed Ticket route, a human/invoker or
context-rich parent may dispatch one fresh isolated Ticket
coordinator directly for smaller work. Each coordinator runs `orchestrate` and
owns exactly one explicitly authorized Ticket end to end through the existing
acyclic graph:

```text
Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator
```

By default, writer and reviewer are fresh, isolated, non-delegating, single-pass leaves.
They return evidence only to the coordinator and never exchange work directly.
After review, the coordinator adjudicates every finding, performs surviving
corrections directly, verifies and integrates the result, completes delivery
obligations, and returns the compact Ticket outcome. There are no automatic delegated
correction or confirmation rounds. Ticket internals and Prompt Audit passes
remain sequential even when independent Tickets occupy a declared parallel
group.

The coordinator checks the selected Ticket's explicit authorization, scope,
setup and actual execution capabilities and, for an Unattended Mission, its live
`PASS` or explicit `BYPASS`. It does not authenticate its parent's role or
provenance, inspect ancestors, or reject merely because its prompt has
`role=user` or lacks a dispatcher/depth assertion. It never discovers or
substitutes work.

After Unattended selection, the current execution gate transfers the exact
contract's in-scope decisions to the coordinator without another user gate. The
coordinator resolves source-determined divergences and minor safe defaults. If
authorized sources cannot determine required behavior, external authority is
unavailable, or required repository setup cannot be completed under the scoped
authorization rule in ADR 0001, it returns a blocked outcome rather than
widening, guessing, or starting interactive setup. Separately authorized,
deterministic setup may precede Ticket implementation without expanding its
Mission envelope; read-only leaves and shared-resource boundaries still apply.
In an Assisted Mission, a materially unresolved decision may instead return to
the available maintainer.

The standard dispatcher, coordinator, writer, and reviewer roles inherit tools
and repository route unless explicitly overridden. Before a model-selectable
delegation, its caller loads the shared user-only `model-routing` skill. Explicit
model/reasoning choices win; authorized task-based routing selects a concrete
available candidate from the maintained provider table; otherwise inheritance
remains the fallback. Selection considers remaining uncertainty, impact and
verification, not task length or the parent's capability alone. A thin dispatcher
and a Ticket coordinator that owns review adjudication and corrections are
different assignments.

The public table contains model candidates and supported effort guidance, not
prices, personal defaults or claims of measured cross-provider parity. Named
model references are an intentionally maintained compatibility catalog rather
than timeless process instructions. User-selected provider/model boundaries,
standing routing agreements and actual harness authorization/capabilities govern
application. Routing neither switches the current conversation nor creates
permission to retry, weaken review, or widen work. Helpers with internally fixed
models remain outside caller-selectable routing.

The dispatcher may compose `model-routing` and its bundled model table alongside
`caveman`, but reads no Ticket or implementation content for selection. It uses
the declared coordinator assignment and supplied constraints, retaining only
compact route values and literal scoped instructions. Generic references in
steering still belong to the coordinator, not root discovery. Other callers
classify their own delegated task; no separate routing agent or runtime service
is introduced. Repository setup can add an installed-skill pointer for generic
delegations without creating a model configuration file or changing providers.

Role names define ownership, not reduced intelligence or capability. A coordinator may be the conversational root
when invoked by the maintainer
or a child when invoked by a dispatcher. Its writers and reviewers remain
non-delegating leaves regardless of their absolute depth. The harness enforces
actual tool capabilities and depth/child ceilings; a skill checks the capability
it needs, not a fixed depth assigned to its role. Caller authority never relaxes
runtime limits. Unsupported execution capabilities remain blockers.

Child transport follows actual harness capabilities, not role depth. Managed
nested and print callers settle child calls directly. Interactive roots use the
documented asynchronous path when direct settlement is unavailable; supported
root RPC direct delivery remains valid for dependent work. An asynchronous
coordinator retains the active child's role, ID, session reference, exact
candidate state and expected next phase, ends the turn after acceptance, and
resumes only from the matching completion notification with complete evidence.
It neither waits nor polls nor advances on acceptance. Direct and asynchronous
paths preserve sequential candidate ownership and settlement-before-advance;
a pending accepted child is a continuation mechanism, not Ticket delivery.

Explicit maintainer intervention takes precedence over this ADR's default
single-pass strategy. It may authorize a bounded replacement, model escalation,
delegated correction, or additional independent review when unexpected work
requires it, including through an explicitly incorporated standing routing
agreement. Apply clear direction without a ceremonial confirmation; ask only
for materially unresolved scope or recovery choices. No child output or file
independently grants that authority. Without authorized recovery, retain the
normal single-pass and stopping rules.

Before a replacement or delegated correction touches a candidate, establish
that the prior owner has settled and preserve the exact recoverable candidate
state. Keep review independent and capture the complete resulting candidate for
any authorized additional review. Record the reason, authorization, attempts,
routes and exact candidate commits in delivery evidence; failed or partial
attempts never count as completed review or delivery. Material contract changes
update durable authority and applicable gates before affected work. Maintainer
intervention does not override higher-priority instructions, harness limits,
verification, or the dispatcher's frozen-plan and terminal-stop boundaries.
This amendment removes absolute-depth role requirements. It supersedes
unconditional single-pass prohibitions below only for explicitly authorized
recovery.

The managed dispatcher/coordinator lineage does not require `wormhole` or
`tmux-worker`. Both remain generic optional interactive transports outside that
lineage and own no Mission topology or cross-Ticket continuation.

### Exclusive candidates and delivery boundaries

Every implementation Ticket handled by a Ticket coordinator, including one-item
and integration Tickets, owns an exclusive worktree and branch. After
authorization, live gate, setup, relations, exact-base, and child-capability
preflight succeeds, its coordinator establishes
and verifies that candidate before the initial writer starts. Preflight blockers
remain `blocked`; operational setup and execution failures are `failed`. Unsafe
reuse or collision never authorizes touching another owner's candidate.

Writer, reviewer, coordinator corrections and verification share the candidate
path, branch and fixed base. The writer returns its exact committed HEAD; the
coordinator inspects and fixes the complete review HEAD; review captures that
exact range; final checks record the final SHA. Unexpected branch/HEAD drift or
incomplete capture cannot count as review. The caller checkout stays untouched
by candidate work, and unrelated changes are preserved during integration.

Planning declares each delivery boundary. Parallel members deliver verified,
committed, pushed branch artifacts, not an implicit shared-target merge or group
completion. Every parallel group has a preplanned ordinary integration Ticket
blocked by all members, naming predecessor identities, intended base/target and
combination requirements. Other Tickets state their normal integration target
and whether delivery uses a pull request. Pull requests remain optional unless
repository policy or the accepted request requires one; Direct Assisted commits
to an allowed target do not acquire a branch or pull-request requirement merely
from this decision.

The integration coordinator resolves and verifies each predecessor's durable
tracker delivery evidence, repository/remote branch reference and exact full
commit SHA before combining those exact results in its own candidate through
the same writer/reviewer graph. Missing, mismatched or unresolved inputs stop
safe integration; floating tips, child prose and dispatcher inspection cannot
replace evidence. Only authorized conflicts are resolved. Complete combined
review from the fixed base, final verification and durable input-to-result
commit evidence precede dependent work. Whenever a pull request is used,
including non-member and one-item delivery, squash-merge it into the declared
target and durably map every exact source commit to the resulting target commit
before calling the Ticket delivered.

The responsible agent owns resource disposition. In both Direct Assisted and
Mission work, verified cleanup of eligible owned temporary artifacts is part of
completion, not optional housekeeping after publication. Required integration
inputs and unrelated or recoverable unfinished work remain protected; the
integration coordinator owns eligible declared predecessor cleanup after the
final consumer. Publication success cannot hide cleanup failure.

The [shared worktree policy](../../skills/engineering/orchestrate/WORKTREES.md)
is the single operational reference for home-relative project-grouped locations,
parent creation, ownership, squash-aware cleanup, verification, and retention.
Skills and repository instructions load that reference instead of duplicating
its mechanics. This placement keeps the policy available in installed skills
without requiring Mission execution for Direct Assisted work.

### Proportionate independent review

Review follows authority and impact rather than file extension. Specs, ADRs,
workflow, security, and other governing documents remain first-class behavior
authority. Direct Assisted code or behavior changes and changes to that governing
authority receive one fresh independent review. Purely editorial
documentation may be self-reviewed. The reviewer receives the concise current
contract, governing sources, complete candidate, and verification instructions,
not the complete conversation by default. The responsible agent adjudicates and
corrects findings; re-review is required only when corrections materially change
the candidate.

This Assisted review contract does not alter the managed Ticket route's isolated
single-pass reviewer, coordinator-owned correction, exact-candidate capture, or
verification requirements.

### External bounded observation

Observation is separate from implementation and dispatch. An external observer
may have at most one payload-free heartbeat outstanding and perform one bounded
inspection of visible tmux plus durable repository and tracker evidence. Healthy
progress is silent except for scheduling the next single heartbeat. Intervention
is allowed only for concrete failure or blockage, an abandoned human gate, or an
invalid or stopped dispatch transition. Mission completion or terminal stop
schedules no further heartbeat.

The observer owns neither implementation nor dispatcher state. Observation adds
no daemon, recurring cron or poller, persistent Mission state, takeover, or
guarantee that a process, host, network, tmux server, or owning session survives.

### Evidence

Phrase, regex, snapshot, injected-wording, and test-only semantic state models do
not prove prompt meaning. Tests remain appropriate for real executable code and
deterministic mechanical or structural invariants. Sequential clean-context
Prompt Audit and bounded real workflow evidence establish prose comprehension.
Prefer deleting redundant semantic assertions or abstractions over replacing
them with another framework.

## Supersession and scope

The accepted dual-axis architecture in Spec #61 and Issue #62 amends this ADR's
universal autonomous-pipeline requirements only where they conflict: Direct
Assisted work no longer requires a Ticket, Prompt Audit, dispatcher, separate
Ticket coordinator, or writer, and Prompt Audit gates Unattended rather than
Assisted execution. Mission topology is selected by real coordination or the
explicit transition to an Unattended Mission, not merely by maintainer absence;
availability is resolved independently. This amendment
preserves #52 and #58 as historical delivery evidence without rewriting their
Issues, audit records, or delivery records.

All unaffected guarantees remain in force: non-transitive authorization,
terminal sequential Prompt Audit when applicable, frozen mechanical Mission
dispatch, established safe parallelism and independent-investigation
parallelism, actual capacity checks, phase barriers and sibling settlement,
review independence, managed single-pass leaves and coordinator corrections,
exclusive candidate isolation, exact commit capture, verification honesty,
branch-artifact and combined-state integration boundaries, privacy, least
privilege, external-resource ownership, recoverable retention, bounded
observation, safe cleanup, and prohibitions on forced cleanup and history
rewrites. This amendment adds no runtime service, retry, monitoring system,
dynamic discovery, or concurrency claim. Downstream skill, catalog, runtime, and
user-facing behavior changes remain separately authorized work in #63, #65, and
#64.

This decision supersedes Issue #50's audit-to-dispatch completion branch while
preserving #50 as historical delivery evidence for the fresh-context boundary.
It also supersedes delivered Spec #33's serial-only/no-parallel limitation while
preserving that Spec as historical evidence for the initial dispatcher. Their
historical delivery records are not rewritten.

The maintainer's caller-authority correction in Issue #58 supersedes only the
exclusive-dispatcher entry and mandatory parent-provenance interpretation of
this ADR and delivered #55/#52 guidance. Their historical records remain
untouched. One-Ticket isolation, live gates, non-transitive authorization,
single-pass leaves, coordinator corrections, actual harness limits and all
mechanical dispatcher boundaries when used remain in force. `implement` retains
its existing dispatcher composition. This governance correction precedes the
separately audited and authorized behavioral text delivery in #58; it is not a
runtime bypass or a retry of the stopped Mission.

This record establishes governing architecture before behavior changes. Issue
#51, implementation, running Prompt Audits, dispatch behavior, releases,
monitoring infrastructure, and skill, catalog, test, or compatibility-evidence
changes remain out of scope and belong to separately authorized downstream
Tickets.
