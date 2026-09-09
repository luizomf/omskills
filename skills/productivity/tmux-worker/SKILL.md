---
name: tmux-worker
description: Connect the root with an agent in a visible tmux window for multi-turn work across systems or harnesses.
---

# Tmux Worker

Use the current project's tmux session when the root needs to work or converse with an agent through another system or harness. Assign each worker one named window containing one pane so the user can observe and interact with it.

`tmux-worker` owns only this visible transport and lifecycle: worker-window creation, readiness, literal message and callback transport, continued dialogue, and directed retirement. The invoking agent or skill owns task instructions, message meaning, result artifacts, callback meaning, completion, post-callback decisions, and whether its current turn may end.

Before a model-selectable worker launch, the invoking agent reads [model-routing](../model-routing/SKILL.md) for the worker's actual assignment. Before reading any relative link, run `python3 -c 'from pathlib import Path; import sys; print((Path(sys.argv[1]).resolve().parent / sys.argv[2]).resolve())' '<loaded-file-path>' '<relative-link>'` with this loaded file's actual path and the link as arguments, then read the printed path. This resolves the source symlink before `..`; read the linked file even when its skill is absent from the discovery list. Apply its authorized route through the launcher's supported mechanism; this transport does not independently reclassify the task. A continuation of the user's own conversation, such as `wormhole`, preserves its route unless the user requests a change.

For shell-based documentation checks, disable interactive pagers (for example, `MANPAGER=cat PAGER=cat man tmux`) and set a short tool timeout so a lookup cannot stall the agent.

1. Capture the current socket, coordinator pane, and session as literal values:

```bash
tmux display-message -t "$TMUX_PANE" -p \
  '#{socket_path} #{pane_id} #{session_name}'
```

Use the coordinator process's `$TMUX_PANE` as the callback target even when another window is active. Continue once all three values have been recorded literally.

2. Resolve the interactive launcher from the active harness and repository instructions, then start it as the top-level command in a detached tmux window in the current working directory and retain the worker pane's literal ID. The launcher owns skill discovery and configured profiles: do not hard-code a global skill directory or disable normal discovery unless that launcher's recorded contract explicitly requires it. For Pi, prefer the configured Pi/ompi profile; apply the caller's authorized model/reasoning selection, or preserve the active route when inheritance was selected. Stop rather than guessing when no suitable interactive launcher or routing mechanism can be identified.

Wait until the worker displays its normal input-ready editor. A project-trust selector is a user gate, not an input-ready editor: send no message and leave that choice to the user. Never auto-approve trust. Do not use a non-interactive print mode; the session must remain visible for user observation and input. Setup is ready for transport only when the worker pane is retained and its normal editor is input-ready; at a trust gate it remains intentionally paused.

3. Keep every tmux message short and on one physical line, with no embedded or trailing CR/LF characters. For long or multiline text, save the full message in a uniquely named file in the OS temporary directory or a verified Git-ignored scratch directory. Confirm the recipient can read that path; a local temporary file is not automatically accessible on another machine. Keep it available until the recipient has read it, and send only a short pointer, for example: `Read /absolute/path/worker-prompt.md in full and follow its instructions.` Do not split a document into successive chat messages. Apply this rule in both directions, including callbacks.

Send the single-line message through a unique tmux buffer, then send `Enter` separately. Use `paste-buffer -p` as additional protection: tmux normally converts LF to CR, which an editor may interpret as submission; `-p` adds paste brackets only when the application has enabled bracketed paste. It does not replace the single-line rule. Do not pass caller-controlled content as a tmux command argument: tmux may reinterpret leading options or command separators even when the shell preserves one argument. Choose each buffer name as a unique identifier containing only ASCII letters, digits, hyphens, and underscores, and keep the recorded addresses shell-quoted:

```bash
printf '%s' "$message" |
  tmux -S "$socket" load-buffer -b "$buffer_name" -
tmux -S "$socket" paste-buffer -p -b "$buffer_name" -t "$worker_pane" -d
tmux -S "$socket" send-keys -t "$worker_pane" Enter
```

The message may be direct conversational text or point to a caller-owned prompt or artifact. `tmux-worker` does not require a task-specific brief, artifact shape, callback wording, or completion signal. A send is complete when the paste deletes its unique buffer and the separate `Enter` reaches the recorded worker pane.

After submission, the invoking agent or skill may continue its own work, continue the dialogue, or follow another caller-owned policy. Sending a message neither imposes a yield nor decides whether the invoking turn may end.

4. When the caller requests a response, agree on the result transport before dispatch. A buffer and bracketed paste protect literal content, not an editor's existing draft: pasting a callback and sending `Enter` can submit the human's partially typed text together with the callback.

For a coordinator pane shared with human input, prefer a native result event that preserves the editor. If none is available, save the caller-owned result artifact and use a unique named tmux event when the caller can await it synchronously with a bounded tool timeout:

