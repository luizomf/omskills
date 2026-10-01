# Workflow map

Start with the goal you have now. Each section describes a useful entry, the
work it composes, and the result you can take forward. Arrows show the sequence
within that route; words such as **when**, **optional**, and **selected** mark
branches. The linked skills own the detailed instructions. Full catalogs live in
[Engineering](../skills/engineering/README.md) and
[Productivity](../skills/productivity/README.md).

## Deliver a bounded change

**Direct delivery** is the usual path for an untracked request or one selected
Ticket. The current conversational agent stays responsible whether the
maintainer is available or authorizes work while away:

```text
user → current owner: investigate / implement → independent reviewer
     → same owner: adjudicate / correct / verify / deliver → user
```

The conversational agent owns decisions, corrections and delivery. Use the
skills that help the task: diagnosis for a bug, TDD for test-first work, or
research for an open factual question. Existing instructions and a clear request
can already settle the scope and stopping point; ask about genuinely missing
choices. [orchestrate](../skills/engineering/orchestrate/SKILL.md) is this
owner's delivery procedure, not another agent to launch.
[implement](../skills/engineering/implement/SKILL.md) loads it in the current
conversation for one selected Ticket.

“I'm leaving; continue through push” keeps the same owner and route. Preserve
established decisions and recoverable state, and continue through that boundary
without inserting approval stops after implementation or review. Progress
messages need not pause work. A genuine missing prerequisite may block progress;
the user's absence alone adds no dispatcher or audit. Asynchronous review may
require releasing a turn, but its completion resumes work without user approval.

[code-review](../skills/engineering/code-review/SKILL.md) supplies a fresh
independent adversarial reviewer for behavior and governing-document changes. It
accepts a committed range or the complete work in progress and requires all
supported findings, without sugar-coating or a top-findings cutoff. The
responsible agent adjudicates every finding, fixes the candidate within scope,
and verifies corrections. Review is a one-way handoff, not an approval loop;
corrections stay with the author. Purely editorial documentation can be
self-reviewed. Delivery follows the repository's commit/push and optional PR
conventions. Direct work needs neither readiness nor Prompt Audit by default,
whether Assisted or Unattended. Apply them when the accepted task or repository
requires them; requested audit readiness means the same in both modes.

## Turn an idea into a plan

- [grill-me](../skills/productivity/grill-me/SKILL.md) explores decisions in
  bounded Question rounds. It finishes with confirmed understanding and a chosen
  destination in the conversation. A later action carries that result forward.
- [grill-with-docs](../skills/engineering/grill-with-docs/SKILL.md) adds durable
  domain terms and accepted ADRs while discussing the idea. On completion, it
  follows the selected destination: conversation summary, Scratchpad, new Spec,
  existing tracked-item update, domain language or ADR.
- [to-spec](../skills/engineering/to-spec/SKILL.md) synthesizes established
  context into a new or updated tracker Spec, preserving known execution
  constraints.
- [to-tickets](../skills/engineering/to-tickets/SKILL.md) turns a plan, Spec or
  conversation into approved tracer-bullet Tickets. During planning, decide what
  can safely run in parallel to save time and record that decision with the
  blocking/conflict relations, candidate ownership, and delivery boundaries.

A planning path can therefore be:

```text
idea → grill-with-docs → selected Spec destination → to-spec
     → to-tickets when breakdown is useful → published Tickets
```

Enter at the point your existing context supports. A resolved conversation or
updated domain document can itself be the desired result.

[triage](../skills/engineering/triage/SKILL.md) verifies an Issue or configured
external PR, investigates the code, uses grill-with-docs when decisions remain,
and applies the maintainer-selected category/state. It also supports attention
queries and explicit state changes. Its outcomes include a clarified brief,
missing-information request, human work or closure.

For **readiness**, triage composes
[prompt-comprehension-audits](../skills/productivity/prompt-comprehension-audits/SKILL.md):

