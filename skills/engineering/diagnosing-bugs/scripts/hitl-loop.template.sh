#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# Copy this file, edit the steps below, and run it.
# The agent runs the script; the user follows prompts in their terminal.
#
# Usage:
#   bash hitl-loop.template.sh
#
# Three helpers:
#   step "<instruction>"          → show instruction, wait for Enter
#   capture VAR "<question>"      → show question, read response into VAR
#   capture_choice VAR "<question>" → require a y/n response
#
# At the end, captured values and VERDICT=PASS|FAIL are printed for the agent
# to parse. A reproduced symptom emits VERDICT=FAIL and exits nonzero.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

capture_choice() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  while true; do
    read -r -p "    > " answer
    case "$answer" in
      y|Y) answer="y" ;;
      n|N) answer="n" ;;
      *)
        printf 'Please answer y or n.\n' >&2
        ;;
    esac
    if [ "$answer" = "y" ] || [ "$answer" = "n" ]; then
      printf -v "$var" '%s' "$answer"
      return
    fi
  done
}

# --- edit below ---------------------------------------------------------

step "Open the app at http://localhost:3000 and sign in."

capture_choice SYMPTOM_REPRODUCED \
  "Click the 'Export' button. Did the reported error occur? (y/n)"

capture ERROR_MSG "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'SYMPTOM_REPRODUCED=%s\n' "$SYMPTOM_REPRODUCED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
if [ "$SYMPTOM_REPRODUCED" = "y" ]; then
  printf 'VERDICT=FAIL\n'
  exit 1
fi
printf 'VERDICT=PASS\n'
