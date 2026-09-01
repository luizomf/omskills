# Distributed skill-suite compatibility evidence

This audit originated as the catalog-wide evidence for Ticket #35 and now
maintains the live catalog and bundled-resource inventory. It is an evidence
record, not authorization to repair unrelated behavior. Named Ticket #35 and
runtime results are historical facts at their fixed commits; current workflow
claims follow `CONTEXT.md`, ADR 0002, Spec #52, Ticket #55, and the live skills.

## Scope and baselines

- **Historical Ticket #35 implementation base:**
  `8a0c2df5e3c771a7fc6bb3dd42ffd24c9c2ebcd2`.
- **Historical ompi runtime:**
  `c3aa6aa26878ce8c9f73cb51cf3b826b98439cd8`. The recorded focused run at that
  commit is runtime evidence only and does not define the current skill route.
- **Current integration base:**
  `5158449ab6ff7bb6822ace20b7f3104e4098f3e4`, followed by Ticket #55's catalog
  convergence candidate.
- **Live inventory:** the executable check derives active and optional skills
  from both manifests, frontmatter, the bucket tree, and bundled files. Counts
  are observations, not fixed test inputs.
- **Bundled inventory:** the executable check derives every non-`SKILL.md`
  bundled file and requires one complete schema row for each resource.
- **Governing evidence:** `CONTEXT.md`, ADR 0001, ADR 0002, Spec #52, Ticket #55
  and its current Prompt Audit, predecessor commits, and
  [the bounded delegated-helper audit](./2026-08-bounded-delegated-helpers.md).
  Ignored working notes are neither authority nor citations here.

Ticket #35's Prompt Audit remains durable historical evidence at
<https://github.com/luizomf/omskills/issues/35#issuecomment-5470868703>; it does
not define the current terminal two-pass Prompt Audit. Runtime inheritance and
native-session facts below are bounded to their named historical ompi run.

## Classification method

**Inherited clean baseline (ICB)** means a managed child receives the active
Pi and extension tools, required providers, normal skill installation and
agent-discoverable metadata, repository instructions and project context,
working directory, routing defaults, and environment. Its conversation starts
with the explicit child prompt only: no parent transcript, compaction summary,
or hidden continuation state. Restrictions may narrow this baseline; a role
name never grants capability. A user-only skill remains absent from model
context under ICB and requires explicit invocation or an installed-name
composition pointer.

**Delivery baseline** means a root interactive dependent helper may use one
asynchronous acceptance and one later pong, print mode returns directly, and a
depth-2 caller uses direct depth-3 settlement with no later pong. Depth-3
writer/reviewer/evidence leaves do not request depth 4. Native session
references recover bounded decision-bearing terminal evidence; research and
architecture still require their declared artifacts. TUI-only transports stay
outside this managed lineage.

**Compatible** means the current contract does not contradict the delivered
Ticket dispatcher / Ticket coordinator architecture. It does not mean that an
unrelated pre-existing limitation is fixed. **Compatible — preserved finding**
means the architecture is sound while the named limitation still needs
separate authorization. No skill below is classified as an architecture
blocker.

Evidence keys used below:

- **E1 — live contract reconstruction:** complete current skill and bundled
  resource reads against governing sources and predecessor history.
- **E2 — executable omskills scenarios:** dynamic catalog/resource schema,
  installer mechanics, Excalidraw base parsing, HITL shell syntax, and fake
  Queue/TTS command capture.
- **E3 — historical focused ompi runtime:** five subagent files at the named
  `c3aa6aa` commit; **5 test files passed; 70 tests passed**. Those fixed tests
  exercised asynchronous/direct delivery, inheritance/provider preflight, clean
  native sessions, depth, nested process lifetime, cancellation, bounded
  evidence, and presentation. They do not define current prompt semantics.
- **E4 — clean-context Prompt Audit:** Ticket #55's current PASS governs this
  integration contract. Older statuses remain historical at their exact
  contracts and do not define the present route.
- **E5 — risk boundary:** deterministic static reconstruction where real tracker,
  GUI, tmux, Queue/TTS, publishing, or user interaction would create external
  effects. No such live effect was submitted.

## Skill classifications

### `code-review`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/code-review`.
- **Invocation / composition:** selected for one committed or WIP candidate; the Ticket coordinator supplies the designated depth-3 reviewer contract and governing Standards/Spec inputs.
- **Inheritance / clean context:** ICB; one fresh reviewer receives only the self-contained candidate commands/material, contract, instructions, and result channel. Bounded findings are recovered from the native session or predeclared artifact.
- **Role / depth:** root caller may dispatch one reviewer; depth-2 coordinator uses one non-delegating depth-3 leaf; a depth-3 writer neither self-reviews nor requests depth 4.
- **Delivery / modes:** root interactive async or visible isolated, print and dependent depth-2 direct; no TUI dependency and no later pong after direct settlement.
- **Cancellation / effects:** reviewer is read-only; failed, interrupted, cancelled, missing, or unrecoverable evidence makes review incomplete and creates no correction loop.
- **Authorization / continuation / completion:** review grants no implementation authority; coordinator adjudicates accepted-source findings, corrects directly, and completes only after one full Standards/Spec pass is recovered.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1, E3, and predecessor bounded-helper evidence prove clean one-pass direct review and fail-closed recovery.

### `codebase-design`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/codebase-design`.
- **Invocation / composition:** direct architecture reference; `improve-codebase-architecture` composes it, and the optional Design It Twice branch is loaded only for a real interface tradeoff.
- **Inheritance / clean context:** current caller uses repository/domain evidence; an authorized designer receives ICB plus a self-contained design brief, never parent transcript.
- **Role / depth:** direct reference at any role; an authorized root or eligible depth-2 caller may use one non-delegating designer, but the one-Ticket graph adds no third specialist and depth-3 leaves return a blocker instead of requesting depth 4.
- **Delivery / modes:** reference work is mode-neutral; optional designer is root async/visible or print/depth-2 direct, with no TUI requirement.
- **Cancellation / effects:** reference use is read-only; cancellation of the optional pass yields no design evidence, and partial terminal text must be recovered before comparison.
- **Authorization / continuation / completion:** no implementation authority; accepted sources determine Ticket choices, otherwise the authorized caller resolves the tradeoff. Completion requires caller comparison of every recovered option.
- **Bundled resources:** `skills/engineering/codebase-design/DEEPENING.md`, `skills/engineering/codebase-design/DESIGN-IT-TWICE.md`.
- **Evidence / classification:** compatible — E1/E3 prove role-aware direct delivery and the explicit no-third-specialist/no-depth-4 branches.

