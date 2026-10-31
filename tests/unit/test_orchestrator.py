"""Unit tests for Phase 5: Central Scheduler, Dispatcher, and Orchestrator execution loop."""

import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories import (
    ProjectRepository,
    TaskRepository,
    ExecutionRepository,
    EventRepository,
    ArtifactRepository,
    ResourceRepository,
)
from agy_mas.workspace.workspace_manager import WorkspaceManager
from agy_mas.resources.quota_tracker import QuotaTracker
from agy_mas.agents.base import (
    AgentRuntimeAdapter,
    RuntimeCapabilities,
    Invocation,
    RuntimeEvent,
    FailureClassification,
)
from agy_mas.core.orchestrator import Orchestrator


class MockAdapter(AgentRuntimeAdapter):
    """Mock adapter producing predetermined exit codes and messages."""

    def __init__(self, outcomes=None):
        self.outcomes = outcomes or {}  # task_id -> (exit_code, stdout, stderr)

    def validate_runtime(self) -> RuntimeCapabilities:
        return RuntimeCapabilities("mock", "1.0")

    def build_invocation(self, task_contract, execution_record, policy=None):
        tid = task_contract["task_id"]
        outcome = self.outcomes.get(tid, (0, "Mock success", ""))
        # Construct a python one-liner executing this outcome
        code = f"import sys; print({repr(outcome[1])}); sys.stderr.write({repr(outcome[2])}); sys.exit({outcome[0]})"
        return Invocation(
            command_args=[sys.executable, "-c", code],
            cwd=policy.get("workspace_root") if policy else None,
            timeout_seconds=5,
        )

    def parse_line(self, line: str):
        if "QUOTA" in line:
            return RuntimeEvent("QUOTA_EXHAUSTED", "2026-10-31T00:00:00Z", error_type="QUOTA_EXHAUSTED")
        return RuntimeEvent("OUTPUT", "2026-10-31T00:00:00Z", message=line)

    def classify_failure(self, exit_code, stdout_tail, stderr_tail, events=None):
        if "QUOTA" in stdout_tail or "QUOTA" in stderr_tail:
            return FailureClassification("QUOTA_EXHAUSTED", retryable=True, cooldown_required=True, reason="Quota exceeded")
        return FailureClassification("FAILED", retryable=False, cooldown_required=False, reason="Mock failed")


class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.temp_dir).resolve()

        self.db = Database(":memory:")
        MigrationRunner(self.db).run_all()

        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)
        self.execution_repo = ExecutionRepository(self.db)
        self.event_repo = EventRepository(self.db)
        self.artifact_repo = ArtifactRepository(self.db)
        self.resource_repo = ResourceRepository(self.db)

        self.workspace_mgr = WorkspaceManager(str(self.workspace_root), self.resource_repo, self.artifact_repo)
        self.quota_tracker = QuotaTracker(self.resource_repo)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_orchestrator_two_task_dag_execution(self):
        # Create project and DAG: Task A -> Task B
        self.project_repo.create("p1", "Test DAG", "Run tasks", str(self.workspace_root), status="RUNNING")
        self.task_repo.create("task-a", "p1", "Task A", "Produce artifact A")
        self.task_repo.create("task-b", "p1", "Task B", "Consume artifact A", depends_on=["task-a"])

        adapter = MockAdapter(outcomes={
            "task-a": (0, "A finished", ""),
            "task-b": (0, "B finished", ""),
        })

        orchestrator = Orchestrator(
            self.project_repo,
            self.task_repo,
            self.execution_repo,
            self.event_repo,
            self.artifact_repo,
            self.resource_repo,
            self.workspace_mgr,
            adapter,
            self.quota_tracker,
        )

        # Tick 1: Task A is scheduled and dispatched (Task B is blocked)
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertIn("task-a", [v[0] for v in orchestrator.active_executions.values()])
        self.assertEqual(self.task_repo.get("task-a")["status"], "RUNNING")
        self.assertEqual(self.task_repo.get("task-b")["status"], "PENDING")

        # Wait for Task A process to finish
        for _, proc, _, _, _ in orchestrator.active_executions.values():
            proc.wait(timeout_seconds=5)

        # Tick 2: Task A finishes -> transitions to ACCEPTED -> Task B becomes READY and gets dispatched
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-a")["status"], "ACCEPTED")
        self.assertIn("task-b", [v[0] for v in orchestrator.active_executions.values()])

        # Wait for Task B process to finish
        for _, proc, _, _, _ in orchestrator.active_executions.values():
            proc.wait(timeout_seconds=5)

        # Tick 3: Task B finishes -> transitions to ACCEPTED -> Project COMPLETED
        res = orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-b")["status"], "ACCEPTED")
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(self.project_repo.get("p1")["status"], "COMPLETED")

    def test_orchestrator_quota_failover_to_alternative_account(self):
        self.project_repo.create("p2", "Quota Test", "Test failover", str(self.workspace_root), status="RUNNING")
        self.task_repo.create("task-q", "p2", "Task Q", "Triggers quota", task_spec={"max_retries": 2})

        # First attempt on acc-1 will fail with QUOTA
        adapter = MockAdapter(outcomes={
            "task-q": (1, "QUOTA_EXHAUSTED: Daily limit hit", ""),
        })

        orchestrator = Orchestrator(
            self.project_repo,
            self.task_repo,
            self.execution_repo,
            self.event_repo,
            self.artifact_repo,
            self.resource_repo,
            self.workspace_mgr,
            adapter,
            self.quota_tracker,
        )

        # Tick 1: Dispatched to acc-1
        orchestrator.tick("p2", available_accounts=["acc-1", "acc-2"])
        for _, proc, _, _, _ in orchestrator.active_executions.values():
            proc.wait(timeout_seconds=5)

        # Wait for first attempt on acc-1 to finish
        for _, proc, _, _, _ in orchestrator.active_executions.values():
            proc.wait(timeout_seconds=5)

        # Set outcome for acc-2 attempt to succeed
        adapter.outcomes["task-q"] = (0, "Succeeded on second account", "")

        # Tick 2: Execution fails with QUOTA -> acc-1 put in cooldown -> auto-failover schedules acc-2 immediately!
        orchestrator.tick("p2", available_accounts=["acc-1", "acc-2"])
        self.assertTrue(self.resource_repo.is_in_cooldown("acc-1", "gemini-3.8-flash"))

        # Task is immediately rescheduled to acc-2
        active_vals = list(orchestrator.active_executions.values())
        self.assertEqual(len(active_vals), 1)
        self.assertEqual(active_vals[0][3], "acc-2")  # Account is acc-2!
        self.assertEqual(self.task_repo.get("task-q")["status"], "RUNNING")

        for _, proc, _, _, _ in orchestrator.active_executions.values():
            proc.wait(timeout_seconds=5)

        # Tick 3: Accepted on acc-2
        orchestrator.tick("p2", available_accounts=["acc-1", "acc-2"])
        self.assertEqual(self.task_repo.get("task-q")["status"], "ACCEPTED")


if __name__ == "__main__":
    unittest.main()
