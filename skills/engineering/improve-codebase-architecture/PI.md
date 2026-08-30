# Pi Architecture Scan Runner

The architecture-scan caller owns the scan scope, domain and architecture references, worker constraints and brief, findings artifact, candidate adjudication, report continuation, and completion.

## Choose one Pi transport

- **Root visible:** follow `tmux-worker` to launch exactly one fresh interactive Pi conversation. Delegate only worker-window creation, readiness, literal message and callback transport, continued dialogue, and directed retirement. Restrict delegation tools when the resolved launcher supports that restriction. The callback is cooperative transport, not an Accepted continuation mechanism, and cannot justify ending unattended work.
- **Root asynchronous:** start one fresh Pi subagent with asynchronous delivery, `maxDepth` equal to the child's assigned depth (normally `2`), and `maxChildren: 0`. After prompt acceptance, do not wait, sleep, poll, or repeatedly inspect status. Continue only independent work or end the response; read and validate the findings when the single pong arrives.
- **Root print:** start one fresh subagent with the same leaf ceilings. Print mode returns one bounded terminal result through the pending call and emits no later pong.
- **Dependent depth-2 caller:** start one fresh depth-3 subagent with explicit `delivery: "direct"`, `maxDepth: 3`, and `maxChildren: 0`. Consume that result in the pending call; no later pong follows.
- **Depth-3 leaf:** never invoke `subagent_start` or `subagent_continue`. Pi rejects a further start before process launch. Continue only when the coordinator supplied the complete predeclared findings artifact and validate it locally; otherwise return a blocker.

Every managed Explore dispatch is a clean start, not a continuation. Omit model and reasoning overrides unless the user explicitly requested them. Omit `tools` to inherit the complete active snapshot, or narrow it only after verifying every required read and artifact-write tool is active. The `Explore` name is descriptive only. Pi loads required providers and verifies the exact tool/provider set before accepting the prompt; a preflight mismatch means no scan was accepted.

Use the OS temporary directory when available, falling back to `~/scratch/`, and keep both the worker brief and findings outside the repository:

```bash
scratch_root="${TMPDIR:-$HOME/scratch}"
mkdir -p "$scratch_root"
```

The caller writes and owns the self-contained brief and findings destination. The brief must identify the worker as the delegated Explore worker and include the repository path, scan scope, exact findings-artifact path, relevant `CONTEXT.md` and ADR paths, the authoritative `codebase-design` references, and the required finding fields from [SKILL.md](SKILL.md). Require the worker to inspect the codebase directly and write evidence-backed candidate findings to that artifact. It must not edit the repository, invoke `improve-codebase-architecture`, or spawn or delegate again. For visible transport, include the literal callback target and caller-defined callback meaning; for unattended work, let the documented continuation mechanism return control without depending on a cooperative callback.

The worker produces findings only, not the final HTML report. When the selected mechanism returns a completed settlement, the architecture-scan caller reads and validates the findings artifact, adjudicates every candidate by checking its cited code paths against the repository and authoritative docs, and continues with the report process in [SKILL.md](SKILL.md). The caller writes and validates the report before attempting the platform opener, reports any headless opener failure with the absolute path and top recommendation, and alone decides when the scan is complete; neither a callback, bounded terminal response, findings artifact, nor opener success completes it by itself.
