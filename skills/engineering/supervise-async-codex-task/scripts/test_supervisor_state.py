#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("supervisor_state.py")


class SupervisorStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.environment = {**os.environ, "XDG_STATE_HOME": self.temporary.name}

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_command(self, *arguments: str) -> dict:
        result = subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            check=True,
            capture_output=True,
            text=True,
            env=self.environment,
        )
        return json.loads(result.stdout)

    def run_with_explicit_root(self, *arguments: str) -> dict:
        explicit_root = Path(self.temporary.name) / "explicit"
        result = subprocess.run(
            ["python3", str(SCRIPT), "--state-root", str(explicit_root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            env=os.environ,
        )
        return json.loads(result.stdout)

    def initialize(self) -> None:
        self.run_command(
            "init",
            "test-run",
            "--executor-thread",
            "thread-1",
            "--repository",
            "owner/repo",
            "--objective",
            "Finish issue",
            "--automation-id",
            "heartbeat-1",
        )

    def test_unchanged_observation_avoids_detail_read(self) -> None:
        self.initialize()
        arguments = (
            "observe",
            "test-run",
            "--phase",
            "implementing",
            "--executor-status",
            "active",
            "--event-sequence",
            "3",
            "--sha",
            "abc",
            "--activity-class",
            "normal",
        )
        first = self.run_command(*arguments)
        second = self.run_command(*arguments)
        self.assertTrue(first["changed"])
        self.assertFalse(second["changed"])
        self.assertFalse(second["should_read_details"])

    def test_activity_class_controls_recommendation(self) -> None:
        self.initialize()
        result = self.run_command(
            "observe",
            "test-run",
            "--phase",
            "testing",
            "--executor-status",
            "active",
            "--activity-class",
            "heavy",
        )
        self.assertEqual(result["recommended_interval_seconds"], 1200)

    def test_metrics_record_reads_and_interventions(self) -> None:
        self.initialize()
        self.run_command(
            "observe",
            "test-run",
            "--phase",
            "reviewing",
            "--executor-status",
            "active",
            "--activity-class",
            "normal",
            "--full-read",
            "--intervention",
        )
        state = self.run_command("show", "test-run")
        self.assertEqual(state["metrics"]["full_reads"], 1)
        self.assertEqual(state["metrics"]["interventions"], 1)

    def test_finish_and_improvement_are_persisted(self) -> None:
        self.initialize()
        self.run_command(
            "record-improvement",
            "test-run",
            "--skill",
            "orchestrate-issue-queue",
            "--summary",
            "Batch reviewer findings",
            "--evidence",
            "Two redundant correction rounds",
            "--risk",
            "low",
        )
        self.run_command("finish", "test-run", "--outcome", "blocked", "--summary", "Needs decision")
        state = self.run_command("show", "test-run")
        self.assertEqual(state["status"], "blocked")
        self.assertEqual(len(state["improvements"]), 1)

    def test_explicit_state_root_is_supported(self) -> None:
        result = self.run_with_explicit_root(
            "init",
            "explicit-run",
            "--executor-thread",
            "thread-2",
            "--repository",
            "owner/repo",
            "--objective",
            "Finish issue",
            "--automation-id",
            "heartbeat-2",
        )
        self.assertEqual(result["status"], "active")


if __name__ == "__main__":
    unittest.main()
