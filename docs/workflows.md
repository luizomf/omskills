# Workflow map

Start with the goal you have now. Each section describes a useful entry, the work
it composes, and the result you can take forward. Arrows show the sequence within
that route; words such as **when**, **optional**, and **selected** mark branches.
The linked skills own the detailed instructions. Full catalogs live in
[Engineering](../skills/engineering/README.md) and
[Productivity](../skills/productivity/README.md).

## Deliver a bounded change

**Direct Assisted** is the usual path for an untracked request or one selected
Ticket while the maintainer is available and the work needs one responsible agent:

```text
request → resolve scope and delivery mode → investigate / implement as needed
        → independent review when required → verify → deliver
```

The conversational agent owns decisions, corrections and delivery. Use the skills
that help the task: diagnosis for a bug, TDD for test-first work, or research for
an open factual question. Existing instructions and a clear request can already
settle the delivery mode; ask about genuinely missing choices.

[code-review](../skills/engineering/code-review/SKILL.md) supplies a fresh
independent reviewer for behavior and governing-document changes. It accepts a
committed range or the complete work in progress; the responsible agent adjudicates
findings and fixes the candidate. Purely editorial documentation can be self-reviewed.
Delivery follows the repository's commit/push and optional PR conventions.
Readiness and Prompt Audit belong to the Unattended branch below; Direct Assisted
work can proceed directly from the accepted request.

## Turn an idea into a plan

- [grill-me](../skills/productivity/grill-me/SKILL.md) explores decisions in
  bounded Question rounds. It finishes with confirmed understanding and a chosen
  destination in the conversation. A later action carries that result forward.
- [grill-with-docs](../skills/engineering/grill-with-docs/SKILL.md) adds durable
  domain terms and accepted ADRs while discussing the idea. On completion, it
  follows the selected destination: conversation summary, Scratchpad, new Spec,
  existing tracked-item update, domain language or ADR.
- [to-spec](../skills/engineering/to-spec/SKILL.md) synthesizes established
  context into a new or updated tracker Spec.
- [to-tickets](../skills/engineering/to-tickets/SKILL.md) turns a plan, Spec or
  conversation into approved tracer-bullet Tickets with blocking/conflict relations,
  candidate ownership and delivery boundaries.

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

For **Unattended eligibility**, triage composes
[prompt-comprehension-audits](../skills/productivity/prompt-comprehension-audits/SKILL.md):

```text
audit requested: final contract → fresh interpreter → independent reviewer
                                → adjudication and applicable fit check → PASS / FAIL
explicit waiver: final contract → applicable fit/status checks → BYPASS
```

The audit also checks implementation-Ticket fit using to-tickets. A current PASS
or explicit BYPASS supports `ready-for-agent`; the maintainer's subsequent Mission
authorization selects execution. Requested Assisted and untracked prompt audits
use the same comprehension evidence where applicable and finish with their result.

## Deliver a coordinated Mission

Use Mission topology for several selected Tickets or real coordination. Availability
is a separate choice: **Assisted** with a maintainer available, or **Unattended**
with current durable contracts, resolved relations and the eligibility above.
Changing an ongoing Direct Assisted task to Unattended carries its recoverable state
into an explicitly authorized one-Ticket Mission.

There are three entries:

- One selected Ticket through [implement](../skills/engineering/implement/SKILL.md):
  it forwards a one-item plan to dispatch-tickets in the same root conversation.
- A finite phased plan through
  [dispatch-tickets](../skills/engineering/dispatch-tickets/SKILL.md): the dispatcher
  validates the supplied plan and starts a fresh coordinator for each runnable Ticket.
- One selected Ticket through a directly dispatched fresh
  [orchestrate](../skills/engineering/orchestrate/SKILL.md) coordinator, started by
  an authorized human/invoker or context-rich parent.

Each coordinator owns one Ticket's delivery:

