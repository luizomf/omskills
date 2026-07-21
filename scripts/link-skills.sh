#!/usr/bin/env bash
set -euo pipefail

# Links active skills in the repository to ~/.agents/skills, so they
# can be used by local Codex sessions.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
if [ -n "${OMSKILLS_DEST+x}" ]; then
  DEST="$OMSKILLS_DEST"
  USE_DEFAULT_DEST=false
else
  DEST="$HOME/.agents/skills"
  USE_DEFAULT_DEST=true
fi
STATE="$DEST/.omskills-managed-links"
MODE="install"

if [ "${1:-}" = "--check" ]; then
  MODE="check"
elif [ "$#" -ne 0 ]; then
  echo "usage: $0 [--check]" >&2
  exit 2
fi

# If the destination is a symlink that resolves into this repo, we'd end up
# writing the per-skill symlinks back into the repo's own skills/ tree. Detect
# and bail out instead of polluting the working copy.
if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
      exit 1
      ;;
  esac
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required to read .codex-plugin/plugin.json" >&2
  exit 1
fi

if [ "$MODE" = "install" ]; then
  mkdir -p "$DEST"
elif [ ! -d "$DEST" ]; then
  echo "error: skills destination does not exist: $DEST" >&2
  exit 1
fi

# One-time migration from the state-less installer used before the July 2026
# catalog rename. Remove only the exact obsolete links that installer created.
if [ "$MODE" = "install" ] && [ ! -f "$STATE" ]; then
  while IFS='|' read -r name relative; do
    target="$DEST/$name"
    expected="$REPO/skills/$relative"
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$expected" ]; then
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
  echo "$name" >> "$manifest_names"

  if [ -L "$target" ]; then
    existing="$(readlink "$target")"
    case "$existing" in
      "$REPO/skills"/*) ;;
      *)
        echo "error: refusing to replace external symlink: $target -> $existing" >&2
        exit 1
        ;;
    esac
  elif [ -e "$target" ]; then
    echo "error: refusing to replace non-symlink path: $target" >&2
    exit 1
  fi

  if [ "$MODE" = "check" ]; then
    if [ ! -L "$target" ] || [ "$(readlink "$target")" != "$src" ]; then
      echo "error: missing or incorrect link: $target -> $src" >&2
      exit 1
    fi
    echo "ok $name -> $src"
  else
    ln -sfn "$src" "$target"
    echo "linked $name -> $src"
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
      case "$existing" in
        "$REPO/skills"/*) ;;
        *)
          echo "error: stale managed link now points outside this repo: $target -> $existing" >&2
          exit 1
          ;;
      esac
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
        case "$existing" in
          "$REPO/skills"/*)
            rm "$target"
            echo "removed legacy Codex link $name -> $existing"
            ;;
          *)
            echo "warning: preserving changed legacy link: $target -> $existing" >&2
            legacy_state_safe=false
            ;;
        esac
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
