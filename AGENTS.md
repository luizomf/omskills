# Working on omskills

This repository contains agent skills, prompts, docs, and helper scripts—not an
application. This file is canonical; `CLAUDE.md` is a compatibility pointer.
Use English for repository artifacts and the user's language in chat.

## Working style

- Carry the requested work through verification, conventional commit, and push
  to `origin`, unless the user asks otherwise. No branch or PR ceremony needed.
- Keep going when the next step is clear and in scope. Ask only when missing
  input blocks progress or an action is destructive or hard to reverse.
- Inspect Git status and relevant files before editing. Preserve unrelated work;
  never commit secrets, private notes, local settings, or scratch artifacts.
- Prefer the smallest clear, maintainable solution. Avoid speculative features,
  dependencies, abstractions, and process. Fix relevant outdated docs too.
- Review the diff and run checks relevant to the change. Prefer test-first for
  behavior changes and regression tests for bugs; test observable behavior, not
  incidental wording. Documentation edits do not need invented tests.
- Prefer portable Linux/macOS paths and scripts. Use `rtk` where it preserves
  useful output. Put new worktrees under
  `~/sannux-data/worktrees/<repo>/<worktree_name>` if needed.
- Do not force-push, rewrite history, publish releases, or change repository
  visibility without explicit authorization.
- Finish with a concise summary, verification results, and any remaining issues.

## Where things live

- `skills/engineering/` and `skills/productivity/`: skills and bucket catalogs.
- `README.md`: active catalog; `.codex-plugin/plugin.json`: active distribution;
  `.claude-plugin/plugin.json`: matching entries in the same order.
- `CONTEXT.md` and `docs/adr/`: domain vocabulary and durable design decisions.
- `docs/agents/`: tracker and domain-document configuration when needed.

Read the context relevant to the request, not every workflow document. Workflows
provided by skills are not mandatory steps for ordinary repository maintenance.
Adopt upstream ideas deliberately; do not synchronize wholesale with the source
project. Keep this file short and repository-specific, not a workflow manual.

## Skill catalog and installation

- Active skills belong in the root README, bucket README, and both manifests.
  Optional skills belong only in their bucket README. Link entries to `SKILL.md`.
- New skills default to `disable-model-invocation: true`; making them permanently
  discoverable needs maintainer approval. Active user-only exceptions are
  recorded in `scripts/check-catalog.py`.
- Rename the folder, frontmatter `name`, catalog entries, and references together.
  Preserve existing behavior unless the request changes it.
- Use relative Markdown links for cross-skill loading. Resolve the referring
  file's symlink first, then resolve links from its physical directory—not the
  workspace or flat installation directory.
- Install only what was requested, using relative symlinks from the destination's
  physical directory. For the full active catalog, use `scripts/link-skills.sh`
  with `OMSKILLS_DEST` for the chosen destination. Verify links with `readlink`
  and a readable target `SKILL.md`.

## Checks

Run the applicable checks; catalog or installer changes need both the catalog
checker and installer tests:

```sh
./scripts/check-catalog.py
./tests/test-link-skills.sh
python3 -B tests/test-skill-pointers.py
python3 -B tests/test-html-report.py
```

For manifest or installation changes, also run `./scripts/link-skills.sh --check`
when the managed destination exists. No repository-wide formatter, linter, or
typechecker is configured.
