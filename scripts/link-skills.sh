#!/usr/bin/env bash
set -euo pipefail

# Links active skills in the repository to ~/.codex/skills, so they
# can be used by local Codex sessions.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${OMSKILLS_DEST:-$HOME/.codex/skills}"

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

mkdir -p "$DEST"

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required to read .codex-plugin/plugin.json" >&2
  exit 1
fi

jq -r '.skills[]' "$REPO/.codex-plugin/plugin.json" |
while IFS= read -r skill_path; do
  src="$REPO/${skill_path#./}"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "error: missing skill file: $src/SKILL.md" >&2
    exit 1
  fi

  name="$(basename "$src")"
  target="$DEST/$name"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    rm -rf "$target"
  fi

  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
done
