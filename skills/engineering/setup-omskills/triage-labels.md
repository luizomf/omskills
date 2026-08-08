# Triage Labels

The skills speak in terms of two category roles and five state roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Kind     | Canonical triage role | Label in configured tracker | Meaning                                   |
| -------- | --------------------- | --------------------------- | ----------------------------------------- |
| Category | `bug`                 | `bug`                | Something is broken                       |
| Category | `enhancement`         | `enhancement`        | New feature or improvement                |
| State    | `needs-triage`        | `needs-triage`       | Maintainer needs to evaluate this issue   |
| State    | `needs-info`          | `needs-info`         | Waiting on reporter for more information  |
| State    | `ready-for-agent`     | `ready-for-agent`    | Fully specified, ready for an agent       |
| State    | `ready-for-human`     | `ready-for-human`    | Requires human implementation             |
| State    | `wontfix`             | `wontfix`            | Will not be actioned                      |

Every triaged issue should carry exactly one category role and one state role. When a skill mentions a role (for example, "apply the ready-for-agent triage label"), use the corresponding tracker string from this table.

## Inventory and provisioning invariant

Before recommending or changing this mapping, inventory every existing tracker label with its exact name, color, and description. Prefer an existing semantic equivalent over creating a duplicate canonical label. After approval, re-inventory, create only approved mapped strings that remain missing, then verify with a final inventory that all seven roles resolve to existing labels. Local Markdown records role strings and requires no label provisioning.

Edit the tracker-label column only through that ordered workflow.
