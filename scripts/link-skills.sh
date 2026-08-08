#!/usr/bin/env bash
set -euo pipefail

# Links active skills into a user-level skill directory for local agent sessions.

MODE="install"
if [ "$#" -eq 0 ]; then
  :
elif [ "$#" -eq 1 ] && [ "$1" = "--check" ]; then
  MODE="check"
else
  echo "usage: $0 [--check]" >&2
  exit 2
fi

REPO="$(cd "$(dirname "$0")/.." && pwd -P)"
if [ -n "${OMSKILLS_DEST+x}" ]; then
  DEST="$OMSKILLS_DEST"
  USE_DEFAULT_DEST=false
else
  DEST="$HOME/.agents/skills"
  USE_DEFAULT_DEST=true
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required to read .codex-plugin/plugin.json" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required to create portable relative links" >&2
  exit 1
fi

physical_path() {
  python3 - "$1" <<'PY'
import os
import sys

resolved = os.path.realpath(sys.argv[1])
if "\n" in resolved or "\r" in resolved:
    print("error: physical path must not contain line breaks", file=sys.stderr)
    raise SystemExit(1)
print(resolved)
PY
}

path_relation() {
  python3 - "$1" "$2" "$3" <<'PY'
import os
import sys

candidate = os.path.realpath(sys.argv[1])
root = os.path.realpath(sys.argv[2])
strict = sys.argv[3] == "strict"

try:
    root_stat = os.stat(root)
except OSError:
    raise SystemExit(1)

probe = candidate
missing_suffix = False
while True:
    try:
        probe_stat = os.stat(probe)
        break
    except (FileNotFoundError, NotADirectoryError):
        parent = os.path.dirname(probe)
        if parent == probe:
            raise SystemExit(1)
        probe = parent
        missing_suffix = True
    except OSError:
        raise SystemExit(1)

current = probe
current_stat = probe_stat
while True:
    if os.path.samestat(current_stat, root_stat):
        if strict and not missing_suffix:
            try:
                if os.path.samestat(os.stat(candidate), root_stat):
                    raise SystemExit(1)
            except OSError:
                pass
        raise SystemExit(0)

    parent = os.path.dirname(current)
    if parent == current:
        raise SystemExit(1)
    current = parent
    try:
        current_stat = os.stat(current)
    except OSError:
        raise SystemExit(1)
PY
}

path_is_within() {
  path_relation "$1" "$2" within
}

path_is_descendant() {
  path_relation "$1" "$2" strict
}

is_safe_name() {
  local LC_ALL=C
  [[ "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]
}

validate_managed_state() {
  local state="$1"
  local validated_names="$2"
  local description="$3"

  : > "$validated_names"
  if [ -L "$state" ]; then
    echo "error: $description managed state must not be a symlink: $state" >&2
    return 1
  fi
  if [ ! -e "$state" ]; then
    return 0
  fi
  if [ ! -f "$state" ]; then
    echo "error: $description managed state is not a regular file: $state" >&2
    return 1
  fi

  if ! python3 - "$state" "$validated_names" <<'PY'
import re
import sys
from pathlib import Path

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
data = source.read_bytes()
if not data:
    names = []
elif data.endswith(b"\n"):
    names = data[:-1].split(b"\n")
else:
    names = data.split(b"\n")

pattern = re.compile(rb"[a-z0-9]+(?:-[a-z0-9]+)*")
if any(pattern.fullmatch(name) is None for name in names):
    raise SystemExit(1)
if len(names) != len(set(names)):
    raise SystemExit(1)

destination.write_bytes(b"".join(name + b"\n" for name in names))
PY
  then
    echo "error: invalid $description managed-state entry" >&2
    return 1
  fi
}

if [ -z "$DEST" ]; then
  echo "error: skills destination must not be empty" >&2
  exit 1
fi
case "$DEST" in
  *$'\n'*|*$'\r'*)
    echo "error: skills destination must not contain line breaks" >&2
    exit 1
    ;;
esac

requested_dest="$DEST"
DEST="$(physical_path "$DEST")"
if path_is_within "$DEST" "$REPO"; then
  echo "error: skills destination resolves into this repo: $requested_dest -> $DEST" >&2
  exit 1
fi

WORK_DIR=""
STATE_TEMP=""
create_work_dir() {
  local candidate parent

  for candidate in "${TMPDIR:-}" /tmp /var/tmp "$(dirname "$REPO")" "${HOME:-}"; do
    [ -n "$candidate" ] || continue
    case "$candidate" in
      *$'\n'*|*$'\r'*) continue ;;
    esac
    [ -d "$candidate" ] || continue
    parent="$(physical_path "$candidate")"

    # The scratch parent must be disjoint from both the requested destination
    # and the repository. This keeps check mode destination-local mutation free
    # even when GNU mktemp honors an adversarial TMPDIR.
    if path_is_within "$parent" "$DEST" || path_is_within "$DEST" "$parent" ||
      path_is_within "$parent" "$REPO" || path_is_within "$REPO" "$parent"; then
      continue
    fi

    if WORK_DIR="$(umask 077 && mktemp -d "$parent/omskills.XXXXXX" 2>/dev/null)"; then
      return 0
    fi
  done
  return 1
}

