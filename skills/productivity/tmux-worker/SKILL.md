---
name: tmux-worker
description: Delegate independent work to a visible tmux window and receive a short completion callback.
disable-model-invocation: true
---

# Tmux Worker

Use the current project's tmux session. Give each worker one named window and pane so the user can observe or interact with it.

1. Read the current socket, pane, and session:

```bash
tmux display-message -p '#{socket_path} #{pane_id} #{session_name}'
```

2. Write a self-contained worker prompt to a temporary or project scratch file. Include scope, relevant artifact paths, completion criteria, and literal callback socket and pane values.

3. Start the active harness in a detached tmux window using its verified non-interactive invocation. Do not guess harness syntax. Pass the prompt file, keep the working directory, and avoid embedding the full prompt in shell quoting.

4. Require detailed results in an artifact. The worker's final action sends only a short callback:

```bash
tmux -S <socket> send-keys -t <pane> -l \
  '[PONG <task>] done; report: <artifact-path>'
tmux -S <socket> send-keys -t <pane> Enter
```

The callback wakes the delegating conversation; it does not carry the result. Leave the window available when continued observation or interaction is useful. Close it only when the worker has exited and its result is preserved.
