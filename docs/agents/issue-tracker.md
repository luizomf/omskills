# Issue tracker: GitHub

Specs, Tickets, issues, and Wayfinder maps for this repository live as GitHub issues. Use `gh` for all operations.

## Repository selection

- **Selected remote:** `origin`
- **Repository target:** `github.com/luizomf/omskills`
- **API host:** `github.com`
- **API repository:** `luizomf/omskills`

Pass `--repo github.com/luizomf/omskills` to every `gh issue`, `gh pr`, and `gh label` command. Pass `--hostname github.com` and the explicit `repos/luizomf/omskills/...` path to every `gh api` command. Do not rely on ambient remote inference.

Pass tracker values as direct command arguments or through body files. The command snippets below are argument shapes, not permission to interpolate tracker values into a shell command. When only a shell tool is available, use a standard-library subprocess argument array with shell execution disabled. Do not construct or evaluate shell command strings from issue titles, bodies, comments, labels, usernames, or other tracker content.

## Conventions and triage metadata

- **Create an issue noninteractively:** `gh issue create --repo github.com/luizomf/omskills --title <title> --body-file <body-file>`. Both flags are required; use a body file even for an empty body so `gh` cannot prompt.
- **Read an issue:** `gh issue view <number> --repo github.com/luizomf/omskills --json number,title,body,state,labels,author,createdAt,updatedAt,comments`.
- **List issues:** `gh issue list --repo github.com/luizomf/omskills --state open --limit 1000 --json number,title,body,state,labels,assignees,author,createdAt,updatedAt,comments`. Retain the item author's login, item timestamps, and every comment's author and timestamps until oldest-first and reporter-activity decisions are complete.
- **Read complete comments for an issue or PR:** `gh api --hostname github.com --paginate 'repos/luizomf/omskills/issues/<number>/comments?per_page=100' --jq '.[]'`. This emits every comment from every page. Preserve `user.login`, `created_at`, and `updated_at`.
- **Comment:** `gh issue comment <number> --repo github.com/luizomf/omskills --body-file <comment-file>`.
- **Apply / remove labels:** `gh issue edit <number> --repo github.com/luizomf/omskills --add-label <label>` / `--remove-label <label>`.
- **Close:** post the durable comment first, then run `gh issue close <number> --repo github.com/luizomf/omskills`.
- **Inventory labels:** `gh label list --repo github.com/luizomf/omskills --limit 1000 --json name,color,description`.
- **Create one approved missing label:** `gh label create <label> --repo github.com/luizomf/omskills --color <rrggbb> --description <description>`. Inventory before mapping, inventory again before creation, create only approved missing mapped labels, and run a final inventory.

