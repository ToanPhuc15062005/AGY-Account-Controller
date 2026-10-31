"""Unit tests for Phase 2: Task Engine, State Machine, DAG Dependency Graph, and Plan Validator."""

import unittest
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories.project_repo import ProjectRepository
from agy_mas.storage.repositories.task_repo import TaskRepository
from agy_mas.storage.repositories.event_repo import EventRepository
from agy_mas.core.state_machine import TaskStateMachine, TaskState, InvalidStateTransitionError
from agy_mas.planning.plan_schema import (
    TaskContract,
    PermissionProfile,
    OutputScope,
    ExpectedArtifact,
    AcceptanceCriterion,
)
from agy_mas.planning.dependency_graph import DependencyGraph, CycleDetectedError
from agy_mas.planning.plan_validator import PlanValidator


class TestTaskEngine(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        MigrationRunner(self.db).run_all()
        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)
        self.event_repo = EventRepository(self.db)
        self.project_repo.create("proj-1", "Test", "Goal", "C:/test")

    def tearDown(self):
        self.db.close()

    def test_state_machine_valid_flow(self):
        self.task_repo.create("t1", "proj-1", "Task 1", "Desc", status="PENDING")

        # PENDING -> READY -> CLAIMED -> RUNNING -> VERIFYING -> ACCEPTED
        TaskStateMachine.transition(self.task_repo, "t1", TaskState.READY, self.event_repo)
        self.assertEqual(self.task_repo.get("t1")["status"], "READY")

        TaskStateMachine.transition(self.task_repo, "t1", TaskState.CLAIMED, self.event_repo)
        self.assertEqual(self.task_repo.get("t1")["status"], "CLAIMED")

        TaskStateMachine.transition(self.task_repo, "t1", TaskState.RUNNING, self.event_repo)
        self.assertEqual(self.task_repo.get("t1")["status"], "RUNNING")

        TaskStateMachine.transition(self.task_repo, "t1", TaskState.VERIFYING, self.event_repo)
        self.assertEqual(self.task_repo.get("t1")["status"], "VERIFYING")

        TaskStateMachine.transition(self.task_repo, "t1", TaskState.ACCEPTED, self.event_repo)
        self.assertEqual(self.task_repo.get("t1")["status"], "ACCEPTED")

    def test_state_machine_invalid_transition_rejected(self):
        self.task_repo.create("t1", "proj-1", "Task 1", "Desc", status="PENDING")

        # PENDING directly to ACCEPTED is invalid
        with self.assertRaises(InvalidStateTransitionError):
            TaskStateMachine.transition(self.task_repo, "t1", TaskState.ACCEPTED, self.event_repo)

    def test_dag_cycle_detection(self):
        graph = DependencyGraph()
        graph.add_task("A", depends_on=["B"])
        graph.add_task("B", depends_on=["C"])
        graph.add_task("C", depends_on=["A"])

        self.assertTrue(graph.has_cycle())
        with self.assertRaises(CycleDetectedError):
            graph.topological_sort()

    def test_dag_topological_sort_and_readiness(self):
        graph = DependencyGraph()
        graph.add_task("A", depends_on=[])
        graph.add_task("B", depends_on=["A"])
        graph.add_task("C", depends_on=["A"])
        graph.add_task("D", depends_on=["B", "C"])

        order = graph.topological_sort()
        self.assertEqual(order[0], "A")
        self.assertIn("B", order[1:3])
        self.assertIn("C", order[1:3])
        self.assertEqual(order[3], "D")

        statuses = {
            "A": "PENDING",
            "B": "BLOCKED",
            "C": "BLOCKED",
            "D": "BLOCKED",
        }
        ready = graph.get_ready_tasks(statuses)
        self.assertEqual(ready, ["A"])

        # Once A is ACCEPTED, B and C become READY
        statuses["A"] = "ACCEPTED"
        statuses["B"] = "PENDING"
        statuses["C"] = "PENDING"
        ready2 = sorted(graph.get_ready_tasks(statuses))
        self.assertEqual(ready2, ["B", "C"])

    def test_plan_validator_detects_conflicts(self):
        # 1. Parallel write collision
        c1 = TaskContract(
            task_id="t1",
            project_id="p1",
            title="T1",
            description="T1",
            permission_profile=PermissionProfile(write_paths=["src/auth/"]),
        )
        c2 = TaskContract(
            task_id="t2",
            project_id="p1",
            title="T2",
            description="T2",
            permission_profile=PermissionProfile(write_paths=["src/auth/login.py"]),
        )
        ok, errors = PlanValidator.validate_plan([c1, c2])
        self.assertFalse(ok)
        self.assertTrue(any("Concurrent write conflict" in e for e in errors))

        # 2. Resolving with dependency makes it valid
        c2.depends_on = ["t1"]
        ok2, errors2 = PlanValidator.validate_plan([c1, c2])
        self.assertTrue(ok2, msg=f"Expected valid plan, got errors: {errors2}")

    def test_plan_validator_detects_unsafe_paths(self):
        c1 = TaskContract(
            task_id="t1",
            project_id="p1",
            title="T1",
            description="T1",
            permission_profile=PermissionProfile(write_paths=["../../etc/passwd"]),
        )
        ok, errors = PlanValidator.validate_plan([c1])
        self.assertFalse(ok)
        self.assertTrue(any("unsafe path" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
