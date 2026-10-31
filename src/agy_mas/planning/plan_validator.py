"""Plan validation logic verifying DAG safety, write scope overlap, and contract integrity."""

from typing import List, Dict, Tuple, Optional
import fnmatch
from .plan_schema import TaskContract
from .dependency_graph import DependencyGraph, CycleDetectedError


class PlanValidationError(ValueError):
    """Raised when plan validation fails."""
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors or [message]


class PlanValidator:
    """Validates candidate plans prior to persistence and execution dispatch."""

    @classmethod
    def validate_plan(cls, contracts: List[TaskContract]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        task_map: Dict[str, TaskContract] = {c.task_id: c for c in contracts}

        if len(task_map) != len(contracts):
            errors.append("Duplicate task_id detected in plan contracts.")

        # 1. Dependency validity & existence
        graph = DependencyGraph()
        for c in contracts:
            for dep in c.depends_on:
                if dep not in task_map:
                    errors.append(f"Task '{c.task_id}' depends on missing task '{dep}'.")
            try:
                graph.add_task(c.task_id, c.depends_on)
            except CycleDetectedError as e:
                errors.append(str(e))

        # 2. Cycle detection
        try:
            graph.topological_sort()
        except CycleDetectedError as e:
            errors.append(str(e))

        # 3. Path safety: relative paths only, no path traversal
        for c in contracts:
            all_paths = (
                c.inputs.paths
                + [a.path for a in c.outputs.expected_artifacts]
                + c.outputs.target_paths
                + c.permission_profile.read_paths
                + c.permission_profile.write_paths
            )
            for p in all_paths:
                clean_p = p.replace("\\", "/").strip()
                if clean_p.startswith("/") or clean_p.startswith("..") or "/../" in clean_p:
                    errors.append(f"Task '{c.task_id}' specifies invalid/unsafe path: '{p}'")

        # 4. Acceptance criteria check
        for c in contracts:
            if c.outputs.expected_artifacts and not c.acceptance_criteria:
                errors.append(
                    f"Task '{c.task_id}' defines expected output artifacts but has no acceptance criteria."
                )

        # 5. Write Scope overlap between parallel (independent) tasks
        # Two tasks can only write to the same path pattern if one transitively depends on the other
        ancestors_map: Dict[str, set] = {}
        for c in contracts:
            ancestors_map[c.task_id] = cls._get_all_ancestors(c.task_id, graph)

        for i in range(len(contracts)):
            for j in range(i + 1, len(contracts)):
                t1 = contracts[i]
                t2 = contracts[j]

                # Check if independent (neither t1 depends on t2 nor t2 on t1)
                is_dependent = (t1.task_id in ancestors_map[t2.task_id]) or (t2.task_id in ancestors_map[t1.task_id])
                if not is_dependent:
                    # Check write path overlap
                    overlap = cls._find_path_overlap(
                        t1.permission_profile.write_paths,
                        t2.permission_profile.write_paths
                    )
                    if overlap:
                        errors.append(
                            f"Concurrent write conflict between independent tasks '{t1.task_id}' and '{t2.task_id}' on path(s): {overlap}"
                        )

        return (len(errors) == 0, errors)

    @classmethod
    def _get_all_ancestors(cls, task_id: str, graph: DependencyGraph) -> set:
        ancestors = set()
        queue = list(graph.rev_adj.get(task_id, set()))
        while queue:
            curr = queue.pop(0)
            if curr not in ancestors:
                ancestors.add(curr)
                queue.extend(graph.rev_adj.get(curr, set()))
        return ancestors

    @staticmethod
    def _find_path_overlap(paths1: List[str], paths2: List[str]) -> List[str]:
        conflicts = []
        for p1 in paths1:
            norm1 = p1.replace("\\", "/").strip("/")
            for p2 in paths2:
                norm2 = p2.replace("\\", "/").strip("/")
                if norm1 == norm2:
                    conflicts.append(norm1)
                elif fnmatch.fnmatch(norm1, norm2) or fnmatch.fnmatch(norm2, norm1):
                    conflicts.append(f"{norm1} ~ {norm2}")
                elif norm1.startswith(norm2 + "/") or norm2.startswith(norm1 + "/"):
                    conflicts.append(f"{norm1} ~ {norm2}")
        return conflicts