### `diagnosing-bugs`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/diagnosing-bugs`.
- **Invocation / composition:** direct reproduction-first diagnosis; architecture findings are passed as recommendations rather than delegated from a depth-3 leaf.
- **Inheritance / clean context:** current-context workflow uses repository tools, domain docs, and ADRs; a clean assigned leaf receives ICB but no parent diagnosis history unless included in its brief.
- **Role / depth:** root or authorized writer leaf; no managed child call appears in the contract, so it cannot create depth 4.
- **Delivery / modes:** synchronous/direct; ordinary tests and scripts are headless, but the bundled HITL loop requires a real terminal and cannot be treated as an RPC dialog.
- **Cancellation / effects:** tool cancellation does not roll back temporary instrumentation or a partial fix; cleanup and original-symptom rerun remain explicit completion checks.
- **Authorization / continuation / completion:** diagnosis does not itself grant fix authority. Under authorized fix work, completion requires the original reproduction, regression evidence when a valid seam exists, and cleanup.
- **Bundled resources:** `skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh`.
- **Evidence / classification:** compatible — preserved finding — E1/E2 prove a non-delegating contract and valid shell syntax; no-TTY behavior and diagnosis-versus-fix authority remain separately authorized work.

### `dispatch-tickets`
- **Distribution / discovery:** active, user-only — `skills/engineering/dispatch-tickets`.
- **Invocation / composition:** explicitly invoked with one finite pre-resolved Mission plan, including a one-item plan composed by `implement`; composes installed `caveman`, its sole file read.
- **Inheritance / clean context:** root retains tools only for lifecycle preflight/inheritance; each fresh coordinator gets ICB and the exact minimal prompt, while user-only `orchestrate` is loaded by installed name rather than model discovery.
- **Role / depth:** canonical and only depth-1 Ticket dispatcher; starts one fresh depth-2 coordinator per runnable identity, with at most two declared-compatible coordinators in one active phase, and owns no implementation semantics.
- **Delivery / modes:** interactive asynchronous acceptance/pong or print direct settlement; declared compatible groups start together, phases remain sequential, and no polling, custom TUI, wormhole, or tmux dependency exists.
- **Cancellation / effects:** records matching intent, interrupts only the targeted active coordinator, lets accepted siblings settle, and maps only its confirmed interrupted return to cancelled; recursive managed cleanup is runtime-owned. It has no Queue/TTS or publishing effect.
- **Authorization / continuation / completion:** authorization is the frozen supplied topology; the dispatcher owns the phase cursor and literal targeted steering, advances only after every active identity returns matching delivered, stops on every other or invalid transition, and reports Mission complete only after all selected identities deliver.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E3 and predecessor delivery evidence cover plan/envelope validation, phase barriers, interactive/direct paths, cancellation, cleanup, and compact outcomes; prose meaning is governed by E4 rather than phrase assertions.

### `grill-with-docs`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/grill-with-docs`.
- **Invocation / composition:** deliberate planning interview; may route a confirmed Spec through `to-spec`, and records only user-confirmed domain terms/ADRs under their gates.
- **Inheritance / clean context:** current conversation and repository evidence are authoritative; a clean invocation gets ICB but only prompt-supplied prior decisions, never an implied transcript.
- **Role / depth:** interactive planning role, not dispatcher/coordinator/leaf implementation authority; isolated factual help is optional and does not select Tickets.
- **Delivery / modes:** conversational rounds; TUI/RPC can carry Questions, while print/headless stops at the visible Question or unresolved fact rather than claiming completion.
- **Cancellation / effects:** may have already written confirmed domain/ADR updates; cancellation does not roll them back or authorize later routing.
- **Authorization / continuation / completion:** user answers each Question and separately confirms understanding and destination; completion never implements and routing preserves Prompt Audit/Mission gates.
- **Bundled resources:** `skills/engineering/grill-with-docs/ADR-FORMAT.md`, `skills/engineering/grill-with-docs/CONTEXT-FORMAT.md`.
- **Evidence / classification:** compatible — E1/E5 show bounded interactive continuation without dispatcher authority or a hidden audited-leaf gate.

### `implement`
- **Distribution / discovery:** active, user-only — `skills/engineering/implement`.
- **Invocation / composition:** accepts exactly one explicitly Mission-authorized identity and, in the same root invocation, composes it unchanged as a one-item Mission plan through installed `dispatch-tickets`.
- **Inheritance / clean context:** adds no child context; the composed dispatcher retains the root's normal route for coordinator inheritance and performs no repository or tracker discovery.
- **Role / depth:** one-Ticket convenience entry only; it is neither dispatcher, coordinator, writer, nor reviewer and creates no child or alternate execution path.
- **Delivery / modes:** follows the loaded dispatcher's interactive or print path without adding another settlement mode.
- **Cancellation / effects:** owns no repository, tracker, lifecycle, or cancellation effect; these remain with the dispatcher and its coordinator.
- **Authorization / continuation / completion:** rejects anything other than one fully qualified selected Ticket, supplies empty complete relation arrays, and delegates all routing and delivery completion to `dispatch-tickets`.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E4 establish the single one-item composition route and user-only discovery state.

### `improve-codebase-architecture`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/improve-codebase-architecture`.
- **Invocation / composition:** caller loads `codebase-design`, delegates one Explore findings pass, writes/validates the report, and uses `grill-with-docs` only for a selected candidate.
- **Inheritance / clean context:** Explore receives ICB plus explicit scope, references, required fields, and artifact path; no parent conversation. Artifact and cited code, not terminal prose, are authoritative.
- **Role / depth:** root caller or authorized depth-2 helper caller; one non-delegating Explore leaf; depth-3 caller validates a supplied artifact or blocks rather than requesting depth 4.
- **Delivery / modes:** root async/visible, print direct, dependent depth-2 direct; report is headless-safe after validation and opener failure is non-fatal. No custom TUI is required.
- **Cancellation / effects:** cancellation invalidates an incomplete Explore pass; caller owns temporary findings/report and visible-worker retirement. Opener success never establishes completion.
- **Authorization / continuation / completion:** diagnosis/design only, not refactor authority; caller validates every candidate, then either completes the report or enters the separately selected grill.
- **Bundled resources:** `skills/engineering/improve-codebase-architecture/HTML-REPORT.md`, `skills/engineering/improve-codebase-architecture/PI.md`.
- **Evidence / classification:** compatible — preserved finding — E1/E3 prove nesting, artifact, and headless behavior; public HTML/Mermaid escaping remains separately authorized work.