GitHub shares one number space across issues and PRs. Resolve a bare `#42` with `gh pr view 42 --repo github.com/luizomf/omskills` and fall back to `gh issue view 42 --repo github.com/luizomf/omskills`.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` only when this repository treats external PRs as feature requests.)_

When set to `yes`, PRs use the same triage roles as issues:

- **Read a PR:** `gh pr view <number> --repo github.com/luizomf/omskills --json number,title,body,state,labels,author,createdAt,updatedAt,comments` and `gh pr diff <number> --repo github.com/luizomf/omskills`.
- **Discover external PRs:** `gh api --hostname github.com --paginate 'repos/luizomf/omskills/pulls?state=open&per_page=100' --jq '.[] | select(.author_association as $association | ["OWNER", "MEMBER", "COLLABORATOR"] | index($association) | not)'`. The per-page filter excludes only `OWNER`, `MEMBER`, and `COLLABORATOR`; every other current or future association value is external. Retain `user.login`, `author_association`, `created_at`, and `updated_at`; use the paginated issue-comments operation above for reporter activity.
- **Comment / label / close:** use `gh pr comment --body-file`, `gh pr edit --add-label` / `--remove-label`, and `gh pr close`, always with the explicit `--repo` target.

Do not request `authorAssociation` from `gh pr list`; it is not a supported JSON field. GitHub's REST `author_association` response is the configured membership evidence.

## Publishing and fetching

- **Publish to the issue tracker:** use the noninteractive create operation above with an explicit title and body file.
- **Fetch the relevant Ticket:** use the read operation and complete-comments operation above; read the full body, labels, author, timestamps, and comments.

## Planning publication operations

Use these operations for `to-spec` and `to-tickets` in addition to the conventions above. Prefer each native relation and use its documented fallback only when that native capability is unavailable:

- **Publish a planning Spec:** create the complete issue with explicit `--title` and `--body-file` and no configured state-role label. Record its Prompt Audit with the comment operation only after the complete body is stable.
- **Discover approved Ticket identities:** prefer the paginated native child scope at `repos/luizomf/omskills/issues/<spec-number>/sub_issues?per_page=100` and match the exact `## Planning identity` value in each body. One match is reconciled, no match is created, and multiple matches stop publication as a duplicate. Do not use repository-wide title search as identity.
- **Create a non-ready Ticket with its native parent:** `gh issue create --repo github.com/luizomf/omskills --title <title> --body-file <body-file> --label <category-label> --label <needs-triage-label> --parent <spec-number>`. The two labels must resolve to exactly one configured category role and exactly the configured `needs-triage` state role.
- **Reconcile a native parent:** `gh issue edit <ticket-number> --repo github.com/luizomf/omskills --parent <spec-number>`. Inspect it with `gh api --hostname github.com 'repos/luizomf/omskills/issues/<ticket-number>/parent'`.
- **Documented fallback for parentage:** use only when the native parent relation is unavailable. Prepend `Part of #<spec-number>` to the Ticket body and maintain a `## Tickets` checklist of approved Ticket identifiers on the Spec. Reconcile the checklist with `gh issue edit <spec-number> --repo github.com/luizomf/omskills --body-file <spec-body-file>`; never append a duplicate entry.
- **Add a native blocker:** `gh issue edit <ticket-number> --repo github.com/luizomf/omskills --add-blocked-by <blocker-number>`. Inspect all blockers with `gh api --hostname github.com --paginate 'repos/luizomf/omskills/issues/<ticket-number>/dependencies/blocked_by?per_page=100' --jq '.[]'`. Add only a missing relation.
- **Documented fallback for blockers:** use only when native dependencies are unavailable. Maintain the identifiers under the Ticket's `## Blocked by` section and inspect every referenced issue's current state.
- **Record direct conflicts:** no native conflict relation is configured. Record each edge under `## Conflicts with` on both Ticket bodies, including the shared file, contract, artifact, or integration surface, and reconcile with `gh issue edit <ticket-number> --repo github.com/luizomf/omskills --body-file <body-file>`.
- **Audit a final Ticket:** use the comment operation after its final body, parent, blockers, and conflicts have been reconciled. A later material body or relation change makes that status stale.
- **Transition one audited Ticket to ready:** `gh issue edit <ticket-number> --repo github.com/luizomf/omskills --remove-label <needs-triage-label> --add-label <ready-for-agent-label>`. Remove every other configured category or state label as needed so the Ticket finishes with exactly one configured category role and exactly the configured `ready-for-agent` state role. A missing, stale, or `FAIL` audit instead keeps or restores the single category plus `needs-triage` pair.

Create or reconcile every approved identity and parent before adding identifier-dependent blockers or conflicts. A partial attempt reports exact completed and missing identities, parents, relations, audits, and readiness transitions. Resume by repeating discovery and reconciliation rather than creating replacements.

## Wayfinding operations

The **map** is one issue labelled `wayfinder:map`; its **Tickets** are child issues.

- **Create a map noninteractively:** `gh issue create --repo github.com/luizomf/omskills --title <title> --body-file <map-body-file> --label wayfinder:map`.
- **Create a child noninteractively:** `gh issue create --repo github.com/luizomf/omskills --title <title> --body-file <ticket-body-file> --label wayfinder:<type> --parent <map-number>`. Create all children before adding blocker edges.
- **Native child scope:** enumerate only the map's actual sub-issues with `gh api --hostname github.com --paginate 'repos/luizomf/omskills/issues/<map-number>/sub_issues?per_page=100' --jq '.[]'`. This emits every sub-issue from every page while preserving the returned order.
- **Documented task-list fallback:** use only when native sub-issues are unavailable. Add a `## Tickets` task list to the map and `Part of #<map-number>` as the child's first body line. Extract child numbers only from checklist entries in that section, preserve their order, and fetch exactly those issues. Never treat repository-wide search results or unrelated issue references in the map body as children.
- **Add a native blocker:** get the blocker's numeric database ID with `gh api --hostname github.com 'repos/luizomf/omskills/issues/<blocker-number>' --jq '.id'`, then run `gh api --hostname github.com --method POST 'repos/luizomf/omskills/issues/<child-number>/dependencies/blocked_by' -F issue_id=<blocker-database-id>`. If dependencies are unavailable, use a `Blocked by: #<number>, ...` body line and check each referenced issue's current state.
- **Compute the frontier:** first obtain the ordered native-sub-issue or task-list child scope. Only then retain open children, remove children with `issue_dependencies_summary.blocked_by > 0` (or an open fallback blocker), and remove children with any assignee. Never start from `gh issue list` across the repository.
- **Claim:** `gh issue edit <number> --repo github.com/luizomf/omskills --add-assignee @me`.
- **Resolve:** `gh issue comment <number> --repo github.com/luizomf/omskills --body-file <answer-file>`, close the Ticket, then update the map with `gh issue edit <map-number> --repo github.com/luizomf/omskills --body-file <updated-map-body-file>`.

The fixed Wayfinder label inventory and provisioning policy belongs to the `wayfinder` consumer. This configuration provides the supported label inventory and creation operations it uses.
