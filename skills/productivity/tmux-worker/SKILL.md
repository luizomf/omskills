---
name: tmux-worker
description: Delegate a Pi task to a tmux window and receive a short wake-up ping. Use when independent work can run in another Pi conversation.
---

# Tmux Worker

Use the current project's tmux session. Each task gets one window with one pane.

1. Get the session and the callback address:

```bash
tmux display-message -p '#{socket_path} #{pane_id} #{session_name}'
```

2. Write the worker prompt to a file. Give it the scope, artifact paths, and the literal socket and pane values. Its final action sends a short ping:

```bash
tmux -S <socket> send-keys -t <pane> -l \
  '[PONG dependency-audit] done; report: .scratch/dependency-audit.md'
tmux -S <socket> send-keys -t <pane> Enter
```

Code, reports, and other detailed output belong in files. The ping only wakes the delegating Pi and points to the result.

3. Start a named, saved Pi conversation in a detached window:

```bash
TASK=dependency-audit
PROMPT="$PWD/.scratch/$TASK-prompt.md"
SESSION="$(tmux display-message -p '#{session_name}')"
SOCKET="$(tmux display-message -p '#{socket_path}')"

tmux -S "$SOCKET" new-window -d -t "$SESSION:" -n "$TASK" -c "$PWD" \
  "pi -p --name '$TASK' '@$PROMPT'"
```

The window closes when the one-shot Pi exits. Resume its saved conversation with Pi's session history when needed.
