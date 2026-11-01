"""Unit tests for Phase 6: Pair-Programming Architecture (Coder <-> Reviewer)."""

import unittest
import tempfile
import shutil
import sys
import time
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
    ReviewRepository,
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
from agy_mas.agents.adapters.agy_adapter import AGYAdapter
from agy_mas.agents.review_engine import ReviewEngine
from agy_mas.planning.plan_schema import TaskContract, ReviewReport, ReviewVerdict
from agy_mas.core.orchestrator import Orchestrator
from agy_mas.core.state_machine import TaskState


class MockPairAdapter(AgentRuntimeAdapter):
    def __init__(self, outcomes=None):
        self.outcomes = outcomes or {}
        self.captured_prompts = []

    def validate_runtime(self) -> RuntimeCapabilities:
        return RuntimeCapabilities("mock", "1.0")

    def build_invocation(self, task_contract, execution_record, policy=None):
        tid = task_contract["task_id"]
        outcome = self.outcomes.get(tid, (0, "Mock success", ""))
        code = f"import sys; print({repr(outcome[1])}); sys.stderr.write({repr(outcome[2])}); sys.exit({outcome[0]})"
        return Invocation(
            command_args=[sys.executable, "-c", code],
            cwd=policy.get("workspace_root") if policy else None,
            timeout_seconds=5,
        )

    def parse_line(self, line: str):
        return RuntimeEvent("OUTPUT", "2026-10-31T00:00:00Z", message=line)

    def classify_failure(self, exit_code, stdout_tail, stderr_tail, events=None):
        return FailureClassification("FAILED", retryable=False, cooldown_required=False, reason="Mock failed")


