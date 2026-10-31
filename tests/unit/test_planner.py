"""Unit tests for Autonomous Planner and goal decomposition."""

import unittest
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories.project_repo import ProjectRepository
from agy_mas.storage.repositories.task_repo import TaskRepository
from agy_mas.planning.planner import Planner
from agy_mas.planning.plan_validator import PlanValidator


class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        MigrationRunner(self.db).run_all()
        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)
        self.project_repo.create("p_test", "Demo", "Build auth", "C:/ws")
        self.planner = Planner(self.task_repo)

    def tearDown(self):
        self.db.close()

    def test_plan_project_auto_decomposes_and_persists(self):
        contracts = self.planner.plan_project(
            project_id="p_test",
            goal="Build JWT authentication and login endpoints",
            workspace_root="C:/ws",
        )
        self.assertGreaterEqual(len(contracts), 2)

        # Validate with PlanValidator
        is_valid, errors = PlanValidator.validate_plan(contracts)
        self.assertTrue(is_valid, f"Generated contracts must be valid: {errors}")

        # Check persisted in DB
        persisted = self.task_repo.list_by_project("p_test")
        self.assertEqual(len(persisted), len(contracts))

        # Check no write collisions
        write_paths = [c.permission_profile.write_paths for c in contracts]
        for i in range(len(contracts)):
            for j in range(i + 1, len(contracts)):
                if not (contracts[i].task_id in contracts[j].depends_on or contracts[j].task_id in contracts[i].depends_on):
                    overlap = PlanValidator._find_path_overlap(contracts[i].permission_profile.write_paths, contracts[j].permission_profile.write_paths)
                    self.assertEqual(len(overlap), 0, f"Independent tasks must not have write collisions: {overlap}")


if __name__ == "__main__":
    unittest.main()
