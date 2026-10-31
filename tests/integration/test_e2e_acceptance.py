"""End-to-End Acceptance Test Suite for Multi-Agent System Architecture v1.1.

Verifies:
  - VER-01: Exit code zero with permission denial does not accept task.
  - VER-02: Exit code zero but expected artifact missing fails verification.
  - VER-03: All acceptance criteria pass -> task transitions to ACCEPTED.
  - QUOTA-01: Structured-first quota detection, cooldown per (account, model), and failover.
  - WIN-01: Windows file sharing retry bounds and overcomes transient WinError 32.
  - REC-01: Startup reconciliation detects dead PID and recovers orphaned locks.
"""

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
from agy_mas.workspace.file_lock_manager import WindowsFileRetryManager
from agy_mas.resources.quota_tracker import QuotaTracker
from agy_mas.agents.base import (
    AgentRuntimeAdapter,
    RuntimeCapabilities,
    Invocation,
    RuntimeEvent,
    FailureClassification,
)
from agy_mas.planning.plan_schema import (
    TaskContract,
    OutputScope,
    ExpectedArtifact,
    AcceptanceCriterion,
    PermissionProfile,
)
from agy_mas.verification.verifier import Verifier
from agy_mas.recovery.recovery_manager import RecoveryManager
from agy_mas.core.orchestrator import Orchestrator


class ConfigurableTestAdapter(AgentRuntimeAdapter):
    """Adapter with controllable execution outcomes for acceptance testing."""

    def __init__(self, script_generator=None):
        self.script_generator = script_generator or (lambda tid: "import sys; sys.exit(0)")

    def validate_runtime(self) -> RuntimeCapabilities:
        return RuntimeCapabilities("test_runtime", "1.1")

    def build_invocation(self, task_contract, execution_record, policy=None):
        tid = task_contract["task_id"]
        py_code = self.script_generator(tid)
        return Invocation(
            command_args=[sys.executable, "-c", py_code],
            cwd=policy.get("workspace_root") if policy else None,
            timeout_seconds=10,
        )

    def parse_line(self, line: str):
        if "SOFT_DENIAL" in line:
            return RuntimeEvent("PERMISSION_SOFT_DENIED", "2026-10-31T00:00:00Z", error_type="PERMISSION_SOFT_DENIED")
        if "QUOTA_EXHAUSTED" in line:
            return RuntimeEvent("QUOTA_EXHAUSTED", "2026-10-31T00:00:00Z", error_type="QUOTA_EXHAUSTED")
        return RuntimeEvent("OUTPUT", "2026-10-31T00:00:00Z", message=line)

    def classify_failure(self, exit_code, stdout_tail, stderr_tail, events=None):
        if events:
            for ev in events:
                if ev.error_type == "PERMISSION_SOFT_DENIED":
                    return FailureClassification("PERMISSION_SOFT_DENIED", retryable=False, cooldown_required=False, reason="Soft denial")
                if ev.error_type == "QUOTA_EXHAUSTED":
                    return FailureClassification("QUOTA_EXHAUSTED", retryable=True, cooldown_required=True, reason="Quota exhausted")
        return FailureClassification("UNKNOWN", retryable=False, cooldown_required=False, reason="Unknown failure")


