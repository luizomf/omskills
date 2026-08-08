#!/usr/bin/env python3
"""Deterministic checks for diagnosis and conflict-resolution evidence safety."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIAGNOSING = (ROOT / "skills/engineering/diagnosing-bugs/SKILL.md").read_text()
MERGE_RESOLUTION = (
    ROOT / "skills/engineering/resolving-merge-conflicts/SKILL.md"
).read_text()
HITL_TEMPLATE = (
    ROOT / "skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh"
)


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


@dataclass
class GitFixture:
    repo: Path
    environment: dict[str, str]

    @classmethod
    def create(cls, temporary: str, *, standalone_marker: bool = False) -> "GitFixture":
        root = Path(temporary)
        repo = root / "repo"
        home = root / "home"
        repo.mkdir()
        home.mkdir()
        environment = {
            "HOME": str(home),
            "PATH": os.environ["PATH"],
            "LC_ALL": "C",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_EDITOR": "true",
            "GIT_SEQUENCE_EDITOR": "true",
        }
        fixture = cls(repo=repo, environment=environment)
        fixture.git("init", "--quiet", "--initial-branch=main")
        fixture.git("config", "user.name", "Fixture User")
        fixture.git("config", "user.email", "fixture@example.invalid")
        fixture.write("conflict.txt", "base intent\n")
        fixture.write("staged.txt", "staged baseline\n")
        fixture.write("unstaged.txt", "unstaged baseline\n")
        standalone = (
            "<<<<<<< local\nlocal intent\n=======\nincoming intent\n>>>>>>> incoming\n"
            if standalone_marker
            else "no standalone conflict\n"
        )
        fixture.write("standalone.txt", standalone)
        fixture.git("add", "--all", "--")
        fixture.git("commit", "--quiet", "-m", "base")
        return fixture

    def git(
        self, *arguments: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            env=self.environment,
            stdin=subprocess.DEVNULL,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            shell=False,
        )
        if check and result.returncode != 0:
            raise AssertionError(
                f"git {' '.join(arguments)} failed: {result.stderr}"
            )
        return result

    def write(self, relative: str, content: str) -> None:
        (self.repo / relative).write_text(content)


def run_hitl(scripted_input: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(HITL_TEMPLATE)],
        cwd=ROOT,
        input=scripted_input,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def check_hitl_answer_validation_and_verdicts() -> None:
    passing = run_hitl("\nn\nnone\n")
    expect(passing.returncode == 0, "non-reproducing symptom did not exit zero")
    expect("SYMPTOM_REPRODUCED=n" in passing.stdout, "passing output lost the validated answer")
    expect("VERDICT=PASS" in passing.stdout, "passing output lost its machine-readable verdict")

    failing = run_hitl("\ny\nfixture error\n")
    expect(failing.returncode != 0, "reproducing symptom did not exit nonzero")
    expect("SYMPTOM_REPRODUCED=y" in failing.stdout, "failing output lost the validated answer")
    expect("VERDICT=FAIL" in failing.stdout, "failing output lost its machine-readable verdict")

    retried = run_hitl("\nnot-an-answer\nY\nfixture error\n")
    expect(retried.returncode != 0, "validated reproducing answer did not fail")
    expect("Please answer y or n." in retried.stderr, "invalid answer was not rejected")
    expect("VERDICT=FAIL" in retried.stdout, "retry did not produce the final verdict")


def check_shortest_practical_diagnosis_loop_contract() -> None:
    for phrase in (
        "shortest practical loop",
        "inherently time-bound",
        "why a shorter run cannot exercise the symptom",
        "chosen duration",
        "evidence supporting that duration",
    ):
        expect(phrase in DIAGNOSING, f"diagnosis contract omits {phrase!r}")
    expect(
        "completes in seconds, not minutes" not in DIAGNOSING,
        "diagnosis still has an absolute seconds-only completion gate",
    )


def check_merge_resolution_contract() -> None:
    for phrase in (
        "description: Resolves active merge/rebase conflicts or standalone conflict markers",
        "active merge or rebase",
        "standalone conflict-marker cleanup",
        "pre-existing staged, unstaged, and untracked work",
        "source-supported resolution for every",
        "before editing any file",
        "operation, worktree, and index unchanged from the recorded baseline",
        "Only conflict resolutions and intentional merge-caused fixes",
        "`git add -A`",
        "`git add .`",
        "`git commit -a`",
        "`git diff --cached --`",
        "restore its exact staged, unstaged, and untracked state",
        "repository-defined checks that apply",
        "Run `git merge --continue` or `git rebase --continue` only after",
    ):
        expect(phrase in MERGE_RESOLUTION, f"merge contract omits {phrase!r}")
    expect(
        "Stage everything" not in MERGE_RESOLUTION,
        "merge contract still stages unrelated work",
    )

    discovery = MERGE_RESOLUTION.index("Discover operation and baseline")
    intent = MERGE_RESOLUTION.index("Determine every resolution before editing")
    editing = MERGE_RESOLUTION.index("Edit only established resolutions")
    checks = MERGE_RESOLUTION.index("Run applicable checks")
    staging = MERGE_RESOLUTION.index("Stage selectively and inspect")
    finishing = MERGE_RESOLUTION.index("Finish the active operation or cleanup")
    expect(
        discovery < intent < editing < checks < staging < finishing,
        "merge resolution evidence is not gathered in a safe order",
    )


def prepare_active_conflict(fixture: GitFixture, operation: str) -> tuple[str, str, str]:
    if operation == "merge":
        fixture.git("checkout", "--quiet", "-b", "incoming")
        fixture.write("conflict.txt", "incoming intent\n")
        fixture.git("add", "--", "conflict.txt")
        fixture.git("commit", "--quiet", "-m", "incoming intent")
        fixture.git("checkout", "--quiet", "main")
        fixture.write("conflict.txt", "current intent\n")
        fixture.git("add", "--", "conflict.txt")
        fixture.git("commit", "--quiet", "-m", "current intent")
        result = fixture.git("merge", "incoming", check=False)
        expected = ("current intent\n", "incoming intent\n")
    elif operation == "rebase":
        fixture.git("checkout", "--quiet", "-b", "topic")
        fixture.write("conflict.txt", "topic intent\n")
        fixture.git("add", "--", "conflict.txt")
        fixture.git("commit", "--quiet", "-m", "topic intent")
        fixture.git("checkout", "--quiet", "main")
        fixture.write("conflict.txt", "upstream intent\n")
        fixture.git("add", "--", "conflict.txt")
        fixture.git("commit", "--quiet", "-m", "upstream intent")
        fixture.git("checkout", "--quiet", "topic")
        result = fixture.git("rebase", "main", check=False)
        expected = ("upstream intent\n", "topic intent\n")
    else:
        raise AssertionError(f"unsupported operation fixture: {operation}")

    expect(result.returncode != 0, f"{operation} fixture did not conflict")
    expect(
        fixture.git("ls-files", "-u", "--", "conflict.txt").stdout,
        f"{operation} fixture has no unmerged index entries",
    )
    return expected[0], expected[1], "".join(expected)


def seed_unrelated_work(fixture: GitFixture) -> dict[str, str]:
    content = {
        "staged": "pre-existing staged work\n",
        "unstaged": "pre-existing unstaged work\n",
        "untracked": "pre-existing untracked work\n",
    }
    fixture.write("staged.txt", content["staged"])
    fixture.git("add", "--", "staged.txt")
    fixture.write("unstaged.txt", content["unstaged"])
    fixture.write("untracked.txt", content["untracked"])
    content["staged_patch"] = fixture.git(
        "diff", "--cached", "--binary", "--", "staged.txt"
    ).stdout
    content["unstaged_patch"] = fixture.git(
        "diff", "--binary", "--", "unstaged.txt"
    ).stdout
    return content


def assert_unrelated_work_preserved(
    fixture: GitFixture, baseline: dict[str, str]
) -> None:
    expect(
        fixture.git("diff", "--cached", "--binary", "--", "staged.txt").stdout
        == baseline["staged_patch"],
        "pre-existing staged patch changed",
    )
    expect(
        fixture.git("diff", "--binary", "--", "unstaged.txt").stdout
        == baseline["unstaged_patch"],
        "pre-existing unstaged patch changed",
    )
    expect(
        (fixture.repo / "untracked.txt").read_text() == baseline["untracked"],
        "pre-existing untracked content changed",
    )


def check_active_merge_and_rebase_evidence() -> None:
    for operation in ("merge", "rebase"):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = GitFixture.create(temporary)
            side_two, side_three, resolution = prepare_active_conflict(
                fixture, operation
            )
            baseline = seed_unrelated_work(fixture)

            marker_snapshot = (fixture.repo / "conflict.txt").read_text()
            expect("<<<<<<<" in marker_snapshot, f"{operation} marker is absent")
            expect(
                fixture.git("show", ":2:conflict.txt").stdout == side_two,
                f"{operation} did not inspect the first source intent",
            )
            expect(
                fixture.git("show", ":3:conflict.txt").stdout == side_three,
                f"{operation} did not inspect the second source intent",
            )
            expect(
                (fixture.repo / "conflict.txt").read_text() == marker_snapshot,
                f"{operation} source inspection edited the conflict",
            )

            fixture.write("conflict.txt", resolution)
            fixture.git("add", "--", "conflict.txt")
            staged_diff = fixture.git(
                "diff", "--cached", "--binary", "--"
            ).stdout
            staged_names = set(
                fixture.git("diff", "--cached", "--name-only", "--").stdout.splitlines()
            )
            expect(
                staged_names == {"conflict.txt", "staged.txt"},
                f"{operation} staged an unrelated unstaged or untracked path",
            )
            expect(
                side_two.strip() in staged_diff
                and side_three.strip() in staged_diff
                and baseline["staged"].strip() in staged_diff,
                f"{operation} staged-diff evidence is incomplete",
            )
            assert_unrelated_work_preserved(fixture, baseline)

            # Keep pre-existing unrelated state out of the operation commit.
            # The fixture snapshots stand outside the disposable repository.
            fixture.git(
                "restore",
                "--source=HEAD",
                "--staged",
                "--worktree",
                "--",
                "staged.txt",
                "unstaged.txt",
            )
            (fixture.repo / "untracked.txt").unlink()
            expect(
                set(
                    fixture.git(
                        "diff", "--cached", "--name-only", "--"
                    ).stdout.splitlines()
                )
                == {"conflict.txt"},
                f"{operation} continuation index contains unrelated work",
            )

            fixture.git(operation, "--continue")
            expect(
                "in progress" not in fixture.git("status").stdout.lower(),
                f"{operation} operation did not complete",
            )
            expect(
                set(
                    fixture.git(
                        "show", "--format=", "--name-only", "HEAD"
                    ).stdout.splitlines()
                )
                == {"conflict.txt"},
                f"{operation} commit included unrelated work",
            )

            fixture.write("staged.txt", baseline["staged"])
            fixture.git("add", "--", "staged.txt")
            fixture.write("unstaged.txt", baseline["unstaged"])
            fixture.write("untracked.txt", baseline["untracked"])
            assert_unrelated_work_preserved(fixture, baseline)


def check_standalone_marker_cleanup_evidence() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary, standalone_marker=True)
        baseline = seed_unrelated_work(fixture)
        original_head = fixture.git("rev-parse", "HEAD").stdout.strip()
        marker_text = (fixture.repo / "standalone.txt").read_text()
        for source_intent in ("local intent", "incoming intent"):
            expect(
                source_intent in marker_text,
                f"standalone marker lost {source_intent}",
            )

        fixture.write("standalone.txt", "local intent\nincoming intent\n")
        fixture.git("add", "--", "standalone.txt")
        staged_diff = fixture.git(
            "diff", "--cached", "--binary", "--"
        ).stdout
        staged_names = set(
            fixture.git("diff", "--cached", "--name-only", "--").stdout.splitlines()
        )
        expect(
            staged_names == {"standalone.txt", "staged.txt"},
            "standalone cleanup staged unrelated unstaged or untracked work",
        )
        cleaned = (fixture.repo / "standalone.txt").read_text()
        expect(
            "<<<<<<<" not in cleaned
            and "=======" not in cleaned
            and ">>>>>>>" not in cleaned
            and "-<<<<<<< local" in staged_diff
            and "local intent" in staged_diff
            and "incoming intent" in staged_diff,
            "standalone staged diff does not prove marker cleanup",
        )
        expect(
            fixture.git("rev-parse", "HEAD").stdout.strip() == original_head,
            "standalone cleanup invented a commit",
        )
        expect(
            fixture.git("rev-parse", "--verify", "MERGE_HEAD", check=False).returncode
            != 0,
            "standalone cleanup invented a merge operation",
        )
        assert_unrelated_work_preserved(fixture, baseline)


def main() -> None:
    check_hitl_answer_validation_and_verdicts()
    check_shortest_practical_diagnosis_loop_contract()
    check_merge_resolution_contract()
    check_active_merge_and_rebase_evidence()
    check_standalone_marker_cleanup_evidence()
    print("diagnosis and merge safety tests ok")


if __name__ == "__main__":
    main()
