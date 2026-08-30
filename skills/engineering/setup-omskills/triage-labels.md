# Triage Labels

The skills speak in terms of two category roles and five state roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Kind     | Canonical triage role | Label in configured tracker | Meaning                                   |
| -------- | --------------------- | --------------------------- | ----------------------------------------- |
| Category | `bug`                 | `bug`                | Something is broken                       |
| Category | `enhancement`         | `enhancement`        | New feature or improvement                |
| State    | `needs-triage`        | `needs-triage`       | Maintainer needs to evaluate this issue   |
| State    | `needs-info`          | `needs-info`         | Waiting on reporter for more information  |
| State    | `ready-for-agent`     | `ready-for-agent`    | Eligible; Mission authorization selects work |
| State    | `ready-for-human`     | `ready-for-human`    | Requires human implementation             |
| State    | `wontfix`             | `wontfix`            | Will not be actioned                      |

Every triaged issue should carry exactly one category role and one state role. When a skill mentions a role (e.g. "apply the ready-for-agent triage label"), use the corresponding label string from this table.

Edit the tracker-label column to match the repository's configured vocabulary.