class TestArchitectureV11Acceptance(unittest.TestCase):
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
        self.verifier = Verifier(str(self.workspace_root))
        self.recovery_mgr = RecoveryManager(self.task_repo, self.execution_repo, self.resource_repo, self.event_repo)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_VER_01_exit_zero_with_permission_soft_denial(self):
        """VER-01: Exit code zero with permission soft denial must NOT automatically accept task."""
        contract = TaskContract(
            task_id="ver01_task",
            project_id="proj_ver",
            title="VER-01 Task",
            description="Tests soft denial in headless mode",
            acceptance_criteria=[AcceptanceCriterion("NO_SOFT_DENIAL", "No soft denial allowed")],
        )

        # Simulation: process exited with 0, but stdout contained soft-denial
        report = self.verifier.verify_task(
            contract=contract,
            exit_code=0,
            has_soft_denial=True,
        )
        self.assertFalse(report.passed, "Task must not pass verification when soft denial occurred")
        self.assertIn("Permission soft denial was detected", report.errors[0])

    def test_VER_02_exit_zero_with_missing_artifact(self):
        """VER-02: Exit code zero but expected artifact missing fails verification."""
        contract = TaskContract(
            task_id="ver02_task",
            project_id="proj_ver",
            title="VER-02 Task",
            description="Tests missing output artifact",
            outputs=OutputScope(
                expected_artifacts=[ExpectedArtifact(path="src/generated.py", min_size_bytes=5, required=True)]
            ),
        )

        report = self.verifier.verify_task(
            contract=contract,
            exit_code=0,
            has_soft_denial=False,
        )
        self.assertFalse(report.passed, "Task must fail when expected artifact does not exist")
        self.assertTrue(any("was not found on disk" in e for e in report.errors))

    def test_VER_03_all_acceptance_criteria_pass(self):
        """VER-03: All acceptance criteria and artifacts verified -> ACCEPTED."""
        gen_file = self.workspace_root / "src" / "generated.py"
        gen_file.parent.mkdir(parents=True, exist_ok=True)
        gen_file.write_text("# Generated production code", encoding="utf-8")

        contract = TaskContract(
            task_id="ver03_task",
            project_id="proj_ver",
            title="VER-03 Task",
            description="Tests full acceptance",
            outputs=OutputScope(
                expected_artifacts=[ExpectedArtifact(path="src/generated.py", min_size_bytes=5, required=True)]
            ),
            permission_profile=PermissionProfile(write_paths=["src/*"]),
            acceptance_criteria=[
                AcceptanceCriterion("EXIT_CODE_ZERO", "Exit 0"),
                AcceptanceCriterion("NO_SOFT_DENIAL", "No soft denial"),
            ],
        )

        report = self.verifier.verify_task(
            contract=contract,
            exit_code=0,
            has_soft_denial=False,
            touched_paths=["src/generated.py"],
        )
        self.assertTrue(report.passed, f"Expected verification pass, got: {report.errors}")
        self.assertEqual(report.artifacts_verified, 1)

    def test_QUOTA_01_cooldown_and_failover(self):
        """QUOTA-01: Quota exhaustion initiates (account, model) cooldown and failover."""
        # acc-1 hits quota on gemini-2.5-pro
        until = self.quota_tracker.record_quota_exhaustion("acc-1", "gemini-2.5-pro", retry_after_seconds=3600)
        self.assertTrue(self.quota_tracker.resource_repo.is_in_cooldown("acc-1", "gemini-2.5-pro"))

        # acc-1 should NOT be chosen for gemini-2.5-pro; failover must select acc-2
        selected = self.quota_tracker.select_eligible_account("gemini-2.5-pro", ["acc-1", "acc-2"])
        self.assertEqual(selected, "acc-2")

        # acc-1 is still valid for other models (e.g. claude-sonnet-4-6)
        self.assertTrue(self.quota_tracker.is_available("acc-1", "claude-sonnet-4-6"))

    def test_WIN_01_windows_file_sharing_retry(self):
        """WIN-01: Windows file sharing retry overcomes transient lock contention."""
        retry_mgr = WindowsFileRetryManager()
        counter = [0]

        def transient_locked_read():
            counter[0] += 1
            if counter[0] < 2:
                err = PermissionError("WinError 32: The process cannot access the file because it is being used")
                setattr(err, "winerror", 32)
                raise err
            return "CONTENT_LOADED"

        result = retry_mgr.execute_with_retry(transient_locked_read)
        self.assertEqual(result, "CONTENT_LOADED")
        self.assertEqual(counter[0], 2)

    def test_REC_01_startup_crash_recovery(self):
        """REC-01: Dead worker PID on startup is reconciled, locks freed, task reset to READY."""
        self.project_repo.create("p_rec", "Recovery Test", "Goal", str(self.workspace_root))
        self.task_repo.create("t_crash", "p_rec", "Crash Task", "Desc", status="RUNNING")
        self.execution_repo.create("e_crash", "t_crash", runtime_type="agy")
        self.execution_repo.mark_process_started("e_crash", pid=88888888)

        # Acquire lock and file ownership
        self.resource_repo.acquire_lock("l1", "ACCOUNT", "acc-1", "e_crash", "2099-01-01T00:00:00Z")
        self.resource_repo.claim_file_ownership("own1", "p_rec", "src/*", "WRITE", "e_crash", "2099-01-01T00:00:00Z")

        # Run startup reconciliation
        rec_res = self.recovery_mgr.reconcile_startup("p_rec")
        self.assertEqual(rec_res["reconciled_count"], 1)

        # Task reset to READY
        self.assertEqual(self.task_repo.get("t_crash")["status"], "READY")

        # Locks and ownerships freed
        self.assertIsNone(self.resource_repo.get_lock("ACCOUNT", "acc-1"))
        active_ownerships = self.resource_repo.db.fetchall("SELECT * FROM file_ownerships WHERE owner_execution_id = 'e_crash';")
        self.assertEqual(len(active_ownerships), 0)


if __name__ == "__main__":
    unittest.main()
