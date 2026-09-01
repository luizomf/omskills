# Acyclic single-pass Ticket orchestration

## Context

Prompt Audit, Mission dispatch, Ticket delivery, observation, and evidence need one
recoverable architecture. Earlier deliveries established a fresh implementation
context and a serial dispatcher, but left an audit-to-dispatch branch, a direct
one-Ticket route, and a no-parallel limitation. Prompt meaning was also sometimes
modeled through wording assertions rather than clean-context comprehension.

## Decision

### Ticket contract and execution gate

The final Ticket Issue, including any explicitly incorporated tracker artifact,
is the complete recoverable implementation contract. It contains or identifies
every accepted outcome, scope boundary, required workflow or order, deliverable,
acceptance criterion, relation, and completion condition. Conversations,
handoffs, coordinator analysis, and audit transcripts contain no secret
implementation requirement.

A current Prompt Audit `PASS` or explicit maintainer `BYPASS` for that exact
contract is an autonomous-execution eligibility gate, not Mission selection.
Only explicit Mission authorization selects work. A material change to outcome,
scope, workflow or order, deliverables, acceptance criteria, relations, or
completion makes the prior status stale.

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

Mission authorization selects either one Ticket or one finite, non-empty,
pre-resolved plan supplied by the invoker. Before dispatch, that plan contains
fully qualified unique Ticket identities, ordered sequential phases, declared
compatible parallel groups, blockers, and conflicts. A one-Ticket Mission is a
one-item plan. The dispatcher validates and freezes the supplied topology; it
never discovers, expands, removes, replaces, reorders, or semantically schedules
work.

The dispatcher owns only the frozen topology and compact mechanical routing
state, coordinator references, cancellation intent, and Ticket outcomes. It is
the only root contract that starts fresh `orchestrate` Ticket coordinators and
starts one for every identity runnable under the frozen topology. A parallel
group may run concurrently only when the
invoker declared it compatible. The next phase waits until every identity in the
active group returns matching `delivered`; a blocked, failed, cancelled, missing,
malformed, mismatched, or otherwise invalid transition stops the Mission.

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

### One-Ticket ownership and role inheritance

Each fresh Ticket coordinator is created only by `dispatch-tickets`, runs
`orchestrate`, and owns exactly one Ticket end to end through the existing
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

After selection, the current execution gate transfers the exact contract's
in-scope decisions to the coordinator without another user gate. The coordinator
resolves source-determined divergences and minor safe defaults. If authorized
sources cannot determine required behavior, external authority is unavailable,
or required repository setup is missing during a headless run, it returns a
blocked outcome rather than widening, guessing, or starting interactive setup.

The standard dispatcher, coordinator, writer, and reviewer roles inherit the
active provider, model, reasoning level, tools, and repository route unless an
authorized caller explicitly overrides them. Role names define ownership, not
reduced intelligence or capability. The hierarchy remains dispatcher at depth
1, Ticket coordinator at depth 2, and non-delegating leaves at depth 3; there is
no depth 4.

The managed dispatcher/coordinator lineage does not require `wormhole` or
`tmux-worker`. Both remain generic optional interactive transports outside that
lineage and own no Mission topology or cross-Ticket continuation.

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

This decision supersedes Issue #50's audit-to-dispatch completion branch while
preserving #50 as historical delivery evidence for the fresh-context boundary.
It also supersedes delivered Spec #33's serial-only/no-parallel limitation while
preserving that Spec as historical evidence for the initial dispatcher. Their
historical delivery records are not rewritten.

This record establishes governing architecture before behavior changes. Issue
#51, implementation, running Prompt Audits, dispatch behavior, releases,
monitoring infrastructure, and skill, catalog, test, or compatibility-evidence
changes remain out of scope and belong to separately authorized downstream
Tickets.
