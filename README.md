# omskills

A practical skill collection for keeping agent-assisted software work structured, reviewable, and less likely to jump from a vague idea straight into code.

## Origin

This repository started as a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), first copied on May 24, 2026, and has since pulled in selected changes from later upstream snapshots.

This is not the original repository. To see the source project, use [mattpocock/skills](https://github.com/mattpocock/skills).

This repository is maintained independently and does not track or synchronize with the original. Useful ideas may be implemented here deliberately under this project's own conventions.

## What This Is

`omskills` is not runtime application code. It is a curated set of agent skills, prompts, setup docs, and helper scripts for working with Codex and other coding agents.

For ordinary work, the default is Direct Assisted delivery: one conversational responsible agent handles an untracked request or exactly one selected Ticket while the maintainer remains available. Use only the planning and implementation skills the request needs.

For coordinated or Unattended work, the planned Mission flow is:

`idea -> grill -> spec -> tickets -> prompt audit -> explicit authorization -> dispatch -> implementation -> review -> optional PR -> handoff`

The skills act as proportionate checkpoints: clarify before planning, document durable authority before changing it, triage and audit Unattended work, test before coding, review behavior and governing documents before shipping, and hand off before context is lost.

### Runtime Relationship with ompi

This collection has no package or checkout dependency on [ompi](https://github.com/luizomf/ompi), and many skills remain usable in any compatible coding-agent harness. However, the advanced Mission-oriented `implement` -> `dispatch-tickets` -> `orchestrate` workflow depends on isolated subagents, bounded nesting, direct and asynchronous delivery, capability inheritance, and managed cancellation semantics currently implemented and validated by ompi. Using that workflow outside ompi requires a harness that provides the same contract. A human/invoker or context-rich parent may also dispatch one fresh isolated `orchestrate` coordinator directly for smaller Mission work; this still requires explicit selected-Ticket authorization, applicable live gates and actual child capabilities, not parent provenance or role/depth assertions. Ordinary Direct Assisted work does not require this graph. These texts prescribe prompt obligations, not runtime guarantees. Parallel groups require affirmative active ROOT capacity and same-batch start evidence in the current transport mode; child limits or an absent bound cannot establish capacity. Its Ticket identity format is currently `owner/repository#integer`; local Markdown paths and nested GitLab namespaces are not supported by this delivery route, even though planning and triage support those trackers.

The relationship also runs in the other direction: ompi's skill-enabled profiles consume selected skills from this repository. Each repository remains independently installed and maintained; neither checkout is synchronized from the other.

## Operating Model

Before asking an agent to "build it", resolve delivery topology and maintainer availability independently. Read-only exploration may happen first, but implementation mutation waits for this adaptive semantic gate. Do not turn it into a fixed questionnaire: ask only about a materially unresolved dimension and accept choices already clear from the request.

- Untracked request or exactly one selected Ticket, with the maintainer available and no real coordination: use Direct Assisted delivery. The conversational responsible agent owns the work end to end; readiness, Prompt Audit, dispatcher, separate coordinator, and writer are not required by default.
- Multiple selected Tickets or real dependency, conflict, integration, shared-resource, or multiple-writer coordination: use Mission topology. A Mission may be Assisted or Unattended.
- Moving Direct Assisted work to Unattended: preserve recoverable state and establish durable contracts, resolved relations, a current Prompt Audit `PASS` or explicit `BYPASS`, and explicit one-Ticket Mission authorization. Silence is not authorization.

Then select only the skills the work needs:

- Need to think through an idea: `/grill-me` or `/grill-with-docs`
- The work is too large or foggy for one session: `/wayfinder`
- Know the goal, but not the implementation Tickets: `/to-spec`, then `/to-tickets`
- Want one explicitly Mission-authorized Ticket delivered through the dispatcher route: `/implement`
- Want a Mission-authorized phased plan dispatched: `/dispatch-tickets`
- Want the diff checked before it ships: `/code-review`
- Something broke: `/diagnosing-bugs`
- Need high-trust reading legwork: `/research`
- The architecture is getting muddy: `/improve-codebase-architecture`
- Want to learn a topic over multiple sessions: `/teach`
- Need to pause without losing context: `/handoff`
- Need a fresh agent window that retires the old Pi after transfer: `/wormhole`

For `/implement`, select one fully qualified Ticket, state Assisted or Unattended availability, and confirm that its external blockers and conflicts are resolved; the convenience entry does not inspect the tracker. Direct dispatch of one fresh coordinator is also allowed for Mission work; when `/dispatch-tickets` is used, its root remains strictly mechanical.

Every implementation Ticket handled through the managed Mission route owns an exclusive coordinator-established worktree and branch; writer, reviewer, corrections and checks share its exact candidate/base/HEAD handoffs. Approved parallel plans include an ordinary integration Ticket blocked by every member. Members deliver verified pushed branch artifacts with durable repository/remote branch/full-SHA tracker evidence; integration delivers the verified combined state to its declared target before dependent work. Other Tickets state their target and direct-push or pull-request method explicitly. Pull requests are optional unless repository policy or the accepted request requires one; every used pull request is squash-merged with a durable source-to-squash mapping. After target verification and completion of all integration consumers, remove clean owned worktrees and delete verified-delivered local and remote source branches; expected lack of ancestry after squash does not prevent deletion. Preserve unrelated, failed, cancelled, dirty, undelivered, or still-consumed work. Prefer independent investigations and Ticket phases in parallel when independence, capacity, shared resources, and integration boundaries are established; otherwise fail closed or plan serial work rather than silently changing an authorized group.

Direct Assisted code or behavior changes receive one fresh independent review. Specs, ADRs, workflow, security, and other governing documents are also first-class review subjects; only purely editorial documentation may be self-reviewed.

The core habit is to ask: "Is this clear enough to become code?"

If the answer is not clearly yes, use grill, triage, specs, tickets, research, or wayfinder before implementation.

If there is a conflict, architectural ambiguity, unresolved dependency, or two plausible options with real tradeoffs, stop and discuss.

## Common Scenarios

### New Empty Project

The risk in an empty repo is inventing too much architecture too early.

1. Create the minimum project identity: `README.md`, `AGENTS.md`, license if needed, and the stack decision if it is already known.
2. Run `/setup-omskills` before tracker-backed planning or delivery to record the issue tracker, triage labels, and docs layout.
3. Use `/grill-with-docs` before substantial coding when domain language, constraints, or the smallest useful slice remains unclear.
4. Use `/to-spec` when the direction needs durable planning authority.
5. Use `/to-tickets` when the Spec needs multiple small, vertical implementation units.
6. For one bounded request with the maintainer available, proceed through Direct Assisted delivery once the adaptive gate is resolved. Use `/implement` only when selecting the Mission route; Unattended execution also requires `ready-for-agent`, a current Prompt Audit `PASS` or explicit `BYPASS`, and explicit authorization.

Good prompt:

```text
Before implementing, help identify the smallest useful first slice.
```

### Existing Project Without These Skills

The risk in an existing project is enforcing process before understanding the system.

1. Start with normal repo exploration and, when the request is broad, `/research` or `/wayfinder`.
2. Run `/setup-omskills` when tracker-backed planning or delivery needs repository configuration.
3. Use `/grill-with-docs` if project language is unclear or undocumented.
4. Use `/triage` when a tracked request is unclear or needs Unattended eligibility established.
5. Use `/improve-codebase-architecture` when coupling or structure needs attention; treat the output as diagnosis and issue material, not blanket permission to refactor.
6. Use Direct Assisted delivery for one bounded request while the maintainer is available. Use `/implement` for an explicitly authorized one-Ticket Mission; Unattended execution also requires a mature `ready-for-agent` Ticket and a current Prompt Audit `PASS` or explicit `BYPASS`.

Good prompt:

```text
Before changing code, explain how this request fits into the current system.
```

### Project Already Using These Skills

The risk in a prepared repo is ignoring decisions that already exist.

1. Read the local instructions and context: `AGENTS.md`, `CONTEXT.md`, `docs/agents/*`, and `docs/adr/*`.
2. Start from an existing issue or Ticket when durable authority already exists or the work must survive the conversation.
3. Use `/triage` if tracked work is unclear or needs Unattended eligibility established.
4. Use Direct Assisted delivery for one bounded selected Ticket while the maintainer is available. Use `/implement` only for an explicitly authorized one-Ticket Mission; Unattended execution additionally requires maturity, `ready-for-agent`, acceptance criteria, and a current Prompt Audit `PASS` or explicit `BYPASS`.
5. Use `/grill-with-docs` if the issue conflicts with domain language or decisions.
6. Stop and discuss when the task conflicts with an ADR, changes architecture, or has meaningful tradeoffs.
7. Use `/handoff` before pausing a long session.

Good prompt:

```text
Follow the repo instructions, read the issue, and tell me whether it is ready for implementation.
```

## Local Quickstart

1. Link the active skills into local Codex. This requires Bash, `jq`, and Python 3.9 or newer:

```bash
./scripts/link-skills.sh
```

The installer creates relative symlinks, prunes only obsolete symlinks
managed by this repository, and refuses to overwrite real paths or external
symlinks. Relative targets avoid embedding a username or absolute home path
when the same checkout layout is used across macOS and Linux. Verify the
current installation without changing it:

```bash
./scripts/check-catalog.py
./scripts/link-skills.sh --check
```

By default, the script writes to `~/.agents/skills`, the shared user-level skills directory used by current Codex surfaces. On the first default installation, it safely removes this repository's managed links from the legacy `~/.codex/skills` location while preserving unrelated content. To test another destination:

```bash
OMSKILLS_DEST=/tmp/omskills-test ./scripts/link-skills.sh
```

Active skills are installed by the plugin independently of discovery state. Supporting harnesses include agent-discoverable skills in the model's system context, while active user-only skills remain installed without permanent context load. `design`, `teach`, `dispatch-tickets`, `implement`, and `orchestrate` are the current active user-only skills. Select `design`, `teach`, `dispatch-tickets`, or `implement` deliberately; `orchestrate` is loaded explicitly in a fresh coordinator by an authorized direct caller or the dispatcher. The groupings below describe the selection and composition path, not discovery status.

2. In each repo that will consume these skills, run:

```text
/setup-omskills
```

This setup records where issues live, which triage labels the repo uses, and how the agent should consume `CONTEXT.md` and ADRs. All `.scratch/` artifacts stay local and Git-ignored; choose paths as needed and prefer the durable issue tracker for project-relevant requirements, decisions, and delivery history.

## Triage Model

The skills use two category roles and five state roles. Each repo can map those roles to real labels in `docs/agents/triage-labels.md`.

Categories:

- `bug`: something is broken.
- `enhancement`: new feature or improvement.

States:

- `needs-triage`: maintainer needs to evaluate.
- `needs-info`: missing information from the reporter/author.
- `ready-for-agent`: well-specified issue eligible for Unattended execution when a current Prompt Audit gate and explicit Mission authorization also exist; the state does not select the issue and is not required for Direct Assisted work by default.
- `ready-for-human`: needs human implementation or decision-making.
- `wontfix`: will not be actioned.

For mature projects, the eligible Ticket set should favor small, vertical, verifiable units. Changes to shared systems such as architecture, runtime, persistence, deployment, or AI integration need to be mature before implementation. A ready-work query only discovers eligible Tickets; explicit user or invoker direction selects one Ticket or supplies a finite pre-resolved Mission plan.

## Active Skills

### Engineering

**Typically user-selected**

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: runs bounded Question rounds while maintaining domain language and ADRs.
- **[triage](./skills/engineering/triage/SKILL.md)**: moves issues and external PRs through a state machine based on triage roles.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: scans a codebase for deepening opportunities and presents a visual report with a top recommendation.
- **[setup-omskills](./skills/engineering/setup-omskills/SKILL.md)**: configures issue tracker, triage labels, and docs layout per repo.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: turns the current conversation context into a spec and publishes it to the issue tracker.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: breaks a plan, spec, or conversation into tracer-bullet tickets with blocking and conflict edges.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: maps a huge or foggy effort into investigation tickets on the issue tracker.
- **[dispatch-tickets](./skills/engineering/dispatch-tickets/SKILL.md)**: dispatches one finite pre-resolved Assisted or Unattended Mission plan from the canonical minimal root.
- **[implement](./skills/engineering/implement/SKILL.md)**: composes one explicitly authorized Ticket as a one-item Assisted or Unattended Mission through `dispatch-tickets`.

**Fresh-coordinator execution**

- **[orchestrate](./skills/engineering/orchestrate/SKILL.md)**: runs as a fresh Mission Ticket coordinator dispatched by an authorized direct caller or `dispatch-tickets`, owning one writer/reviewer delivery graph.

**Typically agent-selected**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: creates throwaway prototypes to validate logic, state, or UI alternatives.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: disciplined loop for hard bugs and regressions: reproduce, minimise, hypothesise, instrument, fix, and regression-test.
- **[research](./skills/engineering/research/SKILL.md)**: investigates a bounded question or produces a durable cited research artifact from high-trust primary sources.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: red -> green -> refactor development at confirmed test seams.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: shared vocabulary and principles for designing deep modules.
- **[code-review](./skills/engineering/code-review/SKILL.md)**: reviews a committed range or complete WIP candidate along Standards and Spec axes.
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**: resolves an in-progress git merge or rebase conflict.

### Productivity

**Typically user-selected**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: runs bounded Question rounds without touching code or docs.
- **[caveman](./skills/productivity/caveman/SKILL.md)**: uses ultra-compressed communication while preserving technical accuracy.
- **[design](./skills/productivity/design/SKILL.md)**: designs and refines context-fit user interfaces, then verifies the rendered result.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: compacts useful, undocumented conversation state for a fresh agent.
- **[wormhole](./skills/productivity/wormhole/SKILL.md)**: moves the current conversation into a fresh interactive agent window and retires the origin Pi after transfer; it remains a generic optional transport outside managed Ticket subagent lineage.
- **[tmux-worker](./skills/productivity/tmux-worker/SKILL.md)**: connects the root with an agent in a visible tmux window for multi-turn work across systems or harnesses; it remains a generic optional transport outside managed Ticket subagent lineage.
- **[teach](./skills/productivity/teach/SKILL.md)**: teaches a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[writing-great-skills](./skills/productivity/writing-great-skills/SKILL.md)**: reference for the vocabulary and design principles behind predictable skills.

**Typically agent-selected**

- **[prompt-comprehension-audits](./skills/productivity/prompt-comprehension-audits/SKILL.md)**: gathers sequential interpreter and reviewer evidence, records one audit status, and ends without dispatch.
- **[write-a-skill](./skills/productivity/write-a-skill/SKILL.md)**: creates new skills with structure, frontmatter, and supporting resources.

## Optional Skills

User-only optional skills are listed in their bucket README and stay out of the active plugin manifests.

## Maintenance

When an active skill is renamed, promoted, or removed, update these together:

- skill folder
- frontmatter `name`
- top-level README
- bucket README
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json` (kept as a mirror of the Codex manifest)
- hard-coded mentions in other skills, ADRs, scripts, and docs
