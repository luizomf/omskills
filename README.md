# omskills

A practical skill collection for keeping agent-assisted software work structured, reviewable, and less likely to jump from a vague idea straight into code.

## Origin

This repository started as a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), copied as it existed on May 24, 2026.

This is not the original repository. To see the source project, use [mattpocock/skills](https://github.com/mattpocock/skills).

The repositories are expected to diverge over time. The original repo should remain separate for upstream tracking; this repo adapts names, rituals, triage, installation, and project defaults for a Codex-oriented workflow.

## What This Is

`omskills` is not runtime application code. It is a curated set of agent skills, prompts, setup docs, and helper scripts for working with Codex and other coding agents.

The main flow this repo reinforces is:

`idea -> grill -> docs -> issue -> branch -> PR -> handoff`

The skills act as checkpoints: clarify before planning, document before queuing, triage before implementation, test before refactoring, and hand off before context is lost.

## Operating Model

Before asking an agent to "build it", classify the moment:

- Need to think through an idea: `/grill-me` or `/grill-with-docs`
- Know the goal, but not the queue: `/to-prd`, `/to-issues`, or `/triage`
- Have a mature, small issue: `/tdd`
- Something broke: `/diagnose`
- Do not understand an area of the code: `/zoom-out`
- The architecture is getting muddy: `/improve-codebase-architecture`
- Need to pause without losing context: `/handoff`

The core habit is to ask: "Is this clear enough to become code?"

If the answer is not clearly yes, use grill, triage, docs, or zoom-out before implementation.

If there is a conflict, architectural ambiguity, unresolved dependency, or two plausible options with real tradeoffs, stop and discuss.

## Common Scenarios

### New Empty Project

The risk in an empty repo is inventing too much architecture too early.

1. Create the minimum project identity: `README.md`, `AGENTS.md`, license if needed, and the stack decision if it is already known.
2. Run `/setup-omskills` to record issue tracker, triage labels, and docs layout.
3. Use `/grill-with-docs` before substantial coding to clarify domain language, constraints, and the smallest useful first slice.
4. Use `/to-prd` if the direction needs a durable spec.
5. Use `/to-issues` to break the spec into small, vertical issues.
6. Use `/tdd` only when a slice is clear and verifiable.

Good prompt:

```text
Before implementing, help identify the smallest useful first slice.
```

### Existing Project Without These Skills

The risk in an existing project is enforcing process before understanding the system.

1. Start with `/zoom-out` to map modules, workflows, risks, and conventions.
2. Run `/setup-omskills` to connect the repo to the skills.
3. Use `/grill-with-docs` if project language is unclear or undocumented.
4. Use `/triage` before picking work from a messy queue.
5. Use `/improve-codebase-architecture` when coupling or structure needs attention; treat the output as diagnosis and issue material, not blanket permission to refactor.
6. Use `/tdd` when a specific issue is mature enough to implement.

Good prompt:

```text
Before changing code, explain how this request fits into the current system.
```

### Project Already Using These Skills

The risk in a prepared repo is ignoring decisions that already exist.

1. Read the local instructions and context: `AGENTS.md`, `CONTEXT.md`, `docs/agents/*`, and `docs/adr/*`.
2. Start from an existing issue when possible.
3. Use `/triage` if the task is new or unclear.
4. Use `/tdd` if the issue is small, mature, and has acceptance criteria.
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

By default, the script writes to `~/.codex/skills`. To test another destination:

```bash
OMSKILLS_DEST=/tmp/omskills-test ./scripts/link-skills.sh
```

2. In each repo that will consume these skills, run:

```text
/setup-omskills
```

This setup records where issues live, which triage labels the repo uses, and how the agent should consume `CONTEXT.md` and ADRs.

## Triage Model

The skills use five canonical roles. Each repo can map those roles to real labels in `docs/agents/triage-labels.md`.

- `needs-triage`: maintainer needs to evaluate.
- `needs-info`: missing information from the reporter/author.
- `ready-for-agent`: well-specified issue, ready for an agent to implement without extra context.
- `ready-for-human`: needs human implementation or decision-making.
- `wontfix`: will not be actioned.

For mature projects, the queue should favor small, vertical, verifiable issues. Changes to shared systems such as architecture, runtime, persistence, deployment, or AI integration need to be mature before implementation.

## Active Skills

### Engineering

- **[diagnose](./skills/engineering/diagnose/SKILL.md)**: disciplined loop for bugs and regressions: reproduce, minimize, hypothesize, instrument, fix, and add a regression test.
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: interviews the user, cross-checks answers with code when possible, sharpens domain language, and updates `CONTEXT.md`/ADRs when decisions crystallize.
- **[triage](./skills/engineering/triage/SKILL.md)**: moves issues through a state machine based on triage roles.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: finds opportunities to deepen modules and reduce coupling, using `CONTEXT.md` and ADRs as context.
- **[setup-omskills](./skills/engineering/setup-omskills/SKILL.md)**: configures issue tracker, triage labels, and docs layout per repo.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: development with red-green-refactor, in small vertical slices.
- **[to-issues](./skills/engineering/to-issues/SKILL.md)**: breaks plans, specs, or PRDs into independent issues.
- **[to-prd](./skills/engineering/to-prd/SKILL.md)**: turns the current conversation context into a PRD and publishes it to the issue tracker.
- **[zoom-out](./skills/engineering/zoom-out/SKILL.md)**: asks for a system-level perspective before touching an unfamiliar area.
- **[prototype](./skills/engineering/prototype/SKILL.md)**: creates throwaway prototypes to validate logic, state, or UI alternatives.

### Productivity

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: rigorous interview to mature an idea without necessarily touching code.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: compacts the session into a handoff so another agent can continue.
- **[daily-paper-social-post](./skills/productivity/daily-paper-social-post/SKILL.md)**: turns a Daily Paper Automation article into compact PT-BR social posts.
- **[write-a-skill](./skills/productivity/write-a-skill/SKILL.md)**: creates new skills with structure, frontmatter, and supporting resources.

## Optional Skills

Kept as inspiration or for occasional use, but outside the main Codex manifest for now:

- **[caveman](./skills/productivity/caveman/SKILL.md)**
- **[setup-pre-commit](./skills/misc/setup-pre-commit/SKILL.md)**
- **[git-guardrails-claude-code](./skills/misc/git-guardrails-claude-code/SKILL.md)**
- **[scaffold-exercises](./skills/misc/scaffold-exercises/SKILL.md)**
- **[migrate-to-shoehorn](./skills/misc/migrate-to-shoehorn/SKILL.md)**

Ignore for now:

- `skills/deprecated/`
- `skills/personal/`
- `skills/in-progress/`

## Maintenance

When an active skill is renamed or promoted, update these together:

- skill folder
- frontmatter `name`
- top-level README
- bucket README
- `.codex-plugin/plugin.json`
- hard-coded mentions in other skills, ADRs, scripts, and docs
