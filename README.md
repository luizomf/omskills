# omskills

the maintainer's personal skill collection for working with Codex and other agents without drifting off track.

## Origin

This repository is basically a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), copied as it existed on May 24, 2026, and adapted to the maintainer's use cases.

the maintainer did not create the original base for these skills. This is not the original repository; to see the source project, use [mattpocock/skills](https://github.com/mattpocock/skills).

The repositories are expected to diverge significantly over time. The original repo should remain separate for upstream tracking; this repo is the maintainer's personal space for adapting names, rituals, triage, and installation to his workflow.

## the maintainer Workflow

The flow this repo should reinforce:

`idea -> grill -> docs -> issue -> branch -> PR -> handoff`

Mental model:

- I want to think: `/grill-with-docs`
- I want to organize the queue: `/triage`
- I want to decide architecture: `/improve-codebase-architecture`
- I want to implement a mature issue: `/tdd`
- Something broke: `/diagnose`
- I am stopping: `/handoff`

Safety rule for repos like `omnews`: if the task touches architecture, shared behavior, Docker/runtime, AI runners, TTS, persistence, or publish flows, do not implement directly. First check for an existing issue, triage it, use `/grill-with-docs` if there is ambiguity, record language/decisions in `CONTEXT.md` or `docs/adr/`, and only then move to branch + PR.

If there is a conflict, architectural ambiguity, unresolved dependency, or two plausible options with real tradeoffs, stop and discuss.

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

For `omnews`, the queue should favor small, vertical, verifiable issues. Runtime, AI runner, TTS, persistence, Docker, and publish issues need to be mature before implementation.

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