```text
coordinator: resolve Ticket and prepare exclusive worktree
  → fresh writer: implement, verify, commit
  → coordinator: inspect and complete candidate
  → fresh code-review reviewer: return findings
  → coordinator: adjudicate, correct, verify, deliver and clean up
  → Ticket outcome
```

Writer and reviewer are isolated leaves. The coordinator retains decisions and
corrections. The dispatcher tracks compact outcomes and forwards user steering;
Ticket context stays with the coordinator.

A declared parallel group delivers branch artifacts for a later integration Ticket:

```text
phase 1: prerequisite Ticket
phase 2: compatible A + B → each delivers its verified pushed branch
phase 3: integration Ticket → combines exact A/B commits → delivers target
phase 4: dependent work
```

Parallel phases use established independence, shared-resource compatibility and
available runtime capacity. Each phase settles before the next; a failed, blocked,
cancelled or invalid outcome stops later dispatch while accepted siblings settle.
A Mission completes when every selected Ticket has a matching delivered outcome.

The [worktree policy](../skills/engineering/orchestrate/WORKTREES.md) covers candidate
placement, ownership, retained inputs and cleanup. [ADR 0002](adr/0002-acyclic-single-pass-orchestration.md)
owns the detailed phase, recovery, integration and delivery rules.

## Find a route through large or uncertain work

[wayfinder](../skills/engineering/wayfinder/SKILL.md) starts by clarifying the
destination with grill-with-docs. If the route becomes clear and fits one session,
it offers that simpler continuation. Otherwise it publishes a shared map and
investigation Tickets. A working session resolves one selected or available frontier Ticket:

```text
map → one investigation → answer in tracker → updated map
    → another session as needed → resolved destination
```

Research Tickets produce cited evidence; prototype Tickets seek a reaction to an
artifact; grilling Tickets resolve decisions; task Tickets complete preparation.
Human input participates where the investigation needs it. Once the destination
is actionable, choose the appropriate Direct Assisted or Mission delivery route.

## Investigate, repair and test

- [research](../skills/engineering/research/SKILL.md) answers a bounded question
  with evidence or produces a durable cited Markdown artifact. Work can be local
  or assigned to a fresh investigation worker; the caller validates the result.
- [diagnosing-bugs](../skills/engineering/diagnosing-bugs/SKILL.md) proceeds from
  reproduction through minimization, hypotheses and instrumentation to a verified
  cause. For an accepted fix, use a faithful regression test when a suitable seam
  exists; otherwise document the limitation and verify with before/after evidence.
  A request limited to diagnosis ends with the evidence and recommended next step.
- [tdd](../skills/engineering/tdd/SKILL.md) develops a change one red → green →
  refactor slice at a time, using the accepted caller-visible test seam. It uses
  [codebase-design](../skills/engineering/codebase-design/SKILL.md) for seam vocabulary.
- [resolving-merge-conflicts](../skills/engineering/resolving-merge-conflicts/SKILL.md)
  enters an existing merge/rebase, traces both sides' intent, resolves conflicts,
  runs checks and continues the Git operation through completion.

These are task-specific routes within the selected delivery mode. A bug fix can
combine diagnosis, TDD and review; a research question can finish with its answer.

## Explore architecture or an interface

[improve-codebase-architecture](../skills/engineering/improve-codebase-architecture/SKILL.md)
uses codebase-design vocabulary to scan for deepening opportunities, normally with
a fresh Explore worker, or locally when requested. The caller validates findings
and produces a visual HTML report. That report is a complete result.

When a candidate is selected, grill-with-docs develops its constraints, ownership,
seams and applicable domain/ADR updates. The optional
[Design It Twice](../skills/engineering/codebase-design/DESIGN-IT-TWICE.md) process
uses one fresh designer to compare interfaces when that specialist pass is selected.
Accepted implementation then follows the normal delivery route.

For visual or interaction work:

