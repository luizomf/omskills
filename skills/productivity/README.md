# Productivity

Tools for planning, communication, learning and agent transport. See the
[workflow map](../../docs/workflows.md) for how they compose and what each route
produces. Active skills are grouped by typical use; optional skills are user-only.

## Shared delegation policy

- **[model-routing](./model-routing/SKILL.md)** - Select a model and supported reasoning level for a delegated task using a cross-provider task table. User-only; composed on demand by callers rather than added to permanent discovery.

## Typically user-selected

- **[grill-me](./grill-me/SKILL.md)** - Run bounded Question rounds without touching code or docs.
- **[caveman](./caveman/SKILL.md)** - Use ultra-compressed communication while preserving technical accuracy.
- **[design](./design/SKILL.md)** - Design and refine context-fit user interfaces, then verify the rendered result.
- **[handoff](./handoff/SKILL.md)** - Compact undocumented conversation state for a fresh agent.
- **[wormhole](./wormhole/SKILL.md)** - Move the current conversation into a fresh interactive agent window and retire the origin Pi after transfer.
- **[tmux-worker](./tmux-worker/SKILL.md)** - Connect the root with an agent in a visible tmux window for multi-turn work across systems or harnesses.
- **[teach](./teach/SKILL.md)** - Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[writing-great-skills](./writing-great-skills/SKILL.md)** - Reference for the vocabulary and design principles behind predictable skills.

## Optional

- **[excalidraw](./excalidraw/SKILL.md)** - Create and edit clear, editable Excalidraw diagrams from text or an existing scene.
- **[voice](./voice/SKILL.md)** - Speak assistant responses through private OMQueue serialization and Edge text-to-speech playback.

## Typically agent-selected

- **[prompt-comprehension-audits](./prompt-comprehension-audits/SKILL.md)** - Gather sequential interpreter and reviewer evidence, record one audit status, and end without dispatch.
- **[write-a-skill](./write-a-skill/SKILL.md)** - Create new skills with SKILL.md, progressive disclosure, and bundled resources.
