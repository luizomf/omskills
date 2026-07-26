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
- A wayfinder map is a GitHub issue whose child investigations are sub-issues, with native dependency edges where supported.
