# Issue tracker: GitHub

Specs, Tickets, issues, and Wayfinder maps for this repository live as GitHub issues. Use `gh` for all operations.

## Repository selection

- **Selected remote:** `<remote-name>`
- **Repository target:** `<host>/<owner>/<repo>`
- **API host:** `<host>`
- **API repository:** `<owner>/<repo>`

Pass `--repo <host>/<owner>/<repo>` to every `gh issue`, `gh pr`, and `gh label` command. Pass `--hostname <host>` and the explicit `repos/<owner>/<repo>/...` path to every `gh api` command. Do not rely on ambient remote inference.

Pass tracker values as direct command arguments or through body files. The command snippets below are argument shapes, not permission to interpolate tracker values into a shell command. When only a shell tool is available, use a standard-library subprocess argument array with shell execution disabled. Do not construct or evaluate shell command strings from issue titles, bodies, comments, labels, usernames, or other tracker content.

## Conventions and triage metadata

- **Create an issue noninteractively:** `gh issue create --repo <host>/<owner>/<repo> --title <title> --body-file <body-file>`. Both flags are required; use a body file even for an empty body so `gh` cannot prompt.
- **Read an issue:** `gh issue view <number> --repo <host>/<owner>/<repo> --json number,title,body,state,labels,author,createdAt,updatedAt,comments`.
- **List issues:** `gh issue list --repo <host>/<owner>/<repo> --state open --limit 1000 --json number,title,body,state,labels,assignees,author,createdAt,updatedAt,comments`. Retain the item author's login, item timestamps, and every comment's author and timestamps until oldest-first and reporter-activity decisions are complete.
- **Read complete comments for an issue or PR:** `gh api --hostname <host> --paginate 'repos/<owner>/<repo>/issues/<number>/comments?per_page=100' --jq '.[]'`. This emits every comment from every page. Preserve `user.login`, `created_at`, and `updated_at`.
- **Comment:** `gh issue comment <number> --repo <host>/<owner>/<repo> --body-file <comment-file>`.
- **Apply / remove labels:** `gh issue edit <number> --repo <host>/<owner>/<repo> --add-label <label>` / `--remove-label <label>`.
- **Close:** post the durable comment first, then run `gh issue close <number> --repo <host>/<owner>/<repo>`.
- **Inventory labels:** `gh label list --repo <host>/<owner>/<repo> --limit 1000 --json name,color,description`.
- **Create one approved missing label:** `gh label create <label> --repo <host>/<owner>/<repo> --color <rrggbb> --description <description>`. Inventory before mapping, inventory again before creation, create only approved missing mapped labels, and run a final inventory.

GitHub shares one number space across issues and PRs. Resolve a bare `#42` with `gh pr view 42 --repo <host>/<owner>/<repo>` and fall back to `gh issue view 42 --repo <host>/<owner>/<repo>`.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` only when this repository treats external PRs as feature requests.)_

When set to `yes`, PRs use the same triage roles as issues:

- **Read a PR:** `gh pr view <number> --repo <host>/<owner>/<repo> --json number,title,body,state,labels,author,createdAt,updatedAt,comments` and `gh pr diff <number> --repo <host>/<owner>/<repo>`.
- **Discover external PRs:** `gh api --hostname <host> --paginate 'repos/<owner>/<repo>/pulls?state=open&per_page=100' --jq '.[] | select(.author_association as $association | ["OWNER", "MEMBER", "COLLABORATOR"] | index($association) | not)'`. The per-page filter excludes only `OWNER`, `MEMBER`, and `COLLABORATOR`; every other current or future association value is external. Retain `user.login`, `author_association`, `created_at`, and `updated_at`; use the paginated issue-comments operation above for reporter activity.
- **Comment / label / close:** use `gh pr comment --body-file`, `gh pr edit --add-label` / `--remove-label`, and `gh pr close`, always with the explicit `--repo` target.

Do not request `authorAssociation` from `gh pr list`; it is not a supported JSON field. GitHub's REST `author_association` response is the configured membership evidence.

## Publishing and fetching

- **Publish to the issue tracker:** use the noninteractive create operation above with an explicit title and body file.
- **Fetch the relevant Ticket:** use the read operation and complete-comments operation above; read the full body, labels, author, timestamps, and comments.

## Wayfinding operations

The **map** is one issue labelled `wayfinder:map`; its **Tickets** are child issues.

- **Create a map noninteractively:** `gh issue create --repo <host>/<owner>/<repo> --title <title> --body-file <map-body-file> --label wayfinder:map`.
- **Create a child noninteractively:** `gh issue create --repo <host>/<owner>/<repo> --title <title> --body-file <ticket-body-file> --label wayfinder:<type> --parent <map-number>`. Create all children before adding blocker edges.
- **Native child scope:** enumerate only the map's actual sub-issues with `gh api --hostname <host> --paginate 'repos/<owner>/<repo>/issues/<map-number>/sub_issues?per_page=100' --jq '.[]'`. This emits every sub-issue from every page while preserving the returned order.
- **Documented task-list fallback:** use only when native sub-issues are unavailable. Add a `## Tickets` task list to the map and `Part of #<map-number>` as the child's first body line. Extract child numbers only from checklist entries in that section, preserve their order, and fetch exactly those issues. Never treat repository-wide search results or unrelated issue references in the map body as children.
- **Add a native blocker:** get the blocker's numeric database ID with `gh api --hostname <host> 'repos/<owner>/<repo>/issues/<blocker-number>' --jq '.id'`, then run `gh api --hostname <host> --method POST 'repos/<owner>/<repo>/issues/<child-number>/dependencies/blocked_by' -F issue_id=<blocker-database-id>`. If dependencies are unavailable, use a `Blocked by: #<number>, ...` body line and check each referenced issue's current state.
- **Compute the frontier:** first obtain the ordered native-sub-issue or task-list child scope. Only then retain open children, remove children with `issue_dependencies_summary.blocked_by > 0` (or an open fallback blocker), and remove children with any assignee. Never start from `gh issue list` across the repository.
- **Claim:** `gh issue edit <number> --repo <host>/<owner>/<repo> --add-assignee @me`.
- **Resolve:** `gh issue comment <number> --repo <host>/<owner>/<repo> --body-file <answer-file>`, close the Ticket, then update the map with `gh issue edit <map-number> --repo <host>/<owner>/<repo> --body-file <updated-map-body-file>`.

The fixed Wayfinder label inventory and provisioning policy belongs to the `wayfinder` consumer. This configuration provides the supported label inventory and creation operations it uses.
