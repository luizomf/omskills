# Sannux consumer verification

**Ticket:** [luizomf/omskills#41](https://github.com/luizomf/omskills/issues/41)
**Verified:** 2026-08-31
**Result:** PASS with the synchronization gap recorded below

This report is public-safe evidence for one non-publishing integration run. It
contains no credentials, environment values, native sessions, real logs,
private configuration, production marker identities, or private runtime input.
Paths use these placeholders:

```text
PROJECTS_DIR=$HOME/Desktop/tutoriais_e_cursos
FIXTURE=$PROJECTS_DIR/omskills/.scratch/ticket-41-run
AUTOMATION_ROOT=$HOME/.codex/automations/daily-paper-llm-roundup
SNAPSHOT=$HOME/sannux-data/agent-homes/pi/.pi/agent
```

`FIXTURE` was ignored, disposable, and removed after extracting the bounded
evidence in this report.

## Safety preflight

The successful run fixed these source identities before snapshot or container
mutation:

| Source | Commit or identity |
| --- | --- |
| omskills candidate and report base | `e53d4efe78ab30812151d7b41d72296980990ed4` |
| ompi extension candidate | `6bdc3a7488270683cf9934301f30ad9466d4c9bd` |
| Sannux consumer | `9b60bca44642736c737cf855442ad60e51ece013` |
| Omnews fixture source | `a800ac15eac7d9ca875512c6d5e35a0090d503c9` |
| Daily Paper consumer | `22e56513e14910251b9a2a6f7423237b4120de1b` |
| Sannux Pi image | `sha256:64c462d4a0256499007b94ea5f210c5ff331f229a7c25fda5132784faeb2ae00` |
| Pi in the image | `0.84.4` |

All four product checkouts were clean on `main` and equal to `origin/main`.
The Daily Paper checkout was also clean on `main` and equal to its remote.
Sannux had no open Issue or pull request, no Compose project or container was
active, and no Sannux/Daily Paper/Omnews consumer process was running. The
current Ticket was the only open Sannux-consumer work in omskills.

An earlier preflight had fixed ompi at
`c3aa6aa26878ce8c9f73cb51cf3b826b98439cd8`. Two independently delivered ompi
changes advanced `main` before synchronization. That attempt stopped before
snapshot or container mutation. The successful run repeated preflight and fixed
the current clean `6bdc3a7` source shown above; it did not silently exercise the
older candidate.

Only environment key presence and ownership/mode were inspected. No value was
printed. The Pi and nested Codex authentication files and the ephemeral GitHub
configuration existed with private modes. The container path
`$HOME/.config/bq/config.json` was absent, so no host OMQueue configuration,
socket, state, or authority could enter the run. Neither fixture invoked `bq`,
`scheduler_submit`, a Queue payload, or the production runner.

The Daily Paper invocation explicitly set these path keys to reviewed fixture
or source locations without recording values:

```text
PROJECTS_DIR AUTOMATION_ROOT SANNUX_ROOT SITE_ROOT SANNUX_EPHEMERAL
TTS_READY_DIR NODE_MODULES_DIR CURDIR
```

The reviewed process boundary was synchronous and non-detached:

- `run-pi-ephemeral.sh` executes `sannux_ephemeral` in the foreground;
- `sannux_ephemeral` uses `docker compose run --rm`, with no `-d`;
- non-TTY execution adds `-T`, and Compose uses `init: true`;
- an `EXIT` trap removes the random ephemeral Pi home;
- print-mode `subagent_start` remains pending for its direct result;
- the disposable workspace, TTS inbox, dependency mount, and bounded outputs
  stayed under `FIXTURE` and were removed after review.

## Candidate synchronization and identity

The reviewed synchronization command was:

```bash
PROJECTS_DIR="$PROJECTS_DIR" \
  "$HOME/dotfiles/scripts/sannux_ephemeral" --refresh-pi-resources
```

The launcher followed the host Pi extension and skill links, excluded host
`node_modules`, rebuilt extension production dependencies in Linux, and replaced
the two snapshot resource directories. It reported:

```text
added 2 packages, and audited 3 packages
found 0 vulnerabilities
Refreshed current Pi resources from $HOME/.pi/agent
```

The distributed `dispatch-tickets` skill was installed in the shared
`$HOME/.agents/skills` destination, while this snapshot launcher reads the
legacy `$HOME/.pi/agent/skills` destination. It was therefore absent immediately
after the standard refresh. The authorized snapshot synchronization copied the
exact delivered skill directly from the fixed omskills checkout:

```bash
mkdir -p "$SNAPSHOT/skills/dispatch-tickets"
rsync -aL --delete \
  "$PROJECTS_DIR/omskills/skills/engineering/dispatch-tickets/" \
  "$SNAPSHOT/skills/dispatch-tickets/"
```

No repository or host installation behavior was changed. The snapshot then
contained 29 omskills skills and 8 Pi extension entries. Source and snapshot
SHA-256 values matched byte-for-byte:

| Candidate file | SHA-256 |
| --- | --- |
| `extensions/subagents/index.ts` | `e8097c930df0116386d1bcf7df186c33a453496329653b010a902818e22ee3af` |
| `extensions/subagents/controller.ts` | `395cb3f3c334cd7ef0f77d391245eaf2955e3da5da4d8041c73926ba66789dca` |
| `skills/dispatch-tickets/SKILL.md` | `b1114d9edb85d312aa0c680e04c9a70845e1080d7c370272b3944420bca2e8ad` |
| `skills/orchestrate/SKILL.md` | `7547d2ca18e6cb34d1cca38a1ed33f2284dfcf47beaeb84d3f5d2f2f2a7a9766` |

An in-container inventory independently returned the same four hashes, Pi
`0.84.4`, `skills=29`, and `extensions=8`. This proves that the consumers loaded
the refreshed candidate rather than the previous snapshot.

## Omnews non-subagent smoke

The fixture was a clean `--no-hardlinks` clone at Omnews commit
`a800ac15eac7d9ca875512c6d5e35a0090d503c9`. It had no runtime data or
untracked files. The smallest read-only print invocation was:

```bash
PROMPT='Authorized isolated Omnews compatibility smoke. Do not invoke subagents, managed processes, schedulers, tmux, network access, or write files. Work only in /workspace. Use the bash tool to verify all of these: Node reads package.json with name exactly omnews and version exactly 0.1.0; git status --porcelain is empty; /home/agent/.pi/agent/extensions/subagents/index.ts exists; /home/agent/.pi/agent/skills/dispatch-tickets/SKILL.md exists. Then use bash again to prove git status is still empty. If and only if every check passes, make your final assistant response exactly OMNEWS_SMOKE_OK with no other text.'

PROJECTS_DIR="$PROJECTS_DIR" CURDIR="$FIXTURE/omnews-smoke" \
  "$HOME/dotfiles/scripts/sannux_ephemeral" pi -p "$PROMPT"
```

The command exited zero and its complete stdout was:

```text
OMNEWS_SMOKE_OK
```

The output contained no subagent result or pong. The cloned workspace remained
clean, the container was removed, and no launcher process remained. This proves
that ordinary loading of the refreshed extension set did not regress the
non-subagent Omnews path.

## Daily Paper fixed sequence

The disposable local Git repository began at fixture commit `5a4a174`. It had
no remote and configured an immutable local tracker. Its accepted synthetic
Tickets were:

1. `fixture/daily-paper#1` — create only `deliverables/alpha.txt` with the exact
   line `alpha delivered` and verify it locally;
2. `fixture/daily-paper#2` — require Ticket 1, create only
   `deliverables/beta.txt` with the exact line `beta delivered`, and verify both.

Each Ticket was open, `enhancement`, `ready-for-agent`, dependency/conflict
complete, and carried a current local Prompt Audit `PASS`. Fixture instructions
required installed `orchestrate`, one fresh direct writer, one fresh direct
read-only reviewer, local commits, and no remote, tracker mutation, network,
publishing, Queue, server, tmux, or detached process.

The actual Daily Paper Sannux runner and read-only Compose override were used
with every writable or outbound path replaced by the disposable fixture:

```bash
PROMPT='Load and follow installed `dispatch-tickets`. This invocation explicitly grants Mission authorization for exactly this fixed ordered list of unique Tickets: [fixture/daily-paper#1, fixture/daily-paper#2]. Preserve that order and dispatch no other work. This is the authorized disposable non-publishing Daily Paper Sannux fixture; resolve each Ticket only from the local /workspace repository and obey its AGENTS.md. Complete the finite print-mode Mission and return the dispatcher compact terminal report.'

PROJECTS_DIR="$PROJECTS_DIR" \
AUTOMATION_ROOT="$AUTOMATION_ROOT" \
SANNUX_ROOT="$PROJECTS_DIR/sannux" \
SITE_ROOT="$FIXTURE/daily-workspace" \
SANNUX_EPHEMERAL="$HOME/dotfiles/scripts/sannux_ephemeral" \
TTS_READY_DIR="$FIXTURE/daily-tts-ready" \
NODE_MODULES_DIR="$FIXTURE/daily-node-modules" \
  "$AUTOMATION_ROOT/runners/run-pi-ephemeral.sh" -p "$PROMPT"
```

The command did **not** invoke
`queue-automatic-daily-paper-live.sh`, `--publish-live`, host `bq`, OMQueue,
the production site checkout, production Omnews data, or a real TTS marker.
It exited zero. Its one-line terminal output, with native session paths redacted,
was:

```text
fixture/daily-paper#1 delivered; ref 66340e79a09b5a6907b0138083e2e5d060fc099f; session <coordinator-session-1> | fixture/daily-paper#2 delivered; ref 3056ca4e85493e6057e2cc9b4cf87adae8e964c9; session <coordinator-session-2>; 2/2 delivered; Mission complete; print settled; no pong pending.
```

The two distinct coordinator session references were present in the bounded
result. The disposable repository independently proved the ordered commits:

```text
5a4a174 chore(fixture): initialize disposable tickets
66340e7 feat(fixture): deliver alpha
3056ca4 feat(fixture): deliver beta
```

Commit `66340e7` changed only `deliverables/alpha.txt`; commit `3056ca4`
changed only `deliverables/beta.txt`. `./verify.sh all` returned
`fixture verification ok: all`, both files had exactly the accepted bytes, and
the worktree was clean. The dispatcher emitted no `[PONG]`, advanced only after
each matching `delivered`, and reported both `Mission complete` and
`print settled; no pong pending` before the foreground container exited.

## Failure, cancellation, and cleanup fixtures

The deterministic dispatcher reference model was run with:

```bash
cd "$PROJECTS_DIR/omskills"
./tests/test-dispatch-tickets.py
```

It passed with:

```text
dispatch-tickets contract and state-machine scenarios ok
```

Those executable scenarios distinguish:

- a recorded matching dispatcher interrupt and matching `interrupted` pong,
  which alone becomes `cancelled`;
- rejected or mismatched interrupt confirmation;
- unsolicited interruption;
- missing, malformed, duplicate, truncated, wrong-path, wrong-identity, and
  wrong-status outcomes;
- failure cleanup of the still-active matching coordinator;
- preserved native session references in stopped reports.

The current ompi candidate's real controller/RPC/process fixtures were run with:

```bash
cd "$PROJECTS_DIR/ompi"
npm test -- \
  extensions/subagents/controller.test.ts \
  extensions/subagents/inheritance.test.ts \
  extensions/subagents/native-inheritance.test.ts \
  extensions/subagents/native-nesting.test.ts \
  extensions/subagents/presentation.test.ts
```

Result: 5 files and 71 tests passed. The native nested fixture creates a real
depth-2 coordinator and depth-3 direct leaf using `process.execPath` with literal
arguments, records their PIDs, interrupts the owner, and asserts both processes
are dead, the active subtree is empty, and the interrupted native session
reference is retained. Its shutdown path repeats the descendant cleanup. The
presentation fixture preserves session references in bounded failed and
interrupted direct results. No fixture uses an unmanaged shell worker.

Before and after the Daily Paper run, the following bounded counts were exactly
equal:

| Observable | Before | After |
| --- | ---: | ---: |
| production untrusted TTS inbox files | 0 | 0 |
| production trusted TTS directory files | 91 | 91 |
| existing unrelated tmux sessions | 27 | 27 |
| Docker containers | 0 | 0 |
| Pi ephemeral homes | 0 | 0 |
| snapshot staging/backup paths | 0 | 0 |

The fixture TTS inbox and dependency directory stayed empty. A final process
check found no `run-pi-ephemeral`, `sannux_ephemeral`, `pi-agent-run`, subagent
RPC, or transfer-watchdog process. There was no later output path because the
print call settled directly, the foreground Pi process exited, Compose removed
the container, and the ephemeral home trap completed.

## Repository verification

The final candidate passed:

```text
./scripts/check-catalog.py
  catalog ok: 27 active skills

./tests/test-link-skills.sh
  linker tests ok

./scripts/link-skills.sh --check
  27 active managed links reported ok

./tests/test-dispatch-tickets.py
  dispatch-tickets contract and state-machine scenarios ok

./tests/test-skill-suite-evidence.py
  skill-suite evidence ok: dynamic catalog and resource contracts complete

ompi focused runtime
  5 files / 71 tests passed
```

`git diff --check` was also required on the final report commit and committed
range.

## Evidence gaps and boundaries

- The standard Sannux refresh currently reads Pi-local skills, while the current
  omskills installer manages active skills in the shared agent destination.
  Without the explicit, hash-verified snapshot copy recorded above, a later
  refresh would omit `dispatch-tickets`. This Ticket performed only the
  authorized snapshot synchronization; it did not change the launcher,
  installer, Sannux, or Pi behavior.
- Ephemeral session files were intentionally deleted with the credential-bearing
  Pi home. The public report retains only the fact that two distinct native
  coordinator references were returned; it does not retain or expose session
  contents or paths.
- Cancellation classification is covered by the omskills executable state
  machine, while recursive process and session behavior is covered by ompi's
  native deterministic fixture. A real model-driven cancellation was not forced
  into the successful print Mission because print delivery is intentionally
  direct and has no interactive stop turn.
- No product defect was repaired, and no Sannux, Omnews, Daily Paper, ompi,
  dotfiles, production automation, Queue/TTS state, tag, release, or publication
  was changed. The only persistent runtime write outside the disposable fixture
  was the authorized refreshed Sannux Pi resource snapshot.
