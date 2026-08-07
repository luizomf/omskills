#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd -P)"
TEST_ROOT="$(mktemp -d)"
FIXTURES="$TEST_ROOT/fixtures"
mkdir "$FIXTURES"
trap 'rm -rf "$TEST_ROOT"' EXIT

fail() {
  echo "error: $1" >&2
  exit 1
}

assert_no_state_temp() {
  local destination="$1"
  local residue

  residue="$(find "$destination" -maxdepth 1 -name '.omskills-managed-links.tmp.*' -print)"
  [ -z "$residue" ] || fail "temporary managed state was not cleaned: $residue"
}

make_fixture_repo() {
  local fixture

  fixture="$(mktemp -d "$FIXTURES/repo.XXXXXX")"
  mkdir -p "$fixture/scripts" "$fixture/.codex-plugin"
  cp "$REPO/scripts/link-skills.sh" "$fixture/scripts/link-skills.sh"
  chmod +x "$fixture/scripts/link-skills.sh"
  printf '%s\n' "$fixture"
}

add_fixture_skill() {
  local fixture="$1"
  local bucket="$2"
  local name="$3"

  mkdir -p "$fixture/skills/$bucket/$name"
  printf '%s\n' 'fixture skill' > "$fixture/skills/$bucket/$name/SKILL.md"
}

set_fixture_manifest() {
  local fixture="$1"
  shift

  jq -n --args '$ARGS.positional | {skills: .}' "$@" > "$fixture/.codex-plugin/plugin.json"
}

make_valid_fixture_repo() {
  local fixture

  fixture="$(make_fixture_repo)"
  add_fixture_skill "$fixture" engineering safe-skill
  set_fixture_manifest "$fixture" './skills/engineering/safe-skill'
  printf '%s\n' "$fixture"
}

assert_fixture_install_rejected_without_destination() {
  local label="$1"
  local fixture="$2"
  local destination="$FIXTURES/$label-destination"

  if OMSKILLS_DEST="$destination" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
    fail "installer accepted $label"
  fi
  [ ! -e "$destination" ] || fail "$label created or mutated its destination"
}

assert_invalid_arguments() {
  local label="$1"
  shift
  local destination="$FIXTURES/arguments-$label"
  local status

  set +e
  OMSKILLS_DEST="$destination" "$REPO/scripts/link-skills.sh" "$@" >/dev/null 2>&1
  status=$?
  set -e
  [ "$status" -eq 2 ] || fail "$label arguments did not exit with status 2"
  [ ! -e "$destination" ] || fail "$label arguments mutated the destination"
}

# The complete CLI grammar is checked before dependencies or filesystem work.
assert_invalid_arguments unknown-option --unknown
assert_invalid_arguments check-extra --check extra
assert_invalid_arguments duplicate-check --check --check
assert_invalid_arguments positional extra --check

# Manifest entries must retain exactly one canonical ./ prefix and three safe
# components. Each case must fail before destination creation.
manifest_entries=(
  'skills/engineering/safe-skill'
  $'./skills/engineering/safe-skill\nother-skill'
  $'./skills/engineering/safe-skill\n'
  '/tmp/absolute-skill'
  './skills/engineering/safe-skill/extra'
  './skills/engineering/../outside'
  './skills/unknown/safe-skill'
  './skills/engineering/'
  './skills/engineering/.hidden'
  './skills/engineering/-reserved'
  './skills/engineering/bad_name'
  './../skills/engineering/safe-skill'
)
for index in "${!manifest_entries[@]}"; do
  fixture="$(make_valid_fixture_repo)"
  set_fixture_manifest "$fixture" "${manifest_entries[$index]}"
  assert_fixture_install_rejected_without_destination "invalid-manifest-$index" "$fixture"
done

fixture="$(make_valid_fixture_repo)"
printf '%s\n' '{"skills":[null]}' > "$fixture/.codex-plugin/plugin.json"
assert_fixture_install_rejected_without_destination manifest-non-string "$fixture"
fixture="$(make_valid_fixture_repo)"
printf '%s\n' '{"skills":["./skills/engineering/safe\u0000-skill"]}' > "$fixture/.codex-plugin/plugin.json"
assert_fixture_install_rejected_without_destination manifest-null-byte "$fixture"
fixture="$(make_valid_fixture_repo)"
printf '%s\n' '{"skills":"./skills/engineering/safe-skill"}' > "$fixture/.codex-plugin/plugin.json"
assert_fixture_install_rejected_without_destination manifest-non-array "$fixture"

