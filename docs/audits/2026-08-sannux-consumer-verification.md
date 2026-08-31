# Sannux consumer verification

**Ticket:** [luizomf/omskills#41](https://github.com/luizomf/omskills/issues/41)
**Verified:** 2026-08-31
**Result:** PASS with the synchronization gap recorded below

This is the public-safe evidence record for a non-publishing integration run.
It contains no credentials, environment values, native sessions, raw logs,
private configuration, production marker identities, or private runtime input.
Commands use these placeholders:

```text
PROJECTS_DIR=$HOME/Desktop/tutoriais_e_cursos
FIXTURE=$PROJECTS_DIR/omskills/.scratch/ticket-41-run
AUTOMATION_ROOT=$HOME/.codex/automations/daily-paper-llm-roundup
SNAPSHOT=$HOME/sannux-data/agent-homes/pi/.pi/agent
```

`FIXTURE` was ignored, disposable, and removed after the bounded facts below
were extracted and reviewed.

## Safety preflight

The successful run fixed these identities before snapshot or container mutation:

| Source | Commit or identity |
| --- | --- |
| omskills candidate/report base | `e53d4efe78ab30812151d7b41d72296980990ed4` |
| ompi extension candidate | `6bdc3a7488270683cf9934301f30ad9466d4c9bd` |
| Sannux consumer | `9b60bca44642736c737cf855442ad60e51ece013` |
| Omnews fixture source | `a800ac15eac7d9ca875512c6d5e35a0090d503c9` |
| Daily Paper consumer | `22e56513e14910251b9a2a6f7423237b4120de1b` |
| Sannux Pi image | `sha256:64c462d4a0256499007b94ea5f210c5ff331f229a7c25fda5132784faeb2ae00` |
| Pi in the image | `0.84.4` |

The literal clean-source guard was equivalent to:

```bash
set -euo pipefail
for spec in \
  "$PROJECTS_DIR/omskills e53d4efe78ab30812151d7b41d72296980990ed4" \
  "$PROJECTS_DIR/ompi 6bdc3a7488270683cf9934301f30ad9466d4c9bd" \
  "$PROJECTS_DIR/sannux 9b60bca44642736c737cf855442ad60e51ece013" \
  "$PROJECTS_DIR/omnews a800ac15eac7d9ca875512c6d5e35a0090d503c9"; do
  repo=${spec% *}; expected=${spec##* }
  test "$(git -C "$repo" rev-parse HEAD)" = "$expected"
  test -z "$(git -C "$repo" status --porcelain)"
done
test "$(git -C "$HOME/.codex" rev-parse HEAD)" = \
  22e56513e14910251b9a2a6f7423237b4120de1b
test -z "$(git -C "$HOME/.codex" status --porcelain)"
test ! -e "$HOME/sannux-data/agent-homes/pi/.config/bq/config.json"
command -v docker rsync node npm git >/dev/null
docker compose version >/dev/null
```

Sannux had no open Issue or pull request, and no concurrent process was changing
the resource snapshot or either disposable fixture. An unrelated short-lived
Sannux consumer observed during later evidence correction was neither stopped
nor inspected; fixture cleanup was bound to its exact container name rather
than to a global container count.

An earlier preflight had fixed ompi at
`c3aa6aa26878ce8c9f73cb51cf3b826b98439cd8`. Two separately delivered ompi
changes advanced `main` before synchronization. That attempt stopped before
snapshot or container mutation. Preflight then fixed the clean `6bdc3a7` source
above; no consumer silently exercised the older candidate.

Only environment-key presence and ownership/mode were inspected; no value was
printed. Pi, nested Codex, and ephemeral GitHub credentials existed with private
modes. The absent container `bq` configuration meant no host OMQueue
configuration, socket, state, or authority entered the run. No fixture invoked
`bq`, `scheduler_submit`, a Queue payload, or the production runner.

The process boundary was synchronous and non-detached:

- the fixture runner executed `sannux_ephemeral` in the foreground;
- `sannux_ephemeral` used `docker compose run --rm`, never `-d`;
- non-TTY execution added `-T`, and Compose used `init: true`;
- an `EXIT` trap removed each random ephemeral Pi home;
- print-mode `subagent_start` remained pending for its direct result;
- every writable fixture path stayed under the guarded `FIXTURE` root.

## Candidate synchronization and identity

The actual persistent Sannux Pi destination was refreshed with:

```bash
PROJECTS_DIR="$PROJECTS_DIR" \
  "$HOME/dotfiles/scripts/sannux_ephemeral" --refresh-pi-resources
```

The launcher followed host links, excluded host `node_modules`, rebuilt
extension production dependencies in Linux, atomically replaced both resource
directories, and reported:

```text
added 2 packages, and audited 3 packages
found 0 vulnerabilities
Refreshed current Pi resources from $HOME/.pi/agent
```

`dispatch-tickets` was installed in the shared `$HOME/.agents/skills`
destination, while this snapshot launcher reads the legacy
`$HOME/.pi/agent/skills` destination. It was absent after the standard refresh.
The authorized snapshot synchronization copied the exact fixed skill directly:

```bash
test "$SNAPSHOT" = \
  "$HOME/sannux-data/agent-homes/pi/.pi/agent"
mkdir -p "$SNAPSHOT/skills/dispatch-tickets"
rsync -aL --delete \
  "$PROJECTS_DIR/omskills/skills/engineering/dispatch-tickets/" \
  "$SNAPSHOT/skills/dispatch-tickets/"
```

No repository or host installation behavior changed. A normalized complete-tree
manifest hashed `relative-path NUL file-bytes NUL`, followed symlinked source
directories, and excluded only extension `node_modules` on both sides. The
source, snapshot, and in-container results were:

| Complete tree | Files | SHA-256 |
| --- | ---: | --- |
| host extension source | 47 | `66495c23484afd26127f42e1ebc3b053f49a39c3d3177938825e54dad1d2e65f` |
| snapshot extensions | 47 | `66495c23484afd26127f42e1ebc3b053f49a39c3d3177938825e54dad1d2e65f` |
| in-container extensions | 47 | `66495c23484afd26127f42e1ebc3b053f49a39c3d3177938825e54dad1d2e65f` |
| 29 repository skill sources | 55 | `ec7c91538b2281df9bc037b1c3eb371ad66a61084b91f0323ab9b9e0930de17a` |
| snapshot skills | 55 | `ec7c91538b2281df9bc037b1c3eb371ad66a61084b91f0323ab9b9e0930de17a` |
| in-container skills | 55 | `ec7c91538b2281df9bc037b1c3eb371ad66a61084b91f0323ab9b9e0930de17a` |

The mechanical source/snapshot check was:

```bash
python3 - "$HOME/.pi/agent/extensions" "$SNAPSHOT/extensions" \
  "$PROJECTS_DIR/omskills/skills" "$SNAPSHOT/skills" <<'PY'
from pathlib import Path
import hashlib, os, sys

def walk(root, exclude_node=False):
    root = Path(root)
    items = []
    for current, dirs, files in os.walk(root, followlinks=True):
        dirs[:] = sorted(d for d in dirs if not (exclude_node and d == "node_modules"))
        for name in sorted(files):
            path = Path(current) / name
            items.append((path.relative_to(root).as_posix(), path.read_bytes()))
    return items

def digest(items):
    value = hashlib.sha256()
    for relative, data in sorted(items):
        value.update(relative.encode()); value.update(b"\0")
        value.update(data); value.update(b"\0")
    return len(items), value.hexdigest()

source_extensions = walk(sys.argv[1], True)
snapshot_extensions = walk(sys.argv[2], True)
source_skills = []
for skill_file in sorted(Path(sys.argv[3]).glob("*/*/SKILL.md")):
    for relative, data in walk(skill_file.parent):
        source_skills.append((f"{skill_file.parent.name}/{relative}", data))
snapshot_skills = walk(sys.argv[4])
assert digest(source_extensions) == digest(snapshot_extensions)
assert digest(source_skills) == digest(snapshot_skills)
print(digest(source_extensions), digest(source_skills))
PY
```

The same algorithm ran inside `sannux_ephemeral pi --shell`. It also returned
Pi `0.84.4`, 29 skill directories, and 8 extension entries. The complete
manifest, including every runtime file changed after `c3aa6aa`, excludes an
older or mixed candidate.

## Omnews mechanically non-subagent smoke

The fixture was a clean `--no-hardlinks` clone at Omnews commit
`a800ac15eac7d9ca875512c6d5e35a0090d503c9` with no runtime data. Extension
discovery remained enabled, while the Pi CLI mechanically allowed only the
built-in `read` and `bash` tools:

```bash
git clone --quiet --no-hardlinks \
  "$PROJECTS_DIR/omnews" "$FIXTURE/omnews-smoke"
PROMPT='Authorized isolated Omnews compatibility smoke. The CLI mechanically allows only read and bash, so no subagent or other extension tool can be invoked. Do not use network access or write files. Work only in /workspace. Use bash to verify: Node reads package.json with name exactly omnews and version exactly 0.1.0; git status --porcelain is empty; /home/agent/.pi/agent/extensions/subagents/index.ts exists; /home/agent/.pi/agent/skills/dispatch-tickets/SKILL.md exists. Use bash again to prove git status is still empty. If and only if every check passes, make your final assistant response exactly OMNEWS_SMOKE_NO_SUBAGENT_OK with no other text.'
PROJECTS_DIR="$PROJECTS_DIR" CURDIR="$FIXTURE/omnews-smoke" \
  "$HOME/dotfiles/scripts/sannux_ephemeral" pi -p \
  --tools read,bash "$PROMPT"
test -z "$(git -C "$FIXTURE/omnews-smoke" status --porcelain)"
```

The command exited zero with complete stdout:

```text
OMNEWS_SMOKE_NO_SUBAGENT_OK
```

Because `--tools read,bash` is a CLI allowlist across built-in, extension, and
custom tools, `subagent_start` was unavailable even though the refreshed
extension set loaded. The exact fixture container was removed, and the clone
remained clean. Ordinary extension loading therefore did not regress the
non-subagent Omnews path.

## Daily Paper fixed sequence

### Reconstructable disposable fixture

The local repository had no remote and an immutable tracker. Its base commit was
`d6bb68f729d736c6bd39c496319488b83305ecab`; its complete base tree was
`01f160a407d208b2c98ebcdc514e75f6666e8c43`.

The exact public fixture source is bundled at
`docs/audits/fixtures/prepare-sannux-consumers.sh`. It writes the complete
`AGENTS.md`, domain/ADR/tracker configuration, both OPEN `ready-for-agent`
Tickets and current Prompt Audit `PASS` records, byte-exact deliverable
contracts, verifier, fixture-only runner, and Compose override. It refuses an
existing or unexpected target. The durable topology analyzer is
`docs/audits/fixtures/analyze-sannux-topology.py`.

The construction and identity commands were:

```bash
cd "$PROJECTS_DIR/omskills"
AUTOMATION_ROOT="$AUTOMATION_ROOT" \
  ./docs/audits/fixtures/prepare-sannux-consumers.sh
git -C "$FIXTURE/daily-workspace" init -b main
git -C "$FIXTURE/daily-workspace" add \
  AGENTS.md CONTEXT.md docs tracker verify.sh
git -C "$FIXTURE/daily-workspace" commit \
  -m 'chore(fixture): initialize instrumented tickets'
test -z "$(git -C "$FIXTURE/daily-workspace" remote)"
test "$(git -C "$FIXTURE/daily-workspace" rev-parse HEAD^{tree})" = \
  01f160a407d208b2c98ebcdc514e75f6666e8c43
```

The exact synthetic Tickets authorize only `alpha delivered\n` and
`beta delivered\n` in distinct files and deterministic local verification.
They prohibit network, remote, push, Queue, tmux, server, watcher, detached
work, tracker mutation, and depth-3 delegation.

### Non-publishing Compose boundary

A first path review found that the production runner fixes its TTS-ready and
Linux dependency paths internally; caller variables do not override them. That
preliminary run changed neither path, but it is not the non-publishing evidence
used here.

The accepted run used an ignored fixture-only copy of the runner contract with
all seven path variables required explicitly. It retained the same foreground
`exec "$SANNUX_EPHEMERAL" pi "$@"` and base Sannux Compose file, but exported a
fixture-only Compose override. The override:

- mounted the real Daily Paper agents, skills, assets, and marker script
  read-only through fixture symlinks;
- mounted only `$FIXTURE/daily-tts-ready` and
  `$FIXTURE/daily-node-modules` as writable non-workspace paths;
- mounted the disposable Git repository as `/workspace`;
- changed unused `OMNEWS_BASE_URL` to `http://127.0.0.1:9`;
- omitted the production Git URL rewrite and credential helper;
- set `PI_CODING_AGENT_SESSION_DIR=/workspace/.evidence-sessions` solely for
  bounded topology inspection.

The exact resolved-Compose guards were:

```bash
PROJECTS_DIR="$PROJECTS_DIR" \
AUTOMATION_ROOT="$FIXTURE/daily-automation" \
SANNUX_ROOT="$PROJECTS_DIR/sannux" \
SITE_ROOT="$FIXTURE/daily-workspace" \
SANNUX_EPHEMERAL="$HOME/dotfiles/scripts/sannux_ephemeral" \
TTS_READY_DIR="$FIXTURE/daily-tts-ready" \
NODE_MODULES_DIR="$FIXTURE/daily-node-modules" \
  "$FIXTURE/daily-automation/runners/run-pi-ephemeral-fixture.sh" \
  --compose-config > "$FIXTURE/compose.yml"
! grep -q '192\.168\.' "$FIXTURE/compose.yml"
! grep -q 'git-credential\|insteadOf\|GIT_CONFIG' "$FIXTURE/compose.yml"
grep -q 'OMNEWS_BASE_URL: http://127.0.0.1:9' "$FIXTURE/compose.yml"
grep -q 'PI_CODING_AGENT_SESSION_DIR: /workspace/.evidence-sessions' \
  "$FIXTURE/compose.yml"
grep -q "$FIXTURE/daily-tts-ready" "$FIXTURE/compose.yml"
grep -q "$FIXTURE/daily-node-modules" "$FIXTURE/compose.yml"
```

Provider credentials remained in the ephemeral Pi home because the model and
nested agents require them. The disposable repository had no remote, the
production checkout was not mounted, the Queue configuration was absent, and
no production trigger or marker path was available. These are narrower,
mechanical non-publishing boundaries rather than a claim that the model had no
network transport.

### Print execution and topology evidence

The finite invocation was:

```bash
PROMPT='Load and follow installed `dispatch-tickets`. This invocation explicitly grants Mission authorization for exactly this fixed ordered list of unique Tickets: [fixture/daily-paper#1, fixture/daily-paper#2]. Preserve that order and dispatch no other work. This is the authorized disposable non-publishing Daily Paper Sannux fixture; resolve each Ticket only from the local /workspace repository and obey its AGENTS.md. Complete the finite print-mode Mission and return the dispatcher compact terminal report.'
PROJECTS_DIR="$PROJECTS_DIR" \
AUTOMATION_ROOT="$FIXTURE/daily-automation" \
SANNUX_ROOT="$PROJECTS_DIR/sannux" \
SITE_ROOT="$FIXTURE/daily-workspace" \
SANNUX_EPHEMERAL="$HOME/dotfiles/scripts/sannux_ephemeral" \
TTS_READY_DIR="$FIXTURE/daily-tts-ready" \
NODE_MODULES_DIR="$FIXTURE/daily-node-modules" \
  "$FIXTURE/daily-automation/runners/run-pi-ephemeral-fixture.sh" \
  -p "$PROMPT"
```

It did **not** invoke `queue-automatic-daily-paper-live.sh`, `--publish-live`,
host `bq`, OMQueue, the production site checkout, production Omnews data, or a
real TTS marker. It exited zero with this one-line result after redacting only
native session paths:

```text
fixture/daily-paper#1 delivered; ref 01d47286dcef3690010aeb631e116842c73f3d54; session <coordinator-session-1> | fixture/daily-paper#2 delivered; ref 497c4ea70860a29ae502fefa119b037df2f95b6d; session <coordinator-session-2>; 2/2 delivered; Mission complete; print settled; no pong pending.
```

Before deleting sessions, the bundled public-safe analyzer counted assistant
`toolCall` records and their literal `delivery` arguments:

```bash
python3 docs/audits/fixtures/analyze-sannux-topology.py \
  "$FIXTURE/daily-workspace/.evidence-sessions"
```

It emitted only:

```text
session_files=7
root_sessions=1
coordinator_sessions=2
writer_sessions=2
reviewer_sessions=2
root_direct_starts=2
coordinator_direct_starts=4
leaf_starts=0
pong_markers=0
```

The assertions required exactly one root, two distinct fresh coordinators, two
writers, two reviewers, two root `subagent_start` calls with `delivery=direct`,
two direct starts in each coordinator, zero leaf starts, and zero pong markers.
Role classification used only each session's initial fixture prompt. No message,
prompt, response, path, or session identity entered the report.

The disposable repository independently proved:

```text
d6bb68f chore(fixture): initialize instrumented tickets
01d4728 feat(fixture): deliver alpha
497c4ea feat(fixture): deliver beta
fixture verification ok: all
```

Commit `01d4728` changed only `deliverables/alpha.txt`; commit `497c4ea`
changed only `deliverables/beta.txt`. Both had the exact accepted bytes, and the
worktree was clean after the seven inspected session files were removed. The
dispatcher advanced only through matching `delivered`, returned both native
coordinator references, and settled without a pong before the foreground
fixture container exited.

## Failure, cancellation, and cleanup fixtures

The deterministic dispatcher model passed:

```bash
cd "$PROJECTS_DIR/omskills"
./tests/test-dispatch-tickets.py
# dispatch-tickets contract and state-machine scenarios ok
```

It distinguishes the sole matching-cancellation path from rejected, mismatched,
or unsolicited interruption and from missing, malformed, duplicate, truncated,
wrong-path, wrong-identity, and wrong-status outcomes. It also preserves native
references in stopped reports and requires cleanup settlement before failure.

The current ompi candidate's real controller/RPC/process fixtures passed 5 files
and 71 tests:

```bash
cd "$PROJECTS_DIR/ompi"
npm test -- \
  extensions/subagents/controller.test.ts \
  extensions/subagents/inheritance.test.ts \
  extensions/subagents/native-inheritance.test.ts \
  extensions/subagents/native-nesting.test.ts \
  extensions/subagents/presentation.test.ts
```

The native fixture starts a real depth-2 coordinator and depth-3 direct leaf
with `process.execPath` and literal arguments, records their PIDs, interrupts the
owner, and asserts both are dead, the active subtree is empty, and the native
session reference survives. Shutdown repeats recursive cleanup. Presentation
fixtures retain session references for bounded failed/interrupted direct
results. No fixture uses an unmanaged shell worker.

The exact bounded cleanup guard was:

```bash
SESSIONS="$FIXTURE/daily-workspace/.evidence-sessions"
test "$SESSIONS" = "$FIXTURE/daily-workspace/.evidence-sessions"
find "$SESSIONS" -maxdepth 2 -type f -print >/dev/null
rm -rf -- "$SESSIONS"
test ! -e "$SESSIONS"
test -z "$(git -C "$FIXTURE/daily-workspace" status --porcelain)"
# Extract the fixture container name from its own stderr, then:
! docker ps -a --format '{{.Names}}' | grep -qx "$FIXTURE_CONTAINER"
test -z "$(pgrep -f "$FIXTURE_CONTAINER" || true)"
test -z "$(find "$FIXTURE/daily-tts-ready" -mindepth 1 -print -quit)"
test -z "$(find "$FIXTURE/daily-node-modules" -mindepth 1 -print -quit)"
test "$FIXTURE" = "$PROJECTS_DIR/omskills/.scratch/ticket-41-run"
rm -rf -- "$FIXTURE"
test ! -e "$FIXTURE"
```

Before/after counts for the production untrusted TTS inbox (`0`), production
trusted TTS directory (`91`), and unrelated tmux sessions (`27`) were identical.
The fixture TTS and dependency directories stayed empty. The exact fixture
container and process were absent. Snapshot staging/backup paths were absent.
The seven session files occupied 316 KiB before guarded deletion; no native
session, raw output, cloned repository, or fixture file remained afterward.

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
bundled fixture reconstruction
  shell/Python syntax passed; generated tree matched 01f160a; Compose guards passed
  generated verification fixture removed
git diff --check <fixed-base>..HEAD
  passed
```

## Evidence gaps and boundaries

- The standard Sannux refresh reads Pi-local skills, while the current omskills
  installer manages active skills in the shared agent destination. Without the
  explicit complete-manifest-verified snapshot copy above, a later refresh
  would omit `dispatch-tickets`. This Ticket synchronized the authorized
  snapshot; it did not change launcher, installer, Sannux, or Pi behavior.
- Ephemeral session files were retained only long enough to produce bounded
  role/tool-count metadata, then deleted. The public report preserves two
  coordinator-reference facts and topology counts, not identities or contents.
- Cancellation classification is covered by the omskills executable state
  machine; recursive process/session behavior is covered by ompi's native
  deterministic fixture. A model-driven cancellation was not forced into the
  successful print Mission because direct print delivery has no interactive
  stop turn.
- No product defect was repaired, and no Sannux, Omnews, Daily Paper, ompi,
  dotfiles, production automation, Queue/TTS state, tag, release, or publication
  changed. The only persistent runtime write outside the disposable fixture was
  the authorized refreshed Sannux Pi resource snapshot.