```text
audit requested: final contract → fresh interpreter → independent reviewer
                                → adjudication and applicable fit check → PASS / FAIL
explicit waiver: final contract → applicable fit/status checks → BYPASS
```

The audit also checks implementation-Ticket fit using to-tickets. A current PASS
or explicit BYPASS promotes a complete tracked implementation Ticket to
`ready-for-agent` regardless of availability; failed or materially stale
readiness is removed. A complete Ticket body needs no duplicate brief. Readiness
never authorizes execution.

“Audit #42” records status/readiness and stops. “Audit and implement #42”
already authorizes delivery: after PASS, the owning workflow continues in a
fresh session or clean-context implementation agent without another approval.
The audit context never implements or corrects that work. The fresh owner
retains decisions, one independent candidate review, adjudication, corrections,
verification and delivery; no extra dispatcher or automatic writer/reviewer loop
is required.

## Deliver a coordinated Mission

Use Mission topology for multiple selected Tickets. The dispatcher provides the
user's operational supervision: it tracks the queue, time and progress, supports
owners, and verifies delivery without writing code. Availability is independent:
**Assisted** with the maintainer available, or **Unattended** continuing within
established decisions to the authorized stopping point. Neither absence nor
several subtasks inside one request creates a Mission.

[dispatch-tickets](../skills/engineering/dispatch-tickets/SKILL.md) is
discoverable for carrying an authorized queue through delivery. Supply selected
Tickets, their recorded execution decisions, relations, required order, and
delivery boundaries in prose, a list, or an existing phased plan. The dispatcher
follows that plan, checks live tracker/repository evidence and capacity, starts
or resumes eligible owners, routes decisions, and verifies delivery. It keeps
Mission continuity while technical work stays with each Ticket owner.

New dispatched Tickets get fresh owners running
[orchestrate](../skills/engineering/orchestrate/SKILL.md) themselves; paused or
already-owned work stays with its existing conversation. For only one selected
Ticket, use the direct route above. A Mission already underway keeps its
dispatcher through completion even when only one Ticket remains.

The topology is `user → dispatcher → Ticket owner → reviewer`, with findings
returning to that same owner and delivery evidence to the dispatcher. Each owner
keeps the technical work end to end:

```text
owner: resolve Ticket and prepare exclusive worktree
  → investigate, implement, test and commit
  → fresh independent reviewer: challenge the complete candidate
  → same owner: adjudicate, correct, verify, deliver and clean up
  → evidence report to dispatcher or caller
```

The reviewer investigates the complete candidate in one adversarial pass. The
owner then resolves findings and continues debugging and verification without
sending corrections for reviewer approval or another review. Completion depends
on the accepted requirements and final-state evidence, not reviewer agreement.
Record reviewed and final commits honestly; interrupted review remains
incomplete and follows the caller's recovery authority.

Scheduling comes from the Tickets' execution plan, not a fixed serial or
parallel default. Correctable findings and failing checks stay with the owner as
work to resolve. A genuine missing prerequisite preserves the Ticket's owner,
candidate, evidence, and next step; it does not end the whole Mission. The
dispatcher continues other eligible selected Tickets where required order and
dependencies permit. Resume the same owner when the prerequisite is resolved,
carrying relevant intervening deliveries.

Track start time, last observed progress, and the next useful check for active
owners. If a checkpoint is missed or progress is unclear, inspect evidence or
request a focused update; time alone does not establish a stall. Use existing
scheduler reminders when supervision needs a wake beyond worker completion,
following the transport's lifecycle rather than polling. State any reentry
limitation honestly, and cancel reminders once their purpose ends. No fixed
universal timeout or new monitoring service is required.

Concrete failures prompt diagnosis and recovery of the current owner first.
Replacement within authority requires the previous candidate-writing activity to
stop and recoverable state to transfer. Unknown acceptance calls for evidence
recovery rather than duplicate dispatch. User plan changes preserve unaffected
progress and update material contracts and applicable gates.

