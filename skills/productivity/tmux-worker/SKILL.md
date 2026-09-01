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

3. Send each caller-supplied message through a unique tmux buffer, then send `Enter` separately. Do not pass caller-controlled content as a tmux command argument: tmux may reinterpret leading options or command separators even when the shell preserves one argument. Choose each buffer name as a unique identifier containing only ASCII letters, digits, hyphens, and underscores, and keep the recorded addresses shell-quoted:

```bash
printf '%s' "$message" |
  tmux -S "$socket" load-buffer -b "$buffer_name" -
tmux -S "$socket" paste-buffer -b "$buffer_name" -t "$worker_pane" -d
tmux -S "$socket" send-keys -t "$worker_pane" Enter
```

The message may be direct conversational text or point to a caller-owned prompt or artifact. `tmux-worker` does not require a task-specific brief, artifact shape, callback wording, or completion signal. A send is complete when the paste deletes its unique buffer and the separate `Enter` reaches the recorded worker pane.

After submission, the invoking agent or skill may continue its own work, continue the dialogue, or follow another caller-owned policy. Sending a message neither imposes a yield nor decides whether the invoking turn may end.

4. When the caller requests a response, give the worker the literal callback socket and coordinator pane. The worker returns any caller-defined callback through the same buffered transport, with a new safe unique buffer name:

```bash
printf '%s' "$callback_message" |
  tmux -S "$callback_socket" load-buffer -b "$callback_buffer_name" -
tmux -S "$callback_socket" paste-buffer \
  -b "$callback_buffer_name" -t "$callback_pane" -d
tmux -S "$callback_socket" send-keys -t "$callback_pane" Enter
```

A callback is a cooperative transport event. It may carry a reply, question, progress message, or result pointer, and only the caller decides what it means and what follows. It is not an Accepted continuation mechanism by itself and does not justify ending an unattended autonomous turn. Repeat the buffered literal transport in either direction for as many conversational exchanges as the caller needs; each transport leg is complete when its paste deletes the unique buffer and separate `Enter` reaches the recorded pane.

5. Keep the worker running throughout continued dialogue. Retire it only when the invoking agent or skill directs retirement, by sending literal `/quit` and `Enter` in separate calls to the recorded worker pane:

```bash
tmux -S "$socket" send-keys -t "$worker_pane" -l '/quit'
tmux -S "$socket" send-keys -t "$worker_pane" Enter
```

`/quit` exits Pi; it does not manage tmux. Because step 2 starts Pi as the worker pane's top-level command, tmux normally removes that pane and its one-pane window when Pi exits. If Pi was instead started from an existing shell, that shell and window remain; tmux configuration may also change either result. Do not separately kill or preserve the pane or window. Treat its resulting lifecycle as tmux behavior, not worker success or failure. Directed retirement is submitted once literal `/quit` and separate `Enter` reach the recorded worker pane; the resulting pane and window lifecycle remains tmux-owned.

## Apply caller-owned bounded Mission observation

A separate external root may deliberately act as **Mission observer** for a long Mission whose dispatcher runs in the visible worker window. The observer, not `tmux-worker`, owns this optional policy. It receives the fixed Mission identities and uses the recorded pane only as a visible transport endpoint; it adopts neither Ticket implementation nor dispatcher state.

While the Mission is active, submit at most one self-terminating, payload-free heartbeat. Its reentry prompt must carry the fixed identities, recorded dispatcher target, allowed evidence, and this decision policy without adding work. With Pi's `scheduler_submit`, use one `in` or `at` timing value and omit `payload`, `cron`, `every`, and `count`. Do not submit the next heartbeat before the current one fires. If the active harness has no documented payload-free heartbeat and reentry mechanism, report that observation is unavailable; never imitate it with a background command, sleep, polling loop, recurring or infinite schedule, daemon, monitoring code or script, persistent workflow state, takeover mechanism, or new infrastructure.

When the heartbeat fires, perform one bounded inspection: capture the visible dispatcher pane once, then read only the commit and Issue evidence needed for the fixed Tickets and current transition. Pane prose may show activity or a mechanical transition, but never proves delivery by itself; corroborate a delivery claim with durable repository and tracker evidence. Do not sleep, recapture repeatedly, poll, loop, inspect implementation semantics, or supervise healthy choices. Quiet output or elapsed time alone is not a failure.

Choose exactly one outcome from that inspection:

- **Healthy and active:** send no message, submit one next payload-free heartbeat, and otherwise remain silent.
- **Concrete failure or blockage, abandoned human gate, or mechanically invalid or stopped dispatch transition:** make at most one intervention. Address it explicitly to the applicable dispatcher root or name exactly one active coordinator ID for literal forwarding; never target a writer, change the frozen plan, or select adjacent work. If the Mission remains active afterward, submit one next heartbeat. Never auto-approve a trust or other human gate.
- **Every fixed Ticket durably delivered, or a real terminal stop:** submit no heartbeat. Report any concrete terminal problem to the applicable root, then direct the visible worker's normal retirement once through step 5; do not kill or take over its pane or window.

This observation does not create a continuation or survival guarantee. A cooperative callback remains only a transport event, and neither callbacks nor pane text permit an unattended turn to claim Mission completion.
