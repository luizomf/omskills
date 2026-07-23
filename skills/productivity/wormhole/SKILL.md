---
name: wormhole
description: Move the current conversation into a fresh interactive agent window while keeping the origin recoverable.
---

# Wormhole

Transfer control to a fresh interactive agent window in the current tmux session.

1. Capture the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Use the coordinator process's `$TMUX_PANE` as the callback target even when another window is active.

2. Read [`handoff`](../handoff/SKILL.md) and follow its contract. Write the handoff under a unique Markdown filename in the OS temporary directory. Add this section near the top:

```md
## Wormhole context

You are the fresh continuation of a conversation transferred through a wormhole, not an independent worker. The origin session remains alive and recoverable.
```

Use this file as the only continuation context.

3. Write a uniquely named temporary bootstrap prompt containing:

- the exact handoff path;
- instructions to restore only the context recorded in that file;
- the literal origin socket and pane values;
- two literal callback commands that send `[PONG worm] jump complete; report: <handoff-path>` and then `Enter` to the origin pane;
- instructions to confirm the jump briefly in the user's language, then, in the same turn, either start the authorized immediate next step from the handoff or remain interactive when the handoff records a user gate or no authorized action.

4. Choose an unused `worm-...` window name. Using the captured socket and session, open a detached named window in the current working directory:

- In Pi, run `pi --no-skills --skill "${HOME}/.pi/agent/skills"`.
- In another harness, run its supported command for a fresh interactive session. If that command cannot be identified safely, return the handoff path instead of guessing.

Keep the origin window open.

5. After the new harness displays an input-ready interface, tell it to read and follow the bootstrap prompt. Send the literal instruction and `Enter` in separate `tmux send-keys` calls.

6. Switch the captured tmux session to the new window. The jump is complete only when the fresh agent, in one turn:

- sends the callback;
- confirms the handoff to the user; and
- starts the authorized immediate next step recorded in the handoff, or remains interactive because the handoff records a user gate or no authorized action.
