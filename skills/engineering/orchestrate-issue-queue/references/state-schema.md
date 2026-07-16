# State and event model

## Storage

`run_state.py` stores each run under:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/codex/orchestrate-issue-queue/<run-id>/
├── state.json
├── events.jsonl
└── .lock
```

Pass `--state-root PATH` before the subcommand to use an isolated location for tests or a project-owned orchestration runtime.

`state.json` is the latest resumable snapshot. `events.jsonl` is the append-only diagnostic history. Git and the configured tracker remain authoritative; always revalidate them after resuming.

## Run fields

- `schema_version`: State format version.
- `run_id`: Filesystem-safe run identifier.
- `repository`: Repository identity or absolute path.
- `goal`: User-visible completion outcome. It is not copied into the event log.
- `status`: `active`, `complete`, or `blocked`.
- `goal_status`: `none`, `active`, or `paused`; this describes Goal mode, not business completion.
- `review_policy`: `single` or `dual`.
- `max_correction_attempts`: Automatic correction budget per issue.
- `active_issue`: The only issue allowed to have a writer.
- `queue`: Ordered issue snapshots.
- `event_sequence`: Last event incorporated into the snapshot.

## Issue fields

- `status`: `pending`, `active`, `done`, or `blocked`.
- `phase`: `queued`, `preflight`, `implementing`, `reviewing`, `correcting`, `done`, or `blocked`.
- `branch`, `pr`, `remote_sha`: Current delivered Git identity.
- `review_rounds`: SHA-scoped reviewer dispatches and results. A new delivery creates a new round and cannot inherit results or reviewer identities.
- `verification`: Repository gates recorded for the current reviewed SHA. A new delivery invalidates it.
- `correction_attempts`: Corrections actually dispatched.
- `awaiting`: External or delegated result currently expected.
- `next_action`: The next safe orchestration action.
- `merged`, `closed`: Confirmed tracker outcomes.

## Review roles

- `single`: require `reviewer`.
- `dual`: require both `adversarial` and `standards-spec`.

Record a reviewer result only after checking that `reviewed_sha` equals the current remote SHA. A blocking result must report at least one blocking finding. Record non-blocking observations outside `blocking_findings` in the review artifact; the ledger intentionally stores only counts and outcomes.

Record each reviewer dispatch before accepting its result. Writer and reviewer agent identifiers must be distinct, and every correction round requires fresh writer and reviewer identifiers.

After all reviews pass, record the repository-defined gates with `record-verification`. Integration requires a passing verification for the same remote SHA. Store check names and the combined outcome, not raw command output.

## Correction limit

Dispatching a correction consumes one attempt. If a completed review round still blocks after the configured budget is exhausted, the script sets:

```text
goal_status = paused
awaiting = human_decision
next_action = request_human_decision
```

Use `authorize-correction --additional-attempts N` only after explicit human authorization. It may resume a review-blocked run that was terminalized with `block-run`, but it preserves `goal_status`; Goal mode must be resumed separately when applicable. Use `block-run` when the decision is to stop.

## Event log

Every accepted mutation appends one compact JSON object containing a monotonic sequence number, timestamp, run ID, event name, issue/phase when applicable, and metadata required to diagnose the transition. Rejected transitions also append `transition_rejected` without changing the snapshot.

Do not put secrets or large raw artifacts into `--reason`, agent IDs, issue IDs, branch names, PR identifiers, or repository identifiers.
