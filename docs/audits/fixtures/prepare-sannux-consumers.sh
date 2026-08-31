#!/usr/bin/env bash
set -euo pipefail

: "${AUTOMATION_ROOT:?Set AUTOMATION_ROOT to the reviewed Daily Paper source}"
repo_root="$(git rev-parse --show-toplevel)"
fixture="${repo_root}/.scratch/ticket-41-run"
workspace="${fixture}/daily-workspace"
fixture_automation="${fixture}/daily-automation"

test ! -e "$fixture" || {
  printf 'Fixture already exists: %s\n' "$fixture" >&2
  exit 73
}
case "$fixture" in
  "$repo_root"/.scratch/ticket-41-run) ;;
  *) printf 'Unsafe fixture path: %s\n' "$fixture" >&2; exit 70 ;;
esac

mkdir -p \
  "$workspace/docs/agents" \
  "$workspace/docs/adr" \
  "$workspace/tracker/tickets" \
  "$fixture_automation/runners" \
  "$fixture_automation/hooks/on-end/tts" \
  "$fixture/daily-tts-ready" \
  "$fixture/daily-node-modules" \
  "$fixture/outputs"

cat > "$workspace/AGENTS.md" <<'EOF'
# Disposable Daily Paper orchestration fixture

This repository exists only for the authorized non-publishing Sannux integration fixture for `luizomf/omskills#41`.

- Read `CONTEXT.md`, `docs/agents/issue-tracker.md`, and the selected Ticket before editing.
- English only for files, commits, and agent output.
- Tickets are immutable local files under `tracker/tickets/`; never use a network tracker or mutate those files.
- Work directly on the current local `main`. Do not create a branch, remote, pull request, tag, release, Queue job, tmux session, server, watcher, or detached process.
- There is intentionally no Git remote. A local commit is the complete integration boundary; never push.
- Writes are limited to the exact `deliverables/` file authorized by the selected Ticket. Preserve all other files.
- Each Ticket must use installed `orchestrate`: exactly one fresh direct writer, then exactly one fresh read-only reviewer. Depth-3 leaves must not delegate.
- The writer commits the complete tiny candidate. The coordinator adjudicates review, makes any surviving correction directly, verifies, and returns the required one-line Ticket outcome with the final commit as `ref`.
- Run only the Ticket's deterministic local verification command. No network, publication, production automation, secrets, or user Questions are needed or authorized.
EOF

cat > "$workspace/CONTEXT.md" <<'EOF'
# Fixture domain

**Fixture Ticket**: one immutable local tracked implementation unit used only to prove direct nested orchestration.

**Fixture deliverable**: one deterministic text file under `deliverables/`.

**Delivery**: a verified local Git commit. This disposable repository has no remote and requires no tracker mutation.
EOF

cat > "$workspace/docs/agents/issue-tracker.md" <<'EOF'
# Issue tracker: immutable local fixture

Resolve `fixture/daily-paper#N` by reading `tracker/tickets/N.md` in full. Each file contains its state, labels, assignment, dependencies, conflicts, complete contract, Agent Brief, and newest Prompt Audit status.

This fixture is read-only tracker evidence. Do not call `gh`, access a network, edit Ticket files, add comments, or close Tickets. The final local commit and coordinator outcome are the only delivery records required in this disposable repository.
EOF

cat > "$workspace/docs/agents/domain.md" <<'EOF'
# Domain docs

Read `CONTEXT.md` and `docs/adr/0001-disposable-local-delivery.md` before changing a fixture deliverable.
EOF

cat > "$workspace/docs/agents/triage-labels.md" <<'EOF'
# Triage labels

- Category: `enhancement`
- Eligible state: `ready-for-agent`
EOF

cat > "$workspace/docs/adr/0001-disposable-local-delivery.md" <<'EOF'
# Disposable local delivery

The fixture uses local commits without a remote so integration cannot publish or mutate an external tracker. Ticket files are immutable execution authority. Each Ticket changes one distinct file, which keeps the fixed sequence deterministic and conflict-free.
EOF