### `orchestrate`
- **Distribution / discovery:** active, user-only — `skills/engineering/orchestrate`.
- **Invocation / composition:** only `dispatch-tickets` loads it into one fresh coordinator for exactly one Mission-authorized Ticket; the coordinator composes one writer plus one `code-review` reviewer.
- **Inheritance / clean context:** depth-2 coordinator receives ICB from the dispatcher but no root transcript; it independently reads complete live governing/setup/repository context. Each leaf is another clean explicit assignment.
- **Role / depth:** depth-2 Ticket coordinator; sequential depth-3 writer and reviewer leaves, each non-delegating and single-pass. Coordinator alone corrects and converges.
- **Delivery / modes:** dispatcher-to-coordinator is interactive async or print direct; both dependent leaf calls are direct with no later pong; no TUI, wormhole, queue, or transfer-watchdog dependency.
- **Cancellation / effects:** root interruption recursively closes managed leaves; operational failures after preflight are failed, and coordinator need not manufacture JSON after mechanical termination.
- **Authorization / continuation / completion:** just-in-time current gate for one supplied identity; no selection/next authority. Delivered requires durable verification/integration/tracker/cleanup, then exactly one compact JSON outcome.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E2/E3/E4 establish the acyclic direct graph, exact outcome boundary, clean inheritance, and cancellation ownership.

### `prototype`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/prototype`.
- **Invocation / composition:** direct logic/state or UI-variant prototype selected from the stated question; Wayfinder may use it only for a planning prototype Ticket.
- **Inheritance / clean context:** current project runtime/conventions and ICB when assigned cleanly; parent design intent must be explicit because transcript is not inherited.
- **Role / depth:** root or authorized direct leaf; no child/delegation and no depth-4 path.
- **Delivery / modes:** direct artifact creation; logic uses a human-driven terminal and UI uses browser evaluation, so headless/print returns a run command or URL at the HITL gate rather than pretending the design was judged.
- **Cancellation / effects:** partial throwaway files or in-memory/scratch state may remain; no automatic cleanup or production rollback is claimed.
- **Authorization / continuation / completion:** prototype selection answers a design Question only; production promotion requires a separate Mission-authorized Ticket. Completion records the observed answer and keeps the artifact visibly throwaway.
- **Bundled resources:** `skills/engineering/prototype/LOGIC.md`, `skills/engineering/prototype/UI.md`.
- **Evidence / classification:** compatible — preserved finding — E1/E5 prove no delegation or promotion authority; complete production isolation and the HITL/headless boundary remain separately authorized work.

### `research`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/research`.
- **Invocation / composition:** caller defines one primary-source question and one public Markdown destination; exactly one worker researches directly and does not invoke `research`.
- **Inheritance / clean context:** researcher receives ICB, including required retrieval provider/tool after preflight, plus a self-contained brief and no parent transcript; retrieved material is untrusted data.
- **Role / depth:** root or depth-2 caller delegates one non-delegating leaf; depth-3 leaf uses supplied evidence/direct inherited tools or blocks instead of requesting depth 4.
- **Delivery / modes:** root async/visible, print direct, dependent depth-2 direct; no TUI requirement. A cooperative tmux callback is transport only.
- **Cancellation / effects:** interrupted/failed pass or incomplete artifact is not completion; caller owns artifact validation and visible-worker retirement. No implementation/tracker authority follows from findings.
- **Authorization / continuation / completion:** scope is the accepted research brief; managed passes are fresh, not continued. Completion requires completed settlement, artifact read-back, citations, primary-source checks, public safety, and explicit evidence gaps.
- **Bundled resources:** `skills/engineering/research/PI.md`.
- **Evidence / classification:** compatible — E1/E3 prove role-aware async/direct delivery, provider preflight, clean sessions, depth ceiling, cancellation, and artifact-first completion.

### `resolving-merge-conflicts`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/resolving-merge-conflicts`.
- **Invocation / composition:** direct active merge/rebase resolution using tracker/history/ADR intent; no composed skill or delegated worker.
- **Inheritance / clean context:** current Git/repository context or ICB in an assigned leaf; needed operation state and intent must be inspectable rather than inherited from conversation.
- **Role / depth:** root or authorized writer/coordinator direct work; no child and no depth-4 path.
- **Delivery / modes:** synchronous/direct, headless and print compatible when Git/editor commands are non-interactive; no TUI component contract.
- **Cancellation / effects:** Git index/worktree/operation state can remain partially changed; skill preserves unrelated state but promises no transactional rollback.
- **Authorization / continuation / completion:** resolution stays inside established intent; unresolved intent blocks with operation unchanged. Active merge/rebase completion repeats until Git settles.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — preserved finding — E1 establishes topology compatibility; standalone-marker discovery and explicit staged-diff verification remain separately authorized work.

### `setup-omskills`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/setup-omskills`.
- **Invocation / composition:** explicit interactive repository setup using tracker/domain/label seed templates; hard-dependency skills point here only from standalone interactive use.
- **Inheritance / clean context:** current repository evidence and installed skill list are inputs; a clean invocation gets ICB but no prior approvals unless supplied in the prompt or files.
- **Role / depth:** root configuration workflow, never Ticket dispatcher; a headless Ticket coordinator reports missing setup instead of invoking it.
- **Delivery / modes:** conversational Questions and final draft approval require an interactive owner; RPC/TUI may carry them, while print/headless stops with the setup blocker/gate.
- **Cancellation / effects:** approved file and remote label writes already performed remain; partial setup must be reported and rerun deliberately, not inferred complete.
- **Authorization / continuation / completion:** user confirms choices and exact output; completion requires every approved config file and mapped tracker label. It grants configuration, not Mission authority.
- **Bundled resources:** `skills/engineering/setup-omskills/domain.md`, `skills/engineering/setup-omskills/issue-tracker-github.md`, `skills/engineering/setup-omskills/issue-tracker-gitlab.md`, `skills/engineering/setup-omskills/issue-tracker-local.md`, `skills/engineering/setup-omskills/triage-labels.md`.
- **Evidence / classification:** compatible — E1/E5 confirm the standalone interactive/headless blocker split and no dispatcher mediation.

