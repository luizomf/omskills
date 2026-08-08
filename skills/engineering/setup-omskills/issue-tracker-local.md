# Issue tracker: Local Markdown

Specs, Tickets, issues, and Wayfinder maps for this repository live as Markdown files under `.scratch/`. Local Markdown is the selected Issue tracker, not a fallback from a failed hosted tracker.

## Repository selection

- **Repository target:** the current repository root
- **Tracker root:** `.scratch/`

Keep every tracker path inside `.scratch/`. Pass titles, bodies, authors, and timestamps as file content; do not construct or evaluate shell command strings from tracker content.

## Conventions and triage metadata

- One feature uses one directory: `.scratch/<feature-slug>/`.
- A Spec is `.scratch/<feature-slug>/spec.md`.
- Implementation Tickets use one file each at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`.
- Every created item supplies an explicit `# <title>` and noninteractive body in the file. Never open an editor to obtain missing creation input.
- Every item records `Author:`, `Created:`, and `Updated:` using an author identity and ISO 8601 timestamps. Preserve those fields for oldest-first ordering.
- Triage roles are `Category:` and `Status:` lines near the top of each Ticket or issue file, using `triage-labels.md`.
- Comments append under `## Comments` and record the comment author plus ISO 8601 created and updated timestamps. Preserve that metadata so reporter activity can be compared with the latest triage note.
- Closing an item records its durable closing comment before changing its state to closed.

Before recommending triage mappings, inventory the category and state strings already present in `.scratch/`. Reuse semantic equivalents rather than introducing duplicate role strings. Local Markdown requires no label provisioning.

## Pull requests as a triage surface

**PRs as a request surface: no.** Local Markdown does not discover pull requests. An explicitly named hosted PR follows its host's separately configured operations, if any.

## Publishing and fetching

- **Publish to the Issue tracker:** create the complete Markdown file with explicit title, body, author, created timestamp, and updated timestamp.
- **Fetch the relevant Ticket:** read the complete file, including role fields, author/timestamps, and every comment.

## Wayfinding operations

The **map** is one Markdown file; its **Tickets** are child files in that map's dedicated issues directory.

- **Create a map noninteractively:** write `.scratch/<effort>/map.md` with an explicit title, complete map body, `Author:`, `Created:`, and `Updated:` fields.
- **Create a child noninteractively:** write `.scratch/<effort>/issues/<NN>-<slug>.md` with an explicit title and complete question body. Record `Parent: .scratch/<effort>/map.md`, `Type: research|prototype|grilling|task`, `Status: open`, author, and timestamps.
- **Blocking:** record `Blocked by: <NN>, <NN>` near the top. A Ticket is unblocked only when every listed child file is resolved.
- **Frontier:** first scope to files directly under this map's `.scratch/<effort>/issues/` directory whose `Parent:` field exactly names this map. Then retain open files, remove files with unresolved blockers, and remove claimed files; first by numeric filename wins.
- **Claim:** record the driving developer in `Assignee:` and set `Status: claimed` before work.
- **Resolve:** append the attributed, timestamped answer under `## Comments`, set `Status: resolved`, update `Updated:`, then append the linked title and one-line gist to the map's **Decisions so far**.

Fixed Wayfinder type values are represented by the `Type:` field. No hosted label operation applies.
