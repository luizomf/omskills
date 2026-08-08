#!/usr/bin/env python3
"""Disposable Git checks for the code-review candidate contract."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CODE_REVIEW = (ROOT / "skills/engineering/code-review/SKILL.md").read_text()
IMPLEMENT = (ROOT / "skills/engineering/implement/SKILL.md").read_text()
ORCHESTRATE = (ROOT / "skills/engineering/orchestrate/SKILL.md").read_text()
FIXTURE = json.loads(
    (ROOT / "tests/fixtures/code-review-candidates.json").read_text()
)
SHELL_FRAGMENT_TOKENS = (";", "&", "|", "`", "$(", "<", ">")


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


@dataclass
class GitFixture:
    root: Path
    repo: Path
    environment: dict[str, str]

    @classmethod
    def create(cls, temporary: str) -> "GitFixture":
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
        }
        fixture = cls(root=root, repo=repo, environment=environment)
        fixture.git("init", "--quiet", "--initial-branch=main")
        fixture.git("config", "user.name", "Fixture User")
        fixture.git("config", "user.email", "fixture@example.invalid")
        fixture.write("base.txt", b"base\n")
        fixture.git("add", "--", "base.txt")
        fixture.git("commit", "--quiet", "-m", "base")
        return fixture

    def git(
        self, *arguments: str, check: bool = True
    ) -> subprocess.CompletedProcess[bytes]:
        result = subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            env=self.environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            shell=False,
        )
        if check and result.returncode != 0:
            raise AssertionError(
                f"git {' '.join(arguments)} failed: "
                f"{result.stderr.decode(errors='replace')}"
            )
        return result

    def write(self, relative: str, content: bytes) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def commit_all(self, message: str) -> None:
        self.git("add", "--all", "--")
        self.git("commit", "--quiet", "-m", message)


class RejectedRef(ValueError):
    pass


def resolve_commit(fixture: GitFixture, value: str) -> str:
    """Model the documented safe fixed-point boundary with a real Git call."""

    if (
        not value
        or value.startswith("-")
        or any(character.isspace() or ord(character) < 32 for character in value)
        or any(token in value for token in SHELL_FRAGMENT_TOKENS)
    ):
        raise RejectedRef(value)
    result = fixture.git(
        "rev-parse",
        "--verify",
        "--end-of-options",
        f"{value}^{{commit}}",
        check=False,
    )
    if result.returncode != 0:
        raise RejectedRef(value)
    resolved = result.stdout.decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-fA-F]+", resolved):
        raise RejectedRef(value)
    return resolved


def committed_candidate(fixture: GitFixture, fixed_point: str) -> dict[str, Any]:
    base = resolve_commit(fixture, fixed_point)
    head = resolve_commit(fixture, "HEAD")
    diff = fixture.git(
        "diff",
        "--no-ext-diff",
        "--binary",
        f"{base}...{head}",
        "--",
    ).stdout
    log = fixture.git("log", "--oneline", f"{base}..{head}", "--").stdout
    return {
        "mode": "committed",
        "base": base,
        "head": head,
        "diff": diff,
        "log": log,
        "empty": not diff,
    }


def wip_candidate(fixture: GitFixture) -> dict[str, Any]:
    staged = fixture.git(
        "diff", "--no-ext-diff", "--binary", "--cached", "--"
    ).stdout
    unstaged = fixture.git(
        "diff", "--no-ext-diff", "--binary", "--"
    ).stdout
    raw_paths = fixture.git(
        "ls-files", "--others", "--exclude-standard", "-z", "--"
    ).stdout
    untracked: list[dict[str, Any]] = []
    limitations: list[str] = []
    for raw_path in filter(None, raw_paths.split(b"\0")):
        path = os.fsdecode(raw_path)
        patch = fixture.git(
            "diff",
            "--no-index",
            "--no-ext-diff",
            "--binary",
            "--",
            os.devnull,
            path,
            check=False,
        )
        if patch.returncode not in {0, 1}:
            limitations.append(path)
            untracked.append({"path": path, "patch": b"", "limited": True})
        else:
            untracked.append(
                {"path": path, "patch": patch.stdout, "limited": False}
            )
    return {
        "mode": "WIP",
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
        "limitations": limitations,
        "empty": not staged and not unstaged and not untracked,
    }


def authority_result(case: dict[str, Any]) -> dict[str, str]:
    claims = {source["claim"] for source in case["sources"]}
    if len(claims) == 1:
        return {"status": "ready", "report": ""}
    evidence = "; ".join(
        f"{source['name']}: {source['claim']}" for source in case["sources"]
    )
    return {
        "status": "conflict",
        "report": f"Material authority conflict for owning authority — {evidence}",
    }


def reviewer_prompt(
    case: dict[str, Any], candidate: bytes, instructions: str
) -> str:
    if "durable_source" in case:
        source = case["durable_source"]
        contract = f"{source['name']}\n{source['content']}"
    else:
        source = case["conversation_contract"]
        contract = "\n".join(
            (
                f"Outcome: {source['outcome']}",
                f"Scope: {source['scope']}",
                f"Deferrals: {source['deferrals']}",
                f"Acceptance criteria: {source['acceptance_criteria']}",
                f"Completion: {source['completion']}",
            )
        )
    return (
        f"Selected mode: {case['mode']}\n"
        f"Repository instructions:\n{instructions}\n"
        f"Accepted behavior:\n{contract}\n"
        f"Complete candidate:\n{candidate.decode(errors='replace')}"
    )


def check_skill_contract() -> None:
    for phrase in (
        "exactly one repository implementation unit",
        "blocked or conflicting set of Tickets",
        "unavailable",
        "inapplicable",
        "skipped",
        "failed",
        "passed",
    ):
        expect(phrase in IMPLEMENT, f"implement contract omits {phrase!r}")
    expect(
        "Run typechecking regularly" not in IMPLEMENT,
        "implement still assumes typechecking and one conventional full suite",
    )

    for phrase in (
        "committed mode",
        "WIP mode",
        "Selected mode",
        "--end-of-options",
        "--no-ext-diff",
        "--binary",
        "--cached",
        "--others --exclude-standard -z",
        "option-like",
        "shell fragment",
        "without dispatching an isolated reviewer",
        "staged",
        "unstaged",
        "untracked",
        "binary",
        "unreadable",
        "Outcome",
        "Deferrals",
        "Acceptance criteria",
        "Completion",
        "parent conversation",
        "materially conflict",
        "owning authority",
    ):
        expect(phrase in CODE_REVIEW, f"code-review contract omits {phrase!r}")
    expect(
        "committed mode" in ORCHESTRATE,
        "orchestrate does not select committed mode for candidate commits",
    )


def check_committed_range_and_empty_candidate() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        base = resolve_commit(fixture, "HEAD")
        fixture.write("committed.txt", b"complete committed range\n")
        fixture.commit_all("committed candidate")
        candidate = committed_candidate(fixture, base)
        expect(candidate["mode"] == "committed", "committed mode was not named")
        expect(not candidate["empty"], "non-empty committed candidate was missed")
        expect(b"committed.txt" in candidate["diff"], "committed diff lost a path")
        expect(
            b"committed candidate" in candidate["log"],
            "committed candidate lost its associated log",
        )

    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        base = resolve_commit(fixture, "HEAD")
        candidate = committed_candidate(fixture, base)
        expect(candidate["empty"], "empty committed candidate was not detected")
        expect(not candidate["log"], "empty committed range unexpectedly has a log")


def check_staged_and_unstaged_candidates() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        fixture.write("base.txt", b"staged content\n")
        fixture.git("add", "--", "base.txt")
        candidate = wip_candidate(fixture)
        expect(candidate["mode"] == "WIP", "WIP mode was not named")
        expect(b"staged content" in candidate["staged"], "staged change was omitted")
        expect(not candidate["unstaged"], "staged fixture leaked into unstaged diff")

    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        fixture.write("base.txt", b"unstaged content\n")
        candidate = wip_candidate(fixture)
        expect(b"unstaged content" in candidate["unstaged"], "unstaged change was omitted")
        expect(not candidate["staged"], "unstaged fixture leaked into staged diff")


def check_untracked_text_binary_and_mixed_wip() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        fixture.write("untracked.txt", b"untracked text\n")
        fixture.write("untracked.bin", b"\x00\xffbinary fixture\x00")
        candidate = wip_candidate(fixture)
        by_path = {entry["path"]: entry for entry in candidate["untracked"]}
        expect(
            set(by_path) == {"untracked.txt", "untracked.bin"},
            "untracked inventory omitted text or binary path",
        )
        expect(
            b"untracked text" in by_path["untracked.txt"]["patch"],
            "untracked text content was omitted",
        )
        expect(
            b"GIT binary patch" in by_path["untracked.bin"]["patch"],
            "untracked binary content was silently omitted",
        )
        expect(not candidate["limitations"], "readable untracked paths were limited")

    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        fixture.write("base.txt", b"staged side\n")
        fixture.git("add", "--", "base.txt")
        fixture.write("base.txt", b"unstaged side\n")
        fixture.write("mixed.txt", b"untracked side\n")
        candidate = wip_candidate(fixture)
        expect(b"staged side" in candidate["staged"], "mixed WIP lost staged state")
        expect(b"unstaged side" in candidate["unstaged"], "mixed WIP lost unstaged state")
        expect(
            [entry["path"] for entry in candidate["untracked"]] == ["mixed.txt"],
            "mixed WIP lost its untracked path",
        )

    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        candidate = wip_candidate(fixture)
        expect(candidate["empty"], "empty WIP candidate was not detected")


def check_untrusted_refs_are_rejected_without_evaluation() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        fixture = GitFixture.create(temporary)
        expect(resolve_commit(fixture, "HEAD") == resolve_commit(fixture, "main"), "valid ref did not resolve")
        for case in FIXTURE["rejected_refs"]:
            try:
                committed_candidate(fixture, str(case["value"]))
            except RejectedRef:
                pass
            else:
                expect(False, f"unsafe ref was accepted: {case['id']}")
        expect(
            not (fixture.repo / "fixture-semicolon").exists()
            and not (fixture.repo / "fixture-substitution").exists()
            and not (fixture.repo / "fixture-ampersand").exists(),
            "shell-fragment literal was evaluated",
        )


def check_authority_conflicts_and_reviewer_contracts() -> None:
    for case in FIXTURE["authority_cases"]:
        result = authority_result(case)
        expect(
            result["status"] == case["expected_status"],
            f"wrong authority result for {case['id']}",
        )
        if result["status"] == "conflict":
            expect(
                "owning authority" in result["report"]
                and "owning authority" in CODE_REVIEW,
                "authority conflict has no escalation owner",
            )
            for source in case["sources"]:
                expect(
                    source["name"] in result["report"]
                    and source["claim"] in result["report"],
                    f"authority conflict omitted evidence from {source['name']}",
                )

    candidate = b"diff --git a/base.txt b/base.txt\n"
    instructions = "AGENTS.md: preserve repository scope."
    for case in FIXTURE["review_contracts"]:
        prompt = reviewer_prompt(case, candidate, instructions)
        for term in case["expected_terms"]:
            expect(term in prompt, f"review prompt {case['id']} omits {term!r}")
        expect(
            f"Selected mode: {case['mode']}" in prompt,
            f"review prompt {case['id']} omits its selected mode",
        )
        expect(instructions in prompt, f"review prompt {case['id']} omits instructions")
        expect(candidate.decode() in prompt, f"review prompt {case['id']} omits candidate")
        if "private_parent_turn" in case:
            expect(
                case["private_parent_turn"] not in prompt,
                "conversation-only prompt exposed a parent turn",
            )


def main() -> None:
    check_skill_contract()
    check_committed_range_and_empty_candidate()
    check_staged_and_unstaged_candidates()
    check_untracked_text_binary_and_mixed_wip()
    check_untrusted_refs_are_rejected_without_evaluation()
    check_authority_conflicts_and_reviewer_contracts()
    print("code-review candidate tests ok")


if __name__ == "__main__":
    main()