### `tdd`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/tdd`.
- **Invocation / composition:** direct red-green-refactor discipline, normally used by the Ticket coordinator's assigned writer; uses `codebase-design` seam vocabulary and disclosed test/mocking references.
- **Inheritance / clean context:** current repository runner/domain/ADR context or ICB in a clean writer; accepted source-confirmed seams are explicit inputs, not parent-memory assumptions.
- **Role / depth:** root or depth-3 writer leaf; no managed child and no depth-4 path.
- **Delivery / modes:** synchronous/direct and TUI-independent; standalone interactive may ask the explicit seam Question, audited Ticket mode blocks unresolved material seams, and other print/headless use stops rather than waits.
- **Cancellation / effects:** cancellation may leave one red/green/refactor slice in progress; rerunning the current and prior relevant tests establishes resumable state.
- **Authorization / continuation / completion:** PASS/BYPASS sources resolve established seams without a new user gate. Every vertical slice completes only after demonstrated red, minimal green, and passing refactor.
- **Bundled resources:** `skills/engineering/tdd/mocking.md`, `skills/engineering/tdd/tests.md`.
- **Evidence / classification:** compatible — E1/E4 and predecessor #36 prove source-resolved authority, explicit blocker routing, and no delegated leaf gate.

### `to-spec`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/to-spec`.
- **Invocation / composition:** synthesizes established conversation/repository/Scratchpad information and publishes one new or updated Spec; it does not interview or implement.
- **Inheritance / clean context:** current established inputs plus configured tracker/domain docs; in a clean context only supplied artifacts and repository evidence count, never imagined conversation history.
- **Role / depth:** root planning/tracker role, not dispatcher/coordinator; no child/depth semantics.
- **Delivery / modes:** direct tracker workflow with no custom TUI; missing setup is interactive setup only at root and a blocker in headless Ticket use.
- **Cancellation / effects:** a created/updated issue or removed temporary continuation file is an external/durable effect and is not rolled back by harness cancellation.
- **Authorization / continuation / completion:** publishing creates planning authority only, with no readiness or Mission authorization. Completion preserves all established content, marks unknowns, and adds no unstated decision.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E5 show explicit tracker ownership and no dispatcher, implementation, or child-selection authority.

### `to-tickets`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/to-tickets`.
- **Invocation / composition:** interactive approved tracer-bullet breakdown; creates every identity first and then parent/blocking/conflict relations.
- **Inheritance / clean context:** current plan/Spec/conversation and configured tracker/domain/triage docs; clean use must read supplied sources completely rather than inherit prior turns.
- **Role / depth:** root planning/tracker role with no child; does not dispatch or coordinate implementation.
- **Delivery / modes:** direct external tracker work after an interactive breakdown approval; print/headless stops at the approval gate unless accepted approval is already supplied.
- **Cancellation / effects:** partially created tracker identities/edges require explicit reconciliation; publication is not transactional.
- **Authorization / continuation / completion:** every Ticket starts `needs-triage`; later authorization supplies a finite pre-resolved plan to `dispatch-tickets`, with `implement` available only to compose a one-item plan. Completion never applies readiness or starts work.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E5 establish correct dispatcher routing without granting dispatcher authority to planning.

### `triage`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/triage`.
- **Invocation / composition:** tracker state machine for a named item, attention query, override, or ready-work query; composes `grill-with-docs` and Prompt Audit only under its recorded branches.
- **Inheritance / clean context:** configured tracker/labels/domain docs and full item evidence; clean use gets ICB but must read body/comments/diff rather than rely on parent summaries.
- **Role / depth:** maintainer-facing tracker role, not dispatcher; composed audit isolation follows its own depth contract and readiness does not select work.
- **Delivery / modes:** interactive recommendation/approval for normal transitions; headless print can report candidates/evidence but stops at maintainer gates. No custom TUI.
- **Cancellation / effects:** comments, labels, closures, and out-of-scope files already written persist; every final state requires exact reconciliation.
- **Authorization / continuation / completion:** maintainer-approved state plus current audit controls eligibility only. A ready-work query never becomes Mission authorization or an ordered dispatcher input.
- **Bundled resources:** `skills/engineering/triage/AGENT-BRIEF.md`, `skills/engineering/triage/OUT-OF-SCOPE.md`.
- **Evidence / classification:** compatible — E1/E5 prove eligibility/selection separation and no dispatcher work discovery.

### `wayfinder`
- **Distribution / discovery:** active, agent-discoverable — `skills/engineering/wayfinder`.
- **Invocation / composition:** charts one map or resolves one investigation Ticket per session; may compose research, prototype, or grilling according to Ticket type.
- **Inheritance / clean context:** configured tracker Wayfinding operations, map body, selected child, domain docs, and explicit Notes; clean sessions load only needed linked decisions, not all prior ticket transcripts.
- **Role / depth:** root planning/tracker role with no Mission cursor; transitive helper depth/mode rules remain owned by those helpers.
- **Delivery / modes:** direct tracker work; HITL types require interactive continuation, AFK research follows role-aware delivery, and print/headless stops at any real human gate.
- **Cancellation / effects:** claims/comments/closures/map edits are external durable effects and need reconciliation; one-Ticket-per-session limits abandoned work.
- **Authorization / continuation / completion:** plan by default; maps and ready Tickets never authorize destination implementation. Completion resolves one investigation or hands off before execution.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — preserved finding — E1/E5 show no dispatcher authority; live host-specific Wayfinder tracker operations were not exercised and any contract repair needs separate authorization.

### `caveman`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/caveman`.
- **Invocation / composition:** direct communication mode; `dispatch-tickets` composes it by installed name before adopting state.
- **Inheritance / clean context:** current conversation behavior; under ICB it carries no parent transcript and adds no capability, provider, or hidden state.
- **Role / depth:** role-neutral prose constraint at root/coordinator/leaf; owns no child or dispatcher lifecycle.
- **Delivery / modes:** TUI/RPC/print/headless neutral and synchronous; only compresses user-visible wording.
- **Cancellation / effects:** no external effect or cancellation ownership.
- **Authorization / continuation / completion:** grants no work authority or continuation boundary; preserves exact identifiers, warnings, and ordered procedures while active.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1 establishes the composition and no-authority boundary; current compressed-report behavior is not claimed from prompt text.

### `design`
- **Distribution / discovery:** active, user-only — `skills/productivity/design`.
- **Invocation / composition:** explicit command with the complete design request; inherited installation does not make it model-selected.
- **Inheritance / clean context:** explicit invocation may use ICB tools, repository conventions, cwd, and environment, but receives no parent visual rationale unless included in the request or repository.
- **Role / depth:** direct design/editor role with no child or Ticket dispatcher authority.
- **Delivery / modes:** direct; RPC/print/headless are valid only with a headless-safe renderer, otherwise limitations are reported. No custom TUI contract.
- **Cancellation / effects:** code/design edits and explicitly launched preview work are ordinary tool-owned effects; no rollback is promised.
- **Authorization / continuation / completion:** explicit design request controls scope, not Mission Ticket selection. Completion requires actual desktop/narrow rendering and primary interaction checks or an honest unverified limitation.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E2/E5 verify actual user-only installation state and fail-honest rendered completion without assigning child discovery.

