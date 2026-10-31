"""Directed Acyclic Graph (DAG) manager and cycle detector for MAS tasks."""

from typing import Dict, List, Set, Optional


class CycleDetectedError(ValueError):
    """Raised when a dependency cycle is detected in task definitions."""
    pass


class DependencyGraph:
    """Represents task dependency relations and computes topological order and readiness."""

    def __init__(self):
        self.adj: Dict[str, Set[str]] = {}       # task_id -> set of task_ids that DEPEND ON this task
        self.rev_adj: Dict[str, Set[str]] = {}   # task_id -> set of task_ids THIS TASK depends on

    def add_task(self, task_id: str, depends_on: Optional[List[str]] = None) -> None:
        if task_id not in self.adj:
            self.adj[task_id] = set()
        if task_id not in self.rev_adj:
            self.rev_adj[task_id] = set()

        for dep in (depends_on or []):
            if dep == task_id:
                raise CycleDetectedError(f"Self-dependency detected on task '{task_id}'")
            if dep not in self.adj:
                self.adj[dep] = set()
            if dep not in self.rev_adj:
                self.rev_adj[dep] = set()

            self.adj[dep].add(task_id)
            self.rev_adj[task_id].add(dep)

    def has_cycle(self) -> bool:
        try:
            self.topological_sort()
            return False
        except CycleDetectedError:
            return True

    def topological_sort(self) -> List[str]:
        """Performs Kahn's algorithm for topological sorting and cycle detection."""
        in_degree: Dict[str, int] = {node: len(self.rev_adj.get(node, set())) for node in self.adj}
        queue = [node for node, deg in in_degree.items() if deg == 0]
        sorted_nodes: List[str] = []

        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            for dependent in self.adj.get(node, set()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_nodes) != len(self.adj):
            unresolved = [node for node, deg in in_degree.items() if deg > 0]
            raise CycleDetectedError(f"Dependency cycle detected involving tasks: {unresolved}")

        return sorted_nodes

    def get_ready_tasks(self, task_statuses: Dict[str, str]) -> List[str]:
        """Returns task_ids eligible to run: all dependencies have reached 'ACCEPTED' status."""
        ready = []
        for task_id, status in task_statuses.items():
            if status in ("PENDING", "BLOCKED", "READY"):
                deps = self.rev_adj.get(task_id, set())
                if all(task_statuses.get(dep) == "ACCEPTED" for dep in deps):
                    ready.append(task_id)
        return ready

    def has_failed_dependencies(self, task_id: str, task_statuses: Dict[str, str]) -> bool:
        """Checks if any dependency failed or was cancelled."""
        deps = self.rev_adj.get(task_id, set())
        for dep in deps:
            status = task_statuses.get(dep)
            if status in ("FAILED", "CANCELLED"):
                return True
        return False
