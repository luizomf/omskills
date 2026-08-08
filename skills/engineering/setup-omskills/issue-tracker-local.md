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

## Planning publication operations

Use these operations for `to-spec` and `to-tickets` in addition to the conventions above:

- **Publish a planning Spec:** write the complete `.scratch/<feature-slug>/spec.md` without a `Status:` state role, then append its current Prompt Audit under `## Comments`. A planning Spec never receives `ready-for-agent` or another implementation-ready state.
- **Create or reconcile a Ticket identity:** use the approved numbered path and exact `Planning identity: <source-identity>/ticket-<NN>` field. Search the feature's direct `issues/` children for that field before writing. Reconcile one match, create no match, and stop on multiple matches or a different identity at the approved path.
- **Record the parent and initial roles:** every Ticket records `Parent: <spec-path>`, `Category: <configured-category-role>`, and `Status: needs-triage`. Keep exactly one configured category role and this one configured state role until audit authorizes readiness.
- **Record blockers and conflicts:** use `Blocked by: <identities>` and `Conflicts with: <identities plus each shared file, contract, artifact, or integration surface>`. Write all approved identity files and `Parent:` fields before replacing symbolic references with final numbered identities.
- **Audit and transition:** append the Ticket's Prompt Audit under `## Comments` only after its complete body, parent, blockers, and conflicts are final. A current `PASS` or explicit maintainer-authorized `BYPASS` changes `Status:` from `needs-triage` to `ready-for-agent`. A missing, stale, or `FAIL` status keeps or restores `needs-triage`.

Publication succeeds only after every file and field is re-read and all authorizing audits and exact role invariants hold. On interruption, report exact completed and missing identities, parents, blockers, conflicts, audits, and readiness transitions. Resume by reconciling exact `Planning identity:` values rather than creating duplicate files.

## Wayfinding operations

The **map** is one Markdown file; its **Tickets** are child files in that map's dedicated issues directory.

- **Create a map noninteractively:** write `.scratch/<effort>/map.md` with an explicit title, complete map body, `Author:`, `Created:`, and `Updated:` fields.
- **Create a child noninteractively:** write `.scratch/<effort>/issues/<NN>-<slug>.md` with an explicit title and complete question body. Record `Parent: .scratch/<effort>/map.md`, `Type: research|prototype|grilling|task`, `Status: open`, author, and timestamps.
- **Blocking:** record `Blocked by: <NN>, <NN>` near the top. A Ticket is unblocked only when every listed child file is resolved.
- **Frontier:** first scope to files directly under this map's `.scratch/<effort>/issues/` directory whose `Parent:` field exactly names this map. Then retain open files, remove files with unresolved blockers, and remove claimed files; first by numeric filename wins.
- **Claim:** record the driving developer in `Assignee:` and set `Status: claimed` before work.
- **Resolve:** append the attributed, timestamped answer under `## Comments`, set `Status: resolved`, update `Updated:`, then append the linked title and one-line gist to the map's **Decisions so far**.

Fixed Wayfinder type values are represented by the `Type:` field. No hosted label operation applies.