```bash
# Caller awaits the agreed event; this does not inspect the editor or poll.
tmux -S "$socket" wait-for "$callback_event"
# Worker signals once after saving the terminal result, including a blocker.
tmux -S "$callback_socket" wait-for -S "$callback_event"
```

Choose an event name unique to the invocation, using only ASCII letters, digits, hyphens, and underscores. A signal carries no result payload and proves neither success nor delivery: after it arrives, read the agreed artifact and verify the required evidence. On timeout, inspect the known worker/result for the next decision rather than resubmitting the task. If neither a native event nor a synchronous wait is available, use a status-line notice and leave the result for the caller's next natural turn; the notice does not wake an idle agent. These options do not create a background observer or an Accepted continuation mechanism.

Use buffered editor callbacks only when the caller has explicitly reserved that destination for agent input without concurrent human editing. A momentary empty-editor capture is not such a reservation. Give the worker the literal socket and reserved pane, and use a new safe unique buffer name:

```bash
printf '%s' "$callback_message" |
  tmux -S "$callback_socket" load-buffer -b "$callback_buffer_name" -
tmux -S "$callback_socket" paste-buffer -p \
  -b "$callback_buffer_name" -t "$callback_pane" -d
tmux -S "$callback_socket" send-keys -t "$callback_pane" Enter
```

A callback is a cooperative transport event. It may carry a reply, question, progress message, or result pointer, and only the caller decides what it means and what follows. It is not an Accepted continuation mechanism by itself and does not justify ending an unattended autonomous turn. Repeat the agreed transport for as many conversational exchanges as the caller needs. A reserved-editor transport leg is complete when its paste deletes the unique buffer and separate `Enter` reaches the recorded pane; an event transport leg is complete when the caller receives the named signal and reads its result artifact.

5. Keep the worker running throughout continued dialogue. Retire it only when the invoking agent or skill directs retirement. For Pi, send literal `/quit` and `Enter` in separate calls to the recorded worker pane:

```bash
tmux -S "$socket" send-keys -t "$worker_pane" -l '/quit'
tmux -S "$socket" send-keys -t "$worker_pane" Enter
```

For another harness, use its known exit command; if unknown, report that retirement is blocked rather than guessing. The exit command stops the harness, not tmux. A harness launched as the pane's top-level command normally leaves tmux to remove the pane and its one-pane window; one launched inside an existing shell normally returns to that shell. Tmux configuration may change either result. Do not separately kill or preserve the pane or window. Directed retirement is submitted once the exit command and separate `Enter` reach the recorded pane; the resulting pane and window lifecycle remains tmux-owned.

## Apply caller-owned bounded Mission observation

A separate external root may deliberately act as **Mission observer** for a long Mission whose dispatcher runs in the visible worker window. The observer, not `tmux-worker`, owns this optional policy. It receives the fixed Mission identities and uses the recorded pane only as a visible transport endpoint; it adopts neither Ticket implementation nor dispatcher state.

While the Mission is active, submit at most one self-terminating, payload-free heartbeat. Its reentry prompt must carry the fixed identities, recorded dispatcher target, allowed evidence, and this decision policy without adding work. With Pi's `scheduler_submit`, use one `in` or `at` timing value and omit `payload`, `cron`, `every`, and `count`. Do not submit the next heartbeat before the current one fires. If the active harness has no documented payload-free heartbeat and reentry mechanism, report that observation is unavailable; never imitate it with a background command, sleep, polling loop, recurring or infinite schedule, daemon, monitoring code or script, persistent workflow state, takeover mechanism, or new infrastructure.

When the heartbeat fires, perform one bounded inspection: capture the visible dispatcher pane once, then read only the commit and Issue evidence needed for the fixed Tickets and current transition. Pane prose may show activity or a mechanical transition, but never proves delivery by itself; corroborate a delivery claim with durable repository and tracker evidence. Do not sleep, recapture repeatedly, poll, loop, inspect implementation semantics, or supervise healthy choices. Quiet output or elapsed time alone is not a failure.

Choose exactly one outcome from that inspection:

- **Healthy and active:** send no message, submit one next payload-free heartbeat, and otherwise remain silent.
- **Concrete failure or blockage, abandoned human gate, or mechanically invalid or stopped dispatch transition:** make at most one intervention. Address it explicitly to the applicable dispatcher root or name exactly one active coordinator ID for literal forwarding; never target a writer, change the frozen plan, or select adjacent work. If the Mission remains active afterward, submit one next heartbeat. Never auto-approve a trust or other human gate.
- **Every fixed Ticket durably delivered, or a real terminal stop:** submit no heartbeat. Report any concrete terminal problem to the applicable root, then direct the visible worker's normal retirement once through step 5; do not kill or take over its pane or window.

This observation does not create a continuation or survival guarantee. A cooperative callback remains only a transport event, and neither callbacks nor pane text permit an unattended turn to claim Mission completion.
