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

You are the fresh continuation of a conversation transferred through a wormhole, not an independent worker. The origin Pi remains alive until your single jump-complete callback confirms that you restored the handoff and reached the first Safe turn boundary; only then do you retire that Pi process. `/quit` exits Pi; it does not manage tmux. An origin started inside an existing shell normally returns to that shell and leaves its window open. An origin running as the pane's top-level command normally lets tmux remove the pane and its one-pane window. Tmux configuration may change either result, and both are valid transfer outcomes.
```

Use this file as the only continuation context.

3. Write a uniquely named temporary bootstrap prompt containing:

- the exact handoff path;
- instructions to restore only the context recorded in that file;
- the literal origin socket and pane values;
- four literal completion commands that send `[PONG worm] jump complete; report: <handoff-path>` and `Enter`, then `/quit` and `Enter` to the origin pane;
- the complete continuation contract:
  - The handoff's recorded authorized immediate action, explicit user gate, or absence of authorized action selects the branch. The transfer creates neither work nor authority.
  - Restore every needed detail before evaluating the boundary. With no authorized immediate action, complete restoration into a clean interactive context is the first Safe turn boundary. At an explicit user gate, restore the context and wait at the recorded gate.
  - With authorized immediate work, follow the governing workflow to its concrete first Safe turn boundary. Context restoration, skill reading, state inspection, work selection or claiming, planning, and statements of intent are preparation and do not reach that boundary.
  - Without a workflow-specific asynchronous boundary, continue the authorized direct action until it completes, reaches the recorded explicit gate, or encounters a genuine blocker.
  - After complete restoration and the first Safe turn boundary, run the four completion commands exactly once. Completed, blocked, and explicit-gate outcomes all require the same definitive callback before origin retirement.
- instructions, after the completion commands, to confirm the jump briefly in the user's language, state that the origin Pi exited, report the resulting origin pane or window state when observable without treating either outcome as an error, report whether the continuation is safely running, completed, blocked, or waiting at the recorded gate, and remain interactive when the handoff records a user gate or no authorized action.

4. Choose an unused `worm-...` window name. Resolve the fresh interactive launcher from the active harness and repository instructions, then use the captured socket and session to open a detached named window in the current working directory.

The launcher owns skill discovery and configured profiles: do not hard-code a global skill directory or disable normal discovery unless that launcher's recorded contract explicitly requires it. For Pi, prefer the configured Pi/ompi profile and preserve the active provider, model, and reasoning through its supported mechanism unless the user requested an override. In another harness, use its supported fresh-session mechanism. If the launcher or routing mechanism cannot be identified, return the handoff path instead of guessing.

Keep the origin Pi running until it receives the definitive callback. The origin does not infer a terminal state independently and retires only through the `/quit` sent after that callback. Do not separately kill or preserve the origin pane or window after `/quit`; let tmux apply the lifecycle implied by how the origin was launched and configured.

5. After the new harness displays its normal input-ready editor, tell it to read and follow the bootstrap prompt. A project-trust selector is a user gate: do not send bootstrap input or auto-approve it. Send the literal instruction and `Enter` in separate `tmux send-keys` calls only after readiness.

6. Switch the captured tmux session to the new window. The jump is complete only when the fresh agent, in one turn:

- restores every needed detail from the handoff outside the origin pane;
- follows the handoff-selected branch and reaches its first Safe turn boundary under the continuation contract;
- sends exactly one definitive callback and then retires the origin Pi with literal `/quit` and `Enter` in separate `tmux send-keys` calls; and
- confirms the handoff and exited origin Pi, reports the resulting origin pane or window state when observable without treating either outcome as an error, and reports or waits at the reached outcome.
