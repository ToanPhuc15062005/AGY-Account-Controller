"""Autonomous Planner decomposing high-level user goals into validated DAG subtasks."""

import json
import re
import uuid
import subprocess
import shutil
from typing import List, Dict, Any, Optional
from pathlib import Path
from .plan_schema import (
    TaskContract,
    InputScope,
    OutputScope,
    ExpectedArtifact,
    AcceptanceCriterion,
    PermissionProfile,
)
from .plan_validator import PlanValidator
from ..storage.repositories.task_repo import TaskRepository


PLANNER_SYSTEM_PROMPT = """
You are the MAS Lead Software Architect.
Your task is to decompose the following user project goal into 2 to 4 CONCURRENT, DECOUPLED subtasks
that multiple coding agents can execute in parallel without write collisions.

CRITICAL RULES:
1. Divide work strictly into isolated write scopes (e.g. Task 1 writes to src/api/*, Task 2 writes to src/ui/*, Task 3 writes to tests/*).
2. Independent tasks MUST NOT share write paths.
3. If a task requires output from another task, declare it in 'depends_on'.
4. Every task must declare at least 1 expected output file in 'expected_artifacts'.
5. Return ONLY a valid JSON array of tasks matching this schema:

[
  {
    "task_id": "short_unique_id",
    "title": "Concise task title",
    "description": "Detailed instructions for the agent",
    "domain": "software",
    "role": "developer",
    "priority": 50,
    "write_paths": ["relative/path/or/pattern/*"],
    "expected_artifacts": ["relative/path/to/file.ext"],
    "depends_on": []
  }
]
"""


class Planner:
    """Decomposes a user goal into an executable, validated DAG task plan."""

    def __init__(self, task_repo: TaskRepository, agy_cmd: Optional[str] = None):
        self.task_repo = task_repo
        self.agy_cmd = agy_cmd or shutil.which("agy") or shutil.which("agy.cmd") or "agy"

    def plan_project(
        self,
        project_id: str,
        goal: str,
        workspace_root: str,
        model: str = "gemini-2.5-pro",
    ) -> List[TaskContract]:
        """Generates candidate subtasks from goal, validates with PlanValidator, and persists."""
        raw_subtasks = self._decompose_with_llm(goal, workspace_root, model)
        if not raw_subtasks:
            raw_subtasks = self._decompose_heuristic_fallback(goal)

        contracts = self._build_contracts(project_id, raw_subtasks)

        # Validate with PlanValidator
        is_valid, errors = PlanValidator.validate_plan(contracts)
        if not is_valid:
            # Auto-resolve collisions by serializing conflicting tasks
            contracts = self._auto_serialize_collisions(contracts, errors)
            is_valid, errors = PlanValidator.validate_plan(contracts)
            if not is_valid:
                raise ValueError(f"Generated plan could not be validated: {errors}")

        # Persist valid plan into task repository
        for c in contracts:
            self.task_repo.create(
                task_id=c.task_id,
                project_id=project_id,
                title=c.title,
                description=c.description,
                domain=c.domain,
                role=c.role,
                priority=c.priority,
                status="PENDING",
                task_spec=c.to_dict(),
                depends_on=c.depends_on,
            )

        return contracts

    def _decompose_with_llm(self, goal: str, workspace_root: str, model: str) -> List[Dict[str, Any]]:
        prompt = (
            f"{PLANNER_SYSTEM_PROMPT}\n\n"
            f"PROJECT GOAL: {goal}\n"
            f"WORKSPACE ROOT: {workspace_root}\n\n"
            "Produce the JSON array of tasks:"
        )

        try:
            res = subprocess.run(
                [self.agy_cmd, "-p", prompt, "--model", model],
                capture_output=True,
                text=True,
                timeout=6,
                check=False,
            )
            raw = res.stdout.strip()
            # Extract JSON block
            match = re.search(r"\[\s*\{.*\}\s*\]", raw, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except (subprocess.TimeoutExpired, Exception):
            pass

        return []

    def _decompose_heuristic_fallback(self, goal: str) -> List[Dict[str, Any]]:
        """Fast fallback generating decoupled Core, API/Docs, and Test subtasks."""
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", goal.lower()).strip("_")[:12]
        return [
            {
                "task_id": f"task_{slug}_core",
                "title": f"Implement core logic for {goal}",
                "description": f"Implement main functionality for: {goal}",
                "domain": "software",
                "role": "developer",
                "priority": 80,
                "write_paths": ["src/core/*"],
                "expected_artifacts": ["src/core/main.py"],
                "depends_on": [],
            },
            {
                "task_id": f"task_{slug}_docs",
                "title": f"Write documentation for {goal}",
                "description": f"Write user guide and API documentation for: {goal}",
                "domain": "docs",
                "role": "writer",
                "priority": 40,
                "write_paths": ["docs/*"],
                "expected_artifacts": ["docs/README.md"],
                "depends_on": [],
            },
            {
                "task_id": f"task_{slug}_tests",
                "title": f"Implement test suite for {goal}",
                "description": f"Create automated unit and integration tests for: {goal}",
                "domain": "qa",
                "role": "tester",
                "priority": 60,
                "write_paths": ["tests/unit/*"],
                "expected_artifacts": ["tests/unit/test_core.py"],
                "depends_on": [f"task_{slug}_core"],
            },
        ]

    def _build_contracts(self, project_id: str, raw_tasks: List[Dict[str, Any]]) -> List[TaskContract]:
        contracts = []
        for raw in raw_tasks:
            tid = raw.get("task_id") or f"t_{uuid.uuid4().hex[:6]}"
            write_paths = raw.get("write_paths", [f"src/{tid}/*"])
            expected = raw.get("expected_artifacts", [])

            expected_arts = [
                ExpectedArtifact(path=p, artifact_type="FILE", min_size_bytes=1, required=True)
                for p in expected
            ]

            criteria = [
                AcceptanceCriterion(
                    criterion_type="EXIT_CODE_ZERO",
                    description="Agent process exits successfully with 0",
                ),
                AcceptanceCriterion(
                    criterion_type="NO_SOFT_DENIAL",
                    description="No permission soft-denial in headless mode",
                ),
            ]
            for exp in expected:
                criteria.append(
                    AcceptanceCriterion(
                        criterion_type="ARTIFACT_EXISTS",
                        description=f"File {exp} must be created",
                        params={"path": exp},
                    )
                )

            contract = TaskContract(
                task_id=tid,
                project_id=project_id,
                title=raw.get("title", tid),
                description=raw.get("description", ""),
                domain=raw.get("domain", "software"),
                role=raw.get("role", "developer"),
                priority=raw.get("priority", 50),
                outputs=OutputScope(expected_artifacts=expected_arts),
                acceptance_criteria=criteria,
                permission_profile=PermissionProfile(
                    write_paths=write_paths,
                    dangerously_skip_permissions=False,
                ),
                depends_on=raw.get("depends_on", []),
            )
            contracts.append(contract)
        return contracts

    def _auto_serialize_collisions(self, contracts: List[TaskContract], errors: List[str]) -> List[TaskContract]:
        """If two tasks have conflicting write scopes, automatically serializes them."""
        for err in errors:
            if "Concurrent write conflict" in err:
                match = re.search(r"tasks '([^']+)' and '([^']+)'", err)
                if match:
                    t1_id, t2_id = match.group(1), match.group(2)
                    for c in contracts:
                        if c.task_id == t2_id and t1_id not in c.depends_on:
                            c.depends_on.append(t1_id)
        return contracts