- [prototype](../skills/engineering/prototype/SKILL.md) creates a throwaway logic/state
  experiment or comparable UI variants, then records observations and trade-offs.
- [design](../skills/productivity/design/SKILL.md) grounds a visual direction in the
  product, designs the requested surface, and renders and checks interactions,
  accessibility and responsive states. Its result is the refined interface with
  verification evidence.

## Author skills or teach a topic

[write-a-skill](../skills/productivity/write-a-skill/SKILL.md) loads
[writing-great-skills](../skills/productivity/writing-great-skills/SKILL.md) and its
Glossary, establishes requirements, drafts the skill/resources, and verifies them.
Behavior changes receive independent code-review under the selected delivery route.
The result is the skill and its supporting files. writing-great-skills can also be
consulted directly for discovery, information hierarchy and pruning decisions.

[teach](../skills/productivity/teach/SKILL.md) maintains a learning workspace:
mission and resources → suitable lesson → practice and feedback → learning record.
Later sessions use that state to select the next target. Outputs include sourced
HTML lessons, reusable assets and reference material, with practitioner/community
input for questions that call for experiential judgment.

## Share policies and configure a repository

- [setup-omskills](../skills/engineering/setup-omskills/SKILL.md) records tracker
  operations, triage labels, domain-document locations and a verified model-routing
  pointer. Existing choices and authorized defaults drive setup. Tracker-backed
  consumers need their applicable configuration; domain docs enrich diagnosis,
  TDD, architecture scans and grilling when present. Untracked review and untracked
  prompt audits work from their supplied contracts. See the
  [setup dependency decision](adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md).
- [model-routing](../skills/productivity/model-routing/SKILL.md) and its
  [model table](../skills/productivity/model-routing/MODELS.md) guide callers before
  model-selectable delegation: explicit choices first, then task-based selection
  within authorized scope and harness support, with inheritance as the fallback.
  This applies to review, research, design, audit and coordination workers.
- [caveman](../skills/productivity/caveman/SKILL.md) compresses communication while
  preserving technical accuracy. The dispatcher loads it for compact reporting;
  it is also usable directly.

Cross-skill file pointers make these resources available on demand, including
user-only skills hidden from discovery. The referring skill supplies physical-path
resolution instructions for relative-symlink installations.

## Continue context or work through a visible agent

- [handoff](../skills/productivity/handoff/SKILL.md) writes a temporary Markdown
  continuation record and returns its path, linking durable sources and retaining
  the immediate next step and unresolved context.
- [wormhole](../skills/productivity/wormhole/SKILL.md) composes handoff, opens a
  fresh interactive conversation and transfers it. The destination restores the
  recorded state, follows its selected continuation to the first Safe turn boundary,
  then confirms the transfer and retires the origin Pi.
- [tmux-worker](../skills/productivity/tmux-worker/SKILL.md) opens a visible agent
  for continued dialogue. Its caller supplies the task, selects the model route,
  interprets results and directs retirement; the skill provides buffered messages,
  callbacks and window lifecycle. Research and architecture scans can use it.
  A Mission observer can also use this transport for caller-owned bounded checks
  of a dispatcher running in the visible window.

These utilities carry conversations and messages. Implementation ownership remains
with the workflow using them. A cooperative tmux callback is transport evidence;
managed subagent completion uses the harness's own settlement mechanism.

## Optional utilities

These two skills are available separately from the active plugin catalog:

- [excalidraw](../skills/productivity/excalidraw/SKILL.md): text or an existing scene
  → editable diagram → structural checks and visual inspection when available.
- [voice](../skills/productivity/voice/SKILL.md): selected useful responses → spoken
  summary → serialized audio submission and normal written response. It needs the
  private OMQueue/Edge TTS playback tools and the active harness's supported route.

For terminology, see [CONTEXT](../CONTEXT.md); for execution decisions, see
[ADR 0001](adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md) and
[ADR 0002](adr/0002-acyclic-single-pass-orchestration.md).
