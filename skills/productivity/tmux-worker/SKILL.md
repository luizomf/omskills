---
name: tmux-worker
description: Connect the root with an agent in a visible tmux window for multi-turn work across systems or harnesses.
---

# Tmux Worker

Use the current project's tmux session when the root needs to work or converse with an agent through another system or harness. Assign each worker one named window containing one pane so the user can observe and interact with it.

`tmux-worker` owns only this visible transport and lifecycle: worker-window creation, readiness, literal message and callback transport, continued dialogue, and directed retirement. The invoking agent or skill owns task instructions, message meaning, result artifacts, callback meaning, completion, post-callback decisions, and whether its current turn may end.

1. Capture the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Use the coordinator process's `$TMUX_PANE` as the callback target even when another window is active. Continue once all three values have been recorded literally.

2. Resolve the interactive launcher from the active harness and repository instructions, then start it as the top-level command in a detached tmux window in the current working directory and retain the worker pane's literal ID. The launcher owns skill discovery and configured profiles: do not hard-code a global skill directory or disable normal discovery unless that launcher's recorded contract explicitly requires it. For Pi, prefer the configured Pi/ompi profile; preserve the active provider, model, and reasoning through the launcher's supported mechanism unless the user requested an override. Stop rather than guessing when no suitable interactive launcher or routing mechanism can be identified.

Wait until the worker displays its normal input-ready editor. A project-trust selector is a user gate, not an input-ready editor: send no message and leave that choice to the user. Never auto-approve trust. Do not use a non-interactive print mode; the session must remain visible for user observation and input. Setup is ready for transport only when the worker pane is retained and its normal editor is input-ready; at a trust gate it remains intentionally paused.

3. Send each caller-supplied message as one literal argument with `tmux send-keys -l`, then send `Enter` separately. Keep the recorded address and message shell-quoted as literal values:

```bash
tmux -S "$socket" send-keys -t "$worker_pane" -l "$message"
tmux -S "$socket" send-keys -t "$worker_pane" Enter
```

The message may be direct conversational text or point to a caller-owned prompt or artifact. `tmux-worker` does not require a task-specific brief, artifact shape, callback wording, or completion signal. A send is complete when the literal message and separate `Enter` reach the recorded worker pane.

After submission, the invoking agent or skill may continue its own work, continue the dialogue, or follow another caller-owned policy. Sending a message neither imposes a yield nor decides whether the invoking turn may end.

4. When the caller requests a response, give the worker the literal callback socket and coordinator pane. The worker returns any caller-defined callback through the same literal transport:

```bash
tmux -S "$callback_socket" send-keys -t "$callback_pane" -l "$callback_message"
tmux -S "$callback_socket" send-keys -t "$callback_pane" Enter
```

A callback is a cooperative transport event. It may carry a reply, question, progress message, or result pointer, and only the caller decides what it means and what follows. It is not an Accepted continuation mechanism by itself and does not justify ending an unattended autonomous turn. Repeat the literal send sequence in either direction for as many conversational exchanges as the caller needs; each transport leg is complete when its message and separate `Enter` reach the recorded pane.

5. Keep the worker running throughout continued dialogue. Retire it only when the invoking agent or skill directs retirement, by sending literal `/quit` and `Enter` in separate calls to the recorded worker pane:

```bash
tmux -S "$socket" send-keys -t "$worker_pane" -l '/quit'
tmux -S "$socket" send-keys -t "$worker_pane" Enter
```

`/quit` exits Pi; it does not manage tmux. Because step 2 starts Pi as the worker pane's top-level command, tmux normally removes that pane and its one-pane window when Pi exits. If Pi was instead started from an existing shell, that shell and window remain; tmux configuration may also change either result. Do not separately kill or preserve the pane or window. Treat its resulting lifecycle as tmux behavior, not worker success or failure. Directed retirement is submitted once literal `/quit` and separate `Enter` reach the recorded worker pane; the resulting pane and window lifecycle remains tmux-owned.