if ! create_work_dir; then
  echo "error: no secure temporary workspace is available outside the destination" >&2
  exit 1
fi

cleanup() {
  if [ -n "$STATE_TEMP" ]; then
    rm -f "$STATE_TEMP"
  fi
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT

manifest_entries="$WORK_DIR/manifest-entries"
manifest_records="$WORK_DIR/manifest-records"
manifest_names="$WORK_DIR/manifest-names"
: > "$manifest_records"
: > "$manifest_names"

if ! jq -ce '.skills | if type == "array" then .[] else error("skills must be an array") end' \
  "$REPO/.codex-plugin/plugin.json" > "$manifest_entries"; then
  echo "error: invalid skills manifest" >&2
  exit 1
fi

REPO_SKILLS="$(physical_path "$REPO/skills")"
if [ ! -d "$REPO_SKILLS" ] || ! path_is_descendant "$REPO_SKILLS" "$REPO"; then
  echo "error: repository skills root is not a directory inside this repo" >&2
  exit 1
fi

while IFS= read -r encoded_entry; do
  if ! skill_path="$(printf '%s\n' "$encoded_entry" | jq -er '
    if type == "string"
      and (contains("\n") | not)
      and test("^\\./skills/(engineering|productivity|misc)/[a-z0-9]+(-[a-z0-9]+)*$")
    then .
    else error("invalid canonical skill path")
    end
  ')"; then
    echo "error: invalid manifest skill path" >&2
    exit 1
  fi

  if [[ ! "$skill_path" =~ ^\./skills/(engineering|productivity|misc)/([a-z0-9]+(-[a-z0-9]+)*)$ ]]; then
    echo "error: invalid manifest skill path: $skill_path" >&2
    exit 1
  fi

  bucket="${BASH_REMATCH[1]}"
  name="${BASH_REMATCH[2]}"
  bucket_path="$REPO/skills/$bucket"
  src="$bucket_path/$name"
  skill_file="$src/SKILL.md"

  if [ ! -d "$bucket_path" ]; then
    echo "error: missing skill bucket: $bucket_path" >&2
    exit 1
  fi
  bucket_root="$(physical_path "$bucket_path")"
  if ! path_is_descendant "$bucket_root" "$REPO_SKILLS"; then
    echo "error: skill bucket escapes the repository skills root: $bucket_path" >&2
    exit 1
  fi

  if [ ! -d "$src" ]; then
    echo "error: missing skill directory: $src" >&2
    exit 1
  fi
  src_root="$(physical_path "$src")"
  if ! path_is_descendant "$src_root" "$bucket_root"; then
    echo "error: skill directory escapes its approved bucket: $src" >&2
    exit 1
  fi

  if [ ! -f "$skill_file" ]; then
    echo "error: missing skill file: $skill_file" >&2
    exit 1
  fi
  skill_file_root="$(physical_path "$skill_file")"
  if ! path_is_descendant "$skill_file_root" "$src_root"; then
    echo "error: skill file escapes its skill directory: $skill_file" >&2
    exit 1
  fi

  if grep -Fqx "$name" "$manifest_names"; then
    echo "error: duplicate installed skill name: $name" >&2
    exit 1
  fi
  printf '%s/%s\n' "$bucket" "$name" >> "$manifest_records"
  printf '%s\n' "$name" >> "$manifest_names"
done < "$manifest_entries"

relative_link_target() {
  python3 - "$1" "$2" <<'PY'
import os
import sys

print(os.path.relpath(sys.argv[1], start=sys.argv[2]))
PY
}

link_points_into_repo_skills() {
  python3 - "$1" "$REPO_SKILLS" <<'PY'
import os
import sys

link = sys.argv[1]
root = os.path.realpath(sys.argv[2])
target = os.path.realpath(os.path.join(os.path.dirname(link), os.readlink(link)))

try:
    root_stat = os.stat(root)
except OSError:
    raise SystemExit(1)

probe = target
missing_suffix = False
while True:
    try:
        probe_stat = os.stat(probe)
        break
    except (FileNotFoundError, NotADirectoryError):
        parent = os.path.dirname(probe)
        if parent == probe:
            raise SystemExit(1)
        probe = parent
        missing_suffix = True
    except OSError:
        raise SystemExit(1)

current = probe
current_stat = probe_stat
while True:
    if os.path.samestat(current_stat, root_stat):
        if not missing_suffix:
            try:
                if os.path.samestat(os.stat(target), root_stat):
                    raise SystemExit(1)
            except OSError:
                pass
        raise SystemExit(0)
    parent = os.path.dirname(current)
    if parent == current:
        raise SystemExit(1)
    current = parent
    try:
        current_stat = os.stat(current)
    except OSError:
        raise SystemExit(1)
PY
}

link_points_to() {
  python3 - "$1" "$2" <<'PY'
import os
import sys

link = sys.argv[1]
expected = os.path.realpath(sys.argv[2])
target = os.path.realpath(os.path.join(os.path.dirname(link), os.readlink(link)))
try:
    matches = os.path.samefile(target, expected)
except OSError:
    matches = target == expected
raise SystemExit(0 if matches else 1)
PY
}

# Create only the already-resolved destination. Using the raw request here
# would let mkdir create cancelled intermediate components inside the repo.
if [ "$MODE" = "install" ]; then
  mkdir -p -- "$DEST"
elif [ ! -d "$DEST" ]; then
  echo "error: skills destination does not exist: $DEST" >&2
  exit 1
fi

# Relative symlinks must be calculated from the destination's physical path.
# This matters on macOS, where /var resolves to /private/var. Repeat the
# containment check after opening the destination and use only this root.
DEST="$(cd "$DEST" && pwd -P)"
if path_is_within "$DEST" "$REPO"; then
  echo "error: physical skills destination is inside this repo: $DEST" >&2
  exit 1
fi
STATE="$DEST/.omskills-managed-links"
CURRENT_STATE_EXISTS=false
if [ -e "$STATE" ] || [ -L "$STATE" ]; then
  CURRENT_STATE_EXISTS=true
fi
current_state_names="$WORK_DIR/current-state-names"
validate_managed_state "$STATE" "$current_state_names" "current"

LEGACY_DEST=""
LEGACY_STATE=""
LEGACY_STATE_EXISTS=false
legacy_state_names="$WORK_DIR/legacy-state-names"
: > "$legacy_state_names"
if [ "$MODE" = "install" ] && [ "$USE_DEFAULT_DEST" = true ]; then
  legacy_requested="$HOME/.codex/skills"
  case "$legacy_requested" in
    *$'\n'*|*$'\r'*)
      echo "error: legacy skills destination must not contain line breaks" >&2
      exit 1
      ;;
  esac
  if [ -e "$legacy_requested" ] || [ -L "$legacy_requested" ]; then
    if [ ! -d "$legacy_requested" ]; then
      echo "error: legacy skills destination is not a directory: $legacy_requested" >&2
      exit 1
    fi
    LEGACY_DEST="$(cd "$legacy_requested" && pwd -P)"
    if path_is_within "$LEGACY_DEST" "$REPO"; then
      echo "error: legacy skills destination resolves into this repo: $LEGACY_DEST" >&2
      exit 1
    fi
    if [ "$LEGACY_DEST" = "$DEST" ]; then
      echo "error: current and legacy skills destinations resolve to the same root" >&2
      exit 1
    fi

    LEGACY_STATE="$LEGACY_DEST/.omskills-managed-links"
    if [ -e "$LEGACY_STATE" ] || [ -L "$LEGACY_STATE" ]; then
      LEGACY_STATE_EXISTS=true
    fi
    validate_managed_state "$LEGACY_STATE" "$legacy_state_names" "legacy"
  fi
