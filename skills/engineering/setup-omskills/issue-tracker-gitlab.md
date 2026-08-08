# Issue tracker: GitLab

Specs, Tickets, issues, and Wayfinder maps for this repository live as GitLab issues. Use `glab` for all operations.

## Repository selection

- **Selected remote:** `<remote-name>`
- **Repository target:** `https://<host>/<namespace>/<project>`
- **API host:** `<host>`
- **GitLab project ID:** `<project-id>`

Pass `--repo https://<host>/<namespace>/<project>` to every project-scoped `glab issue`, `glab mr`, and `glab label` command. Pass `--hostname <host>` and an explicit `projects/<project-id>/...` path to every project API call. Resolve the numeric project ID during setup with `glab repo view https://<host>/<namespace>/<project> -F json --jq '.id'`. This is a read-only request against the selected project; do not rely on ambient remote inference.

Pass tracker values as direct command arguments. The command snippets below are argument shapes, not permission to interpolate tracker values into a shell command. When only a shell tool is available, use a standard-library subprocess argument array with shell execution disabled. Do not construct or evaluate shell command strings from issue titles, descriptions, notes, labels, usernames, or other tracker content.

## Conventions and triage metadata

- **Create an issue noninteractively:** `glab api --hostname <host> --method POST 'projects/<project-id>/issues' --raw-field title=<title> --raw-field description=<description>`. Both raw fields are required. The API operation has no editor or confirmation path, including when a description is the literal `-`.
- **Read an issue:** `glab issue view <iid> --repo https://<host>/<namespace>/<project> -F json`.
- **List issues as JSON:** `glab issue list --repo https://<host>/<namespace>/<project> -O json --per-page 100 --page <page> --order created_at --sort asc`. Iterate pages until a page contains fewer than 100 records. Use `-O json`, not `-F json`, because `-F` selects the human output format for `glab issue list`. The explicit order is oldest first. Retain `author.username`, `created_at`, and `updated_at` until oldest-first and reporter-activity decisions are complete.
- **Read complete issue comments:** `glab api --hostname <host> --paginate 'projects/<project-id>/issues/<iid>/notes?per_page=100&sort=asc'`. Preserve each note's `author.username`, `created_at`, and `updated_at`.
- **Read complete MR comments:** `glab api --hostname <host> --paginate 'projects/<project-id>/merge_requests/<iid>/notes?per_page=100&sort=asc'`. Do not rely on the default page from `glab issue view --comments` or `glab mr view --comments` for triage activity.
- **Comment:** `glab issue note <iid> --repo https://<host>/<namespace>/<project> --message <comment>`.
- **Apply / remove labels:** `glab issue update <iid> --repo https://<host>/<namespace>/<project> --label <label>` / `--unlabel <label>`.
- **Close:** post the durable note first, then run `glab issue close <iid> --repo https://<host>/<namespace>/<project>`.
- **Inventory labels:** page through `glab label list --repo https://<host>/<namespace>/<project> --output json --per-page 100 --page <page>` until the final short page, retaining each exact name, color, and description.
- **Create one approved missing label:** `glab label create --repo https://<host>/<namespace>/<project> --name <label> --color <hex-color> --description <description>`. Inventory before mapping, inventory again before creation, create only approved missing mapped labels, and run a final inventory.

GitLab numbers issues and MRs separately, so `#42` is unambiguous only after the request surface is known.

## Merge requests as a triage surface

**MRs as a request surface: no.** _(Set to `yes` only when this repository treats external MRs as feature requests.)_

When set to `yes`, MRs use the same triage roles as issues:

- **Read an MR:** `glab mr view <iid> --repo https://<host>/<namespace>/<project> -F json` and `glab mr diff <iid> --repo https://<host>/<namespace>/<project>`.
- **List MRs:** page through `glab mr list --repo https://<host>/<namespace>/<project> -F json --per-page 100 --page <page>` and retain each MR's `author.username`, `created_at`, and `updated_at`.
- **Inventory project members:** `glab api --hostname <host> --paginate 'projects/<project-id>/members/all?per_page=100'`. This endpoint supplies direct and inherited project membership. An MR is internal only when its author's username appears in that complete membership response; every other author is external. If complete membership cannot be read, report the capability as unavailable instead of guessing which MRs are external.
- **Comment / label / close:** use `glab mr note create --message`, `glab mr update --label` / `--unlabel`, and `glab mr close`, always with the explicit `--repo` target.

Do not infer GitHub-style author associations on GitLab. Project membership is the configured evidence.

## Publishing and fetching

- **Publish to the issue tracker:** use the noninteractive create operation above with explicit title and description arguments.
- **Fetch the relevant Ticket:** use the JSON read operation and paginated comments operation above; read the full description, labels, author, timestamps, and comments.

## Wayfinding operations

The **map** is one issue labelled `wayfinder:map`; its **Tickets** are issues whose first description line is the exact map parent reference.

- **Create a map noninteractively:** `glab api --hostname <host> --method POST 'projects/<project-id>/issues' --raw-field title=<title> --raw-field description=<map-description> --raw-field labels=wayfinder:map`.
- **Create a child noninteractively:** make `Part of #<map-iid>` the first line of the complete description, then run `glab api --hostname <host> --method POST 'projects/<project-id>/issues' --raw-field title=<title> --raw-field description=<ticket-description> --raw-field labels=wayfinder:<type>`. Create all children before adding blocker links.
- **Add a native blocker:** `glab api --hostname <host> --method POST 'projects/<project-id>/issues/<child-iid>/links' -F target_project_id=<project-id> -F target_issue_iid=<blocker-iid> -f link_type=is_blocked_by`. If issue links are unavailable, use a `Blocked by: #<iid>, ...` description line and check each referenced issue's current state.
- **Inspect blockers:** `glab api --hostname <host> 'projects/<project-id>/issues/<child-iid>/links'`. A native blocker is a link whose `link_type` is `is_blocked_by`; it blocks the child only while the linked issue's `state` is `opened`.
- **Compute the frontier:** page through the JSON issue-list operation in ascending `created_at` order. First retain only open issues whose first description line exactly equals `Part of #<map-iid>`. Only after that parent-reference scope exists, inspect each scoped child's links or fallback blocker line and remove blocked children, then remove children with any assignee. Repository-wide open issues and issues that merely mention the map elsewhere are never frontier candidates.
- **Resolve the authenticated username:** run `glab api --hostname <host> user` and parse the response's `username` field with a standard-library JSON parser. `glab api` does not provide a `--jq` flag.
- **Claim:** pass the resolved username as one direct argument to `glab issue update <iid> --repo https://<host>/<namespace>/<project> --assignee <authenticated-username>`. Do not pass the unsupported literal `@me` to `glab issue update`.
- **Resolve:** `glab issue note <iid> --repo https://<host>/<namespace>/<project> --message <answer>`, close the Ticket, then update the map with `glab issue update <map-iid> --repo https://<host>/<namespace>/<project> --description <updated-map-description>`.

The fixed Wayfinder label inventory and provisioning policy belongs to the `wayfinder` consumer. This configuration provides the supported label inventory and creation operations it uses.