# Physical resolution must keep the bucket, source directory, and SKILL.md
# inside their declared repository roots.
fixture="$(make_fixture_repo)"
escaped_bucket="$FIXTURES/escaped-bucket"
mkdir -p "$fixture/skills" "$escaped_bucket/safe-skill"
printf '%s\n' 'escaped skill' > "$escaped_bucket/safe-skill/SKILL.md"
ln -s "$escaped_bucket" "$fixture/skills/engineering"
set_fixture_manifest "$fixture" './skills/engineering/safe-skill'
assert_fixture_install_rejected_without_destination escaped-bucket "$fixture"

fixture="$(make_fixture_repo)"
escaped_source="$FIXTURES/escaped-source"
mkdir -p "$fixture/skills/engineering" "$escaped_source"
printf '%s\n' 'escaped skill' > "$escaped_source/SKILL.md"
ln -s "$escaped_source" "$fixture/skills/engineering/safe-skill"
set_fixture_manifest "$fixture" './skills/engineering/safe-skill'
assert_fixture_install_rejected_without_destination escaped-source "$fixture"

fixture="$(make_fixture_repo)"
escaped_file="$FIXTURES/escaped-SKILL.md"
mkdir -p "$fixture/skills/engineering/safe-skill"
printf '%s\n' 'escaped skill' > "$escaped_file"
ln -s "$escaped_file" "$fixture/skills/engineering/safe-skill/SKILL.md"
set_fixture_manifest "$fixture" './skills/engineering/safe-skill'
assert_fixture_install_rejected_without_destination escaped-skill-file "$fixture"

# Both a not-yet-created destination below a symlinked ancestor and an existing
# symlinked destination are rejected when they resolve into the fixture repo.
fixture="$(make_valid_fixture_repo)"
ln -s "$fixture" "$FIXTURES/repo-parent"
parent_destination="$FIXTURES/repo-parent/generated-destination"
if OMSKILLS_DEST="$parent_destination" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "installer accepted a destination whose ancestor resolves into its repo"
fi
[ ! -e "$fixture/generated-destination" ] || fail "ancestor symlink mutated the fixture repo"

mkdir "$fixture/existing-destination"
ln -s "$fixture/existing-destination" "$FIXTURES/existing-repo-destination"
if OMSKILLS_DEST="$FIXTURES/existing-repo-destination" \
  "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "installer accepted an existing destination that resolves into its repo"
fi
[ ! -e "$fixture/existing-destination/safe-skill" ] || fail "existing destination mutated the fixture repo"

# Every current managed-state entry is validated before an entry derives a
# path or any active link is changed.
state_payloads=(
  $'../outside\n'
  $'/absolute\n'
  $'nested/name\n'
  $'Bad_Name\n'
  $'\n'
  $'safe-skill\n\n'
)
for index in "${!state_payloads[@]}"; do
  fixture="$(make_valid_fixture_repo)"
  destination="$FIXTURES/invalid-state-$index"
  mkdir "$destination"
  printf '%s' "${state_payloads[$index]}" > "$destination/.omskills-managed-links"
  if OMSKILLS_DEST="$destination" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
    fail "installer accepted invalid current managed state $index"
  fi
  [ ! -e "$destination/safe-skill" ] || fail "invalid current state caused a partial link mutation"
  assert_no_state_temp "$destination"
done

# Current state must be a regular, non-symlink file, including dangling links.
fixture="$(make_valid_fixture_repo)"
state_target="$FIXTURES/current-state-target"
printf '%s\n' safe-skill > "$state_target"
for kind in symlink dangling directory; do
  destination="$FIXTURES/current-state-$kind"
  mkdir "$destination"
  case "$kind" in
    symlink) ln -s "$state_target" "$destination/.omskills-managed-links" ;;
    dangling) ln -s "$FIXTURES/missing-current-state" "$destination/.omskills-managed-links" ;;
    directory) mkdir "$destination/.omskills-managed-links" ;;
  esac
  if OMSKILLS_DEST="$destination" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
    fail "installer accepted $kind current managed state"
  fi
  [ ! -e "$destination/safe-skill" ] || fail "$kind current state caused a link mutation"
  assert_no_state_temp "$destination"
