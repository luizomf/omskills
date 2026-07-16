#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$(mktemp -d)"
trap 'rm -rf "$DEST"' EXIT

export OMSKILLS_DEST="$DEST"

ln -s "$REPO/skills/engineering/to-prd" "$DEST/to-prd"
ln -s "$REPO/skills/productivity/caveman" "$DEST/manual-optional"
"$REPO/scripts/link-skills.sh" >/dev/null
"$REPO/scripts/link-skills.sh" --check >/dev/null
[ ! -L "$DEST/to-prd" ] || {
  echo "error: state-less legacy link was not migrated" >&2
  exit 1
}
[ -L "$DEST/manual-optional" ] || {
  echo "error: state-less manual optional link was removed" >&2
  exit 1
}

expected="$(jq '.skills | length' "$REPO/.codex-plugin/plugin.json")"
actual="$(find "$DEST" -type l | wc -l | tr -d ' ')"
expected_with_optional="$((expected + 1))"
[ "$actual" = "$expected_with_optional" ] || {
  echo "error: expected $expected managed links plus one optional link, found $actual" >&2
  exit 1
}

ln -s "$REPO/skills/retired-example" "$DEST/stale-managed"
echo "stale-managed" >> "$DEST/.omskills-managed-links"
"$REPO/scripts/link-skills.sh" >/dev/null
[ ! -L "$DEST/stale-managed" ] || {
  echo "error: stale managed link was not removed" >&2
  exit 1
}

external="$(mktemp -d)"
trap 'rm -rf "$DEST" "$external"' EXIT
ln -s "$external" "$DEST/external-link"
"$REPO/scripts/link-skills.sh" >/dev/null
[ "$(readlink "$DEST/external-link")" = "$external" ] || {
  echo "error: external symlink was modified" >&2
  exit 1
}

"$REPO/scripts/link-skills.sh" >/dev/null
[ -L "$DEST/manual-optional" ] || {
  echo "error: manual optional skill link was removed" >&2
  exit 1
}

rm "$DEST/to-spec"
mkdir "$DEST/to-spec"
if "$REPO/scripts/link-skills.sh" >/dev/null 2>&1; then
  echo "error: installer accepted a non-symlink collision" >&2
  exit 1
fi
[ -d "$DEST/to-spec" ] || {
  echo "error: installer removed a non-symlink collision" >&2
  exit 1
}

echo "linker tests ok"
