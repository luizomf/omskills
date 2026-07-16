#!/usr/bin/env python3
"""Regression tests for the issue queue state machine."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("run_state.py")
SHA_ONE = "1" * 40
SHA_TWO = "2" * 40
STALE_SHA = "f" * 40


class RunStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.state_root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_command(self, *arguments: str, succeeds: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--state-root", str(self.state_root), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
        if succeeds and result.returncode != 0:
            self.fail(f"Command failed: {result.stderr}")
        if not succeeds and result.returncode == 0:
            self.fail("Command unexpectedly succeeded")
        return result

    def state(self, run_id: str = "audit") -> dict:
        return json.loads(self.run_command("show", run_id).stdout)

    def initialize_dual_run(self) -> None:
        self.run_command(
            "init",
            "audit",
            "--repository",
            "owner/repo",
            "--goal",
            "Merge and close every issue",
            "--issues",
            "143",
            "144",
            "--review-policy",
            "dual",
            "--max-corrections",
            "1",
        )

    def deliver_first_implementation(self) -> None:
        self.run_command("record-preflight", "audit", "143")
        self.run_command("dispatch-implementation", "audit", "143", "--agent-id", "writer-1")
        self.run_command(
            "deliver",
            "audit",
            "143",
            "--branch",
            "fix/143",
            "--pr",
            "147",
            "--sha",
            SHA_ONE,
            "--agent-id",
            "writer-1",
        )

    def dispatch_reviewers(self, sha: str, round_number: int) -> None:
        for role in ("adversarial", "standards-spec"):
            self.run_command(
                "dispatch-review",
                "audit",
                "143",
                "--sha",
                sha,
                "--role",
                role,
                "--agent-id",
                f"{role}-{round_number}",
            )

    def test_correction_invalidates_reviews_and_advances_only_after_fresh_passes(self) -> None:
        self.initialize_dual_run()
        self.deliver_first_implementation()
        self.dispatch_reviewers(SHA_ONE, 1)
        self.run_command(
            "record-review",
            "audit",
            "143",
            "--sha",
            SHA_ONE,
            "--role",
            "adversarial",
            "--outcome",
            "passed",
            "--agent-id",
            "adversarial-1",
        )
        self.run_command(
            "record-review",
            "audit",
            "143",
            "--sha",
            SHA_ONE,
            "--role",
            "standards-spec",
            "--outcome",
            "blocked",
            "--blocking-findings",
            "1",
            "--agent-id",
            "standards-spec-1",
        )
        self.run_command("dispatch-correction", "audit", "143", "--agent-id", "writer-2")
        self.run_command("deliver", "audit", "143", "--sha", SHA_TWO, "--agent-id", "writer-2")
        self.dispatch_reviewers(SHA_TWO, 2)

        issue = self.state()["queue"][0]
        self.assertEqual(issue["remote_sha"], SHA_TWO)
        self.assertEqual(issue["review_status"], "pending")
        self.assertEqual(issue["review_rounds"][-1]["results"], {})

        stale_merge = self.run_command(
            "mark-merged", "audit", "143", "--sha", SHA_ONE, "--issue-closed", succeeds=False
        )
        self.assertIn("has not passed", stale_merge.stderr)

        for role in ("adversarial", "standards-spec"):
            self.run_command(
                "record-review",
                "audit",
                "143",
                "--sha",
                SHA_TWO,
                "--role",
                role,
                "--outcome",
                "passed",
                "--agent-id",
                f"{role}-2",
            )
        self.run_command(
            "record-verification",
            "audit",
            "143",
            "--sha",
            SHA_TWO,
            "--outcome",
            "passed",
            "--checks",
            "format",
            "typecheck",
            "test",
            "build",
        )
        self.run_command("mark-merged", "audit", "143", "--sha", SHA_TWO, "--issue-closed")

        state = self.state()
        self.assertEqual(state["active_issue"], "144")
        self.assertEqual(state["queue"][0]["status"], "done")
        self.assertEqual(state["queue"][1]["phase"], "preflight")
        events_path = self.state_root / "audit" / "events.jsonl"
        merge_event = json.loads(events_path.read_text().splitlines()[-1])
        self.assertEqual(merge_event["active_issue"], "143")
        self.assertEqual(merge_event["active_issue_after"], "144")

    def test_review_rejects_a_stale_sha_and_logs_the_rejection(self) -> None:
        self.initialize_dual_run()
        self.deliver_first_implementation()
        self.dispatch_reviewers(SHA_ONE, 1)
        invalid_sha = self.run_command(
            "record-review",
            "audit",
            "143",
            "--sha",
            "not-a-sha",
            "--role",
            "adversarial",
            "--outcome",
            "passed",
            "--agent-id",
            "adversarial-1",
            succeeds=False,
        )
        self.assertIn("Expected a full 40- or 64-character", invalid_sha.stderr)
        result = self.run_command(
            "record-review",
            "audit",
            "143",
            "--sha",
            STALE_SHA,
            "--role",
            "adversarial",
            "--outcome",
            "passed",
            "--agent-id",
            "adversarial-1",
            succeeds=False,
        )
        self.assertIn("differs from current remote SHA", result.stderr)
        events_path = self.state_root / "audit" / "events.jsonl"
        events = [json.loads(line) for line in events_path.read_text().splitlines()]
        self.assertEqual(events[-1]["event"], "transition_rejected")
        self.assertEqual(events[-1]["requested_operation"], "record-review")

    def test_mutations_print_compact_state_and_help_keeps_ranges_compact(self) -> None:
        result = self.run_command(
            "init",
            "compact",
            "--repository",
            "owner/repo",
            "--goal",
            "Close the queue",
            "--issues",
            "1",
        )
        output = json.loads(result.stdout)
        self.assertNotIn("queue", output)
        self.assertEqual(output["active_issue_state"]["next_action"], "perform_preflight")

        help_result = subprocess.run(
            ["python3", str(SCRIPT), "init", "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("0..100", help_result.stdout)
        self.assertNotIn("0,1,2,3,4,5", help_result.stdout)

    def test_second_blocked_round_pauses_for_human_decision(self) -> None:
        self.initialize_dual_run()
        self.deliver_first_implementation()
        self.dispatch_reviewers(SHA_ONE, 1)
        for role in ("adversarial", "standards-spec"):
            self.run_command(
                "record-review",
                "audit",
                "143",
                "--sha",
                SHA_ONE,
                "--role",
                role,
                "--outcome",
                "blocked",
                "--blocking-findings",
                "1",
                "--agent-id",
                f"{role}-1",
            )
        self.run_command("dispatch-correction", "audit", "143", "--agent-id", "writer-2")
        self.run_command("deliver", "audit", "143", "--sha", SHA_TWO, "--agent-id", "writer-2")
        self.dispatch_reviewers(SHA_TWO, 2)
        for role in ("adversarial", "standards-spec"):
            self.run_command(
                "record-review",
                "audit",
                "143",
                "--sha",
                SHA_TWO,
                "--role",
                role,
                "--outcome",
                "blocked",
                "--blocking-findings",
                "1",
                "--agent-id",
                f"{role}-2",
            )

        state = self.state()
        issue = state["queue"][0]
        self.assertEqual(state["goal_status"], "paused")
        self.assertEqual(issue["awaiting"], "human_decision")
        self.assertEqual(issue["next_action"], "request_human_decision")

        self.run_command(
            "authorize-correction",
            "audit",
            "143",
            "--additional-attempts",
            "1",
        )
        authorized_state = self.state()
        authorized_issue = authorized_state["queue"][0]
        self.assertEqual(authorized_state["max_correction_attempts"], 2)
        self.assertEqual(authorized_state["goal_status"], "paused")
        self.assertEqual(authorized_issue["next_action"], "dispatch_corrector")

    def test_human_can_resume_review_blocked_run_without_enabling_goal_mode(self) -> None:
        self.initialize_dual_run()
        self.deliver_first_implementation()
        self.dispatch_reviewers(SHA_ONE, 1)
        for role in ("adversarial", "standards-spec"):
            self.run_command(
                "record-review",
                "audit",
                "143",
                "--sha",
                SHA_ONE,
                "--role",
                role,
                "--outcome",
                "blocked",
                "--blocking-findings",
                "1",
                "--agent-id",
                f"{role}-1",
            )
        self.run_command("block-run", "audit", "143", "--reason", "awaiting human direction")

        self.run_command(
            "authorize-correction",
            "audit",
            "143",
            "--additional-attempts",
            "1",
        )

        state = self.state()
        issue = state["queue"][0]
        self.assertEqual(state["status"], "active")
        self.assertEqual(state["goal_status"], "none")
        self.assertEqual(state["max_correction_attempts"], 2)
        self.assertEqual(issue["status"], "active")
        self.assertEqual(issue["phase"], "reviewing")
        self.assertEqual(issue["next_action"], "dispatch_corrector")


if __name__ == "__main__":
    unittest.main()
