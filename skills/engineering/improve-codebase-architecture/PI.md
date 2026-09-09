# Pi Architecture Scan Runner

The architecture-scan caller owns the scan scope, domain and architecture references, worker constraints and brief, findings artifact, candidate adjudication, report continuation, and completion.

## Choose one Pi transport

- **Root visible:** follow [tmux-worker](../../productivity/tmux-worker/SKILL.md), first obtaining the physical base with `cd '<loaded-file-directory>' && pwd -P` and resolving the link there, to launch exactly one fresh interactive Pi conversation. Delegate only worker-window creation, readiness, literal message and callback transport, continued dialogue, and directed retirement. Restrict delegation tools when the resolved launcher supports that restriction. The callback is cooperative transport, not an Accepted continuation mechanism, and cannot justify ending unattended work.
- **Root asynchronous:** start one fresh Pi subagent with asynchronous delivery and `maxChildren: 0`, inheriting the existing depth ceiling. After prompt acceptance, do not wait, sleep, poll, or repeatedly inspect status. Continue only independent work or end the response; read and validate the findings when the single pong arrives.
- **Root print:** start one fresh subagent with the same leaf ceilings. Print mode returns one bounded terminal result through the pending call and emits no later pong.
- **Managed nested or dependent root RPC caller:** use `delivery: "direct"` and `maxChildren: 0`, inheriting the depth ceiling. Consume the result in the pending call; no later pong follows. Root RPC may instead select the asynchronous path.
- **Non-delegating leaf or maintainer-directed local scan:** perform the explicitly assigned scan directly or validate supplied findings within scope; use the same artifact and evidence checks without launching another worker.

Every managed Explore dispatch is a clean start, not a continuation. Apply the authorized `model-routing` decision using exact supported lifecycle values; honor Pi's requirement for explicit user model/reasoning authorization, including an explicitly adopted routing agreement. Otherwise omit those overrides and inherit. Omit `tools` to inherit the complete active snapshot, or narrow it only after verifying every required read and artifact-write tool is active. The `Explore` name is descriptive only. Pi loads required providers and verifies the exact tool/provider set before accepting the prompt; a preflight mismatch means no scan was accepted.

Use the OS temporary directory when available, falling back to `~/scratch/`, and keep both the worker brief and findings outside the repository:

```bash
scratch_root="${TMPDIR:-$HOME/scratch}"
mkdir -p "$scratch_root"
```

The caller owns the scan scope and findings destination. Both local and delegated scans use the repository path, scan scope, exact findings-artifact path, relevant `CONTEXT.md` and ADR paths, authoritative `codebase-design` references, and required finding fields from [SKILL.md](SKILL.md). For a local scan, the caller inspects the codebase and writes evidence-backed findings directly, without implementation edits.

Only for delegation, put those inputs in a self-contained brief identifying the Explore worker. Require it to inspect the codebase and write findings to the named artifact, without editing the repository, invoking `improve-codebase-architecture`, or delegating again. For visible transport, include the literal callback target and caller-defined callback meaning; for unattended work, use the documented continuation mechanism rather than depending on a cooperative callback.

The worker produces findings only, not the final HTML report. After a completed delegated settlement or local scan, the architecture-scan caller reads and validates the findings artifact, adjudicates every candidate by checking its cited code paths against the repository and authoritative docs, and continues with the report process in [SKILL.md](SKILL.md). The caller writes and validates the report before attempting the platform opener, reports any headless opener failure with the absolute path and top recommendation, and alone decides when the scan is complete; neither a callback, bounded terminal response, findings artifact, nor opener success completes it by itself.