cat > "$workspace/tracker/tickets/1.md" <<'EOF'
# fixture/daily-paper#1 — Add the alpha fixture deliverable

State: OPEN
Category label: enhancement
State label: ready-for-agent
Assignee: none
Dependencies: none
Conflicts: none

## Contract

Create `deliverables/alpha.txt` containing exactly one line:

```text
alpha delivered
```

Do not change any other tracked file. Run `./verify.sh ticket-1`. Commit with `feat(fixture): deliver alpha`.

## Agent Brief

Current behavior: the alpha deliverable is absent.
Desired behavior: the exact deterministic alpha file exists in a local commit.
Out of scope: all external effects, tracker mutation, and other files.

## Prompt Audit

Status: PASS
Contract: this complete current file
Basis: the exact path, bytes, verification, commit, and no-effect boundary are unambiguous and fit one fresh context.
EOF

cat > "$workspace/tracker/tickets/2.md" <<'EOF'
# fixture/daily-paper#2 — Add the beta fixture deliverable

State: OPEN
Category label: enhancement
State label: ready-for-agent
Assignee: none
Dependencies: fixture/daily-paper#1 delivered locally
Conflicts: none

## Contract

Require the committed `deliverables/alpha.txt` from Ticket 1, then create `deliverables/beta.txt` containing exactly one line:

```text
beta delivered
```

Do not change any other tracked file. Run `./verify.sh ticket-2` and `./verify.sh all`. Commit with `feat(fixture): deliver beta`.

## Agent Brief

Current behavior: alpha is delivered and beta is absent.
Desired behavior: both exact deterministic files exist in ordered local commits.
Out of scope: all external effects, tracker mutation, and other files.

## Prompt Audit

Status: PASS
Contract: this complete current file
Basis: the exact dependency, path, bytes, verification, commit, and no-effect boundary are unambiguous and fit one fresh context.
EOF

cat > "$workspace/verify.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

check_alpha() {
  test -f deliverables/alpha.txt
  test "$(wc -l < deliverables/alpha.txt | tr -d ' ')" = 1
  test "$(cat deliverables/alpha.txt)" = "alpha delivered"
}

check_beta() {
  test -f deliverables/beta.txt
  test "$(wc -l < deliverables/beta.txt | tr -d ' ')" = 1
  test "$(cat deliverables/beta.txt)" = "beta delivered"
}

case "${1:-}" in
  ticket-1) check_alpha ;;
  ticket-2) check_alpha; check_beta ;;
  all) check_alpha; check_beta ;;
  *) printf 'usage: %s ticket-1|ticket-2|all\n' "$0" >&2; exit 64 ;;
esac

printf 'fixture verification ok: %s\n' "$1"
EOF
chmod 0755 "$workspace/verify.sh"

cat > "$fixture_automation/runners/run-pi-ephemeral-fixture.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
: "${PROJECTS_DIR:?Set PROJECTS_DIR}"
: "${AUTOMATION_ROOT:?Set AUTOMATION_ROOT}"
: "${SANNUX_ROOT:?Set SANNUX_ROOT}"
: "${SITE_ROOT:?Set SITE_ROOT}"
: "${SANNUX_EPHEMERAL:?Set SANNUX_EPHEMERAL}"
: "${TTS_READY_DIR:?Set TTS_READY_DIR}"
: "${NODE_MODULES_DIR:?Set NODE_MODULES_DIR}"
BASE_COMPOSE="${SANNUX_ROOT}/templates/pi/compose.yml"
OVERRIDE_COMPOSE="${AUTOMATION_ROOT}/runners/pi.daily-paper.override.yml"
for directory in "$AUTOMATION_ROOT" "$SANNUX_ROOT/templates/pi" "$SITE_ROOT" "$TTS_READY_DIR" "$NODE_MODULES_DIR"; do
  [[ -d "$directory" ]] || { printf 'Required directory not found: %s\n' "$directory" >&2; exit 66; }
done
for file in "$BASE_COMPOSE" "$OVERRIDE_COMPOSE" "$SANNUX_EPHEMERAL"; do
  [[ -f "$file" ]] || { printf 'Required file not found: %s\n' "$file" >&2; exit 66; }
