---
name: wormhole
description: Move the current conversation into a fresh interactive agent window while keeping the origin recoverable.
---

# Wormhole

Transfer control to a fresh interactive agent window in the current tmux session without closing the origin.

1. Read the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Targeting the coordinator process's `$TMUX_PANE` keeps the callback stable when
the user views another window.

2. Read [`handoff`](../handoff/SKILL.md) and follow its contract. Write the handoff to a uniquely named Markdown file in the OS temporary directory. Near the top, add:

```md
## Wormhole context

You are the fresh continuation of a conversation transferred through a wormhole, not an independent worker. The origin session remains alive and recoverable.
```

The file is the authoritative continuation context.

3. Write a uniquely named temporary bootstrap prompt. Include:

- the exact handoff path;
- instructions to restore only its recorded context and avoid unrelated history;
- the literal origin socket and pane values;
- two literal callback commands that send `[PONG worm] jump complete; report: <handoff-path>` and then `Enter` to the origin pane;
- instructions to confirm the jump briefly in the user's language, then continue from the handoff in the same turn: start its authorized immediate next step, or remain interactive only when the handoff records a user gate or no authorized action.

4. Choose a unique `worm-...` window name. Using the captured socket and session, open a detached named window in the current working directory:

- In Pi, run `pi --no-skills --skill "${HOME}/.pi/agent/skills"`.
- In another harness, run its supported command for a fresh interactive session. If that command cannot be identified safely, return the handoff path instead of guessing.

Keep the origin window alive.

5. Wait for the harness to become ready. Send a short instruction telling it to read and follow the bootstrap prompt. Send the literal instruction and `Enter` through separate `tmux send-keys` calls.

6. Switch the captured tmux session to the new window. The origin stays available for recovery. The jump is complete when the fresh agent sends the callback, confirms the handoff to the user, and does one of the following in that same turn:

- begins the authorized immediate next step recorded in the handoff;
- remains interactive because the handoff records a user gate or no authorized action.

Confirmation alone is not completion while authorized work remains.
