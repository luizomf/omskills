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

3. Start an interactive Pi session in a detached tmux window, keeping the current working directory and limiting skill discovery to the canonical Pi directory:

```bash
pi --no-skills --skill "${HOME}/.pi/agent/skills"
```

Wait until Pi is visibly ready, then submit a short instruction with `tmux send-keys` telling it to read the prompt file. Send the literal text and `Enter` separately. Do not use `pi -p`: the worker must remain interactive so the user can observe or contact it.

After successfully submitting the instruction, yield control back to the user by returning from the current response and making no further tool calls for this worker. Do not poll, sleep, monitor the worker pane, inspect partial output, or wait for completion. This yields the current turn; it does not complete the delegated task, terminate the delegating process, close its window or session, or mark a long-running goal complete or blocked.

4. Require detailed results in an artifact. The worker's final action sends only a short callback:

```bash
tmux -S <socket> send-keys -t <pane> -l \
  '[PONG <task>] done; report: <artifact-path>'
tmux -S <socket> send-keys -t <pane> Enter
```

The callback resumes the delegating conversation in a later turn; only then read the artifact and continue. It does not carry the result. Leave the window available when continued observation or interaction is useful. Close it only when the worker has exited and its result is preserved.
