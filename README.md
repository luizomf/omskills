# omskills

A practical skill collection for keeping agent-assisted software work structured,
reviewable, and less likely to jump from a vague idea straight into code.

## Origin

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills), first copied
on May 24, 2026, with selected later changes adopted deliberately. This repository
is maintained independently; see the linked project for the original collection.

## What This Is

`omskills` is a curated set of agent skills, prompts, setup docs, and helper scripts
for Codex and other coding agents. Ordinary work uses Direct Assisted delivery:
one conversational agent handles the accepted request while the maintainer is available.

See the **[workflow map](docs/workflows.md)** for complete paths, dependencies and
outcomes, including planning, coordinated Missions, investigations, creative work
and continuation utilities. The [Engineering](skills/engineering/README.md) and
[Productivity](skills/productivity/README.md) catalogs list the individual skills.

### Runtime relationship with ompi

This collection and [ompi](https://github.com/luizomf/ompi) are independently
installed and maintained. Many skills work in any compatible coding-agent harness.
The advanced Mission route uses isolated subagents, bounded nesting, direct and
asynchronous delivery, capability inheritance and managed cancellation, currently
implemented and validated by ompi. Another harness needs equivalent capabilities.
Parallel phases depend on its actual root capacity and concurrent-start support.
The managed route currently accepts `owner/repository#integer` Ticket identities;
planning and triage support additional tracker formats, including local Markdown.
These skills describe agent behavior; the harness provides runtime enforcement.

## Where to Start

- An unclear idea: `/grill-me` or `/grill-with-docs`
- Large or foggy work: `/wayfinder`
- A resolved goal needing planning artifacts: `/to-spec` or `/to-tickets`
- A bounded change: ask the agent directly
- One selected Mission Ticket: `/implement`, or another [Mission entry](docs/workflows.md#deliver-a-coordinated-mission)
- A selected phased Mission plan: `/dispatch-tickets`
- A bug or regression: `/diagnosing-bugs`
- A factual investigation: `/research`
- A diff to review: `/code-review`
- Architecture or interface work: `/improve-codebase-architecture` or `/design`
- A learning goal: `/teach`
- Context to preserve or transfer: `/handoff` or `/wormhole`

For a new repository, start with its basic project identity and configure tracker
operations when needed. For an existing project, start from its code, instructions
and accepted request. The [workflow map](docs/workflows.md) shows the next useful
steps and where each route can finish.

## Local Quickstart

Link the active skills into local Codex with Bash, `jq`, and Python 3.9 or newer:

```bash
./scripts/link-skills.sh
./scripts/check-catalog.py
./scripts/link-skills.sh --check
```

The default destination is `~/.agents/skills`. The installer uses relative
symlinks, tracks the links it owns, and preserves real paths and external links.
On the first default installation, it migrates this repository's managed links
from the legacy `~/.codex/skills` location while preserving unrelated content.
Choose another harness directory with `OMSKILLS_DEST`, for example:

```bash
OMSKILLS_DEST="$HOME/.pi/agent/skills" ./scripts/link-skills.sh
OMSKILLS_DEST="$HOME/.pi/agent/skills" ./scripts/link-skills.sh --check
```

Active status and discovery are separate. Supporting harnesses keep
agent-discoverable descriptions in model context; user-only skills are selected
explicitly or loaded through a composing skill's file pointer. The active user-only
skills are `design`, `teach`, `dispatch-tickets`, `implement`, `orchestrate`, and
`model-routing`.

Cross-skill links resolve from the referring file's physical directory, following
symlinks before parent traversal. This works across macOS/Linux when the directory
layout is preserved. Separately copied skill folders need the linked layout too.
Fresh child prompts receive resolved file paths; hidden skills remain readable.

In a consuming repository, `/setup-omskills` configures tracker operations,
triage-label mappings, domain-document locations and a verified model-routing
pointer. Existing configuration and scoped setup permission guide the changes.
For model selection, invoke `/model-routing` and request its use for future
subagents within your authorized providers, preserving explicit choices.

## Triage Model

The configurable category roles are `bug` and `enhancement`. State roles are
`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`.
See [triage](skills/engineering/triage/SKILL.md) for transitions and the
[workflow map](docs/workflows.md#turn-an-idea-into-a-plan) for eligibility and delivery.

## Active Skills

### Engineering

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: resolve decisions while maintaining domain terms and ADRs.
- **[triage](./skills/engineering/triage/SKILL.md)**: verify and categorize tracker requests.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: scan for deepening opportunities and develop a selected candidate.
- **[setup-omskills](./skills/engineering/setup-omskills/SKILL.md)**: configure repository tracker and domain-document operations.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: publish a Spec from established context.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: publish tracer-bullet Tickets and their relations.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: map multi-session investigation work.
- **[dispatch-tickets](./skills/engineering/dispatch-tickets/SKILL.md)**: dispatch a finite phased Mission plan.
- **[implement](./skills/engineering/implement/SKILL.md)**: compose a one-Ticket Mission through the dispatcher.
- **[orchestrate](./skills/engineering/orchestrate/SKILL.md)**: coordinate one Mission Ticket in a fresh agent.
- **[prototype](./skills/engineering/prototype/SKILL.md)**: evaluate throwaway logic, state or UI alternatives.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: reproduce, diagnose and verify repairs.
- **[research](./skills/engineering/research/SKILL.md)**: return bounded evidence or a cited research artifact.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: develop through red → green → refactor.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: design deep modules and test seams.
- **[code-review](./skills/engineering/code-review/SKILL.md)**: review committed or complete WIP candidates.
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**: resolve and complete an in-progress merge or rebase.

### Productivity

- **[model-routing](./skills/productivity/model-routing/SKILL.md)**: select a model and effort for delegated work.
- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: resolve decisions through conversation.
- **[caveman](./skills/productivity/caveman/SKILL.md)**: compress communication while preserving accuracy.
- **[design](./skills/productivity/design/SKILL.md)**: design interfaces and verify the rendered result.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: preserve undocumented continuation state.
- **[wormhole](./skills/productivity/wormhole/SKILL.md)**: transfer a conversation into a fresh interactive window.
- **[tmux-worker](./skills/productivity/tmux-worker/SKILL.md)**: converse with a visible agent across harnesses.
- **[teach](./skills/productivity/teach/SKILL.md)**: teach through a persistent learning workspace.
- **[writing-great-skills](./skills/productivity/writing-great-skills/SKILL.md)**: reference for predictable skill design.
- **[prompt-comprehension-audits](./skills/productivity/prompt-comprehension-audits/SKILL.md)**: gather independent comprehension evidence and record the result.
- **[write-a-skill](./skills/productivity/write-a-skill/SKILL.md)**: create skills and supporting resources.

## Optional Skills

User-only optional skills appear in their bucket catalog, separately from the
active plugin manifests. See [optional utility workflows](docs/workflows.md#optional-utilities).

## Maintenance

When an active skill is renamed, promoted, or removed, update its folder,
frontmatter, both catalogs, mirrored plugin manifests, and hard-coded references
together. Repository instructions and verification commands live in [AGENTS.md](AGENTS.md).
