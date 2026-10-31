"""Unit tests for SQLite storage, migrations, and repositories."""

import unittest
import datetime
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories import (
    ProjectRepository,
    TaskRepository,
    ExecutionRepository,
    EventRepository,
    ArtifactRepository,
    ResourceRepository,
    ApprovalRepository,
)


class TestStorageLayer(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.runner = MigrationRunner(self.db)
        self.runner.run_all()

        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)
        self.execution_repo = ExecutionRepository(self.db)
        self.event_repo = EventRepository(self.db)
        self.artifact_repo = ArtifactRepository(self.db)
        self.resource_repo = ResourceRepository(self.db)
        self.approval_repo = ApprovalRepository(self.db)

    def tearDown(self):
        self.db.close()

    def test_migrations_idempotent(self):
        applied = self.runner.run_all()
        self.assertEqual(len(applied), 0)

    def test_project_crud(self):
        p = self.project_repo.create("proj-1", "Test Project", "Build MAS", "C:/test", status="CREATED")
        self.assertEqual(p["project_id"], "proj-1")
        self.assertEqual(p["status"], "CREATED")

        self.project_repo.update_status("proj-1", "RUNNING")
        updated = self.project_repo.get("proj-1")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["status"], "RUNNING")

        all_projects = self.project_repo.list_all()
        self.assertEqual(len(all_projects), 1)

    def test_task_and_dependencies(self):
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")
        t1 = self.task_repo.create("task-1", "proj-1", "T1", "Desc 1")
        t2 = self.task_repo.create("task-2", "proj-1", "T2", "Desc 2", depends_on=["task-1"])

        self.assertEqual(t1["task_id"], "task-1")
        self.assertEqual(t2["dependencies"], ["task-1"])

        deps = self.task_repo.get_dependencies("task-2")
        self.assertEqual(deps, ["task-1"])

        dep_map = self.task_repo.get_dependency_map("proj-1")
        self.assertEqual(dep_map, {"task-2": ["task-1"]})

        with self.assertRaises(ValueError):
            self.task_repo.add_dependency("task-1", "task-1")

    def test_execution_attempts(self):
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")
        self.task_repo.create("task-1", "proj-1", "T1", "Desc 1")

        e1 = self.execution_repo.create("exec-1", "task-1", runtime_type="agy", model="gemini-2.5-pro")
        self.assertEqual(e1["attempt"], 1)

        self.execution_repo.mark_process_started("exec-1", pid=1234, command_fingerprint="fp1")
        e1_running = self.execution_repo.get("exec-1")
        self.assertIsNotNone(e1_running)
        self.assertEqual(e1_running["status"], "RUNNING")
        self.assertEqual(e1_running["pid"], 1234)

        self.execution_repo.mark_completed("exec-1", status="FAILED", exit_code=1, error_type="QUOTA_EXHAUSTED")
        e1_done = self.execution_repo.get("exec-1")
        self.assertIsNotNone(e1_done)
        self.assertEqual(e1_done["status"], "FAILED")
        self.assertEqual(e1_done["error_type"], "QUOTA_EXHAUSTED")

        # Second attempt should automatically have attempt=2
        e2 = self.execution_repo.create("exec-2", "task-1", runtime_type="agy", model="gemini-2.5-pro")
        self.assertEqual(e2["attempt"], 2)

    def test_events_monotonic_sequence(self):
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")
        evt1 = self.event_repo.append("proj-1", "TASK_CREATED", {"task_id": "t1"})
        evt2 = self.event_repo.append("proj-1", "TASK_SCHEDULED", {"task_id": "t1"})
        self.assertEqual(evt1["sequence"], 1)
        self.assertEqual(evt2["sequence"], 2)

        events = self.event_repo.list_by_project("proj-1")
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["event_type"], "TASK_CREATED")
        self.assertEqual(events[1]["event_type"], "TASK_SCHEDULED")

    def test_artifact_registration(self):
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")
        self.task_repo.create("task-1", "proj-1", "T1", "Desc 1")
        self.execution_repo.create("exec-1", "task-1", runtime_type="agy")

        art = self.artifact_repo.register("proj-1", "task-1", "exec-1", "src/main.py", "CODE", checksum="abc123")
        self.assertEqual(art["path"], "src/main.py")
        self.assertEqual(art["checksum"], "abc123")

        task_arts = self.artifact_repo.list_by_task("task-1")
        self.assertEqual(len(task_arts), 1)

    def test_account_model_cooldown(self):
        until = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5)).isoformat()
        self.resource_repo.set_account_model_cooldown(
            account_id="acc1",
            model_key="gemini-2.5-pro",
            cooldown_until=until,
            cooldown_reason="Quota exceeded",
            cooldown_source="stream-json",
            last_error_code="QUOTA_EXHAUSTED"
        )

        self.assertTrue(self.resource_repo.is_in_cooldown("acc1", "gemini-2.5-pro"))
        self.assertFalse(self.resource_repo.is_in_cooldown("acc1", "claude-sonnet-4-6"))
        self.assertFalse(self.resource_repo.is_in_cooldown("acc2", "gemini-2.5-pro"))

        self.resource_repo.clear_account_model_cooldown("acc1", "gemini-2.5-pro")
        self.assertFalse(self.resource_repo.is_in_cooldown("acc1", "gemini-2.5-pro"))

    def test_resource_locks(self):
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")
        self.task_repo.create("task-1", "proj-1", "T1", "Desc 1")
        self.execution_repo.create("exec-1", "task-1", runtime_type="agy")
        self.execution_repo.create("exec-2", "task-1", runtime_type="agy")

        expires = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)).isoformat()
        acquired = self.resource_repo.acquire_lock("lock-1", "ACCOUNT", "acc1", "exec-1", expires)
        self.assertTrue(acquired)

        # Another execution cannot acquire active lock
        acquired2 = self.resource_repo.acquire_lock("lock-2", "ACCOUNT", "acc1", "exec-2", expires)
        self.assertFalse(acquired2)

        # Releasing allows acquisition
        self.resource_repo.release_lock("lock-1")
        acquired3 = self.resource_repo.acquire_lock("lock-3", "ACCOUNT", "acc1", "exec-2", expires)
        self.assertTrue(acquired3)

    def test_approval_workflow(self):
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")
        appr = self.approval_repo.request_approval(
            project_id="proj-1",
            requested_action="WRITE_FILE",
            resource_scope="src/security.py",
            reason="Security sensitive edit"
        )
        self.assertEqual(appr["status"], "PENDING")

        pending = self.approval_repo.list_pending("proj-1")
        self.assertEqual(len(pending), 1)

        ok = self.approval_repo.decide(appr["approval_id"], "APPROVED", decided_by="admin")
        self.assertTrue(ok)

        decided = self.approval_repo.get(appr["approval_id"])
        self.assertIsNotNone(decided)
        self.assertEqual(decided["status"], "APPROVED")
        self.assertEqual(decided["decided_by"], "admin")


if __name__ == "__main__":
    unittest.main()