fi

# Preflight every manifest-derived and state-derived target before changing
# any link. All names in these files were validated before reaching this point.
while IFS= read -r relative; do
  name="${relative#*/}"
  target="$DEST/$name"

  if [ -L "$target" ]; then
    existing="$(readlink "$target")"
    if ! link_points_into_repo_skills "$target"; then
      echo "error: refusing to replace external symlink: $target -> $existing" >&2
      exit 1
    fi
  elif [ -e "$target" ]; then
    echo "error: refusing to replace non-symlink path: $target" >&2
    exit 1
  fi
done < "$manifest_records"

if [ "$CURRENT_STATE_EXISTS" = true ]; then
  while IFS= read -r name; do
    if ! grep -Fqx "$name" "$manifest_names"; then
      target="$DEST/$name"
      if [ ! -L "$target" ]; then
        echo "error: stale managed path is no longer a symlink: $target" >&2
        exit 1
      fi
      existing="$(readlink "$target")"
      if ! link_points_into_repo_skills "$target"; then
        echo "error: stale managed link now points outside this repo: $target -> $existing" >&2
        exit 1
      fi
    fi
  done < "$current_state_names"
fi

if [ "$MODE" = "install" ]; then
  STATE_TEMP="$(umask 077 && mktemp "$DEST/.omskills-managed-links.tmp.XXXXXX")"
  if [ -L "$STATE_TEMP" ] || [ ! -f "$STATE_TEMP" ]; then
    echo "error: could not create regular temporary managed state in $DEST" >&2
    exit 1
  fi
  chmod 600 "$STATE_TEMP"
  cat "$manifest_names" > "$STATE_TEMP"
