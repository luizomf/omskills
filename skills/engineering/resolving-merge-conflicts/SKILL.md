---
name: resolving-merge-conflicts
description: Resolves an in-progress git merge or rebase conflict by understanding each change's intent and preserving both where possible. Use when a git merge or rebase has stopped with conflicts, files show conflict markers, or the user asks to resolve merge conflicts.
---

# Resolving Merge Conflicts

1. **Inspect the operation state.** Check Git status, the merge or rebase todo state, the commit ranges on both sides, and every file Git reports as conflicted.
2. **Trace each side's intent.** For every conflict, inspect the commits that introduced both sides and locate the originating PRs, issues, or tickets from links, commit messages, or repository history.
3. **Resolve every hunk.** When both intended behaviors can coexist, preserve both. When they cannot, preserve the behavior that matches the stated goal of the merge or rebase and report the discarded behavior as a trade-off. Do not add behavior absent from both sides. Always resolve the conflict; never abort the operation.
4. **Run automated checks.** Use the repository-defined commands and order; when no order is defined, typically run typecheck, then tests, then formatting. Fix anything the merge or rebase broke.
5. **Finish the operation.** Stage everything. Run `git merge --continue` or `git rebase --continue` as applicable; if Git requires a direct merge commit, create it. For a rebase, repeat these steps for each subsequent conflict until Git reports that all commits have been rebased.
