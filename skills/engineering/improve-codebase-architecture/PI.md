# Pi Architecture Scan Runner

The architecture-scan caller owns the scan scope, domain and architecture references, worker constraints and brief, findings artifact, callback meaning, candidate adjudication, report continuation, and completion.

Choose the transport and continuation mode before delegating:

- For a visible cooperative scan, follow `tmux-worker` to launch exactly one new interactive Pi worker with a clean conversation context. Delegate only worker-window creation, readiness, literal message and callback transport, continued dialogue, and directed retirement. The architecture-scan caller supplies the brief, artifact path, callback target and meaning, and every post-callback decision. The callback is cooperative transport, not an Accepted continuation mechanism by itself, and does not justify ending an unattended autonomous turn.
- When the scan is part of unattended autonomous work, use an Accepted continuation mechanism documented by the active harness instead of relying on a `tmux-worker` callback. Its documented lifecycle must deliver completion automatically or attempt owning-session reentry without requiring the worker to execute a separate callback instruction. If no such mechanism is available through the caller's normal capabilities, report that unattended architecture scanning is blocked because the required continuation capability is unavailable; do not launch a cooperative worker and then silently end the turn, or substitute a background process without automatic return. Follow the active harness documentation rather than naming or guessing a harness API, and do not add a runtime or scheduler.

Use the OS temporary directory when available, falling back to `~/scratch/`, and keep both the worker brief and findings outside the repository:

```bash
scratch_root="${TMPDIR:-$HOME/scratch}"
mkdir -p "$scratch_root"
```

The caller writes and owns the self-contained brief and findings destination. The brief must identify the worker as the delegated Explore worker and include the repository path, scan scope, relevant `CONTEXT.md` and ADR paths, the authoritative `codebase-design` references, and the required finding fields from [SKILL.md](SKILL.md). Require the worker to inspect the codebase directly and write evidence-backed candidate findings to the artifact. It must not edit the repository, invoke `improve-codebase-architecture`, or spawn or delegate again. For visible transport, include the literal callback target and caller-defined callback meaning; for unattended work, let the documented continuation mechanism return control without depending on a cooperative callback.

The worker produces findings only, not the final HTML report. When the selected mechanism returns control, the architecture-scan caller reads the findings artifact, adjudicates every candidate by checking its cited code paths against the repository and authoritative docs, and continues with the report process in [SKILL.md](SKILL.md). The caller writes and opens the report, reports its absolute path and top recommendation, and alone decides when the scan is complete; neither a callback nor the findings artifact completes it.
