# Pi Architecture Scan Runner

Follow the [`tmux-worker`](../../productivity/tmux-worker/SKILL.md) workflow to launch one visible, interactive Pi worker with a clean conversation context. Give it a self-contained architecture scan brief, a findings artifact path, and the callback target.

Use the OS temporary directory when available, falling back to `~/scratch/`, and keep both the worker brief and findings outside the repository:

```bash
scratch_root="${TMPDIR:-$HOME/scratch}"
mkdir -p "$scratch_root"
```

The brief must identify the worker as the delegated Explore worker and include the repository path, scan scope, relevant `CONTEXT.md` and ADR paths, and the authoritative `codebase-design` references. Require it to inspect the codebase directly and write evidence-backed candidate findings to the artifact. It must not edit the repository, invoke `improve-codebase-architecture`, or spawn or delegate again.

The worker produces findings only, not the final HTML report. After its callback arrives, read the findings artifact, adjudicate every candidate against the repository and authoritative docs, and continue with the report process in [SKILL.md](SKILL.md). Do not treat worker conclusions as authoritative without checking their cited code paths.