A declared parallel group delivers branch artifacts for a later integration
Ticket:

```text
phase 1: prerequisite Ticket
phase 2: compatible A + B → each delivers its verified pushed branch
phase 3: integration Ticket → combines exact A/B commits → delivers target
phase 4: dependent work
```

Planning establishes parallel work's independence, shared-resource
compatibility, and integration boundary; dispatch checks the live prerequisites
and capacity before launching it. Explicitly required phase barriers remain
constraints. The dispatcher verifies exact commits, review and check results,
tracker/PR state, and cleanup rather than accepting a status string as proof.
Mission completion requires every selected Ticket and the overall boundary to be
verified.

Use existing subagents or tmux-worker for transport and authorized scheduler
reminders when useful. A concise conversation record or ignored Markdown note
preserves continuity; no coordination code or supervision service is needed.

The [worktree policy](../skills/engineering/orchestrate/WORKTREES.md) covers
candidate placement, ownership, retained inputs and cleanup.
[ADR 0002](adr/0002-acyclic-single-pass-orchestration.md) records the ownership,
recovery, integration and delivery decision.

## Find a route through large or uncertain work

[wayfinder](../skills/engineering/wayfinder/SKILL.md) starts by clarifying the
destination with grill-with-docs. If the route becomes clear and fits one
session, it offers that simpler continuation. Otherwise it publishes a shared
map and investigation Tickets. A working session resolves one selected or
available frontier Ticket:

```text
map → one investigation → answer in tracker → updated map
    → another session as needed → resolved destination
```

Research Tickets produce cited evidence; prototype Tickets seek a reaction to an
artifact; grilling Tickets resolve decisions; task Tickets complete preparation.
Human input participates where the investigation needs it. Once the destination
is actionable, use direct delivery for one selected request or Mission dispatch
for multiple selected Tickets.

## Investigate, repair and test

- [research](../skills/engineering/research/SKILL.md) answers a bounded question
  with evidence or produces a durable cited Markdown artifact. Work can be local
  or assigned to a fresh investigation worker; the caller validates the result.
- [diagnosing-bugs](../skills/engineering/diagnosing-bugs/SKILL.md) proceeds
  from reproduction through minimization, hypotheses and instrumentation to a
  verified cause. For an accepted fix, use a faithful regression test when a
  suitable seam exists; otherwise document the limitation and verify with
  before/after evidence. A request limited to diagnosis ends with the evidence
  and recommended next step.
- [tdd](../skills/engineering/tdd/SKILL.md) develops a change one red → green →
  refactor slice at a time, using the accepted caller-visible test seam. It uses
  [codebase-design](../skills/engineering/codebase-design/SKILL.md) for seam
  vocabulary.
- [resolving-merge-conflicts](../skills/engineering/resolving-merge-conflicts/SKILL.md)
  enters an existing merge/rebase, traces both sides' intent, resolves
  conflicts, runs checks and continues the Git operation through completion.

These are task-specific routes within the selected delivery mode. A bug fix can
combine diagnosis, TDD and review; a research question can finish with its
answer.

## Explore architecture or an interface

[improve-codebase-architecture](../skills/engineering/improve-codebase-architecture/SKILL.md)
uses codebase-design vocabulary to scan for deepening opportunities, normally
with a fresh Explore worker, or locally when requested. The caller validates
findings and produces a visual HTML report. That report is a complete result.

When a candidate is selected, grill-with-docs develops its constraints,
ownership, seams and applicable domain/ADR updates. The optional
[Design It Twice](../skills/engineering/codebase-design/DESIGN-IT-TWICE.md)
process uses one fresh designer to compare interfaces when that specialist pass
is selected. Accepted implementation then follows the normal delivery route.

For visual or interaction work:

- [prototype](../skills/engineering/prototype/SKILL.md) creates a throwaway
  logic/state experiment or comparable UI variants, then records observations
  and trade-offs.
