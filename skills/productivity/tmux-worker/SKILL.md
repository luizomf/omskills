---
name: tmux-worker
description: Connect the root with an agent in a visible tmux window for multi-turn work across systems or harnesses.
---

# Tmux Worker

Use the current project's tmux session when the root needs to work or converse with an agent through another system or harness. Assign each worker one named window containing one pane so the user can observe and interact with it.

1. Capture the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Use the coordinator process's `$TMUX_PANE` as the callback target even when another window is active.

2. Write a self-contained worker prompt to a temporary file or project scratch file. Include the assigned scope, paths to every artifact required by the task, completion criteria, and the literal callback socket and pane values. State that the worker delivers its result only through the artifact and the callback, never as a reply to the user.

3. In the current working directory, start an interactive Pi session in a detached tmux window and retain that worker pane's literal ID. Limit skill discovery to the canonical Pi directory:

```bash
pi --no-skills --skill "${HOME}/.pi/agent/skills"
```

Use `tmux send-keys` to submit one instruction telling Pi to read the prompt file. Send the literal instruction first, wait five seconds for Pi to finish opening, and only then send `Enter` in a separate call. The delay is required even when Pi already appears input-ready; without it, an early `Enter` can interrupt startup before Pi accepts the instruction. Do not use `pi -p`; the session must remain interactive for user observation and input.

```bash
tmux -S <socket> send-keys -t <worker-pane> -l \
  'Read and follow the worker prompt at <prompt-path>.'
sleep 5
tmux -S <socket> send-keys -t <worker-pane> Enter
```

After the instruction is submitted, return from the current response and make no further tool calls for this worker. Do not poll, read the worker pane, or wait for completion. Do not mark the delegated task or its parent goal complete or blocked.

4. Require the worker to write its detailed result to an artifact and make the callback its final action:

```bash
tmux -S <socket> send-keys -t <pane> -l \
  '[PONG <task>] done; report: <artifact-path>'
tmux -S <socket> send-keys -t <pane> Enter
```

The callback completes the transport handshake. The user or invoking skill determines the work and what follows; `tmux-worker` does not.

Conversation with the same worker may continue normally. When the root accepts a callback as the final transfer, first read the artifact and preserve every needed result outside the worker pane. Then retire the old Pi session by sending literal `/quit` and `Enter` in separate calls to the recorded worker pane:

```bash
tmux -S <socket> send-keys -t <worker-pane> -l '/quit'
tmux -S <socket> send-keys -t <worker-pane> Enter
```

`/quit` exits Pi; it does not manage tmux. Because step 3 starts Pi as the worker pane's top-level command, tmux normally removes that pane and its one-pane window when Pi exits. If Pi was instead started from an existing shell, that shell and window remain; tmux configuration may also change either result. Do not separately kill or preserve the pane or window. Treat its resulting lifecycle as tmux behavior, not worker success or failure.

Keep the worker running after intermediate callbacks; retire it only after the final transfer.
