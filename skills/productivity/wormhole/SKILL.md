---
name: wormhole
description: Move the current conversation into a fresh interactive agent window and retire the origin Pi after a successful transfer.
---

# Wormhole

Transfer control to a fresh interactive agent window in the current tmux session.

1. Capture the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Use the coordinator process's `$TMUX_PANE` as the callback target even when another window is active.

2. Read `handoff` and follow its contract. Write the handoff under a unique Markdown filename in the OS temporary directory. Add this section near the top:

```md
## Wormhole context

You are the fresh continuation of a conversation transferred through a wormhole, not an independent worker. The origin Pi remains alive only until you restore the handoff, then you retire that Pi process. `/quit` exits Pi; it does not manage tmux. An origin started inside an existing shell normally returns to that shell and leaves its window open. An origin running as the pane's top-level command normally lets tmux remove the pane and its one-pane window. Tmux configuration may change either result, and both are valid transfer outcomes.
```

Use this file as the only continuation context.

3. Write a uniquely named temporary bootstrap prompt containing:

- the exact handoff path;
- instructions to restore only the context recorded in that file;
- the literal origin socket and pane values;
- four literal completion commands that send `[PONG worm] jump complete; report: <handoff-path>` and `Enter`, then `/quit` and `Enter` to the origin pane;
- instructions to run those completion commands only after restoring every needed detail from the handoff;
- instructions to confirm the jump briefly in the user's language, state that the origin Pi exited, report the resulting origin pane or window state when observable without treating either outcome as an error, then, in the same turn, either start the authorized immediate next step from the handoff or remain interactive when the handoff records a user gate or no authorized action.

4. Choose an unused `worm-...` window name. Resolve the fresh interactive launcher from the active harness and repository instructions, then use the captured socket and session to open a detached named window in the current working directory.

The launcher owns skill discovery and configured profiles: do not hard-code a global skill directory or disable normal discovery unless that launcher's recorded contract explicitly requires it. For Pi, prefer the configured Pi/ompi profile and preserve the active provider, model, and reasoning through its supported mechanism unless the user requested an override. In another harness, use its supported fresh-session mechanism. If the launcher or routing mechanism cannot be identified, return the handoff path instead of guessing.

Keep the origin Pi running until the fresh agent completes the transfer. Do not separately kill or preserve the origin pane or window after `/quit`; let tmux apply the lifecycle implied by how the origin was launched and configured.

5. After the new harness displays its normal input-ready editor, tell it to read and follow the bootstrap prompt. A project-trust selector is a user gate: do not send bootstrap input or auto-approve it. Send the literal instruction and `Enter` in separate `tmux send-keys` calls only after readiness.

6. Switch the captured tmux session to the new window. The jump is complete only when the fresh agent, in one turn:

- restores every needed detail from the handoff outside the origin pane;
- sends the callback and then retires the origin Pi with literal `/quit` and `Enter` in separate `tmux send-keys` calls;
- confirms the handoff and exited origin Pi, and reports the resulting origin pane or window state when observable without treating either outcome as an error; and
- starts the authorized immediate next step recorded in the handoff, or remains interactive because the handoff records a user gate or no authorized action.
