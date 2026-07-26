# July 2026 mpskills migration audit

> Historical record: the optional, personal, in-progress, and deprecated skills
> described below were removed on July 16, 2026. Omskills is now maintained
> independently and does not track or synchronize with the original repository.

## Scope

This audit reconstructs the migration from the sibling `mpskills` checkout into `omskills`, verifies the active catalog and local Codex installation, and separates omissions in PR #9 from upstream changes that landed afterward.

Authoritative comparison points:

- Upstream snapshot: `mattpocock/skills` tag `v1.1.0` (`d574778`), the latest release immediately before the migration PR.
- Migration source commit: `5e50a0c`, merged as `842010d` in PR #9 on 2026-07-08.
- Local upstream checkout: `../mpskills` at `46b600c` (whose tree includes the later skill changes), with remote comparison tip `origin/main` at `391a270`.

## What PR #9 got right

- Added the new `spec -> tickets -> implement -> review` workflow skills.
- Renamed `diagnose` to `diagnosing-bugs`, `to-prd` to `to-spec`, and `to-issues` to `to-tickets` consistently inside the repository.
- Graduated `code-review` and `wayfinder`, removed unused active skills, mirrored the Codex and Claude manifests, and aligned the top-level documentation.
- Preserved deliberate omskills adaptations around Codex, repository vocabulary, explicit setup, and conservative commit behavior.

## Omissions from the pre-merge upstream snapshot

The migration was internally consistent but not exhaustive:

- `prototype` missed upstream invocation and description changes from commit `850873c`.
- `writing-great-skills` missed the glossary restructuring and the later Negation failure mode (`8370e76`, `0847bb3`, `af6d692`).
- `teach` received the requested `./assets` backport but missed the preceding teaching refinements around mission changes, storage strength, primary sources, lesson design, and quiz cues.

These files were synchronized during this audit, while keeping repository-specific adaptations.

## Changes after PR #9

These were not mistakes in the original migration because they landed upstream later:

- `prototype` now preserves the prototype on a throwaway branch as a primary source.
- `setup-*` has a shorter, recommendation-first setup flow.
- Local `to-tickets` output changed from one combined file to one file per ticket.
- `setup-ts-deep-modules` was added under `in-progress/`; it remains excluded from plugin manifests here.

The compatible changes were ported and classified separately from the original omissions.
The local tracker template was also aligned so both normal tickets and wayfinder children use the configured `issues/` directory; otherwise the setup and producer skills would disagree.

## Installation failure and root cause

Issue #8 already identified manifest-versus-symlink drift before PR #9. The PR updated the manifest but did not run or validate the local installer, did not remove renamed links, and did not close the issue. As a result, Codex discovered only the surviving old symlinks; new skills such as `to-spec` were absent.

The old installer also used `rm -rf` on a real path that collided with a skill name. The repaired installer:

- validates source paths before linking;
- refuses to replace real files, directories, or external symlinks;
- removes only stale symlinks that point into this repository's `skills/` tree;
- supports `--check` for non-mutating installation verification.

`scripts/check-catalog.py` validates manifest mirroring, unique names, allowed buckets, skill files, frontmatter, and README coverage. `tests/test-link-skills.sh` covers clean installation, idempotence, stale managed links, preservation of external links, and collision safety.

## Process findings

GitHub contains one source commit and one non-approving `COMMENTED` review for PR #9, with no inline comments or correction commits. Review/correction loops may have happened in agent sessions, but they were not recorded durably. The recorded review explicitly left semantic workflow drift as residual risk and checked repository consistency rather than runtime discovery.

Future upstream syncs should record the upstream base commit, compare every shared active skill, classify additions/removals/renames, run the catalog checker, install into a temporary destination, and run `link-skills.sh --check` against the real installation before merge.

## Shared-skill disposition matrix

Every active manifest entry was compared with the corresponding upstream skill at `d574778` and, where it still exists, `../mpskills` commit `46b600c` plus remote tip `391a270`. “Adapted” means the remaining diff is intentional and omskills-specific.

