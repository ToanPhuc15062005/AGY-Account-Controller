"""Unit tests for Phase 4: Shared Workspace, Path Policy, Windows Retries, Ownership, and Snapshots."""

import unittest
import tempfile
import shutil
from pathlib import Path
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories.resource_repo import ResourceRepository
from agy_mas.storage.repositories.artifact_repo import ArtifactRepository
from agy_mas.storage.repositories.project_repo import ProjectRepository
from agy_mas.storage.repositories.task_repo import TaskRepository
from agy_mas.storage.repositories.execution_repo import ExecutionRepository
from agy_mas.workspace.path_policy import PathPolicy, PathPolicyError
from agy_mas.workspace.file_lock_manager import WindowsFileRetryManager, FileSharingContentionError
from agy_mas.workspace.ownership_manager import OwnershipManager, OwnershipConflictError
from agy_mas.workspace.snapshot_manager import SnapshotManager, SnapshotTimingError
from agy_mas.workspace.workspace_manager import WorkspaceManager
from agy_mas.config import WindowsFileRetryConfig


class DummyProcess:
    def __init__(self, alive: bool):
        self._alive = alive

    def is_alive(self) -> bool:
        return self._alive


class TestWorkspaceCoordination(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.temp_dir).resolve()

        self.db = Database(":memory:")
        MigrationRunner(self.db).run_all()
        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)
        self.execution_repo = ExecutionRepository(self.db)
        self.resource_repo = ResourceRepository(self.db)
        self.artifact_repo = ArtifactRepository(self.db)

        self.project_repo.create("p1", "Project 1", "Goal", str(self.workspace_root))
        self.task_repo.create("t1", "p1", "Task 1", "Desc")
        self.execution_repo.create("e1", "t1", runtime_type="agy")
        self.execution_repo.create("e2", "t1", runtime_type="agy")

        self.path_policy = PathPolicy(self.workspace_root)
        self.ownership_mgr = OwnershipManager(self.resource_repo)
        self.snapshot_mgr = SnapshotManager(self.path_policy)
        self.workspace_mgr = WorkspaceManager(str(self.workspace_root), self.resource_repo, self.artifact_repo)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_path_policy_safety(self):
        # Valid relative path
        safe = self.path_policy.resolve_safe_path("src/core/main.py")
        self.assertEqual(safe, self.workspace_root / "src" / "core" / "main.py")
        self.assertEqual(self.path_policy.get_relative_path(safe), "src/core/main.py")

        # Escaping path raises error
        with self.assertRaises(PathPolicyError):
            self.path_policy.resolve_safe_path("../../outside.txt")

    def test_ownership_conflict_detection(self):
        # e1 claims src/auth/
        self.ownership_mgr.claim_ownership("p1", "src/auth/*", "e1")

        # e1 write permitted
        self.assertTrue(self.ownership_mgr.check_write_permitted("p1", "e1", "src/auth/login.py"))
        # e2 write NOT permitted
        self.assertFalse(self.ownership_mgr.check_write_permitted("p1", "e2", "src/auth/login.py"))

        # e2 cannot claim overlapping path
        with self.assertRaises(OwnershipConflictError):
            self.ownership_mgr.claim_ownership("p1", "src/auth/login.py", "e2")

        # After releasing, e2 can claim
        self.ownership_mgr.release_all("e1")
        self.ownership_mgr.claim_ownership("p1", "src/auth/login.py", "e2")
        self.assertTrue(self.ownership_mgr.check_write_permitted("p1", "e2", "src/auth/login.py"))

    def test_windows_file_retry_backoff(self):
        retry_cfg = WindowsFileRetryConfig(initial_delay_ms=10, max_delay_ms=50, max_attempts=3)
        retry_mgr = WindowsFileRetryManager(retry_cfg)

        calls = [0]

        def flaky_file_op():
            calls[0] += 1
            if calls[0] < 3:
                err = PermissionError("The process cannot access the file because it is being used by another process")
                setattr(err, "winerror", 32)
                raise err
            return "SUCCESS"

        result = retry_mgr.execute_with_retry(flaky_file_op)
        self.assertEqual(result, "SUCCESS")
        self.assertEqual(calls[0], 3)

        # Permanent lock raises FileSharingContentionError
        calls[0] = 0

        def always_locked():
            calls[0] += 1
            err = PermissionError("WinError 32: Sharing violation")
            setattr(err, "winerror", 32)
            raise err

        with self.assertRaises(FileSharingContentionError):
            retry_mgr.execute_with_retry(always_locked)

    def test_snapshot_timing_adr016(self):
        # Create a sample deliverable
        out_file = self.workspace_root / "dist" / "app.exe"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(b"BINARY DELIVERABLE CONTENT 12345")

        # Snapshot while process alive raises SnapshotTimingError
        alive_proc = DummyProcess(alive=True)
        with self.assertRaises(SnapshotTimingError):
            self.snapshot_mgr.snapshot_file("dist/app.exe", process=alive_proc)

        # Snapshot after process exit succeeds
        dead_proc = DummyProcess(alive=False)
        snap = self.snapshot_mgr.snapshot_file("dist/app.exe", process=dead_proc)
        self.assertTrue(snap["exists"])
        self.assertEqual(snap["size_bytes"], 32)
        self.assertIsNotNone(snap["checksum"])

        # WorkspaceManager registers it properly
        registered = self.workspace_mgr.register_task_artifacts(
            "p1", "t1", "e1",
            expected_artifacts=[{"path": "dist/app.exe", "artifact_type": "BINARY"}],
            process=dead_proc,
        )
        self.assertEqual(len(registered), 1)
        self.assertEqual(registered[0]["path"], "dist/app.exe")


if __name__ == "__main__":
    unittest.main()
