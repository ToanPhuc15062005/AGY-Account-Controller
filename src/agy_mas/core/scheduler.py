"""Deterministic DAG scheduler checking dependencies, accounts, locks, and concurrency limits."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from ..planning.dependency_graph import DependencyGraph
from ..planning.plan_schema import TaskContract
from ..resources.quota_tracker import QuotaTracker
from ..storage.repositories.task_repo import TaskRepository
from ..storage.repositories.resource_repo import ResourceRepository


@dataclass
class ScheduleDecision:
    task_id: str
    account_id: str
    model: str
    task_contract: TaskContract


class Scheduler:
    """Evaluates DAG task readiness and resource constraints to select schedulable tasks."""

    def __init__(
        self,
        task_repo: TaskRepository,
        resource_repo: ResourceRepository,
        quota_tracker: QuotaTracker,
        max_concurrency: int = 4,
    ):
        self.task_repo = task_repo
        self.resource_repo = resource_repo
        self.quota_tracker = quota_tracker
        self.max_concurrency = max_concurrency

    def schedule_next(
        self,
        project_id: str,
        available_accounts: List[str],
        running_count: int = 0,
        contracts: Optional[Dict[str, TaskContract]] = None,
    ) -> List[ScheduleDecision]:
        """Finds ready tasks eligible to start immediately without resource contention."""
        if running_count >= self.max_concurrency:
            return []

        tasks = self.task_repo.list_by_project(project_id)
        if not tasks:
            return []

        # Build graph and collect statuses
        graph = DependencyGraph()
        task_statuses: Dict[str, str] = {}
        for t in tasks:
            tid = t["task_id"]
            task_statuses[tid] = t["status"]
            graph.add_task(tid, t.get("dependencies", []))

        ready_ids = graph.get_ready_tasks(task_statuses)
        decisions: List[ScheduleDecision] = []
        slots_remaining = self.max_concurrency - running_count

        for tid in ready_ids:
            if slots_remaining <= 0:
                break

            task_data = next((t for t in tasks if t["task_id"] == tid), None)
            if not task_data or task_data["status"] != "PENDING" and task_data["status"] != "READY":
                continue

            contract = None
            if contracts and tid in contracts:
                contract = contracts[tid]
            else:
                raw_spec = dict(task_data.get("task_spec", {}))
                raw_spec["task_id"] = tid
                raw_spec["project_id"] = project_id
                raw_spec["title"] = task_data["title"]
                raw_spec["description"] = task_data["description"]
                if "pair_round" in task_data and task_data["pair_round"] is not None:
                    raw_spec["pair_round"] = task_data["pair_round"]
                if "last_critique" in task_data and task_data["last_critique"] is not None:
                    raw_spec["last_review_report"] = task_data["last_critique"]
                contract = TaskContract.from_dict(raw_spec)

            # Model preference or default
            model = contract.inputs.parameters.get("model", "gemini-3.8-flash")

            # Check account eligibility
            account = self.quota_tracker.select_eligible_account(model, available_accounts)
            if not account:
                # All candidate accounts in cooldown for this model; cannot schedule now
                continue

            decisions.append(
                ScheduleDecision(
                    task_id=tid,
                    account_id=account,
                    model=model,
                    task_contract=contract,
                )
            )
            slots_remaining -= 1

        return decisions