done

# The legacy Codex root and all legacy state are independently confined and
# validated before active or legacy link mutation.
fixture="$(make_valid_fixture_repo)"
legacy_repo_root="$fixture/legacy-destination"
legacy_root_home="$FIXTURES/legacy-root-home"
mkdir -p "$legacy_repo_root" "$legacy_root_home/.codex"
printf '%s\n' safe-skill > "$legacy_repo_root/.omskills-managed-links"
ln -s "$fixture/skills/engineering/safe-skill" "$legacy_repo_root/safe-skill"
ln -s "$legacy_repo_root" "$legacy_root_home/.codex/skills"
if HOME="$legacy_root_home" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "installer accepted a legacy destination inside its repo"
fi
[ ! -e "$legacy_root_home/.agents/skills/safe-skill" ] || fail "unsafe legacy root caused an active mutation"
[ -L "$legacy_repo_root/safe-skill" ] || fail "unsafe legacy root caused a legacy mutation"

for kind in symlink dangling directory invalid-entry; do
  fixture="$(make_valid_fixture_repo)"
  home="$FIXTURES/legacy-state-$kind-home"
  destination="$home/.codex/skills"
  mkdir -p "$destination"
  case "$kind" in
    symlink)
      printf '%s\n' safe-skill > "$home/state-target"
      ln -s "$home/state-target" "$destination/.omskills-managed-links"
      ;;
    dangling)
      ln -s "$home/missing-state" "$destination/.omskills-managed-links"
      ;;
    directory)
      mkdir "$destination/.omskills-managed-links"
      ;;
    invalid-entry)
      printf '%s\n' '../outside' > "$destination/.omskills-managed-links"
      ;;
  esac
  ln -s "$fixture/skills/engineering/safe-skill" "$destination/safe-skill"
  if HOME="$home" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
    fail "installer accepted $kind legacy managed state"
  fi
  [ ! -e "$home/.agents/skills/safe-skill" ] || fail "$kind legacy state caused an active mutation"
  [ -L "$destination/safe-skill" ] || fail "$kind legacy state caused a legacy mutation"
done

# An external active-name link is rejected and remains untouched.
fixture="$(make_valid_fixture_repo)"
active_destination="$FIXTURES/active-external-destination"
active_external="$FIXTURES/active-external-target"
mkdir "$active_destination" "$active_external"
ln -s "$active_external" "$active_destination/safe-skill"
if OMSKILLS_DEST="$active_destination" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "installer accepted an external symlink at an active name"
fi
[ "$(readlink "$active_destination/safe-skill")" = "$active_external" ] ||
  fail "installer modified an external active-name symlink"
[ ! -e "$active_destination/.omskills-managed-links" ] || fail "active collision wrote managed state"
assert_no_state_temp "$active_destination"

# Unsafe stale ownership is rejected before active mutation. Unowned paths are
# preserved, while a valid repository-owned stale link is removable.
fixture="$(make_valid_fixture_repo)"
unsafe_stale_destination="$FIXTURES/unsafe-stale-destination"
unsafe_stale_target="$FIXTURES/unsafe-stale-target"
mkdir "$unsafe_stale_destination" "$unsafe_stale_target"
ln -s "$unsafe_stale_target" "$unsafe_stale_destination/stale-skill"
printf '%s\n' stale-skill > "$unsafe_stale_destination/.omskills-managed-links"
if OMSKILLS_DEST="$unsafe_stale_destination" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "installer accepted an externally retargeted stale link"
fi
[ ! -e "$unsafe_stale_destination/safe-skill" ] || fail "unsafe stale link caused active mutation"
[ "$(readlink "$unsafe_stale_destination/stale-skill")" = "$unsafe_stale_target" ] ||
  fail "installer modified an unsafe stale link"
assert_no_state_temp "$unsafe_stale_destination"