### `excalidraw`
- **Distribution / discovery:** optional, user-only — `skills/productivity/excalidraw`.
- **Invocation / composition:** absent from default manifests/managed install; deliberate manual installation plus explicit invocation loads the full directory and relative base/reference.
- **Inheritance / clean context:** when explicitly invoked in a clean child it can use ICB read/write/render tools, but user-only metadata is not model-visible and no parent diagram intent is inherited.
- **Role / depth:** direct scene editor with no child or dispatcher role.
- **Delivery / modes:** direct and structurally headless/print capable; rendering is optional but the exact inspection level must be reported. No TUI requirement.
- **Cancellation / effects:** destination writes are skill-owned and the current write-before-verify sequence can leave an invalid/partial result; bundled base must remain unchanged.
- **Authorization / continuation / completion:** only the explicit target/base/request authorizes scene changes; completion requires parsing, reciprocal-binding checks, concept coverage, and reported visual/structural inspection.
- **Bundled resources:** `skills/productivity/excalidraw/REFERENCE.md`, `skills/productivity/excalidraw/assets/diagram-base.excalidraw`.
- **Evidence / classification:** compatible — preserved finding — E1/E2 parse the actual empty base and installation state; authority precedence, preservation, binding/geometry, and validate-before-commit need separate authorization.

### `grill-me`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/grill-me`.
- **Invocation / composition:** direct bounded decision interview; optional isolated factual assistance is evidence help, not Ticket dispatch.
- **Inheritance / clean context:** current conversation supplies decisions; a clean invocation has ICB but no prior answers unless explicitly provided.
- **Role / depth:** read-only planning role at root; no implementation, tracker, dispatcher, or required child authority.
- **Delivery / modes:** interactive rounds through TUI/RPC; print/headless exposes the frontier and stops for a later owner response instead of declaring completion.
- **Cancellation / effects:** stateless and read-only, so cancellation leaves no repository effect.
- **Authorization / continuation / completion:** user settles each Question and both final gates; completion reports a route only and cannot write it or authorize implementation.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E5 show bounded planning continuation and no Mission or dispatcher state.

### `handoff`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/handoff`.
- **Invocation / composition:** direct explicit compaction; `wormhole` composes it and uses its file as the only continuation context.
- **Inheritance / clean context:** records only undocumented state and cites durable sources; a fresh agent learns nothing else from the parent transcript under ICB.
- **Role / depth:** role-neutral context transport with no child or authority selection.
- **Delivery / modes:** synchronous filesystem artifact outside the workspace; TUI/RPC/print/headless neutral.
- **Cancellation / effects:** may leave one temporary Markdown file; it creates no automatic callback, session, or managed continuation.
- **Authorization / continuation / completion:** cannot invent work or authority. Completion is one public-safe, secret-redacted file and its exact path.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E5 align explicit handoff-only context with ompi clean-session inheritance.

### `prompt-comprehension-audits`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/prompt-comprehension-audits`.
- **Invocation / composition:** audit coordinator runs one interpreter and then one independent reviewer; tracked implementation fit composes `to-tickets`. It records one status and ends without repair, confirmation, dispatch, or implementation.
- **Inheritance / clean context:** every pass gets ICB but no parent turns/coordinator analysis/desired answer; asymmetric explicit pass inputs and native-session recovery preserve isolation.
- **Role / depth:** root audit coordinator may use depth-2 leaves; a depth-2 coordinator uses direct depth-3 leaves; depth-3 leaf cannot open a depth-4 audit and records FAIL.
- **Delivery / modes:** root interactive async sequential pongs; print and dependent depth-2 direct; no TUI requirement, no concurrent sibling passes, and no later direct pong.
- **Cancellation / effects:** failed/interrupted/cancelled/missing/unrecoverable pass records FAIL; tracker status comments/labels are durable effects owned by the audit coordinator.
- **Authorization / continuation / completion:** PASS/BYPASS establishes eligibility only; Mission authorization remains separate. Completion records exactly one status after coordinator adjudication and never creates adjacent work.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E3/E4 cover clean native sessions, asymmetric sequential passes, bounded recovery, cancellation FAIL, and the terminal audit boundary.

### `teach`
- **Distribution / discovery:** active, user-only — `skills/productivity/teach`.
- **Invocation / composition:** explicit teaching command; user-only status prevents inherited model selection, while relative format resources load with the active skill directory.
- **Inheritance / clean context:** ICB provides cwd/tools/environment but no parent learning conversation; durable workspace files are the intended continuation source.
- **Role / depth:** direct multi-session teacher with no managed child or Ticket dispatcher authority.
- **Delivery / modes:** interactive lessons and mission Questions fit TUI/RPC owner continuation; print/headless cannot complete a missing-mission interview and GUI opener availability is environmental.
- **Cancellation / effects:** multi-file workspace writes and opener processes are skill/tool-owned; managed cancellation supplies no atomic checkpoint or rollback.
- **Authorization / continuation / completion:** explicit learner interaction confirms mission changes and practice feedback; workspace state, not hidden transcript, carries continuation. Lesson completion requires cited content and one practice/feedback cycle.
- **Bundled resources:** `skills/productivity/teach/GLOSSARY-FORMAT.md`, `skills/productivity/teach/LEARNING-RECORD-FORMAT.md`, `skills/productivity/teach/MISSION-FORMAT.md`, `skills/productivity/teach/RESOURCES-FORMAT.md`.
- **Evidence / classification:** compatible — preserved finding — E1/E2/E5 verify actual user-only state and resource packaging; workspace isolation, continuation/opener behavior, cancellation consistency, and public-data safety need separate authorization.

### `tmux-worker`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/tmux-worker`.
- **Invocation / composition:** caller selects visible cross-harness transport and owns task/artifact/callback meaning; research and architecture may compose it only for visible cooperative work.
- **Inheritance / clean context:** fresh launcher owns discovery/profile/repository cwd; caller message is explicit and there is no managed parent transcript inheritance.
- **Role / depth:** generic transport outside managed subagent lineage; owns no Ticket order, coordinator semantics, or ompi depth guarantee.
- **Delivery / modes:** real tmux TUI only, never print; buffered literal multi-turn transport and cooperative callbacks are visible but not Accepted continuation by themselves.
- **Cancellation / effects:** caller directs one literal `/quit`; tmux owns pane/window lifecycle and there is no recursive managed-lineage cancellation promise.
- **Authorization / continuation / completion:** transport creates neither task authority nor Safe turn boundary. Send/callback/retirement completion is mechanical; caller decides workflow completion.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E5 preserve generic visible transport without dispatcher substitution or callback-based unattended completion.

