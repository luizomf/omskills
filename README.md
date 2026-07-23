# omskills

A practical skill collection for keeping agent-assisted software work structured, reviewable, and less likely to jump from a vague idea straight into code.

## Origin

This repository started as a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), first copied on May 24, 2026, and has since pulled in selected changes from later upstream snapshots.

This is not the original repository. To see the source project, use [mattpocock/skills](https://github.com/mattpocock/skills).

This repository is maintained independently and does not track or synchronize with the original. Useful ideas may be implemented here deliberately under this project's own conventions.

## What This Is

`omskills` is not runtime application code. It is a curated set of agent skills, prompts, setup docs, and helper scripts for working with Codex and other coding agents.

The main flow this repo reinforces is:

`idea -> grill -> spec -> tickets -> implement -> review -> PR -> handoff`

The skills act as checkpoints: clarify before planning, document before queuing, triage before implementation, test before coding, review before shipping, and hand off before context is lost.

## Operating Model

Before asking an agent to "build it", classify the moment:

- Need to think through an idea: `/grill-me` or `/grill-with-docs`
- The work is too large or foggy for one session: `/wayfinder`
- Know the goal, but not the queue: `/to-spec`, then `/to-tickets`
- Have a mature ticket or issue: `/implement`
- Want the diff checked before it ships: `/code-review`
- Something broke: `/diagnosing-bugs`
- Need high-trust reading legwork: `/research`
- The architecture is getting muddy: `/improve-codebase-architecture`
- Want to learn a topic over multiple sessions: `/teach`
- Need to pause without losing context: `/handoff`
- Need a fresh agent window without losing the current one: `/wormhole`

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
6. Use `/implement` only when a ticket is clear and verifiable.

Good prompt:

```text
Before implementing, help identify the smallest useful first slice.
```

### Existing Project Without These Skills

The risk in an existing project is enforcing process before understanding the system.

1. Start with normal repo exploration and, when the request is broad, `/research` or `/wayfinder`.
2. Run `/setup-omskills` to connect the repo to the skills.
3. Use `/grill-with-docs` if project language is unclear or undocumented.
4. Use `/triage` before picking work from a messy queue.
5. Use `/improve-codebase-architecture` when coupling or structure needs attention; treat the output as diagnosis and issue material, not blanket permission to refactor.
6. Use `/implement` when a specific ticket is mature enough to build.

Good prompt:

```text
Before changing code, explain how this request fits into the current system.
```

### Project Already Using These Skills

The risk in a prepared repo is ignoring decisions that already exist.

1. Read the local instructions and context: `AGENTS.md`, `CONTEXT.md`, `docs/agents/*`, and `docs/adr/*`.
2. Start from an existing issue or ticket when possible.
3. Use `/triage` if the task is new or unclear.
4. Use `/implement` if the issue is small, mature, and has acceptance criteria.
5. Use `/grill-with-docs` if the issue conflicts with domain language or decisions.
6. Stop and discuss when the task conflicts with an ADR, changes architecture, or has meaningful tradeoffs.
7. Use `/handoff` before pausing a long session.

Good prompt:

```text
Follow the repo instructions, read the issue, and tell me whether it is ready for implementation.
```

## Local Quickstart

1. Link the active skills into local Codex:

```bash
./scripts/link-skills.sh
```

The installer prunes only obsolete symlinks managed by this repository and refuses to overwrite real paths or external symlinks. Verify the current installation without changing it:

```bash
./scripts/check-catalog.py
./scripts/link-skills.sh --check
```

By default, the script writes to `~/.agents/skills`, the shared user-level skills directory used by current Codex surfaces. On the first default installation, it safely removes this repository's managed links from the legacy `~/.codex/skills` location while preserving unrelated content. To test another destination:

```bash
OMSKILLS_DEST=/tmp/omskills-test ./scripts/link-skills.sh
```

All active skills are agent-discoverable. Supporting harnesses include each skill's name, description, and location in the agent's system context, then load the full `SKILL.md` only when the task matches or the user invokes the skill directly.

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
- `ready-for-agent`: well-specified issue, ready for an agent to implement without extra context.
- `ready-for-human`: needs human implementation or decision-making.
- `wontfix`: will not be actioned.

For mature projects, the queue should favor small, vertical, verifiable tickets. Changes to shared systems such as architecture, runtime, persistence, deployment, or AI integration need to be mature before implementation.

## Active Skills

### Engineering

**User-invoked**

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: runs a grilling session while maintaining domain language and ADRs.
- **[triage](./skills/engineering/triage/SKILL.md)**: moves issues and external PRs through a state machine based on triage roles.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: scans a codebase for deepening opportunities and presents a visual report with a top recommendation.
- **[setup-omskills](./skills/engineering/setup-omskills/SKILL.md)**: configures issue tracker, triage labels, and docs layout per repo.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: turns the current conversation context into a spec and publishes it to the issue tracker.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: breaks a plan, spec, or conversation into tracer-bullet tickets with blocking and conflict edges.
- **[implement](./skills/engineering/implement/SKILL.md)**: implements a spec, issue, or ticket and verifies it against its acceptance criteria.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: maps a huge or foggy effort into investigation tickets on the issue tracker.

**Model-invoked**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: creates throwaway prototypes to validate logic, state, or UI alternatives.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: disciplined loop for hard bugs and regressions: reproduce, minimise, hypothesise, instrument, fix, and regression-test.
- **[research](./skills/engineering/research/SKILL.md)**: investigates a question against high-trust primary sources and saves cited findings in the repo.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: red -> green development at pre-agreed seams.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: shared vocabulary and principles for designing deep modules.
- **[code-review](./skills/engineering/code-review/SKILL.md)**: reviews a diff along standards and spec axes.
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**: resolves an in-progress git merge or rebase conflict.

### Productivity

**User-invoked**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: runs a grilling session without touching code or docs.
- **[caveman](./skills/productivity/caveman/SKILL.md)**: uses ultra-compressed communication while preserving technical accuracy.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: compacts useful, undocumented conversation state for a fresh agent.
- **[wormhole](./skills/productivity/wormhole/SKILL.md)**: moves the current conversation into a fresh interactive agent window while keeping the origin recoverable.
- **[tmux-worker](./skills/productivity/tmux-worker/SKILL.md)**: connects the root with an agent in a visible tmux window for multi-turn work across systems or harnesses.
- **[teach](./skills/productivity/teach/SKILL.md)**: teaches a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[writing-great-skills](./skills/productivity/writing-great-skills/SKILL.md)**: reference for the vocabulary and design principles behind predictable skills.

**Model-invoked**

- **[prompt-comprehension-audits](./skills/productivity/prompt-comprehension-audits/SKILL.md)**: checks an issue or execution prompt with two clean-context agents for exact semantic comprehension.
- **[write-a-skill](./skills/productivity/write-a-skill/SKILL.md)**: creates new skills with structure, frontmatter, and supporting resources.

## Optional Skills

There are no optional skills currently.

## Maintenance

When an active skill is renamed, promoted, or removed, update these together:

- skill folder
- frontmatter `name`
- top-level README
- bucket README
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json` (kept as a mirror of the Codex manifest)
- hard-coded mentions in other skills, ADRs, scripts, and docs
