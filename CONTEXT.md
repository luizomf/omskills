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
A single tracked implementation unit inside an **Issue tracker**, sized to fit one fresh agent context with room for verification. A Ticket may be a bug, task, issue, investigation, or slice produced by `to-tickets`; it is not an interactive **Question**.
_Avoid_: backlog item, multi-agent implementation plan, interview question

**Scratchpad**:
A temporary, untracked, self-contained continuation record under an ignored `.scratch/` directory. It lets an agent with clean context recover established decisions, unresolved **Questions**, evidence pointers, and the recommended next action, but it is not a **Spec**, **Ticket**, ADR, or permanent documentation and carries no implementation authority.
_Avoid_: spec, ticket, ADR, permanent documentation, implementation plan

**Spec**:
The durable planning authority describing a problem, intended behavior, constraints, and established design guidance. A **Spec** guides code only through smaller **Tickets** and is never itself an implementation unit.
_Avoid_: PRD (use only when quoting external systems that call them PRDs), implementation ticket

**Triage role**:
A canonical category or state label applied to a **Ticket** during triage. Category roles are `bug` and `enhancement`; state roles include `needs-triage` and `ready-for-agent`. Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Prompt audit status**:
A durable result attached to one exact execution contract in the **Issue tracker**. `PASS` means no semantic divergence survived audit-coordinator adjudication and the Ticket fits one fresh agent context; `BYPASS` means a maintainer explicitly authorized autonomous delivery without a pass; `FAIL` means the audit did not establish equivalent comprehension or context fit. A current `PASS` or `BYPASS` authorizes autonomous implementation of that contract only. A material contract change makes its prior status stale.

**Mission envelope**:
The exact authorized Ticket identities, governing Specs, scope, deferrals, frozen queue, and completion boundary for one autonomous run. If authorization names a query or queue source, its current Ticket identities are resolved once when the run starts and then frozen. Authorization is non-transitive: findings and newly imagined work outside the envelope are reported, not converted into implementation.
_Avoid_: open-ended mandate, adjacent-work authorization

**Mission complete**:
The terminal state in which all work authorized by the **Mission envelope** has reached its required durable outcome. It describes the global mission, not merely the current agent turn or one dispatched worker.
_Avoid_: turn complete, worker accepted, work started

**Safe turn boundary**:
A state in which the current agent turn may end without abandoning authorized work. It exists only when the **Mission envelope** is complete, genuinely blocked with no independent authorized work runnable, waiting at an explicit user gate, or protected by an **Accepted continuation mechanism**.
_Avoid_: work started, context restored, intent stated

**Accepted continuation mechanism**:
An acknowledged asynchronous operation whose harness-owned lifecycle documents automatic completion delivery or an owning-session reentry attempt without requiring a delegated agent to understand and execute a separate callback instruction. This contract does not claim that a process, host, network, or owning session cannot fail. A cooperative textual callback or a background process with no automatic return path does not qualify by itself.
_Avoid_: guaranteed wake, worker promise, background activity

**Transfer watchdog**:
An experimental one-shot delayed owning-session wake, initially fixed at five minutes, used only when `orchestrate` transfers an active **Mission envelope** through `wormhole`. Through the active harness's documented capability, it lets the origin coordinator detect the absence of the fresh coordinator's safe-boundary callback and, when the fresh editor displays its normal input-ready state under existing transfer semantics, send one continuation reminder. It never repeats, interprets pane text as workflow state, interferes with a busy fresh coordinator, takes over the mission, or closes the origin without the callback. After either timeout branch, the origin remains alive awaiting that callback or user recovery. It is optional when the harness has no delayed owning-session wake.
_Avoid_: mission heartbeat, pane monitor, automatic timeout closure

## Relationships