### `voice`
- **Distribution / discovery:** optional, user-only — `skills/productivity/voice`.
- **Invocation / composition:** absent from default manifests/managed install; explicit manual installation and user-facing invocation are required, and clean children do not inherit voice mode as transcript state.
- **Inheritance / clean context:** explicit invocation needs inherited shell/PATH/environment plus private Queue/TTS commands; user-only metadata never becomes model discovery.
- **Role / depth:** owning user-facing response mode only; no managed child or Ticket dispatcher role and no internal coordinator side channel.
- **Delivery / modes:** direct Queue submission and written response; TUI is unnecessary and print/direct settlement ends at Queue acceptance without polling.
- **Cancellation / effects:** rejection before acceptance creates no playback; an accepted Queue job is outside managed subagent cancellation and may outlive root/child shutdown.
- **Authorization / continuation / completion:** explicit voice mode authorizes one safe spoken submission per user-facing response, not child narrative. Completion is one accepted submission or an accurate written failure.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — preserved finding — E1/E2/E5 use a fake `bq` capture with no Queue/TTS call; accepted work remains outside managed cancellation and must not become an internal coordinator side channel.

### `wormhole`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/wormhole`.
- **Invocation / composition:** explicit fresh interactive transfer; composes `handoff` and uses that file as the only continuation context.
- **Inheritance / clean context:** fresh launcher owns normal repository discovery/route, while handoff—not parent transcript—supplies recorded continuation state.
- **Role / depth:** generic interactive transport outside managed dispatcher/coordinator lineage; owns no Ticket list, work selection, or implementation authority.
- **Delivery / modes:** tmux TUI only; make-before-break callback and origin `/quit`, not RPC/print/direct subagent delivery.
- **Cancellation / effects:** origin remains alive until one definitive callback; tmux owns resulting pane/window state. Failed launch returns the handoff path instead of guessing.
- **Authorization / continuation / completion:** handoff-selected immediate action/gate/no-action controls the branch; transfer creates no authority. Completion requires restoration, first Safe turn boundary, exactly one callback, and origin retirement.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E5 show ordinary Ticket sequencing has no wormhole/watchdog dependency while the generic transfer remains valid.

### `write-a-skill`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/write-a-skill`.
- **Invocation / composition:** loads installed `writing-great-skills` and its glossary before drafting; creates one skill and only required disclosed resources/scripts.
- **Inheritance / clean context:** current accepted sources/repository context or ICB in a clean writer; no parent requirements are assumed unless included in the Ticket/conversation artifacts.
- **Role / depth:** root author or depth-3 audited writer leaf; no delegation, no Ticket-dispatch ownership, and no depth-4 path.
- **Delivery / modes:** direct and TUI-independent; standalone interactive may ask missing-requirement/review Questions, while audited/headless branches resolve sources or return a coordinator/caller blocker without waiting.
- **Cancellation / effects:** partial skill files may remain as ordinary worktree state; exhaustive checklist rerun determines completion.
- **Authorization / continuation / completion:** PASS/BYPASS accepted sources replace hidden user gates; material unresolved authority blocks directly. Completion accounts for every accepted use case and decision-bearing resource.
- **Bundled resources:** None.
- **Evidence / classification:** compatible — E1/E4 and predecessor #36 prove the audited-leaf authority split and no user review gate in headless delivery.

### `writing-great-skills`
- **Distribution / discovery:** active, agent-discoverable — `skills/productivity/writing-great-skills`.
- **Invocation / composition:** direct reference and required composition target of `write-a-skill`; glossary definitions govern every bold term.
- **Inheritance / clean context:** flat reference uses current skill/repository evidence; under ICB it adds no hidden transcript, provider, or capability.
- **Role / depth:** role-neutral reference with no child; Router Skill and canonical Ticket dispatcher remain explicitly distinct.
- **Delivery / modes:** TUI/RPC/print/headless neutral and synchronous; no external effect.
- **Cancellation / effects:** read-only reference with no cancellation ownership.
- **Authorization / continuation / completion:** discovery/readiness never selects Mission work; every Mission enters `dispatch-tickets`, `implement` only composes its one-item form, and `orchestrate` is dispatcher-loaded. Reference completion means every applicable discovery/hierarchy/splitting/completion/pruning rule and glossary term has been checked.
- **Bundled resources:** `skills/productivity/writing-great-skills/GLOSSARY.md`.
- **Evidence / classification:** compatible — E1/E4 independently cover the skill and glossary, active-user-only exceptions, explicit routing, and no leaf delegation.

## Bundled resource classifications

### `skills/engineering/codebase-design/DEEPENING.md`
- **Decision role:** decision-bearing dependency categories, seam discipline, and replace-don't-layer test policy.
- **Owner / loading:** `codebase-design` loads it for a known deepening cluster; it is not independently discovered.
- **Compatibility:** compatible with the dispatcher/coordinator architecture; it adds no role, child, transport, or authority.
- **Evidence:** E1 source reconstruction against TDD and optional designer boundaries.

### `skills/engineering/codebase-design/DESIGN-IT-TWICE.md`
- **Decision role:** decision-bearing authorization, depth, delivery, isolation, bounded recovery, and completion rules for one optional designer.
- **Owner / loading:** `codebase-design` loads it only for an authorized real interface tradeoff.
- **Compatibility:** compatible; explicitly forbids a third one-Ticket specialist and depth-4 delegation.
- **Evidence:** E1/E3 role-aware direct and over-depth runtime evidence.

### `skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh`
- **Decision role:** decision-bearing human-terminal reproduction template and captured-value format.
- **Owner / loading:** `diagnosing-bugs` copies/edits it only when human action is unavoidable.
- **Compatibility:** compatible with preserved finding; it is outside RPC dialog relay and needs a real terminal.
- **Evidence:** E1 plus E2 `bash -n`; no interactive run or external action was performed.

### `skills/engineering/grill-with-docs/ADR-FORMAT.md`
- **Decision role:** decision-bearing ADR qualification, placement, numbering, and concise record format.
- **Owner / loading:** `grill-with-docs` loads it only after separate user approval to record a qualifying decision.
- **Compatibility:** compatible; recording does not authorize implementation or dispatch.
- **Evidence:** E1 comparison with repository ADRs and domain gates.

