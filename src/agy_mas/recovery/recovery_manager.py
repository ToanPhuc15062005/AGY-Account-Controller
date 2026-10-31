"""Recovery manager handling startup reconciliation, stale worker cleanup, and retries."""

import os
import sys
import subprocess
from typing import List, Dict, Any, Optional
from ..storage.repositories import (
    TaskRepository,
    ExecutionRepository,
    ResourceRepository,
    EventRepository,
)
from ..core.state_machine import TaskStateMachine, TaskState


def is_pid_alive(pid: int) -> bool:
    """Checks whether a process with given PID is currently alive on the host."""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            res = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                check=False,
            )
            return str(pid) in res.stdout
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


class RecoveryManager:
    """Reconciles interrupted state after orchestrator restart and recovers orphaned resources."""

    def __init__(
        self,
        task_repo: TaskRepository,
        execution_repo: ExecutionRepository,
        resource_repo: ResourceRepository,
        event_repo: EventRepository,
    ):
        self.task_repo = task_repo
        self.execution_repo = execution_repo
        self.resource_repo = resource_repo
        self.event_repo = event_repo

    def reconcile_startup(self, project_id: str) -> Dict[str, Any]:
        """Detects dead workers from previous runs, releases locks, and safely resets tasks."""
        reconciled_tasks = []
        tasks = self.task_repo.list_by_project(project_id)

        for task in tasks:
            tid = task["task_id"]
            status = task["status"]

            if status in (TaskState.CLAIMED.value, TaskState.RUNNING.value):
                latest_exec = self.execution_repo.get_latest_for_task(tid)
                if not latest_exec:
                    # No execution record found; reset to READY
                    TaskStateMachine.transition(
                        self.task_repo, tid, TaskState.READY,
                        event_repo=self.event_repo, reason="Startup reconciliation: missing execution reset"
                    )
                    reconciled_tasks.append(tid)
                    continue

                exec_id = latest_exec["execution_id"]
                pid = latest_exec.get("pid") or latest_exec.get("process_id")

                # Check if process is still alive
                alive = is_pid_alive(pid) if pid else False

                if not alive:
                    # Clean up orphaned locks and leases
                    self.resource_repo.release_all_for_execution(exec_id)

                    self.execution_repo.mark_completed(
                        exec_id,
                        status="INTERRUPTED",
                        exit_code=-1,
                        error_type="INTERRUPTED_CRASH",
                        error_message="Process died while orchestrator was offline",
                    )

                    # Check retries
                    past_attempts = len(self.execution_repo.list_by_task(tid))
                    task_spec = task.get("task_spec", {})
                    max_retries = task_spec.get("max_retries", 2)

                    if past_attempts <= max_retries:
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.RETRY_WAIT,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason="Recovered from crash; preparing retry"
                        )
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.READY,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason="Reset to READY after crash recovery"
                        )
                    else:
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.FAILED,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason="Max retries exhausted after crash"
                        )

                    reconciled_tasks.append(tid)

        return {
            "project_id": project_id,
            "reconciled_count": len(reconciled_tasks),
            "reconciled_tasks": reconciled_tasks,
        }
