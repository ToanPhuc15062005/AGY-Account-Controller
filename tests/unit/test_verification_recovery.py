"""Unit tests for Phase 6: Verification Pipeline and Crash Recovery."""

import unittest
import tempfile
import shutil
from pathlib import Path
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories import (
    TaskRepository,
    ExecutionRepository,
    ResourceRepository,
    EventRepository,
    ProjectRepository,
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


class TestVerificationAndRecovery(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.temp_dir).resolve()

        self.db = Database(":memory:")
        MigrationRunner(self.db).run_all()

        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)
        self.execution_repo = ExecutionRepository(self.db)
        self.resource_repo = ResourceRepository(self.db)
        self.event_repo = EventRepository(self.db)

        self.project_repo.create("p1", "Test", "Goal", str(self.workspace_root))
        self.verifier = Verifier(str(self.workspace_root))
        self.recovery_mgr = RecoveryManager(
            self.task_repo, self.execution_repo, self.resource_repo, self.event_repo
        )

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_verifier_soft_denial_fails_even_with_exit_code_zero(self):
        # ADR-014: Soft-denial is a verification failure signal, not accepted
        contract = TaskContract(
            task_id="t1",
            project_id="p1",
            title="T1",
            description="T1",
            acceptance_criteria=[AcceptanceCriterion("NO_SOFT_DENIAL", "No soft denials allowed")],
        )

        report = self.verifier.verify_task(
            contract=contract,
            exit_code=0,
            has_soft_denial=True,
        )
        self.assertFalse(report.passed)
        self.assertTrue(any("soft denial" in e.lower() for e in report.errors))

    def test_verifier_missing_artifact_fails_verification(self):
        # ADR-017: Acceptance requires artifact verification
        contract = TaskContract(
            task_id="t1",
            project_id="p1",
            title="T1",
            description="T1",
            outputs=OutputScope(
                expected_artifacts=[ExpectedArtifact(path="build/app.bin", min_size_bytes=10)]
            ),
        )

        report = self.verifier.verify_task(
            contract=contract,
            exit_code=0,
            has_soft_denial=False,
        )
        self.assertFalse(report.passed)
        self.assertTrue(any("was not found on disk" in e for e in report.errors))

    def test_verifier_passes_when_all_conditions_met(self):
        # Create the artifact on disk
        art_path = self.workspace_root / "build" / "app.bin"
        art_path.parent.mkdir(parents=True, exist_ok=True)
        art_path.write_bytes(b"VERIFIED_PAYLOAD_1234567890")

        contract = TaskContract(
            task_id="t1",
            project_id="p1",
            title="T1",
            description="T1",
            outputs=OutputScope(
                expected_artifacts=[ExpectedArtifact(path="build/app.bin", min_size_bytes=10)]
            ),
            permission_profile=PermissionProfile(write_paths=["build/*"]),
            acceptance_criteria=[
                AcceptanceCriterion("EXIT_CODE_ZERO", "Exit 0"),
                AcceptanceCriterion("NO_SOFT_DENIAL", "No soft denial"),
            ],
        )

        report = self.verifier.verify_task(
            contract=contract,
            exit_code=0,
            has_soft_denial=False,
            touched_paths=["build/app.bin"],
        )
        self.assertTrue(report.passed, msg=f"Errors: {report.errors}")
        self.assertEqual(report.artifacts_verified, 1)

    def test_recovery_manager_startup_reconciliation(self):
        # Setup an abandoned RUNNING task whose PID is definitely dead (e.g. PID 99999999)
        self.task_repo.create("t_abandoned", "p1", "Dead Task", "Desc", status="RUNNING")
        self.execution_repo.create("e_abandoned", "t_abandoned", runtime_type="agy")
        self.execution_repo.mark_process_started("e_abandoned", pid=99999999)

        # Acquire a lock for this execution
        self.resource_repo.acquire_lock("lock1", "ACCOUNT", "acc-1", "e_abandoned", "2099-01-01T00:00:00Z")

        # Run startup reconciliation
        result = self.recovery_mgr.reconcile_startup("p1")
        self.assertEqual(result["reconciled_count"], 1)
        self.assertIn("t_abandoned", result["reconciled_tasks"])

        # Task is reset to READY for retry
        task = self.task_repo.get("t_abandoned")
        self.assertEqual(task["status"], "READY")

        # Execution marked INTERRUPTED
        execution = self.execution_repo.get("e_abandoned")
        self.assertEqual(execution["status"], "INTERRUPTED")
        self.assertEqual(execution["error_type"], "INTERRUPTED_CRASH")

        # Orphaned lock released
        self.assertIsNone(self.resource_repo.get_lock("ACCOUNT", "acc-1"))


if __name__ == "__main__":
    unittest.main()
