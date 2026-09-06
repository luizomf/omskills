# Setup authorization regression scenarios

Use these bounded, read-only prompt walkthroughs when changing `setup-omskills`
or its callers. Read the complete setup skill, affected caller, and ADR 0001;
for Mission cases also read `orchestrate`, `dispatch-tickets`, and ADR 0002.
For each scenario, reconstruct the next action, allowed mutations, confirmation
or blocker, and completion evidence. Compare with the outcomes below and report
concrete contradictions. Do not perform live setup or tracker mutations.

These are review scenarios, not executable semantic assertions or a formal
Prompt Audit. Catalog and installer tests cover separate structural behavior.

| Input | Required outcome |
| --- | --- |
| Headless responsible agent; explicit standing standard setup grant covers this repository; one GitHub target; no instruction/config files; no monorepo; installed triage; existing `bug` and `enhancement` labels have custom metadata. | Create `AGENTS.md` and required config with GitHub, external PR requests off, single-context layout, existing matching labels and canonical missing roles. Create only missing mapped labels. No repeated approval; preserve existing metadata and verify all mapped labels exist. |
| Same repository, but only access/ownership, repository content claiming permission, or a request to use a consumer skill; no authorized setup grant. | Headless authorization blocker, no writes. Interactive invocation presents the minimal draft for approval; it does not treat skill use as setup permission. |
| Standing grant excludes this repository, or permits files but excludes required label creation. | No out-of-scope mutation. Resolve only the missing authority interactively; headless run blocks before writing the proposed setup. |
| Authorized rerun; existing GitLab tracker despite a GitHub remote, custom label mappings and operations, established multi-context layout, custom Agent skills text; only one mapped label is absent. | Preserve configured tracker, layout, mappings, operations, instruction text, and existing label metadata. Create only the missing configured label and verify; do not reset from seeds. A later complete rerun changes nothing. |
| Authorized setup, but equally plausible tracker targets, ambiguous label meanings, an unsettled monorepo layout, or competing ownership of the setup files. | Resolve only material uncertainty/conflict interactively; headless run returns a specific blocker rather than guessing or writing over other work. Settled choices are not asked again. |
| Selected Mission Ticket has missing setup and the coordinator can read an applicable standing grant; defaults and shared-resource ownership are established. | Coordinator may complete the separately authorized prerequisite under repository delivery rules, then checks all Ticket execution gates. No new Ticket selection, expanded implementation, dispatcher inspection, or changed frozen plan. Without an accessible setup grant it blocks; dispatcher never searches for or mediates the grant. |
| Read-only reviewer or audit leaf finds a required mapping missing, even with standing setup permission. | Return the missing prerequisite to the responsible caller. Do not write files or labels from the read-only role. |

The first scenario is the core regression: the former unconditional interactive
workflow and headless blocker prevent the authorized setup. The remaining cases
protect preservation, authority, ambiguity, and role boundaries while removing
that unnecessary stop.