### `skills/engineering/grill-with-docs/CONTEXT-FORMAT.md`
- **Decision role:** decision-bearing domain terminology structure, single/multi-context placement, and creation rules.
- **Owner / loading:** `grill-with-docs` loads it when a confirmed domain term must be recorded.
- **Compatibility:** compatible; inline confirmed documentation remains distinct from Ticket authority.
- **Evidence:** E1 comparison with `CONTEXT.md` and ADR 0001.

### `skills/engineering/improve-codebase-architecture/HTML-REPORT.md`
- **Decision role:** decision-bearing report scaffold, diagram language, styling, validation, and opener completion contract.
- **Owner / loading:** `improve-codebase-architecture` uses it after validating Explore findings.
- **Compatibility:** compatible with preserved finding; headless opener behavior is correct, while repository-derived HTML/Mermaid escaping is not claimed fixed.
- **Evidence:** E1/E3 bounded-helper audit and explicit non-fatal opener reconstruction.

### `skills/engineering/improve-codebase-architecture/PI.md`
- **Decision role:** decision-bearing Pi transport matrix, inheritance/leaf ceilings, artifact ownership, and caller completion rules.
- **Owner / loading:** `improve-codebase-architecture` loads it for Pi execution.
- **Compatibility:** compatible; root async/visible, print direct, depth-2 direct, and depth-3 blocker paths match runtime.
- **Evidence:** E1/E3 focused ompi runtime and tracked bounded-helper audit.

### `skills/engineering/prototype/LOGIC.md`
- **Decision role:** decision-bearing logic-prototype isolation, terminal interaction, run command, handoff, and non-promotion rules.
- **Owner / loading:** `prototype` loads it only for logic/state-model Questions.
- **Compatibility:** compatible with preserved finding; human terminal evaluation is an explicit HITL boundary.
- **Evidence:** E1/E5 static scenario reconstruction; no interactive TUI was started.

### `skills/engineering/prototype/UI.md`
- **Decision role:** decision-bearing existing/new route choice, variant switching, user evaluation, and production-promotion boundary.
- **Owner / loading:** `prototype` loads it only for UI appearance Questions.
- **Compatibility:** compatible with preserved finding; complete production subtree isolation is not claimed fixed.
- **Evidence:** E1/E5 reconstruction against the separate-authority production boundary.

### `skills/engineering/research/PI.md`
- **Decision role:** decision-bearing visible/async/print/nested transport, inherited provider preflight, depth ceiling, and retrieval trust policy.
- **Owner / loading:** `research` loads it for Pi worker execution.
- **Compatibility:** compatible; exact modes and no-depth-4 alternatives match delivered runtime.
- **Evidence:** E1/E3 focused inheritance, nesting, cancellation, and session evidence.

### `skills/engineering/setup-omskills/domain.md`
- **Decision role:** decision-bearing emitted domain-doc discovery, terminology, and ADR-conflict policy.
- **Owner / loading:** `setup-omskills` uses it as the approved `docs/agents/domain.md` seed.
- **Compatibility:** compatible; repository context remains coordinator/skill input, never dispatcher input.
- **Evidence:** E1 comparison with ADR 0001 and current repository setup.

### `skills/engineering/setup-omskills/issue-tracker-github.md`
- **Decision role:** decision-bearing GitHub issue, PR, label, and Wayfinding operation contract.
- **Owner / loading:** `setup-omskills` emits it only after GitHub selection and approval.
- **Compatibility:** compatible with preserved finding; no live tracker operation was used to claim host support under this Ticket.
- **Evidence:** E1/E5 command/static reconstruction; external mutation was intentionally not run.

### `skills/engineering/setup-omskills/issue-tracker-gitlab.md`
- **Decision role:** decision-bearing GitLab issue, MR, label, and Wayfinding operation contract.
- **Owner / loading:** `setup-omskills` emits it only after GitLab selection and approval.
- **Compatibility:** compatible with preserved finding; host tier/support remains an explicit fallback concern.
- **Evidence:** E1/E5 static reconstruction; no external GitLab operation was run.

### `skills/engineering/setup-omskills/issue-tracker-local.md`
- **Decision role:** decision-bearing local tracker paths, states, edges, and Wayfinding operation contract.
- **Owner / loading:** `setup-omskills` emits it only after local-Markdown selection and approval.
- **Compatibility:** compatible; local planning files still grant no Mission implementation authority.
- **Evidence:** E1 comparison with Scratchpad/Ticket terminology and ignore requirements.

### `skills/engineering/setup-omskills/triage-labels.md`
- **Decision role:** decision-bearing canonical category/state mapping and exactly-one-role rule.
- **Owner / loading:** `setup-omskills` emits and customizes it only when `triage` is installed.
- **Compatibility:** compatible; ready state is explicitly eligibility rather than Mission selection.
- **Evidence:** E1 comparison with `CONTEXT.md` and current configured mappings.

### `skills/engineering/tdd/mocking.md`
- **Decision role:** decision-bearing system-boundary mocking and dependency-injection guidance.
- **Owner / loading:** `tdd` loads it when a confirmed seam reaches an external dependency.
- **Compatibility:** compatible; mocks change test adapters, not roles, authorization, or dispatcher state.
- **Evidence:** E1 test-seam contract reconstruction.

### `skills/engineering/tdd/tests.md`
- **Decision role:** decision-bearing observable-behavior, anti-coupling, and non-tautological test examples.
- **Owner / loading:** `tdd` loads it when selecting/asserting caller-visible tests.
- **Compatibility:** compatible; examples preserve the confirmed-seam and audited-leaf authority contract.
- **Evidence:** E1 comparison with the red-green-refactor completion rules.

### `skills/engineering/triage/AGENT-BRIEF.md`
- **Decision role:** decision-bearing durable behavioral brief format and acceptance/scope rules.
- **Owner / loading:** `triage` loads it for ready-for-agent and ready-for-human outcomes.
- **Compatibility:** compatible; the brief records readiness but explicitly not Mission authorization.
- **Evidence:** E1 comparison with the live brief format; Ticket #35's revised brief and Prompt Audit remain historical evidence for their fixed contract.

### `skills/engineering/triage/OUT-OF-SCOPE.md`
- **Decision role:** decision-bearing rejected-enhancement knowledge-base format and lifecycle.
- **Owner / loading:** `triage` loads it for prior-rejection checks and maintainer-approved rejected enhancements.
- **Compatibility:** compatible; rejection records neither create adjacent Tickets nor authorize work.
- **Evidence:** E1 tracker-boundary reconstruction.

