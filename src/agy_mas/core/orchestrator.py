"""Central Orchestrator coordinating DAG tasks, process lifecycles, and state transitions."""

import time
import datetime
from typing import Dict, List, Optional, Any, Tuple
from ..storage.repositories import (
    ProjectRepository,
    TaskRepository,
    ExecutionRepository,
    EventRepository,
    ArtifactRepository,
    ResourceRepository,
)
from ..workspace.workspace_manager import WorkspaceManager
from ..resources.quota_tracker import QuotaTracker
from ..agents.base import AgentRuntimeAdapter
from ..agents.process_manager import ManagedProcess
from .state_machine import TaskStateMachine, TaskState
from .scheduler import Scheduler, ScheduleDecision
from .dispatcher import Dispatcher
from ..planning.plan_schema import TaskContract


class Orchestrator:
    """The central authority governing project execution, concurrency, and dispatch."""

    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
        execution_repo: ExecutionRepository,
        event_repo: EventRepository,
        artifact_repo: ArtifactRepository,
        resource_repo: ResourceRepository,
        workspace_mgr: WorkspaceManager,
        adapter: AgentRuntimeAdapter,
        quota_tracker: Optional[QuotaTracker] = None,
        max_concurrency: int = 4,
        default_policy: Optional[Dict[str, Any]] = None,
    ):
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.execution_repo = execution_repo
        self.event_repo = event_repo
        self.artifact_repo = artifact_repo
        self.resource_repo = resource_repo
        self.workspace_mgr = workspace_mgr
        self.adapter = adapter
        self.default_policy = default_policy or {}

        self.quota_tracker = quota_tracker or QuotaTracker(resource_repo)
        self.scheduler = Scheduler(task_repo, resource_repo, self.quota_tracker, max_concurrency)
        self.dispatcher = Dispatcher(task_repo, execution_repo, event_repo, workspace_mgr, adapter)

        # Active executions: execution_id -> (task_id, ManagedProcess, TaskContract, account_id, started_timestamp)
        self.active_executions: Dict[str, Tuple[str, ManagedProcess, TaskContract, str, float]] = {}

    def tick(self, project_id: str, available_accounts: List[str]) -> Dict[str, Any]:
        """Performs a single evaluation tick over the project lifecycle."""
        project = self.project_repo.get(project_id)
        if not project or project["status"] in ("COMPLETED", "FAILED", "CANCELLED", "PAUSED"):
            return {"status": project["status"] if project else "NOT_FOUND", "active": len(self.active_executions)}

        # 1. Reconcile active executions
        finished_execs = []
        for exec_id, (tid, proc, contract, acc_id, start_ts) in list(self.active_executions.items()):
            # Check timeout
            elapsed = time.time() - start_ts
            if proc.is_alive() and elapsed > contract.timeout_seconds:
                proc.terminate_tree(reason="TASK_TIMEOUT")
                self.execution_repo.mark_completed(
                    exec_id, status="TIMEOUT", exit_code=-1,
                    termination_reason="PROCESS_TIMEOUT",
                    error_type="PROCESS_TIMEOUT",
                    error_message=f"Exceeded timeout of {contract.timeout_seconds}s",
                )
                self.workspace_mgr.ownership_manager.release_all(exec_id)
                TaskStateMachine.transition(
                    self.task_repo, tid, TaskState.TIMEOUT,
                    event_repo=self.event_repo, execution_id=exec_id, reason="Timeout reached"
                )
                finished_execs.append(exec_id)
                continue

            if not proc.is_alive():
                exit_code = proc.process.poll() if proc.process else -1
                stdout_text = "\n".join(proc.stdout_lines[-50:])
                stderr_text = "\n".join(proc.stderr_lines[-50:])

                # Collect parsed events from output
                events = [self.adapter.parse_line(l) for l in proc.stdout_lines if l.strip()]
                valid_events = [e for e in events if e is not None]

                # Move to VERIFYING
                TaskStateMachine.transition(
                    self.task_repo, tid, TaskState.VERIFYING,
                    event_repo=self.event_repo, execution_id=exec_id
                )

                # Process completion evaluation
                if exit_code != 0:
                    cls_fail = self.adapter.classify_failure(exit_code, stdout_text, stderr_text, valid_events)
                    self.execution_repo.mark_completed(
                        exec_id,
                        status="FAILED",
                        exit_code=exit_code,
                        error_type=cls_fail.error_type,
                        error_message=cls_fail.reason,
                    )
                    self.workspace_mgr.ownership_manager.release_all(exec_id)

                    # Cooldown handling
                    if cls_fail.cooldown_required:
                        model = contract.inputs.parameters.get("model", "gemini-3.8-flash")
                        self.quota_tracker.record_quota_exhaustion(
                            account_id=acc_id,
                            model_key=model,
                            retry_after_seconds=cls_fail.retry_after_seconds,
                            reason=cls_fail.reason,
                            source=cls_fail.evidence_source,
                        )

                    # Retry evaluation
                    past_attempts = len(self.execution_repo.list_by_task(tid))
                    if cls_fail.retryable and past_attempts <= contract.max_retries:
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.RETRY_WAIT,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason=f"Retryable failure ({cls_fail.error_type}); waiting to retry"
                        )
                        # Immediately return to READY for next tick
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.READY,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason="Resetting to READY after failure"
                        )
                    else:
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.FAILED,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason=f"Task failed: {cls_fail.reason}"
                        )
                else:
                    # Exit code 0: Verify artifacts and accept
                    self.workspace_mgr.register_task_artifacts(
                        project_id=project_id,
                        task_id=tid,
                        execution_id=exec_id,
                        expected_artifacts=[{"path": a.path, "artifact_type": a.artifact_type} for a in contract.outputs.expected_artifacts],
                        process=proc,
                    )
                    self.execution_repo.mark_completed(
                        exec_id, status="COMPLETED", exit_code=0, normalized_outcome="SUCCESS"
                    )
                    self.workspace_mgr.ownership_manager.release_all(exec_id)

                    TaskStateMachine.transition(
                        self.task_repo, tid, TaskState.ACCEPTED,
                        event_repo=self.event_repo, execution_id=exec_id, reason="Execution and artifacts verified"
                    )

                finished_execs.append(exec_id)

        for fid in finished_execs:
            del self.active_executions[fid]

        # 2. Schedule and dispatch new tasks
        decisions = self.scheduler.schedule_next(
            project_id=project_id,
            available_accounts=available_accounts,
            running_count=len(self.active_executions),
        )

        for d in decisions:
            exec_id, proc = self.dispatcher.dispatch(project_id, d, policy=self.default_policy)
            self.active_executions[exec_id] = (d.task_id, proc, d.task_contract, d.account_id, time.time())

        # 3. Check project terminal state
        all_tasks = self.task_repo.list_by_project(project_id)
        if all_tasks:
            if all(t["status"] == "ACCEPTED" for t in all_tasks):
                self.project_repo.update_status(project_id, "COMPLETED")
            elif any(t["status"] == "FAILED" for t in all_tasks) and not any(t["status"] in ("RUNNING", "CLAIMED", "READY", "PENDING", "RETRY_WAIT") for t in all_tasks):
                self.project_repo.update_status(project_id, "FAILED")

        updated_project = self.project_repo.get(project_id)
        return {
            "status": updated_project["status"] if updated_project else "UNKNOWN",
            "active_executions": len(self.active_executions),
            "total_tasks": len(all_tasks),
        }
