"""Unit tests for Phase 3: AGY Adapter, Process Manager, and Quota Tracker."""

import unittest
import sys
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories.resource_repo import ResourceRepository
from agy_mas.agents.adapters.agy_adapter import AGYAdapter
from agy_mas.agents.base import RuntimeEvent
from agy_mas.agents.process_manager import ManagedProcess, Invocation
from agy_mas.resources.quota_tracker import QuotaTracker


class TestAGYAdapterAndQuota(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        MigrationRunner(self.db).run_all()
        self.resource_repo = ResourceRepository(self.db)
        self.quota_tracker = QuotaTracker(self.resource_repo)
        self.adapter = AGYAdapter(agy_cmd_path="agy")

    def tearDown(self):
        self.db.close()

    def test_build_invocation_flags(self):
        task_contract = {
            "task_id": "t1",
            "title": "Build Module",
            "description": "Create files",
            "permission_profile": {"dangerously_skip_permissions": False},
            "timeout_seconds": 600,
        }
        execution_record = {
            "execution_id": "exec-1",
            "model": "claude-sonnet-4-6",
        }
        policy = {"output_format": "stream-json", "workspace_root": "C:/ws"}

        inv = self.adapter.build_invocation(task_contract, execution_record, policy)
        self.assertIn("-p", inv.command_args)
        self.assertIn("--output-format", inv.command_args)
        self.assertIn("stream-json", inv.command_args)
        self.assertIn("--model", inv.command_args)
        self.assertIn("claude-sonnet-4-6", inv.command_args)
        self.assertNotIn("--dangerously-skip-permissions", inv.command_args)
        self.assertEqual(inv.cwd, "C:/ws")

        # Now test opt-in dangerously_skip_permissions
        task_contract["permission_profile"]["dangerously_skip_permissions"] = True
        inv2 = self.adapter.build_invocation(task_contract, execution_record, policy)
        self.assertIn("--dangerously-skip-permissions", inv2.command_args)

    def test_stream_json_line_parsing(self):
        line = '{"type": "tool_call", "tool": "write_file", "args": {"path": "test.py"}}'
        ev = self.adapter.parse_line(line)
        self.assertIsNotNone(ev)
        self.assertEqual(ev.event_type, "tool_call")
        self.assertEqual(ev.structured_payload["tool"], "write_file")

    def test_failure_classification(self):
        # 1. Structured quota takes precedence
        ev = RuntimeEvent(
            event_type="QUOTA_EXHAUSTED",
            timestamp="2026-10-31T00:00:00Z",
            error_type="QUOTA_EXHAUSTED",
        )
        cls_res = self.adapter.classify_failure(
            exit_code=1,
            stdout_tail="Random output",
            stderr_tail="Random error",
            events=[ev],
        )
        self.assertEqual(cls_res.error_type, "QUOTA_EXHAUSTED")
        self.assertTrue(cls_res.retryable)
        self.assertTrue(cls_res.cooldown_required)
        self.assertEqual(cls_res.evidence_source, "structured")

        # 2. Permission soft-denial in headless mode
        cls_perm = self.adapter.classify_failure(
            exit_code=0,
            stdout_tail="Permission denied for tool edit_file",
            stderr_tail="",
        )
        self.assertEqual(cls_perm.error_type, "PERMISSION_SOFT_DENIED")
        self.assertFalse(cls_perm.retryable)

        # 3. Windows file busy
        cls_busy = self.adapter.classify_failure(
            exit_code=1,
            stdout_tail="WinError 32: The process cannot access the file because it is being used by another process",
            stderr_tail="",
        )
        self.assertEqual(cls_busy.error_type, "FILE_BUSY")
        self.assertTrue(cls_busy.retryable)

    def test_quota_tracker_account_model_cooldown(self):
        self.assertTrue(self.quota_tracker.is_available("acc-1", "gemini-2.5-pro"))

        # Put acc-1 in cooldown for gemini-2.5-pro
        self.quota_tracker.record_quota_exhaustion("acc-1", "gemini-2.5-pro", retry_after_seconds=3600)

        # acc-1 is now unavailable for gemini-2.5-pro, but still available for other models
        self.assertFalse(self.quota_tracker.is_available("acc-1", "gemini-2.5-pro"))
        self.assertTrue(self.quota_tracker.is_available("acc-1", "claude-sonnet-4-6"))

        # Select eligible account among candidates
        eligible = self.quota_tracker.select_eligible_account(
            model_key="gemini-2.5-pro",
            candidate_accounts=["acc-1", "acc-2", "acc-3"],
        )
        self.assertEqual(eligible, "acc-2")

    def test_managed_process_execution(self):
        # Run a simple python echo command to verify process supervisor
        cmd = [sys.executable, "-c", "import sys; print('MAS Process OK'); sys.stderr.write('No errors\\n')"]
        inv = Invocation(command_args=cmd, timeout_seconds=10)
        proc = ManagedProcess(inv)
        proc.start()
        code = proc.wait(timeout_seconds=5)
        self.assertEqual(code, 0)
        self.assertIn("MAS Process OK", proc.stdout_lines)
        self.assertIn("No errors", proc.stderr_lines)


if __name__ == "__main__":
    unittest.main()