fixture="$(make_valid_fixture_repo)"
add_fixture_skill "$fixture" misc stale-skill
add_fixture_skill "$fixture" misc manual-skill
owned_destination="$FIXTURES/owned-stale-destination"
mkdir "$owned_destination"
ln -s "$fixture/skills/misc/stale-skill" "$owned_destination/stale-skill"
ln -s "$fixture/skills/misc/manual-skill" "$owned_destination/manual-skill"
printf '%s\n' stale-skill > "$owned_destination/.omskills-managed-links"
chmod 644 "$owned_destination/.omskills-managed-links"
state_snapshot="$FIXTURES/managed-state-before-replacement"
ln "$owned_destination/.omskills-managed-links" "$state_snapshot"
OMSKILLS_DEST="$owned_destination" "$fixture/scripts/link-skills.sh" >/dev/null
[ ! -L "$owned_destination/stale-skill" ] || fail "valid repository-owned stale link was not removed"
[ -L "$owned_destination/manual-skill" ] || fail "manual unowned link was removed"
[ "$(cat "$owned_destination/.omskills-managed-links")" = safe-skill ] || fail "managed state was not replaced"
[ "$(cat "$state_snapshot")" = stale-skill ] || fail "managed state was not atomically replaced"
state_mode="$(python3 -c 'import os, stat, sys; print(oct(stat.S_IMODE(os.stat(sys.argv[1]).st_mode))[2:])' \
  "$owned_destination/.omskills-managed-links")"
[ "$state_mode" = 600 ] || fail "managed state permissions are not owner-only: $state_mode"
assert_no_state_temp "$owned_destination"

# A forced link failure preserves prior state and cleans the destination-local
# temporary state file.
fixture="$(make_valid_fixture_repo)"
add_fixture_skill "$fixture" misc stale-skill
failure_destination="$FIXTURES/forced-failure-destination"
mkdir "$failure_destination"
ln -s "$fixture/skills/misc/stale-skill" "$failure_destination/stale-skill"
printf '%s\n' stale-skill > "$failure_destination/.omskills-managed-links"
fake_bin="$FIXTURES/failing-bin"
mkdir "$fake_bin"
printf '%s\n' '#!/bin/sh' 'exit 73' > "$fake_bin/ln"
chmod +x "$fake_bin/ln"
if PATH="$fake_bin:$PATH" OMSKILLS_DEST="$failure_destination" \
  "$fixture/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "forced link failure unexpectedly succeeded"
fi
[ "$(cat "$failure_destination/.omskills-managed-links")" = stale-skill ] ||
  fail "forced failure replaced prior managed state"
[ -L "$failure_destination/stale-skill" ] || fail "forced failure removed stale state ownership"
[ ! -e "$failure_destination/safe-skill" ] || fail "forced failure left an active link"
assert_no_state_temp "$failure_destination"

# Check mode succeeds without changing valid state and fails without repairing
# invalid installation state or creating destination-local temporary files.
fixture="$(make_valid_fixture_repo)"
check_destination="$FIXTURES/check-destination"
OMSKILLS_DEST="$check_destination" "$fixture/scripts/link-skills.sh" >/dev/null
check_state_before="$(cat "$check_destination/.omskills-managed-links")"
check_link_before="$(readlink "$check_destination/safe-skill")"
OMSKILLS_DEST="$check_destination" "$fixture/scripts/link-skills.sh" --check >/dev/null
chmod 555 "$check_destination"
TMPDIR="$check_destination" OMSKILLS_DEST="$check_destination" \
  "$fixture/scripts/link-skills.sh" --check >/dev/null
chmod 755 "$check_destination"
[ "$(cat "$check_destination/.omskills-managed-links")" = "$check_state_before" ] ||
  fail "successful check changed managed state"
[ "$(readlink "$check_destination/safe-skill")" = "$check_link_before" ] ||
  fail "successful check changed an active link"
assert_no_state_temp "$check_destination"
rm "$check_destination/safe-skill"
if OMSKILLS_DEST="$check_destination" "$fixture/scripts/link-skills.sh" --check >/dev/null 2>&1; then
  fail "check accepted a missing active link"
fi
[ ! -e "$check_destination/safe-skill" ] || fail "failed check repaired a missing link"
[ "$(cat "$check_destination/.omskills-managed-links")" = "$check_state_before" ] ||
  fail "failed check changed managed state"
assert_no_state_temp "$check_destination"
missing_check_destination="$FIXTURES/missing-check-destination"
if OMSKILLS_DEST="$missing_check_destination" "$fixture/scripts/link-skills.sh" --check >/dev/null 2>&1; then
  fail "check accepted a missing destination"
fi
[ ! -e "$missing_check_destination" ] || fail "check created a missing destination"

