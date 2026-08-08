#!/usr/bin/env bash
set -euo pipefail

# Links active skills into a user-level skill directory for local agent sessions.

REPO="$(cd "$(dirname "$0")/.." && pwd -P)"
if [ -n "${OMSKILLS_DEST+x}" ]; then
  DEST="$OMSKILLS_DEST"
  USE_DEFAULT_DEST=false
else
  DEST="$HOME/.agents/skills"
  USE_DEFAULT_DEST=true
fi
MODE="install"

if [ "${1:-}" = "--check" ]; then
  MODE="check"
elif [ "$#" -ne 0 ]; then
  echo "usage: $0 [--check]" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required to read .codex-plugin/plugin.json" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required to create portable relative links" >&2
  exit 1
fi

resolve_link_target() {
  python3 - "$1" <<'PY'
import os
import sys

link = sys.argv[1]
target = os.path.join(os.path.dirname(link), os.readlink(link))
print(os.path.realpath(target))
PY
}

relative_link_target() {
  python3 - "$1" "$2" <<'PY'
import os
import sys

print(os.path.relpath(sys.argv[1], start=sys.argv[2]))
PY
}

link_points_into_repo_skills() {
  local resolved
  resolved="$(resolve_link_target "$1")"
  case "$resolved" in
    "$REPO/skills"/*) return 0 ;;
    *) return 1 ;;
  esac
}

# If the destination is a symlink that resolves into this repo, we'd end up
# writing the per-skill symlinks back into the repo's own skills/ tree. Detect
# and bail out instead of polluting the working copy.
if [ -L "$DEST" ]; then
  resolved="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
      exit 1
      ;;
  esac
fi

if [ "$MODE" = "install" ]; then
  mkdir -p "$DEST"
elif [ ! -d "$DEST" ]; then
  echo "error: skills destination does not exist: $DEST" >&2
  exit 1
fi

# Relative symlinks must be calculated from the destination's physical path.
# This matters on macOS, where /var resolves to /private/var.
DEST="$(cd "$DEST" && pwd -P)"
STATE="$DEST/.omskills-managed-links"

# One-time migration from the state-less installer used before the July 2026
# catalog rename. Remove only the exact obsolete links that installer created.
if [ "$MODE" = "install" ] && [ ! -f "$STATE" ]; then
  while IFS='|' read -r name relative; do
    target="$DEST/$name"
    expected="$REPO/skills/$relative"
    if [ -L "$target" ] && [ "$(resolve_link_target "$target")" = "$expected" ]; then
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

manifest_names="$(mktemp)"
trap 'rm -f "$manifest_names"' EXIT

jq -r '.skills[]' "$REPO/.codex-plugin/plugin.json" |
while IFS= read -r skill_path; do
  src="$REPO/${skill_path#./}"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "error: missing skill file: $src/SKILL.md" >&2
    exit 1
  fi

  name="$(basename "$src")"
  target="$DEST/$name"
  relative_src="$(relative_link_target "$src" "$DEST")"
  echo "$name" >> "$manifest_names"

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
done

# Remove only stale links recorded by a previous installer run. A manually
# linked optional skill from this repository is not owned unless listed here.
if [ -f "$STATE" ]; then
  while IFS= read -r name; do
    [ -n "$name" ] || continue
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
  done < "$STATE"
fi

if [ "$MODE" = "check" ]; then
  if [ ! -f "$STATE" ] || ! cmp -s "$manifest_names" "$STATE"; then
    echo "error: managed-link state is missing or differs from the manifest" >&2
    exit 1
  fi
else
  cp "$manifest_names" "$STATE"
fi

# Codex previously used ~/.codex/skills for user skills. After a successful
# default installation, remove only links recorded there that still point into
# this repository. Preserve unrelated content and any path whose ownership is
# no longer safe to infer.
if [ "$MODE" = "install" ] && [ "$USE_DEFAULT_DEST" = true ]; then
  legacy_dest="$HOME/.codex/skills"
  legacy_state="$legacy_dest/.omskills-managed-links"
  legacy_state_safe=true

  if [ -f "$legacy_state" ]; then
    while IFS= read -r name; do
      [ -n "$name" ] || continue
      target="$legacy_dest/$name"

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
    done < "$legacy_state"

    if [ "$legacy_state_safe" = true ]; then
      rm "$legacy_state"
      echo "removed legacy managed-link state $legacy_state"
    fi
  fi
fi
