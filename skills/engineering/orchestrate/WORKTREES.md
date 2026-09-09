# Worktree and temporary-branch policy

Apply this policy whenever authorized work creates or disposes of temporary Git
worktrees or branches, in Direct Assisted or Mission delivery. Reading this
reference does not invoke the Mission coordinator or require a new worktree.

## Location and ownership

Create new worktrees at `$HOME/sannux-data/worktrees/<project>/<worktree-dir>/`
(for example, `$HOME/sannux-data/worktrees/omskills/ticket-123-a1b2c3/`). Use a
stable project directory name that distinguishes repositories sharing a basename
and a unique child directory per worktree. Resolve the current user's home on
macOS or Linux and create missing project parents with
`mkdir -p "$HOME/sannux-data/worktrees/$project"`. Expand the home path before
passing it to shell-free tools. Project and worktree names must be single safe
path components, not paths supplied verbatim by external text.

Verify and record the resulting path, branch, starting HEAD, and ownership.
Preserve existing worktree locations unless relocation is separately authorized.
Collision or unsafe reuse never permits touching another owner's work.

## Mandatory cleanup before completion

After verifying the final push or merge at the declared delivery target and
confirming that no integration consumer still needs the artifacts:

1. Identify the exact task-owned temporary worktrees and local/remote source
   branches. Verify worktree cleanliness, branch identity, delivery evidence,
   and absence of remaining consumers before removal. Keep the primary checkout
   and delivery target branch.
2. Remove every eligible owned worktree and delete its verified-delivered local
   and remote source branches. For squash delivery, verify the resulting target
   commit and durable source-to-squash mapping; expected lack of ancestry does
   not prevent deletion. Do not retain eligible artifacts merely as a precaution
   or leave their cleanup to the maintainer.
3. Verify absence using Git's worktree inventory and local/remote branch
   references. Record removed artifacts and any retained paths/branches with
   their reasons. Cleanup failure leaves completion outstanding even when
   publication succeeded; report exact remaining artifacts and the failure.

Preserve unrelated, failed, cancelled, dirty, undelivered, or still-consumed work
and required integration inputs. A parallel member's pushed branch artifact is
still a required input, not a leftover: its integration coordinator must clean
eligible declared predecessor artifacts after their final consumer completes.
This grants no authority to touch another task's resources outside those inputs.
No blanket deletion, history rewrite, or force-push is authorized.

Completion requires verified removal of every eligible owned temporary artifact;
protected artifacts remain with an explicit retention reason.