# Default installation migrates only valid repository-owned legacy Codex links
# and preserves unrelated legacy content.
fixture="$(make_valid_fixture_repo)"
default_home="$FIXTURES/default-home"
mkdir -p "$default_home/.codex/skills"
ln -s "$fixture/skills/engineering/safe-skill" "$default_home/.codex/skills/safe-skill"
printf '%s\n' safe-skill > "$default_home/.codex/skills/.omskills-managed-links"
mkdir "$default_home/.codex/skills/unrelated"
HOME="$default_home" "$fixture/scripts/link-skills.sh" >/dev/null
[ -L "$default_home/.agents/skills/safe-skill" ] || fail "default install did not use ~/.agents/skills"
case "$(readlink "$default_home/.agents/skills/safe-skill")" in
  /*) fail "default installer created an absolute skill link" ;;
esac
[ ! -L "$default_home/.codex/skills/safe-skill" ] || fail "owned legacy link was not migrated"
[ ! -e "$default_home/.codex/skills/.omskills-managed-links" ] || fail "safe legacy state was not removed"
[ -d "$default_home/.codex/skills/unrelated" ] || fail "unrelated legacy content was removed"

fixture="$(make_valid_fixture_repo)"
changed_home="$FIXTURES/changed-legacy-home"
changed_target="$FIXTURES/changed-legacy-target"
mkdir -p "$changed_home/.codex/skills" "$changed_target"
ln -s "$changed_target" "$changed_home/.codex/skills/safe-skill"
printf '%s\n' safe-skill > "$changed_home/.codex/skills/.omskills-managed-links"
HOME="$changed_home" "$fixture/scripts/link-skills.sh" >/dev/null 2>&1
[ "$(readlink "$changed_home/.codex/skills/safe-skill")" = "$changed_target" ] ||
  fail "changed legacy link was modified"
[ -f "$changed_home/.codex/skills/.omskills-managed-links" ] || fail "changed legacy ownership state was removed"

# Preserve established real-catalog behavior: relative links, safe renamed-link
# migration, manual optional links, collision rejection, and physical paths.
real_destination="$TEST_ROOT/real-destination"
mkdir "$real_destination"
ln -s "$REPO/skills/engineering/to-prd" "$real_destination/to-prd"
ln -s "$REPO/skills/productivity/caveman" "$real_destination/manual-optional"
OMSKILLS_DEST="$real_destination" "$REPO/scripts/link-skills.sh" >/dev/null
OMSKILLS_DEST="$real_destination" "$REPO/scripts/link-skills.sh" --check >/dev/null
[ ! -L "$real_destination/to-prd" ] || fail "state-less renamed link was not migrated"
[ -L "$real_destination/manual-optional" ] || fail "manual optional link was removed"
case "$(readlink "$real_destination/to-spec")" in
  /*) fail "real-catalog installer created an absolute link" ;;
esac
expected="$(jq '.skills | length' "$REPO/.codex-plugin/plugin.json")"
actual="$(find "$real_destination" -type l | wc -l | tr -d ' ')"
[ "$actual" = "$((expected + 1))" ] ||
  fail "expected $expected managed links plus one optional link, found $actual"

real_external="$TEST_ROOT/real-external"
mkdir "$real_external"
ln -s "$real_external" "$real_destination/unowned-external"
OMSKILLS_DEST="$real_destination" "$REPO/scripts/link-skills.sh" >/dev/null
[ "$(readlink "$real_destination/unowned-external")" = "$real_external" ] ||
  fail "unowned external link was modified"
rm "$real_destination/to-spec"
ln -s "$real_external" "$real_destination/to-spec"
if OMSKILLS_DEST="$real_destination" "$REPO/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "real-catalog installer accepted an active external symlink"
fi
[ "$(readlink "$real_destination/to-spec")" = "$real_external" ] ||
  fail "real-catalog installer modified an active external symlink"
rm "$real_destination/to-spec"
OMSKILLS_DEST="$real_destination" "$REPO/scripts/link-skills.sh" >/dev/null
rm "$real_destination/to-spec"
mkdir "$real_destination/to-spec"
if OMSKILLS_DEST="$real_destination" "$REPO/scripts/link-skills.sh" >/dev/null 2>&1; then
  fail "installer accepted a non-symlink collision"
fi
[ -d "$real_destination/to-spec" ] || fail "installer removed a non-symlink collision"

echo "linker tests ok"
