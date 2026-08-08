# Triage labels

| Kind     | Canonical triage role | GitHub label      | Meaning                                      |
| -------- | --------------------- | ----------------- | -------------------------------------------- |
| Category | `bug`                 | `bug`             | Something is broken                          |
| Category | `enhancement`         | `enhancement`     | New feature or improvement                   |
| State    | `needs-triage`        | `needs-triage`    | Maintainer evaluation is required            |
| State    | `needs-info`          | `needs-info`      | Waiting for reporter or maintainer context   |
| State    | `ready-for-agent`     | `ready-for-agent` | Fully specified and safe for an agent        |
| State    | `ready-for-human`     | `ready-for-human` | Requires human implementation or judgment    |
| State    | `wontfix`             | `wontfix`         | Will not be actioned                         |

Use exactly one category-role label and one state-role label on a triaged issue.

Before changing this mapping, inventory all repository labels with their exact names, colors, and descriptions. Prefer an existing semantic equivalent over creating a duplicate label. Re-inventory immediately before provisioning, create only approved mapped labels that remain missing, and verify afterward that all seven configured labels exist.
