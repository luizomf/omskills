# Issue tracker: GitHub

Specs, tickets, and issues for this repository live as GitHub issues. Use `gh` and infer the repository from the current remote.

## Conventions

- Create one GitHub issue per spec or ticket.
- Read the full issue body, labels, and comments before acting.
- Use native sub-issues and issue dependencies when available; otherwise record parent and blocking issue numbers in the body.
- Apply the configured label from `triage-labels.md` when a skill assigns a triage role.
- Leave a durable comment before closing or superseding an issue.

## Pull requests as a triage surface

**PRs as a request surface: no.** Maintainer PRs are implementation records, not incoming feature requests. Change this flag only if the repository starts accepting external PRs as requests.

## Skill operations

- “Publish to the issue tracker” means create a GitHub issue.
- “Fetch the relevant ticket” means read its body, labels, and comments with `gh issue view`.

## Wayfinding operations

- **Map:** one GitHub issue labelled `wayfinder:map`; child investigations use `wayfinder:<type>` labels.
- **Children:** use native sub-issues. Where unavailable, maintain a child task list in the map body and `Part of #<map>` in each child.
- **Blocking:** use native issue dependencies where supported; otherwise record `Blocked by: #<n>` references in the child body. A child is unblocked only when every blocker is closed.
- **Frontier:** open, unblocked, unassigned children, in native sub-issue order or fallback task-list order.
- **Claim:** assign the selected child to the developer driving the map before resolution work.
- **Resolve:** post the answer, close the child, and append its linked title plus one-line gist to the map's **Decisions so far**.