done
[[ -x "$SANNUX_EPHEMERAL" ]] || exit 69
export DAILY_PAPER_ROOT="$AUTOMATION_ROOT"
export DAILY_PAPER_TTS_READY_DIR="$TTS_READY_DIR"
export DAILY_PAPER_NODE_MODULES="$NODE_MODULES_DIR"
export DAILY_PAPER_HOST_BLOG_ROOT="$SITE_ROOT"
export CURDIR="$SITE_ROOT"
export COMPOSE_FILE="${BASE_COMPOSE}:${OVERRIDE_COMPOSE}"
if [[ "${1:-}" == "--compose-config" ]]; then
  cd "${SANNUX_ROOT}/templates/pi"
  exec docker compose config
fi
exec "$SANNUX_EPHEMERAL" pi "$@"
EOF
chmod 0755 "$fixture_automation/runners/run-pi-ephemeral-fixture.sh"

cat > "$fixture_automation/runners/pi.daily-paper.override.yml" <<'EOF'
services:
  agent:
    volumes:
      - {type: bind, source: "${DAILY_PAPER_ROOT:?Set DAILY_PAPER_ROOT}/agents", target: /opt/daily-paper/agents, read_only: true, bind: {create_host_path: false}}
      - {type: bind, source: "${DAILY_PAPER_ROOT:?Set DAILY_PAPER_ROOT}/runners", target: /opt/daily-paper/runners, read_only: true, bind: {create_host_path: false}}
      - {type: bind, source: "${DAILY_PAPER_ROOT:?Set DAILY_PAPER_ROOT}/skills", target: /opt/daily-paper/skills, read_only: true, bind: {create_host_path: false}}
      - {type: bind, source: "${DAILY_PAPER_ROOT:?Set DAILY_PAPER_ROOT}/assets", target: /opt/daily-paper/assets, read_only: true, bind: {create_host_path: false}}
      - {type: bind, source: "${DAILY_PAPER_ROOT:?Set DAILY_PAPER_ROOT}/hooks/on-end/tts/enqueue-tts-ready.sh", target: /opt/daily-paper/bin/enqueue-tts-ready.sh, read_only: true, bind: {create_host_path: false}}
      - {type: bind, source: "${DAILY_PAPER_TTS_READY_DIR:?Set DAILY_PAPER_TTS_READY_DIR}", target: /handoff/tts-ready, bind: {create_host_path: false}}
      - {type: bind, source: "${DAILY_PAPER_NODE_MODULES:?Set DAILY_PAPER_NODE_MODULES}", target: /workspace/node_modules, bind: {create_host_path: false}}
    environment:
      AUTOMATION_ROOT: /opt/daily-paper
      BLOG_ROOT: /workspace
      OMNEWS_BASE_URL: http://127.0.0.1:9
      OMNEWS_DATA_DIR: ""
      HUMANIZER_SKILL: /opt/daily-paper/skills/humanizer/SKILL.md
      CMUDICT: /opt/daily-paper/assets/cmudict.0.7a
      TTS_DISPATCH: /opt/daily-paper/bin/enqueue-tts-ready.sh
      QUEUE_DIR: /handoff/tts-ready
      NODE_BIN: /usr/bin/node
      MARKER_PATH_REWRITE_FROM: /workspace
      MARKER_PATH_REWRITE_TO: "${DAILY_PAPER_HOST_BLOG_ROOT:?Set DAILY_PAPER_HOST_BLOG_ROOT}"
      PI_CODING_AGENT_SESSION_DIR: /workspace/.evidence-sessions
EOF

ln -s "$AUTOMATION_ROOT/agents" "$fixture_automation/agents"
ln -s "$AUTOMATION_ROOT/skills" "$fixture_automation/skills"
ln -s "$AUTOMATION_ROOT/assets" "$fixture_automation/assets"
ln -s "$AUTOMATION_ROOT/hooks/on-end/tts/enqueue-tts-ready.sh" \
  "$fixture_automation/hooks/on-end/tts/enqueue-tts-ready.sh"

printf 'Prepared disposable fixture: %s\n' "$fixture"
