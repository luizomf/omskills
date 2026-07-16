# Supervisor state

Pass `--state-root PATH` before the subcommand and persist that exact path in the heartbeat prompt. Choose a writable location outside Git, such as a task-owned directory under `$TMPDIR` or `/private/tmp`. Without an override, `supervisor_state.py` stores each run under:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/codex/supervise-async-codex-task/<run-id>/
├── state.json
├── events.jsonl
└── .lock
```

Git, the tracker, executor thread, and executor ledger remain authoritative. This state is a compact cache for cheap heartbeats and a post-run efficiency audit.

The observation fingerprint contains only executor status, phase, update marker, executor event sequence, SHA, active role, and activity class. An unchanged fingerprint means the heartbeat should not reread the executor conversation or remote state.

Activity classes and default heartbeat recommendations:

- `quick`: 180 seconds
- `normal`: 600 seconds
- `heavy`: 1,200 seconds
- `external`: 1,800 seconds
- `stalled`: 180 seconds
- `terminal`: no next heartbeat

The supervisor may override a recommendation when the executor provides better timing evidence. Update the automation only when the effective timing class changes.

Metrics count observations, unchanged observations, full executor reads, interventions, phase transitions, and recorded improvements. Do not put prompts, diffs, command output, credentials, terminal content, or secrets in state or events.
