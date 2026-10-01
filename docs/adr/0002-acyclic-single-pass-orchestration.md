# Context-preserving Ticket delivery and lightweight Mission dispatch

## Context

The former Mission route separated a coordinator from a default writer and
restricted dispatch to frozen phases and JSON outcomes. This increased handoffs
and prevented the dispatcher from checking real delivery or continuing
independent work around a local blocker.

A long-running multi-issue delivery demonstrated a simpler division: one
technical owner keeps each Ticket's context, an independent reviewer challenges
the candidate, and a lightweight dispatcher manages Mission continuity using
existing conversations, tracker/repository evidence, and optional reminders.

This record consolidates the current decision in place so existing links remain
valid. The former topology and its delivery/audit records remain historical
evidence in Git and the tracker; they do not impose the superseded default
writer, frozen JSON protocol, or global-stop behavior.

## Decision

### Delivery authority and availability

Direct delivery keeps an untracked request or one selected Ticket with its
current conversational responsible agent, whether the maintainer stays or
authorizes continuation while away. The accepted conversation is the active
contract. Tracking becomes necessary when the contract must survive that context
or changes existing governing authority; update the applicable durable sources
before delivery. Read-only investigation and reproduction may begin before all
implementation decisions are settled.

Mission topology supervises multiple selected Tickets, including their
dependency, conflict, integration, and shared-resource needs. Several files or
subtasks within one request do not create a Mission. Maintainer availability is
independent: Assisted supports ordinary Questions; Unattended continues within
established decisions and reports genuinely unresolved blockers.

“I'm leaving; continue through X” preserves the current owner and topology.
Retain the decisions and recoverable state needed to reach X; no dispatcher,
audit, readiness transition, or repeated approval is added merely because the
maintainer leaves. Apply gates required by the accepted task or repository.
Silence does not change availability. Continue to the authorized stopping point
without routine approval stops between implementation, review, corrections, and
delivery. Transport-required asynchronous turn release preserves continuation;
it does not require the user to restart the work.

Authorization selects a finite queue, scope, constraints, and completion
boundary. It does not extend to adjacent findings or outside dependencies merely
because the agent reads them. The user may revise the queue or contract; apply
clear direction, update affected authority/gates, and settle ownership before
replacement or conflicting work.

### Ticket contract and Prompt Audit

The final Ticket, including explicitly incorporated tracker artifacts, is the
complete recoverable contract: outcome, scope, required workflow/order,
deliverables, acceptance criteria, relations, and completion conditions.
Conversations and handoffs explain it without carrying hidden requirements.

A current Prompt Audit `PASS` or explicit maintainer `BYPASS` makes a complete
tracked implementation Ticket `ready-for-agent`, preserving one category and one
state role regardless of availability. Readiness establishes eligibility, not
selection. Audits apply when requested or required by the accepted task or
repository, not automatically because the maintainer is absent. A material
contract change makes its older status stale; remove failed or stale readiness.

Prompt Audit remains a terminal sequential workflow. Its coordinator fixes the
reference intent; one fresh read-only non-delegating interpreter reconstructs
the contract; then a fresh independent read-only non-delegating reviewer
compares that reconstruction with the reference intent. The reviewer receives
neither hidden coordinator analysis nor a desired answer. The coordinator
adjudicates and records `PASS`, `FAIL`, or explicit `BYPASS`, including the
Ticket-fit check.

An audit-only request ends after status/readiness recording. Combined
audit-and-implement authorization continues in a fresh implementation context
without another approval. The audit context never implements or corrects the
audited work. Explicit recovery may replace a mechanically settled but
incomplete audit pass before terminal recording, preserving the fixed contract
and all attempt evidence. Unknown acceptance is not settlement; replacement does
not permit verdict shopping or contract changes. Further audit after a terminal
status is separately authorized work.

### Lightweight Mission continuity

`dispatch-tickets` is agent-discoverable. Its description supports automatic
selection when the accepted task is to carry multiple selected Tickets through
delivery. For only one Ticket, `implement` loads `orchestrate` in the current
conversation; direct `orchestrate` invocation also stays there. A dispatcher
already supervising a multi-Ticket Mission stays through its agreed boundary,
even when only one Ticket remains. Discovery selects the skill; the request
selects the work.

