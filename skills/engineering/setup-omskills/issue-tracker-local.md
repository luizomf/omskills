# Issue tracker: Local Markdown

Use Markdown under `.scratch/` for local-only work. Prefer the project's durable Issue tracker for project-relevant requirements, decisions, and delivery history.

## Local-only boundary

Before writing any artifact, verify that Git ignores `.scratch/`. If needed, add `.scratch/` to the repository's ignore rules and confirm the rule takes effect before creating files. If it cannot be made ignored, stop without writing. Never stage or commit `.scratch/` content.

## Conventions

- Choose filenames and subdirectories under `.scratch/` to fit the work; `.scratch/<topic>/spec.md` and `.scratch/<topic>/issues/<name>.md` are examples, not required layouts.
- Keep one file per Spec, Ticket, or map. Its repository-relative path is its local identity; link it explicitly rather than assuming a number identifies it.
- Record triage roles as `Category:` and `Status:` lines, using the configured role strings.
- Record lifecycle separately as `Lifecycle: open`, `claimed`, or `resolved`. Claiming or resolving an item never overwrites its triage `Status`.
- Append comments and history under `## Comments`; preserve existing entries.
- Retain local continuation notes while unresolved work still depends on them. Local paths are not supported identities for `dispatch-tickets`.

## When a skill says "publish to the issue tracker"

Create one file per approved item at the chosen `.scratch/` path, under the local-only boundary above. Return the exact paths.

## When a skill says "fetch the relevant ticket"

Read the referenced file and its complete comments.

## Wayfinding operations

- **Map:** one file containing the **Destination**, **Notes**, **Decisions so far**, **Not yet specified**, and **Out of scope** sections. Maintain an ordered child-path index as the local relationship fallback.
- **Child:** one file per investigation, linked from the map. Record `Type: research`, `prototype`, `grilling`, or `task`, and initialize `Lifecycle: open`.
- **Blocking:** record blocker paths in `Blocked by:`. A child is unblocked only when every blocker has `Lifecycle: resolved`.
- **Frontier:** map children with `Lifecycle: open` and no unresolved blockers, in child-index order.
- **Claim:** set `Lifecycle: claimed` before resolution work.
- **Resolve:** append the answer under `## Comments`, set `Lifecycle: resolved`, and append the child's linked title plus one-line gist to the map's **Decisions so far**.