- [design](../skills/productivity/design/SKILL.md) grounds a visual direction in
  the product, designs the requested surface, and renders and checks
  interactions, accessibility and responsive states. Its result is the refined
  interface with verification evidence.

## Author skills or teach a topic

[write-a-skill](../skills/productivity/write-a-skill/SKILL.md) loads
[writing-great-skills](../skills/productivity/writing-great-skills/SKILL.md) and
its Glossary, establishes requirements, drafts the skill/resources, and verifies
them. Behavior changes receive independent code-review under the selected
delivery route. The result is the skill and its supporting files.
writing-great-skills can also be consulted directly for discovery, information
hierarchy and pruning decisions.

[teach](../skills/productivity/teach/SKILL.md) maintains a learning workspace:
mission and resources → suitable lesson → practice and feedback → learning
record. Later sessions use that state to select the next target. Outputs include
sourced HTML lessons, reusable assets and reference material, with
practitioner/community input for questions that call for experiential judgment.

## Share policies and configure a repository

- [setup-omskills](../skills/engineering/setup-omskills/SKILL.md) records
  tracker operations, triage labels, domain-document locations and a verified
  model-routing pointer. Existing choices and authorized defaults drive setup.
  Tracker-backed consumers need their applicable configuration; domain docs
  enrich diagnosis, TDD, architecture scans and grilling when present. Untracked
  review and untracked prompt audits work from their supplied contracts. See the
  [setup dependency decision](adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md).
- [model-routing](../skills/productivity/model-routing/SKILL.md) and its
  [model table](../skills/productivity/model-routing/MODELS.md) guide callers
  before model-selectable delegation: explicit choices first, then task-based
  selection within authorized scope and harness support, with inheritance as the
  fallback. This applies to review, research, design, audit and coordination
  workers.
- [caveman](../skills/productivity/caveman/SKILL.md) compresses communication
  while preserving technical accuracy when compressed reporting is useful.

Cross-skill file pointers make these resources available on demand, including
user-only skills hidden from discovery. The referring skill supplies
physical-path resolution instructions for relative-symlink installations.

## Continue context or work through a visible agent

- [handoff](../skills/productivity/handoff/SKILL.md) writes a temporary Markdown
  continuation record and returns its path, linking durable sources and
  retaining the immediate next step and unresolved context.
- [wormhole](../skills/productivity/wormhole/SKILL.md) composes handoff, opens a
  fresh interactive conversation and transfers it. The destination restores the
  recorded state, follows its selected continuation to the first Safe turn
  boundary, then confirms the transfer and retires the origin Pi.
- [tmux-worker](../skills/productivity/tmux-worker/SKILL.md) opens a visible
  agent for continued dialogue. Its caller supplies the task, selects the model
  route, interprets results and directs retirement; the skill provides buffered
  messages, callbacks and window lifecycle. Research, architecture scans,
  Mission owners, and their reviewers can use it. A dispatcher can pair its
  existing scheduler with the safe result channel for later bounded checks; an
  optional external observer reports evidence to the responsible workflow.

These utilities carry conversations and messages. Implementation ownership
remains with the workflow using them. A cooperative tmux callback is transport
evidence; managed subagent completion uses the harness's own settlement
mechanism.

## Optional utilities

These two skills are available separately from the active plugin catalog:

- [excalidraw](../skills/productivity/excalidraw/SKILL.md): text or an existing
  scene → editable diagram → structural checks and visual inspection when
  available.
- [voice](../skills/productivity/voice/SKILL.md): selected useful responses →
  spoken summary → serialized audio submission and normal written response. It
  needs the private OMQueue/Edge TTS playback tools and the active harness's
  supported route.

For terminology, see [CONTEXT](../CONTEXT.md); for execution decisions, see
[ADR 0001](adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md) and
[ADR 0002](adr/0002-acyclic-single-pass-orchestration.md).