- An **Issue tracker** holds many **Specs** and **Tickets**
- A **Question** is resolved in a live interaction and may inform a later **Scratchpad**, **Spec**, or **Ticket**
- A **Scratchpad** may preserve temporary planning context and be removed after accepted content reaches a durable artifact, but it carries no implementation authority
- A **Spec** is broken down into many **Tickets** and is never implemented directly
- A triaged **Ticket** carries one category **Triage role** and one state **Triage role**
- A code or behavior-changing **Ticket** becomes `ready-for-agent` only with a current `PASS` or explicit `BYPASS` **Prompt audit status**
- A current `PASS` or `BYPASS` transfers in-scope implementation decisions to the autonomous coordinator; it does not create another user decision gate, and ordinary uncertainty, preference, or a source-resolved choice cannot be converted into one
- Text or documentation work that cannot change behavior does not require a **Prompt audit status**
- A **Ticket** may retain multiple historical **Prompt audit statuses**, but only its newest applicable status governs that exact contract
- Every Ticket supplied for an initial `orchestrate` **Mission envelope** must have a current `PASS` or `BYPASS`; one missing initial gate blocks the whole mission before selection or dispatch, without filtering or partial execution, while a gate that becomes stale only after a fully authorized mission starts blocks that Ticket and lets other independent authorized Tickets continue
- An autonomous coordinator may end a turn while its **Mission envelope** still contains authorized runnable work only after an **Accepted continuation mechanism** starts; otherwise it must continue until the mission is complete, genuinely blocked, or waiting at an explicit user gate
- `wormhole` owns the generic **Safe turn boundary** for a fresh continuation, while the governing workflow defines the concrete accepted continuation mechanism; for `orchestrate`, that mechanism is an accepted isolated-writer dispatch
- On the final `orchestrate` Ticket, an accepted writer creates only a **Safe turn boundary**; **Mission complete** still requires every later wake, review, correction, integration, tracker, and cleanup obligation to reach the mission's durable completion boundary
- A `wormhole` jump reports completion and retires the origin Pi only after the fresh continuation restores its handoff and reaches its first **Safe turn boundary**; that callback, not pane-buffer interpretation, is the transfer source of truth
- When `orchestrate` sends an active **Mission envelope** through `wormhole`, the origin owns and arms one **Transfer watchdog**, retains transfer and retirement responsibility, and releases its branch only after one definitive safe-boundary callback; the fresh coordinator focuses on the mission and owes only that callback after reaching its first **Safe turn boundary**
- A `wormhole` transfer remains available without a **Transfer watchdog** when the harness lacks a delayed owning-session wake; an external delayed-message helper is optional operator tooling, not a distributed skill dependency, and may serve as a fallback only when its lifecycle is known
- Any external watchdog fallback that returns a process handle must be canceled before the origin retires after an early safe-boundary callback; an uncancelled delayed injection cannot target a pane whose lifecycle has ended
- A `wormhole` handoff's recorded authorized immediate action, explicit user gate, or absence of authorized action selects the continuation branch; `wormhole` transfers context but does not create work or implementation authority
- With no authorized immediate action, restoring the fresh interactive context is itself a **Safe turn boundary**; with direct authorized action and no workflow-specific asynchronous boundary, the fresh coordinator continues until completion, the recorded gate, or a genuine blocker, then sends the same definitive callback
- `tmux-worker` owns only visible tmux transport and lifecycle: opening the worker window, sending literal messages, receiving callbacks, supporting further dialogue, and retiring the worker when directed; the invoking agent or skill owns message semantics, task instructions, artifacts, completion, post-callback decisions, and whether its current turn may end
- `tmux-worker` remains a cooperative interactive transport and does not imitate a scheduler or impose an unconditional yield after sending a message
- A cooperative `tmux-worker` callback is a transport event, not an **Accepted continuation mechanism** by itself, and cannot justify ending an unattended autonomous turn

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "issue" remains acceptable when the underlying tracker calls a work item an issue, but the skill vocabulary now uses **Ticket** for implementation slices and **Spec** for durable planning documents.
