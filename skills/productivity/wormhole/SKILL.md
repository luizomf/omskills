---
name: wormhole
description: Move the current conversation into a fresh interactive Pi window while keeping the origin recoverable.
disable-model-invocation: true
---

# Wormhole

Transfer control to a fresh Pi window in the current tmux session without closing the origin.

1. Read the current socket, pane, and session as literal values:

```bash
tmux display-message -p '#{socket_path} #{pane_id} #{session_name}'
```

2. Read [`handoff`](../handoff/SKILL.md) and follow its contract. Write the handoff to a uniquely named Markdown file in the OS temporary directory. The file is the authoritative continuation context.

3. Write a uniquely named temporary bootstrap prompt. Include:

- the exact handoff path;
- instructions to restore only its recorded context and avoid unrelated history;
- the literal origin socket and pane values;
- two literal callback commands that send `[PONG worm] jump complete; report: <handoff-path>` and then `Enter` to the origin pane;
- instructions to confirm the jump briefly in the user's language and remain interactive for the next request.

4. Choose a unique `worm-...` window name. Using the captured socket and session, open a detached named window in the current working directory running:

```bash
pi --no-skills --skill "${HOME}/.pi/agent/skills"
```

Keep the origin window alive.

5. Wait five seconds for Pi to become ready. Send a short instruction telling it to read and follow the bootstrap prompt. Send the literal instruction and `Enter` through separate `tmux send-keys` calls.

6. Switch the captured tmux session to the new window. The jump is complete when the fresh Pi sends the callback, confirms the handoff to the user, and remains interactive; the origin stays available for recovery.