fi

# One-time migration from the state-less installer used before the July 2026
# catalog rename. Remove only the exact obsolete links that installer created.
if [ "$MODE" = "install" ] && [ "$CURRENT_STATE_EXISTS" = false ]; then
  while IFS='|' read -r name relative; do
    if ! is_safe_name "$name" ||
      [[ ! "$relative" =~ ^(engineering|productivity|misc)/[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
      echo "error: invalid built-in migration path: $name -> $relative" >&2
      exit 1
    fi
    target="$DEST/$name"
    expected="$(physical_path "$REPO/skills/$relative")"
    if ! path_is_descendant "$expected" "$REPO_SKILLS"; then
      echo "error: built-in migration target escapes repository skills: $relative" >&2
      exit 1
    fi
    if [ -L "$target" ] && link_points_to "$target" "$expected"; then
      rm "$target"
      echo "removed legacy link $name -> $expected"
    fi
  done <<'LEGACY_LINKS'
daily-paper-social-post|productivity/daily-paper-social-post
deep-coder|engineering/deep-coder
diagnose|engineering/diagnose
to-issues|engineering/to-issues
to-prd|engineering/to-prd
zoom-out|engineering/zoom-out
LEGACY_LINKS
fi

while IFS= read -r relative; do
  src="$REPO/skills/$relative"
  name="${relative#*/}"
  target="$DEST/$name"
  relative_src="$(relative_link_target "$src" "$DEST")"

  if [ -L "$target" ]; then
    existing="$(readlink "$target")"
    if ! link_points_into_repo_skills "$target"; then
      echo "error: refusing to replace external symlink: $target -> $existing" >&2
      exit 1
    fi
  elif [ -e "$target" ]; then
    echo "error: refusing to replace non-symlink path: $target" >&2
    exit 1
  fi

  if [ "$MODE" = "check" ]; then
    if [ ! -L "$target" ] || [ "$(readlink "$target")" != "$relative_src" ]; then
      echo "error: missing or incorrect link: $target -> $relative_src" >&2
      exit 1
    fi
    echo "ok $name -> $relative_src"
  else
    ln -sfn "$relative_src" "$target"
    echo "linked $name -> $relative_src"
  fi
done < "$manifest_records"

# Remove only stale links recorded by a previous installer run. A manually
# linked optional skill from this repository is not owned unless listed here.
if [ "$CURRENT_STATE_EXISTS" = true ]; then
  while IFS= read -r name; do
    target="$DEST/$name"
    if ! grep -Fqx "$name" "$manifest_names"; then
      if [ ! -L "$target" ]; then
        echo "error: stale managed path is no longer a symlink: $target" >&2
        exit 1
      fi
      existing="$(readlink "$target")"
      if ! link_points_into_repo_skills "$target"; then
        echo "error: stale managed link now points outside this repo: $target -> $existing" >&2
        exit 1
      fi
      if [ "$MODE" = "check" ]; then
        echo "error: stale managed link: $target -> $existing" >&2
        exit 1
      fi
      rm "$target"
      echo "removed stale link $name -> $existing"
    fi
  done < "$current_state_names"
fi

if [ "$MODE" = "check" ]; then
  if [ "$CURRENT_STATE_EXISTS" = false ] || ! cmp -s "$manifest_names" "$STATE"; then
    echo "error: managed-link state is missing or differs from the manifest" >&2
    exit 1
  fi
else
  mv -f "$STATE_TEMP" "$STATE"
  STATE_TEMP=""
fi

# Codex previously used ~/.codex/skills for user skills. After a successful
# default installation, remove only links recorded there that still point into
# this repository. Preserve unrelated content and any path whose ownership is
# no longer safe to infer.
if [ "$MODE" = "install" ] && [ "$LEGACY_STATE_EXISTS" = true ]; then
  legacy_state_safe=true

  while IFS= read -r name; do
    target="$LEGACY_DEST/$name"

    if [ -L "$target" ]; then
      existing="$(readlink "$target")"
      if link_points_into_repo_skills "$target"; then
        rm "$target"
        echo "removed legacy Codex link $name -> $existing"
      else
        echo "warning: preserving changed legacy link: $target -> $existing" >&2
        legacy_state_safe=false
      fi
    elif [ -e "$target" ]; then
      echo "warning: preserving changed legacy path: $target" >&2
      legacy_state_safe=false
    fi
  done < "$legacy_state_names"

  if [ "$legacy_state_safe" = true ]; then
    rm "$LEGACY_STATE"
    echo "removed legacy managed-link state $LEGACY_STATE"
  fi
fi
