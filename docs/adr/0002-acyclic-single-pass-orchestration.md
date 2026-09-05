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

Changing from Assisted to Unattended requires a new explicit gate. Before the
transition, preserve recoverable current state, establish durable current
contracts and resolved relations, obtain a current Prompt Audit `PASS` or
explicit maintainer `BYPASS`, and receive explicit Mission authorization.
Silence never changes availability. Once Unattended work starts, it completes
within that authority or stops at a genuine blocker instead of opening ordinary
interactive Questions.

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
never dispatches or implements.

### Frozen Mission plans and mechanical dispatch

When Mission topology is used, Mission authorization supplies one finite,
non-empty, pre-resolved plan. For Unattended Direct delivery, it may instead
select exactly one Ticket without requiring dispatcher composition. Before
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

Explicitly targeted steering may be forwarded literally to one active
coordinator. It cannot change the plan or select an adjacent Ticket. Untargeted
conversation remains at the dispatcher root. Authorization remains
non-transitive: no child receives later identities or returns `next` work, and
adjacent findings are reported without entering the plan. Mission completion
requires every selected identity to be delivered.

The user-only `implement` skill is only the one-Ticket convenience entry. In the
same root invocation, it composes the selected identity unchanged as a one-item
Mission plan through `dispatch-tickets`. It never invokes `orchestrate`, creates
a coordinator, or owns an independent implementation, review, or delivery path.

### Managed one-Ticket ownership and role inheritance

When Mission topology or Unattended delivery uses the managed Ticket route, a
human/invoker or context-rich parent may dispatch one fresh isolated Ticket
coordinator directly for smaller work. Each coordinator runs `orchestrate` and
owns exactly one explicitly authorized Ticket end to end through the existing
acyclic graph:

```text
Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator
```

Writer and reviewer are fresh, isolated, non-delegating, single-pass leaves.
They return evidence only to the coordinator and never exchange work directly.
After review, the coordinator adjudicates every finding, performs surviving
corrections directly, verifies and integrates the result, completes delivery
obligations, and returns the compact Ticket outcome. There are no delegated
correction or confirmation rounds. Ticket internals and Prompt Audit passes
remain sequential even when independent Tickets occupy a declared parallel
group.

The coordinator checks the selected Ticket's explicit authorization, scope,
setup and actual execution capabilities and, for Unattended work, its live
`PASS` or explicit `BYPASS`. It does not authenticate its parent's role or
provenance, inspect ancestors, or reject merely because its prompt has
`role=user` or lacks a dispatcher/depth assertion. It never discovers or
substitutes work.

After Unattended selection, the current execution gate transfers the exact
contract's in-scope decisions to the coordinator without another user gate. The
coordinator resolves source-determined divergences and minor safe defaults. If
authorized sources cannot determine required behavior, external authority is
unavailable, or required repository setup is missing during a headless run, it
returns a blocked outcome rather than widening, guessing, or starting
interactive setup. In an Assisted Mission, a materially unresolved decision may
instead return to the available maintainer.

The standard dispatcher, coordinator, writer, and reviewer roles inherit the
active provider, model, reasoning level, tools, and repository route unless an
authorized caller explicitly overrides them. Role names define ownership, not
reduced intelligence or capability. The standard managed hierarchy is caller
(dispatcher when used) at depth 1, Ticket coordinator at depth 2, and
non-delegating leaves at depth 3; there is no depth 4. The harness enforces
actual tool capabilities and depth/child ceilings. Caller authority never
relaxes them, and textual role or depth assertions cannot establish or override
them. Unsupported execution capabilities remain blockers.

The managed dispatcher/coordinator lineage does not require `wormhole` or
`tmux-worker`. Both remain generic optional interactive transports outside that
lineage and own no Mission topology or cross-Ticket continuation.

### Exclusive candidates and delivery boundaries

Every implementation Ticket handled by a Ticket coordinator, including one-item
and integration Tickets, owns an exclusive worktree and branch. After
authorization, live gate, setup, relations, exact-base, and child-capability
preflight succeeds, its coordinator establishes
and verifies that candidate before the sole writer starts. Preflight blockers
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
combination requirements. Other Tickets state their normal integration target.
The integration coordinator resolves and verifies each predecessor's durable
tracker delivery evidence, repository/remote branch reference and exact full
commit SHA before combining those exact results in its own candidate through
the same writer/reviewer graph. Missing, mismatched or unresolved inputs stop
safe integration; floating tips, child prose and dispatcher inspection cannot
replace evidence. Only authorized conflicts are resolved. Complete combined
review from the fixed base, final verification and durable input-to-result
commit evidence precede dependent work.

The coordinator owns resource disposition. Retain branch artifacts and
recoverable work until declared delivery and all integration consumers no longer
need them. Cleanup is limited to positively identified Ticket-owned resources
that are safe and no longer needed; preserve unrelated, failed, cancelled, dirty
or unintegrated work and required inputs, recording retention reasons. No blanket
or forced cleanup, history rewrite or force-push is authorized.

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
Assisted execution. Mission topology is now selected by real coordination, not
maintainer absence, and availability is resolved independently. This amendment
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
