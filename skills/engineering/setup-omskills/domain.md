# Domain Docs

How engineering skills should consume this repository's domain documentation.

## Before exploring, read these

- In a single-context repository, read root `CONTEXT.md` and applicable records under root `docs/adr/`.
- In a multi-context repository, read root `CONTEXT-MAP.md`, the linked `CONTEXT.md` files relevant to the topic, their derived ADR roots listed below, and applicable system-wide records under root `docs/adr/`.

If a listed file or directory does not exist, proceed silently. The producer skill (`grill-with-docs`) creates domain and ADR files lazily when terms or decisions are resolved.

## Configured layout

**Layout:** `<single-context|multi-context>`

For single-context repositories:

- **Context glossary:** `CONTEXT.md`
- **ADR root:** `docs/adr/`

For multi-context repositories, replace this example table with one row for every local Markdown link under `CONTEXT-MAP.md`'s `## Contexts` section:

| Context | Glossary from `CONTEXT-MAP.md` | Derived ADR root |
| ------- | ------------------------------ | ---------------- |
| `<name>` | `<actual/path/CONTEXT.md>` | `<actual/path/docs/adr/>` |

Resolve each linked glossary path relative to the repository root and keep it inside the repository. Derive its ADR root by appending `docs/adr/` to the directory containing that `CONTEXT.md`. The table is authoritative; do not scan or assume `src/*`, `packages/*`, or another workspace layout. Root `docs/adr/` remains the system-wide ADR root.

If `CONTEXT-MAP.md` has no valid local context links, report the configuration gap instead of inventing context or ADR paths.

## Use the glossary's vocabulary

When output names a domain concept in an issue title, refactor proposal, hypothesis, test name, or similar artifact, use the term defined by the applicable `CONTEXT.md`.

If the concept is absent, reconsider whether the output is inventing project language or note the genuine gap for `grill-with-docs`.

## Flag ADR conflicts

Surface a contradiction with an existing ADR instead of silently overriding it:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