The dispatcher reads tracker configuration, selected Tickets, relevant
repository state, dependencies, shared resources, and delivery evidence. It
maintains a concise record of the queue, constraints, current owners and
conversation references, candidates, start times, last observed progress, next
checks/actions, blockers, and verified deliveries. The conversation or an
ignored Markdown note suffices. Durable requirements and delivery records use
the configured tracker.

The plan can be prose, a list, or an existing phased JSON plan. Record priority
separately from required sequence or phase barriers. The dispatcher chooses
eligible work inside the selected queue, honoring required order and live
relations. Serial execution is the default. Parallel work requires proven
independence, shared-resource compatibility, actual available transport
capacity, and agreed integration boundaries. Preserve a required parallel
topology when capacity is unavailable by reporting the unmet prerequisite rather
than silently changing the agreement.

Correctable findings and failing checks remain work for the same Ticket owner,
not by themselves reasons to stop. A blocker requires a concrete missing
prerequisite preventing further in-scope progress. Preserve that Ticket's owner,
conversation, candidate, evidence, and next action, and continue other eligible
selected work when required order and dependencies permit. A Mission reaches a
stopping point when remaining work lacks an eligible next action or the user
stops it, rather than whenever any one Ticket blocks.

The dispatcher routes user decisions and carries relevant integrated changes to
later owners. It verifies the declared delivery boundary through tracker/PR
state, exact source/target commits, review and check evidence, and cleanup. This
is operational delivery verification; implementation and code review belong to
the Ticket owner and independent reviewer. A status string, JSON envelope,
callback, closed issue, or merged PR alone is insufficient proof.

Mission completion requires all currently selected Tickets and the overall
boundary to be verified. Branch artifacts remain integration inputs until the
planned combined-state delivery completes. An outcome is a concise evidence
report; JSON is optional rather than a terminal protocol.

### Continuous technical ownership

`orchestrate` is a delivery procedure for the current responsible agent, not a
separate coordinator to launch. It covers an untracked bounded request or one
selected Ticket. Its same conversation reproduces, implements, tests, debugs,
obtains review, adjudicates findings, corrects, verifies, and delivers. This
replaces the default coordinator → writer handoff. Bounded research or design
assistance can support the owner within the accepted task and actual
capabilities.

New dispatched Tickets start with fresh owners; an already responsible
conversation stays the owner rather than being wrapped in another coordinator.
Paused work preferably resumes its existing conversation and candidate. Direct
invocation uses the current responsible conversation, except that a Prompt Audit
context hands the audited implementation contract to a fresh owner. Authority
comes from accepted selection and scope, not caller ancestry, role labels, or
fixed delegation depth.

The owner checks the accepted request or live Ticket, governing sources,
applicable audit/readiness, repository instructions, setup, relations, candidate
ownership, and actual implementation/review/delivery capabilities. Missing setup
follows ADR 0001's scoped authorization for both owner and dispatcher. Material
source-undetermined decisions go to the available maintainer or become
Unattended blockers.

Bug fixes preserve reproduction-first diagnosis and a faithful regression test
where a suitable seam exists, with before/after evidence and limitations when
automation is impractical. Required project checks and honest verification apply
to the exact final candidate.

### Independent review

Behavior changes and governing-authority changes receive a fresh independent
review of the complete candidate. Purely editorial documentation can be
self-reviewed in direct delivery. The reviewer receives the concise contract,
applicable standards, complete candidate, exact identity/range, and verification
evidence. It remains read-only and non-delegating, returning full findings to
the implementation owner. Apply the adversarial contract in
[code-review](../../skills/engineering/code-review/SKILL.md): challenge the
complete candidate, continue after blockers, and report every supported problem
without a finding quota or softened severity. Evidence, not a desired verdict,
determines findings; adversarial review does not invent requirements or defects.

Review is a one-way handoff, not an approval loop. The reviewer finishes the
complete investigation in one pass. The author records an evidence-based
disposition for every finding and keeps implementing, debugging, and verifying
in-scope corrections without sending them for reviewer approval or another
review. Completion depends on accepted requirements and final-state evidence,
not reviewer agreement or finding count. A delivery-blocking defect is work to
resolve, not by itself a blocked Ticket.

Interrupted or partial review remains incomplete and needs recovery under the
caller's existing authority; it cannot be counted as a completed pass. Record
reviewed and final SHAs and the changes between them honestly.

### Exclusive candidates and integration