class TestPairProgramming(unittest.TestCase):
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
        self.review_repo = ReviewRepository(self.db)

        self.workspace_mgr = WorkspaceManager(str(self.workspace_root), self.resource_repo, self.artifact_repo)
        self.quota_tracker = QuotaTracker(self.resource_repo)
        self.project_repo.create("p1", "Pair Prog Test", "Goal", str(self.workspace_root), status="RUNNING")

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pair_programming_approval_flow(self):
        """Coder exits with 0, Reviewer approves immediately -> Task becomes ACCEPTED."""
        task_spec = {
            "enable_pair_review": True,
            "max_pair_rounds": 3,
            "outputs": {"expected_artifacts": []},
        }
        self.task_repo.create("task-app", "p1", "Task Approved", "Desc", task_spec=task_spec)

        adapter = MockPairAdapter({"task-app": (0, "Coder done", "")})
        events_emitted = []

        def custom_reviewer(contract_dict, timeout):
            return ReviewReport(
                verdict=ReviewVerdict.APPROVED,
                score=92,
                critique_summary="Clean implementation with good style.",
                actionable_feedback=[],
            )

        review_engine = ReviewEngine(str(self.workspace_root), reviewer_runner=custom_reviewer)
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
            on_event=lambda t, d: events_emitted.append((t, d)),
            review_engine=review_engine,
            review_repo=self.review_repo,
        )

        # Tick 1: Dispatch Coder
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-app")["status"], "RUNNING")
        time.sleep(0.3)

        # Tick 2: Coder process finishes, Reviewer evaluates and APPROVES
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-app")["status"], "ACCEPTED")

        # Verify review recorded in review_repo
        reviews = self.review_repo.list_by_task("task-app")
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["verdict"], "APPROVED")
        self.assertEqual(reviews[0]["score"], 92)

        # Verify telemetry
        event_types = [e[0] for e in events_emitted]
        self.assertIn("PAIR_REVIEW_STARTED", event_types)
        self.assertIn("PAIR_REVIEW_APPROVED", event_types)
        self.assertIn("TASK_ACCEPTED", event_types)

    def test_pair_programming_feedback_loop_retry(self):
        """Round 1: Reviewer rejects -> RETRY_WAIT -> Decoupled promotion to READY -> Round 2: feedback injected -> APPROVED."""
        task_spec = {
            "enable_pair_review": True,
            "max_pair_rounds": 3,
            "retry_delay_seconds": 0,  # immediate backoff for test speed
            "outputs": {"expected_artifacts": []},
        }
        self.task_repo.create("task-retry", "p1", "Task Retry", "Desc", task_spec=task_spec)

        adapter = MockPairAdapter({"task-retry": (0, "Coder done", "")})
        review_counter = [0]

        def dynamic_reviewer(contract_dict, timeout):
            review_counter[0] += 1
            if review_counter[0] == 1:
                return ReviewReport(
                    verdict=ReviewVerdict.CHANGES_REQUESTED,
                    score=45,
                    critique_summary="Missing edge-case check for zero division",
                    actionable_feedback=["Add if x == 0 check at line 15"],
                )
            else:
                return ReviewReport(
                    verdict=ReviewVerdict.APPROVED,
                    score=95,
                    critique_summary="Defect resolved properly",
                    actionable_feedback=[],
                )

        review_engine = ReviewEngine(str(self.workspace_root), reviewer_runner=dynamic_reviewer)
        events_emitted = []

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
            on_event=lambda t, d: events_emitted.append((t, d)),
            review_engine=review_engine,
            review_repo=self.review_repo,
        )

        # Tick 1: Dispatch Round 1
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-retry")["status"], "RUNNING")
        time.sleep(0.3)

        # Tick 2: Round 1 ends -> Reviewer rejects -> RETRY_WAIT
        orchestrator.tick("p1", available_accounts=["acc-1"])
        task_row = self.task_repo.get("task-retry")
        self.assertEqual(task_row["status"], "RETRY_WAIT")
        self.assertEqual(task_row["pair_round"], 1)
        self.assertIsNotNone(task_row["last_critique"])
        self.assertIn("zero division", task_row["last_critique"]["critique_summary"])

        # Check execution status was marked properly
        execs = self.execution_repo.list_by_task("task-retry")
        self.assertEqual(len(execs), 1)
        self.assertEqual(execs[0]["normalized_outcome"], "CHANGES_REQUESTED")
        self.assertIsNotNone(execs[0]["finished_at"])

        # Tick 3: Decoupled promotion moves RETRY_WAIT -> READY and immediately dispatches Round 2
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-retry")["status"], "RUNNING")
        time.sleep(0.3)

        # Tick 4: Round 2 ends -> Reviewer approves -> ACCEPTED
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-retry")["status"], "ACCEPTED")

        reviews = self.review_repo.list_by_task("task-retry")
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0]["verdict"], "CHANGES_REQUESTED")
        self.assertEqual(reviews[1]["verdict"], "APPROVED")

    def test_pair_programming_circuit_breaker(self):
        """Exhausting max_pair_rounds trips Circuit Breaker and marks task FAILED."""
        task_spec = {
            "enable_pair_review": True,
            "max_pair_rounds": 2,
            "retry_delay_seconds": 0,
            "outputs": {"expected_artifacts": []},
        }
        self.task_repo.create("task-cb", "p1", "Task CB", "Desc", task_spec=task_spec)

        adapter = MockPairAdapter({"task-cb": (0, "Coder done", "")})

        def always_reject(contract_dict, timeout):
            return ReviewReport(
                verdict=ReviewVerdict.CHANGES_REQUESTED,
                score=30,
                critique_summary="Persistent failure",
                actionable_feedback=["Fix syntax error"],
            )

        review_engine = ReviewEngine(str(self.workspace_root), reviewer_runner=always_reject)
        events_emitted = []

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
            on_event=lambda t, d: events_emitted.append((t, d)),
            review_engine=review_engine,
            review_repo=self.review_repo,
        )

        # Round 1 dispatch & review
        orchestrator.tick("p1", available_accounts=["acc-1"])
        time.sleep(0.3)
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-cb")["status"], "RETRY_WAIT")

        # Round 2 dispatch & review
        orchestrator.tick("p1", available_accounts=["acc-1"])
        self.assertEqual(self.task_repo.get("task-cb")["status"], "RUNNING")
        time.sleep(0.3)
        orchestrator.tick("p1", available_accounts=["acc-1"])

        # Tripped circuit breaker
        self.assertEqual(self.task_repo.get("task-cb")["status"], "FAILED")
        event_types = [e[0] for e in events_emitted]
        self.assertIn("PAIR_REVIEW_EXHAUSTED", event_types)

    def test_pair_programming_reviewer_fault_tolerance(self):
        """Reviewer crashes or times out -> Orchestrator catches error, handles safely and sets RETRY_WAIT."""
        task_spec = {
            "enable_pair_review": True,
            "max_pair_rounds": 3,
            "outputs": {"expected_artifacts": []},
        }
        self.task_repo.create("task-crash", "p1", "Task Crash", "Desc", task_spec=task_spec)
        adapter = MockPairAdapter({"task-crash": (0, "Coder done", "")})

        def crashing_reviewer(contract_dict, timeout):
            raise TimeoutError("Reviewer process timed out after 180s")

        review_engine = ReviewEngine(str(self.workspace_root), reviewer_runner=crashing_reviewer)
        events_emitted = []

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
            on_event=lambda t, d: events_emitted.append((t, d)),
            review_engine=review_engine,
            review_repo=self.review_repo,
        )

        orchestrator.tick("p1", available_accounts=["acc-1"])
        time.sleep(0.3)
        orchestrator.tick("p1", available_accounts=["acc-1"])

        # Handled safely into RETRY_WAIT
        self.assertEqual(self.task_repo.get("task-crash")["status"], "RETRY_WAIT")
        event_types = [e[0] for e in events_emitted]
        self.assertIn("PAIR_REVIEW_ERROR", event_types)

        execs = self.execution_repo.list_by_task("task-crash")
        self.assertEqual(execs[0]["normalized_outcome"], "REVIEW_ERROR")

    def test_agy_adapter_feedback_prompt_injection(self):
        """Tests that AGYAdapter injects reviewer critique into prompt on retry."""
        adapter = AGYAdapter("agy")
        contract = {
            "task_id": "t-1",
            "title": "Compute Factorial",
            "description": "Implement factorial in python",
            "pair_round": 1,
            "last_review_report": {
                "critique_summary": "Fails for negative integers and 0",
                "actionable_feedback": [
                    "Handle n <= 0 with ValueError",
                    "Add return 1 for n == 0",
                ],
            },
        }
        exec_record = {"execution_id": "exec-2", "execution_role": "PRIMARY"}
        inv = adapter.build_invocation(contract, exec_record)
        prompt_arg = inv.command_args[inv.command_args.index("-p") + 1]

        self.assertIn("FEEDBACK FROM CODE REVIEWER - ROUND #1", prompt_arg)
        self.assertIn("Fails for negative integers and 0", prompt_arg)
        self.assertIn("Handle n <= 0 with ValueError", prompt_arg)
        self.assertIn("Preserve all working logic. Fix ONLY the defects listed above.", prompt_arg)


if __name__ == "__main__":
    unittest.main()