### `skills/productivity/excalidraw/REFERENCE.md`
- **Decision role:** decision-bearing Excalidraw element schema, reciprocal bindings, visual profile, and exhaustive checks.
- **Owner / loading:** `excalidraw` must load it before creating elements; it is bundled with optional manual installation.
- **Compatibility:** compatible with preserved finding; preservation/deleted-element/geometry conflicts are not claimed repaired.
- **Evidence:** E1/E2 comparison with the parsed base and current workflow.

### `skills/productivity/excalidraw/assets/diagram-base.excalidraw`
- **Decision role:** decision-bearing default canvas, shape, binding, typography, color, and roughness values for new scenes.
- **Owner / loading:** `excalidraw` loads it only when no target or supplied base exists and must never mutate it.
- **Compatibility:** compatible with preserved finding; default-precedence and roughness/alignment questions still need separate authorization.
- **Evidence:** E2 parsed a private-data-free empty standard scene and verified its bytes remained unchanged.

### `skills/productivity/teach/GLOSSARY-FORMAT.md`
- **Decision role:** decision-bearing learner-demonstrated terminology, ambiguity, and revision rules.
- **Owner / loading:** `teach` uses it for the durable teaching-workspace glossary.
- **Compatibility:** compatible with preserved finding; workspace/public-data safety remains unresolved outside this Ticket.
- **Evidence:** E1/E5 resource and continuation reconstruction.

### `skills/productivity/teach/LEARNING-RECORD-FORMAT.md`
- **Decision role:** decision-bearing sequential learning evidence, supersession, mission-shift, and completion criteria.
- **Owner / loading:** `teach` uses it when demonstrated learning or mission change qualifies.
- **Compatibility:** compatible with preserved finding; interrupted multi-file consistency is not claimed fixed.
- **Evidence:** E1/E5 cancellation and durable-state reconstruction.

### `skills/productivity/teach/MISSION-FORMAT.md`
- **Decision role:** decision-bearing one-workspace mission, observable success, constraint, and revision rules.
- **Owner / loading:** `teach` uses it before lesson selection and after confirmed mission changes.
- **Compatibility:** compatible with preserved finding; inherited-cwd workspace isolation and headless interview ownership remain open.
- **Evidence:** E1/E5 clean-context and workspace reconstruction.

### `skills/productivity/teach/RESOURCES-FORMAT.md`
- **Decision role:** decision-bearing high-trust knowledge/community source, gap, annotation, and pruning policy.
- **Owner / loading:** `teach` uses it before factual lesson authoring.
- **Compatibility:** compatible with preserved finding; public/private learner-data boundaries still require separate authorization.
- **Evidence:** E1/E5 source and public-safety reconstruction.

### `skills/productivity/writing-great-skills/GLOSSARY.md`
- **Decision role:** decision-bearing definitions for discovery, hierarchy, steering, completion, and pruning, including Router Skill versus Ticket dispatcher.
- **Owner / loading:** `writing-great-skills` requires every bold term to resolve here; `write-a-skill` must read it completely before drafting.
- **Compatibility:** compatible; user-only composition, active status, Mission authorization, and canonical dispatcher roles remain distinct.
- **Evidence:** E1/E4 independent complete read against the skill-authoring and audited-leaf contracts.

## Preserved findings

The following are **non-blocking for dispatcher/coordinator compatibility** and
are not fixed by this Ticket. Every behavior change needs separate
authorization; withdrawn or historical requests do not provide it.

1. **Diagnosis:** the HITL shell template has no defined no-TTY/headless verdict,
   and diagnosis-only versus fix authority is not fully expressed in the skill.
2. **Prototype:** complete production isolation of UI variants and the
   human-evaluation boundary in headless use need a focused contract.
3. **Architecture report:** repository-derived HTML/Mermaid escaping and loose
   Mermaid security remain public-artifact concerns.
4. **Wayfinder:** configured host-specific tracker operations still need
   environment-specific verification before claiming operational support.
5. **Merge conflicts:** standalone marker cleanup and explicit staged-diff
   verification are not fully specified.
6. **Teach:** workspace isolation, owner-chain continuation, opener behavior,
   cancellation-safe writes, and public-data safety remain unresolved.
7. **Excalidraw:** authority/default precedence, preservation, reciprocal
   binding and geometry, and validate-before-commit behavior remain unresolved.
8. **Voice:** an accepted Queue job remains outside managed cancellation. Voice
   is an explicitly invoked user-facing mode and must not become an internal
   coordinator side channel.

None of these limitations assigns work to the Ticket dispatcher, adds a
specialist to the one-Ticket graph, permits a depth-4 leaf, or changes Mission
authorization. No surviving dispatcher/coordinator contradiction was found.

## Verification record

Current verification is limited to repository-required gates, applicable local
installation mechanics, the dynamic catalog/resource schema, and executable
fixtures:

```text
./scripts/check-catalog.py
catalog ok: 27 active skills

./tests/test-link-skills.sh
linker tests ok

./scripts/link-skills.sh --check
27 active managed links reported ok

python3 tests/test-skill-suite-evidence.py
skill-suite evidence ok: inventory, schema, and executable fixtures complete

git diff --check 5158449ab6ff7bb6822ace20b7f3104e4098f3e4...HEAD
passed
```

The compatibility test executes the documented Voice command against a fake
`bq`, parses the Excalidraw base without mutation, and syntax-checks the HITL
template. Its remaining Markdown parsing checks deterministic inventory,
frontmatter, manifest, resource ownership, and row schema only; it makes no
prompt-meaning assertion.

**Historical only:** Ticket #35 recorded a five-file/70-test ompi run and a
then-current dispatcher semantic state-model test. The latter test was deleted
when phased dispatch landed and is not current suite evidence. Neither fixed
historical result defines the present prompt or routing contract.

## Boundaries and historical status

- `docs/audits/2026-07-pi-compatibility.md` is **Historical only**: it describes
  Pi 0.80.10, an older catalog, and pre-nested-helper limitations. It is not the
  current compatibility status and remains unchanged as history.
- The bounded delegated-helper audit remains historical focused predecessor
  evidence only at its recorded runtime and skill commits; its five-file result
  is not a current route claim.
- The Sannux audit documents its own later Ticket #41 fixed run. Its serial
  invocation and then-current tests remain historical, not present catalog or
  route evidence.
- No live Queue/TTS, tracker mutation, GUI opener, tmux transport, publishing,
  release, PR, push, or sibling-repository modification occurred.
