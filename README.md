# omskills

A practical skill collection for keeping agent-assisted software work structured, reviewable, and less likely to jump from a vague idea straight into code.

## Origin

This repository started as a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), first copied on May 24, 2026, and has since pulled in selected changes from later upstream snapshots.

This is not the original repository. To see the source project, use [mattpocock/skills](https://github.com/mattpocock/skills).

This repository is maintained independently and does not track or synchronize with the original. Useful ideas may be implemented here deliberately under this project's own conventions.

## What This Is

`omskills` is not runtime application code. It is a curated set of agent skills, prompts, setup docs, and helper scripts for working with Codex and other coding agents.

The main flow this repo reinforces is:

`idea -> grill -> spec -> tickets -> prompt audit -> explicit authorization -> implement -> review -> PR -> handoff`

The skills act as checkpoints: clarify before planning, document before ticketing, triage before implementation, authorize before autonomous execution, test before coding, review before shipping, and hand off before context is lost.

## Operating Model

Before asking an agent to "build it", classify the moment:

- Need to think through an idea: `/grill-me` or `/grill-with-docs`
- The work is too large or foggy for one session: `/wayfinder`
- Know the goal, but not the implementation Tickets: `/to-spec`, then `/to-tickets`
- Want one explicitly Mission-authorized Ticket delivered through a fresh coordinator, writer, and reviewer: `/orchestrate`
- Want a fixed ordered list of Mission-authorized Tickets dispatched while the root remains responsive: `/dispatch-tickets`
- Want the diff checked before it ships: `/code-review`
- Something broke: `/diagnosing-bugs`
- Need high-trust reading legwork: `/research`
- The architecture is getting muddy: `/improve-codebase-architecture`
- Want to learn a topic over multiple sessions: `/teach`
- Need to pause without losing context: `/handoff`
- Need a fresh agent window that retires the old Pi after transfer: `/wormhole`

The core habit is to ask: "Is this clear enough to become code?"

If the answer is not clearly yes, use grill, triage, specs, tickets, research, or wayfinder before implementation.

If there is a conflict, architectural ambiguity, unresolved dependency, or two plausible options with real tradeoffs, stop and discuss.

## Common Scenarios

### New Empty Project

The risk in an empty repo is inventing too much architecture too early.

1. Create the minimum project identity: `README.md`, `AGENTS.md`, license if needed, and the stack decision if it is already known.
2. Run `/setup-omskills` to record issue tracker, triage labels, and docs layout.
3. Use `/grill-with-docs` before substantial coding to clarify domain language, constraints, and the smallest useful first slice.
4. Use `/to-spec` if the direction needs a durable spec.
5. Use `/to-tickets` to break the spec into small, vertical tickets.
6. Explicitly Mission-authorize the Ticket, then use `/orchestrate` only when it is clear, verifiable, `ready-for-agent`, and carries a current Prompt Audit `PASS` or explicit `BYPASS`.

Good prompt:

```text
Before implementing, help identify the smallest useful first slice.
```

### Existing Project Without These Skills

The risk in an existing project is enforcing process before understanding the system.

1. Start with normal repo exploration and, when the request is broad, `/research` or `/wayfinder`.
2. Run `/setup-omskills` to connect the repo to the skills.
3. Use `/grill-with-docs` if project language is unclear or undocumented.
4. Use `/triage` to establish which work is eligible before explicitly selecting any Ticket for execution.
5. Use `/improve-codebase-architecture` when coupling or structure needs attention; treat the output as diagnosis and issue material, not blanket permission to refactor.
6. Explicitly Mission-authorize the Ticket, then use `/orchestrate` when it is mature, `ready-for-agent`, and carries a current Prompt Audit `PASS` or explicit `BYPASS`.

Good prompt:

```text
Before changing code, explain how this request fits into the current system.
```

### Project Already Using These Skills

The risk in a prepared repo is ignoring decisions that already exist.

1. Read the local instructions and context: `AGENTS.md`, `CONTEXT.md`, `docs/agents/*`, and `docs/adr/*`.
2. Start from an existing issue or ticket when possible.
3. Use `/triage` if the task is new or unclear.
4. Explicitly Mission-authorize the Ticket, then use `/orchestrate` if it is small, mature, has acceptance criteria, and carries a current Prompt Audit `PASS` or explicit `BYPASS`.
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

Active skills are installed by the plugin independently of discovery state. Supporting harnesses include agent-discoverable skills in the model's system context, while active user-only skills remain installed for direct selection without permanent context load. `design`, `teach`, and `dispatch-tickets` are the current active user-only skills; invoke them directly for deliberate interface design, a stateful learning workspace, or fixed-sequence Ticket dispatch. The groupings below describe the typical selection path, not discovery status.

2. In each repo that will consume these skills, run:

```text
/setup-omskills
```

This setup records where issues live, which triage labels the repo uses, and how the agent should consume `CONTEXT.md` and ADRs.

## Triage Model

The skills use two category roles and five state roles. Each repo can map those roles to real labels in `docs/agents/triage-labels.md`.

Categories:

- `bug`: something is broken.
- `enhancement`: new feature or improvement.

States:

- `needs-triage`: maintainer needs to evaluate.
- `needs-info`: missing information from the reporter/author.
- `ready-for-agent`: well-specified issue eligible for autonomous execution when a current Prompt Audit gate and explicit Mission authorization also exist; the state does not select the issue.
- `ready-for-human`: needs human implementation or decision-making.
- `wontfix`: will not be actioned.

For mature projects, the eligible Ticket set should favor small, vertical, verifiable units. Changes to shared systems such as architecture, runtime, persistence, deployment, or AI integration need to be mature before implementation. A ready-work query only discovers eligible Tickets; explicit user or invoker direction selects one Ticket or supplies an already-resolved ordered list for a Mission.

## Active Skills

### Engineering

**Typically user-selected**

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: runs bounded Question rounds while maintaining domain language and ADRs.
- **[triage](./skills/engineering/triage/SKILL.md)**: moves issues and external PRs through a state machine based on triage roles.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: scans a codebase for deepening opportunities and presents a visual report with a top recommendation.
- **[setup-omskills](./skills/engineering/setup-omskills/SKILL.md)**: configures issue tracker, triage labels, and docs layout per repo.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: turns the current conversation context into a spec and publishes it to the issue tracker.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: breaks a plan, spec, or conversation into tracer-bullet tickets with blocking and conflict edges.
- **[implement](./skills/engineering/implement/SKILL.md)**: routes one audited, Mission-authorized code or behavior-changing Ticket to a fresh `orchestrate` coordinator.
- **[orchestrate](./skills/engineering/orchestrate/SKILL.md)**: coordinates complete delivery of one explicitly authorized Ticket through single-pass writer and reviewer agents.
- **[dispatch-tickets](./skills/engineering/dispatch-tickets/SKILL.md)**: dispatches a fixed ordered list of Mission-authorized Tickets from a minimal responsive root through fresh coordinators.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: maps a huge or foggy effort into investigation tickets on the issue tracker.

**Typically agent-selected**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: creates throwaway prototypes to validate logic, state, or UI alternatives.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: disciplined loop for hard bugs and regressions: reproduce, minimise, hypothesise, instrument, fix, and regression-test.
- **[research](./skills/engineering/research/SKILL.md)**: investigates a question against high-trust primary sources and saves cited findings in the repo.
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

- **[prompt-comprehension-audits](./skills/productivity/prompt-comprehension-audits/SKILL.md)**: uses two isolated passes, plus one confirmation after repairs, to test a prompt's semantic equivalence.
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
