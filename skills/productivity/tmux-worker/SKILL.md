---
name: tmux-worker
description: Delegate independent work to a visible tmux window and receive a completion callback containing the result artifact path.
---

# Tmux Worker

Use the current project's tmux session. Assign each worker one named window containing one pane so the user can observe and interact with the worker.

1. Capture the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Use the coordinator process's `$TMUX_PANE` as the callback target even when another window is active.

2. Write a self-contained worker prompt to a temporary file or project scratch file. Include the assigned scope, paths to every artifact required by the task, completion criteria, and the literal callback socket and pane values. State that the worker delivers its result only through the artifact and the callback, never as a reply to the user.

3. In the current working directory, start an interactive Pi session in a detached tmux window. Limit skill discovery to the canonical Pi directory:

```bash
pi --no-skills --skill "${HOME}/.pi/agent/skills"
```

After Pi displays an input-ready interface, use `tmux send-keys` to submit one instruction telling it to read the prompt file. Send the literal instruction and `Enter` in separate calls. Do not use `pi -p`; the session must remain interactive for user observation and input.

After the instruction is submitted, return from the current response and make no further tool calls for this worker. Do not poll, read the worker pane, or wait for completion. Do not mark the delegated task or its parent goal complete or blocked.

4. Require the worker to write its detailed result to an artifact and make the callback its final action:

```bash
tmux -S <socket> send-keys -t <pane> -l \
  '[PONG <task>] done; report: <artifact-path>'
tmux -S <socket> send-keys -t <pane> Enter
```

The callback starts a later turn and identifies the result artifact. Treat it as a resumption trigger, not a completion report: in that turn, read the artifact. Only the root starts workers and decides whether to reply or stop; multi-turn conversation with the same worker is allowed, but neither side may hand off the task or start an autonomous work-review loop. Keep the window open while the worker is running or further interaction is expected. Close it only after the worker exits and the result exists outside the window.