Each implementation Ticket in a multi-Ticket Mission, including integration
Tickets, owns an exclusive worktree and branch with a fixed full base SHA.
Record and verify candidate path, branch, starting HEAD, reviewed commit, and
final commit. Review, corrections, and checks stay on that candidate; unexpected
drift needs diagnosis before further changes. Preserve unrelated work and the
caller checkout.

Parallel members deliver verified pushed branch artifacts. Their planned
integration Ticket names every predecessor, target/base, and combination
requirements, and is blocked by all required inputs. Its owner verifies each
repository, remote reference, and exact produced commit against durable delivery
evidence, combines those inputs in its own candidate, and obtains complete
combined-state review and checks before target delivery.

Other Tickets deliver by the agreed direct-push or PR method. A PR is optional
unless repository policy or the request requires it. PR delivery uses squash
merge, verified target/content equivalence, and durable source-to-squash
mapping. Integration records exact predecessor-to-result mappings before
dependent work.

[WORKTREES.md](../../skills/engineering/orchestrate/WORKTREES.md) is the shared
operational policy for location, ownership, retention, and cleanup. The owner
removes every eligible verified-delivered temporary artifact and records
protected retention reasons. Integration owns eligible declared predecessor
cleanup after their final consumer. Failed, dirty, undelivered, still-consumed,
and unrelated work remains protected. Publication success does not hide
outstanding cleanup or tracker obligations.

### Recovery and transport

Diagnose concrete failures using the known conversation, transport outcome,
repository, and tracker. Silence or elapsed time alone does not prove a stall.
Prefer recovering the current owner. Within the Mission's recovery authority,
replacement begins only after previous candidate-writing activity has stopped
and its recoverable state is preserved: conversation, branch/worktree, HEAD,
dirty changes, checks, hypothesis, and next action. Unknown acceptance requires
evidence recovery before another start. When a result is lost after publication,
verify the target and recover missing obligations rather than repeat delivery.

Use existing managed subagents or `tmux-worker`; transport supplies lifecycle,
not Mission policy. Follow documented direct/asynchronous result delivery,
actual capability/depth limits, callback/editor safety, complete result
recovery, and directed retirement. Release asynchronous turns after acceptance
so their completion events can arrive. A cooperative callback alone is not an
automatic continuation mechanism.

The dispatcher supervises time and progress on the user's behalf, without
writing code. Compare elapsed time with the work, last observed progress, and
agreed checkpoints. Unclear progress calls for inspecting the known owner and
available evidence or requesting a focused update, not automatic replacement.
Use existing scheduler reminders when that supervision needs reentry beyond
worker completion. Choose timing from the task and user instructions rather than
adding universal timeouts. Their prompts restore the Mission, known owners, last
progress, evidence, and next decision, following the scheduler's
mechanical-outcome and untrusted-output rules. Cancel reminders when their
purpose ends and state unavailable reentry honestly. An external observer can
report concrete evidence to the responsible workflow without taking over its
state. These workflows require no new coordinator code, daemon, watchdog,
polling loop, or supervision service.

Model-selectable launches use `model-routing` within explicit user choices,
authorized policy, and active harness constraints; inheritance is the fallback.
Classify full Ticket ownership and operational Mission decisions by their actual
judgment needs. Resolve cross-skill links from the referring file's physical
directory and pass resolved paths to fresh agents. Private operational notes,
credentials, and environment details remain outside public artifacts.

### Verification of these workflows

Use executable checks for actual scripts and structural invariants such as
catalog/discovery consistency, installation, and readable pointers. Use
independent review, applicable clean-context Prompt Audit, and bounded workflow
evidence for prose comprehension. Avoid duplicating these instructions in a
semantic state machine or wording-test framework.

## Supersession

This revision replaces the frozen mechanical dispatcher, compulsory JSON
outcomes, default separate writer, automatic global stop on a local blocker,
transport-specific Mission topology, repeated review of author corrections,
one-Ticket dispatch, and automatic Mission/audit gates upon maintainer
departure. `orchestrate` remains available as the current owner's procedure
while connected workflows converge on that responsibility. Existing phase
constraints remain usable when the accepted Mission actually requires them.
Audit eligibility, scoped authority, independent review, exclusive ownership,
verified integration, privacy, and safe cleanup remain in force. Historical
Issues, audits, and delivery records are preserved rather than rewritten.