| Omskills skill | Upstream lineage | Disposition |
| --- | --- | --- |
| `grill-with-docs` | same name | Matched upstream snapshot/current |
| `triage` | same name | Adapted setup name and ticket vocabulary |
| `improve-codebase-architecture` | same name | Matched; local support-file consolidation retained |
| `setup-omskills` | `setup-matt-pocock-skills` | Adapted for AGENTS-first Codex workflow and omskills naming; current friendlier setup flow ported |
| `to-spec` | `to-prd` → `to-spec` | Renamed and adapted to `setup-omskills` |
| `to-tickets` | `to-issues` → `to-tickets` | Renamed; current one-file-per-ticket behavior ported; setup name adapted |
| `implement` | same name | Adapted conservative commit policy and issue vocabulary |
| `wayfinder` | in-progress → engineering | Graduated; setup name adapted |
| `prototype` | same name | Missed snapshot change and later primary-source changes now ported; current match |
| `diagnosing-bugs` | `diagnose` → `diagnosing-bugs` | Renamed; current match |
| `research` | same name | Imported; current match |
| `tdd` | same name | Current match |
| `domain-modeling` | same name | Imported; current match |
| `codebase-design` | same name | Adapted description, relative links, and omskills architecture pointer |
| `code-review` | in-progress `review` → engineering | Graduated; ticket/spec and setup vocabulary adapted |
| `resolving-merge-conflicts` | same name | Adapted stronger trigger description and heading |
| `grill-me` | same name | Current match |
| `grilling` | same name | Current match |
| `handoff` | same name | Current match |
| `teach` | same name | Missed pre-merge refinements now ported; current match |
| `write-a-skill` | same name | Local procedural skill retained; upstream companion references already integrated |
| `writing-great-skills` | same name | Missed glossary/Negation changes now ported; current match |

Deliberate non-core dispositions: upstream personal `ask-matt` stays excluded; deprecated `ubiquitous-language` remains superseded by `domain-modeling`; upstream experimental `setup-ts-deep-modules` was copied to `in-progress` and remains outside both manifests; omskills-only optional/personal/deprecated skills remain in their documented buckets.

## Upstream commit ledger through the migration snapshot

The following is the complete non-merge commit set touching shared skill lineages from the initial 2026-05-24 adaptation through `d574778`. Commits are grouped by impact and each group has an explicit disposition.

| Area | Upstream commits | Migration disposition |
| --- | --- | --- |
| Planning, tickets, and implementation | `788b5c3`, `ffb2fa6`, `a0329ba`, `aa59111`, `f219e66`, `386d4ff`, `09a72ba`, `d29732e` | Workflow/renames imported in PR #9; current local-ticket shape ported in this audit |
| Wayfinder, research, review, and grilling | `5c3c49d`, `14c13c5`, `0d74d01`, `0e9a072`, `6f9e995`, `8c2a4c5`, `0172e61`, `e5932a7`, `639df6e` | Imported/graduated in PR #9; omskills setup vocabulary retained |
| TDD | `43ea088`, `e81f976`, `80e9dcc`, `bd453a6` | Imported in PR #9; current match |
| Prototype | `850873c` | Missed by PR #9; ported in this audit |
| Skill-writing reference | `bc4cf90`, `801a01c`, `aa7ed40`, `ee8bae4`, `8370e76`, `0847bb3`, `af6d692` | Initial skill imported in #5; glossary restructuring and Negation were missed and are now ported |
| Teaching | `2bf7005`, `59c92aa`, `e3d8b73`, `26ba8ae`, `d752177`, `3b37863`, `dabb725`, `694fa30`, `d20ee26`, `aa024cb` | Assets commits were selectively backported in #4; earlier teaching refinements were missed and are now ported |
| Domain/codebase/merge architecture | `e3b90b5`, `81ddacb`, `221ffca`, `2064fb6`, `cbf6db4`, `800201f`, `3832253`, `658d53e` | Imported through issues #3, #6, and #7 or already present; deliberate omskills adaptations retained |
| Triage request surface | `e00eadb` | Imported, with external PR request-surface default kept off |
| Earlier local teaching refinements | `aaf2453` | Superseded by the complete teaching sync above |

## Upstream changes after the migration snapshot

These commits post-date the comparison release and therefore are follow-up sync work, not PR #9 defects:

| Area | Upstream commits | Disposition here |
| --- | --- | --- |
| Prototype primary-source lifecycle | `d627460`, `cdec9f6`, `371b9c9`, `0375c88`, `fa460cb` | Ported; current shared files match |
| Friendlier setup and local ticket storage | `44eed54` | Ported with AGENTS-first and omskills-name adaptations |
| Stray `to-tickets` closing tag | `19c50d5` | Already absent locally; no change required |
| Experimental TypeScript deep modules | `30a9c74`, `d80ff7a`, `f947f93`, `3ea30af`, `3687fb4` | Copied to `in-progress`; not promoted to manifests |

GitHub bookkeeping was checked separately: issues #3, #5, #6, and #7 correspond to the June imports; issue #4 covers only the teach assets backport; issue #8 predicted installation drift and remained open through PR #9; issue #2 became obsolete when `deep-coder` was deleted. PR #9 has one source commit, one `COMMENTED` review, no inline review findings, and no recorded correction commits.
