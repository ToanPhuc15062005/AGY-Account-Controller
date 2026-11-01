"""Central Orchestrator coordinating DAG tasks, process lifecycles, and state transitions."""

import time
import datetime
from typing import Dict, List, Optional, Any, Tuple, Callable
from ..storage.repositories import (
    ProjectRepository,
    TaskRepository,
    ExecutionRepository,
    EventRepository,
    ArtifactRepository,
    ResourceRepository,
    ReviewRepository,
)
from ..workspace.workspace_manager import WorkspaceManager
from ..resources.quota_tracker import QuotaTracker
from ..agents.base import AgentRuntimeAdapter
from ..agents.process_manager import ManagedProcess
from ..agents.review_engine import ReviewEngine
from .state_machine import TaskStateMachine, TaskState
from .scheduler import Scheduler, ScheduleDecision
from .dispatcher import Dispatcher
from ..planning.plan_schema import TaskContract, ReviewVerdict, ReviewReport


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
        on_event: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        review_engine: Optional[ReviewEngine] = None,
        review_repo: Optional[ReviewRepository] = None,
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
        self.on_event = on_event
        self.last_heartbeat_time = time.time()

        self.review_engine = review_engine or ReviewEngine(workspace_root=self.workspace_mgr.workspace_root)
        self.review_repo = review_repo or (ReviewRepository(self.task_repo.db) if hasattr(self.task_repo, "db") else None)

        self.quota_tracker = quota_tracker or QuotaTracker(resource_repo)
        self.scheduler = Scheduler(task_repo, resource_repo, self.quota_tracker, max_concurrency)
        self.dispatcher = Dispatcher(task_repo, execution_repo, event_repo, workspace_mgr, adapter)

        # Active executions: execution_id -> (task_id, ManagedProcess, TaskContract, account_id, started_timestamp)
        self.active_executions: Dict[str, Tuple[str, ManagedProcess, TaskContract, str, float]] = {}

    def _emit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emits telemetry events safely without interfering with core loop."""
        if self.on_event:
            try:
                self.on_event(event_type, data)
            except Exception:
                pass

    def _finalize_acceptance(
        self,
        project_id: str,
        task_id: str,
        execution_id: str,
        contract: TaskContract,
        proc: ManagedProcess,
        elapsed: float = 0.0,
    ) -> None:
        """Helper to register artifacts, complete execution, release locks, and accept task."""
        self.workspace_mgr.register_task_artifacts(
            project_id=project_id,
            task_id=task_id,
            execution_id=execution_id,
            expected_artifacts=[{"path": a.path, "artifact_type": a.artifact_type} for a in contract.outputs.expected_artifacts],
            process=proc,
        )
        self.execution_repo.mark_completed(
            execution_id, status="COMPLETED", exit_code=0, normalized_outcome="SUCCESS"
        )
        self.workspace_mgr.ownership_manager.release_all(execution_id)

        TaskStateMachine.transition(
            self.task_repo, task_id, TaskState.ACCEPTED,
            event_repo=self.event_repo, execution_id=execution_id, reason="Execution and artifacts verified"
        )
        self._emit("TASK_ACCEPTED", {
            "task_id": task_id,
            "execution_id": execution_id,
            "elapsed_seconds": round(elapsed, 1),
            "artifacts": [a.path for a in contract.outputs.expected_artifacts],
        })

    def tick(self, project_id: str, available_accounts: List[str]) -> Dict[str, Any]:
        """Performs a single evaluation tick over the project lifecycle."""
        project = self.project_repo.get(project_id)
        if not project or project["status"] in ("COMPLETED", "FAILED", "CANCELLED", "PAUSED"):
            return {"status": project["status"] if project else "NOT_FOUND", "active": len(self.active_executions)}

        # 0. Decoupled Promotion: Scan RETRY_WAIT tasks and promote to READY when backoff delay elapses
        retry_tasks = self.task_repo.list_by_project(project_id, status=TaskState.RETRY_WAIT.value)
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        for r_task in retry_tasks:
            r_tid = r_task["task_id"]
            spec = r_task.get("task_spec") or {}
            delay_sec = spec.get("retry_delay_seconds", 5)
            up_str = r_task.get("updated_at")
            can_promote = True
            if up_str:
                try:
                    up_dt = datetime.datetime.fromisoformat(up_str)
                    if (now_dt - up_dt).total_seconds() < delay_sec:
                        can_promote = False
                except Exception:
                    pass
            if can_promote:
                TaskStateMachine.transition(
                    self.task_repo, r_tid, TaskState.READY,
                    event_repo=self.event_repo,
                    reason="Backoff delay completed, promoted to READY"
                )

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
                self._emit("TASK_TIMEOUT", {
                    "task_id": tid,
                    "execution_id": exec_id,
                    "elapsed_seconds": round(elapsed, 1),
                    "timeout_seconds": contract.timeout_seconds,
                })
                finished_execs.append(exec_id)
                continue

            if not proc.is_alive():
                exit_code = proc.process.poll() if proc.process else -1
                stdout_text = "\n".join(proc.stdout_lines[-50:])
                stderr_text = "\n".join(proc.stderr_lines[-50:])

                # Close process log safely
                proc.close_log()

                # Collect parsed events from output
                events = [self.adapter.parse_line(l) for l in proc.stdout_lines if l.strip()]
                valid_events = [e for e in events if e is not None]

                # Move to VERIFYING
                TaskStateMachine.transition(
                    self.task_repo, tid, TaskState.VERIFYING,
                    event_repo=self.event_repo, execution_id=exec_id
                )
                self._emit("TASK_VERIFYING", {
                    "task_id": tid,
                    "execution_id": exec_id,
                    "exit_code": exit_code,
                    "elapsed_seconds": round(elapsed, 1),
                })

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

                    self._emit("TASK_FAILED", {
                        "task_id": tid,
                        "execution_id": exec_id,
                        "exit_code": exit_code,
                        "error_type": cls_fail.error_type,
                        "reason": cls_fail.reason,
                        "retryable": cls_fail.retryable,
                        "cooldown_required": cls_fail.cooldown_required,
                    })

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
                        self._emit("QUOTA_COOLDOWN", {
                            "account_id": acc_id,
                            "model": model,
                            "retry_after_seconds": cls_fail.retry_after_seconds,
                            "reason": cls_fail.reason,
                        })

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
                    # Exit code 0: Verification & Acceptance Flow
                    if not contract.enable_pair_review:
                        self._finalize_acceptance(project_id, tid, exec_id, contract, proc, elapsed)
                        finished_execs.append(exec_id)
                        continue

                    # Active Pair-Review with fault-tolerance safeguards
                    self._emit("PAIR_REVIEW_STARTED", {"task_id": tid, "round": contract.pair_round + 1})

                    try:
                        review_report = self.review_engine.execute_review(
                            project_id=project_id,
                            task_contract=contract,
                            coder_execution_id=exec_id,
                            workspace_root=self.workspace_mgr.workspace_root,
                            timeout_seconds=180,
                        )
                    except Exception as review_err:
                        # Fallback if reviewer crashes or times out
                        self._emit("PAIR_REVIEW_ERROR", {"task_id": tid, "error": str(review_err)})
                        self.execution_repo.mark_completed(
                            exec_id, status="COMPLETED", exit_code=0, normalized_outcome="REVIEW_ERROR"
                        )
                        self.workspace_mgr.ownership_manager.release_all(exec_id)
                        TaskStateMachine.transition(
                            self.task_repo, tid, TaskState.RETRY_WAIT,
                            event_repo=self.event_repo, execution_id=exec_id,
                            reason=f"Reviewer execution failed: {review_err}"
                        )
                        finished_execs.append(exec_id)
                        continue

                    # Persist review report into ReviewRepository
                    if self.review_repo:
                        try:
                            self.review_repo.create(
                                task_id=tid,
                                execution_id=exec_id,
                                round_number=contract.pair_round + 1,
                                verdict=review_report.verdict.value if hasattr(review_report.verdict, "value") else str(review_report.verdict),
                                score=review_report.score,
                                critique=review_report.to_dict(),
                                test_output=review_report.test_output_summary,
                            )
                        except Exception:
                            pass

                    if review_report.verdict == ReviewVerdict.APPROVED:
                        self._finalize_acceptance(project_id, tid, exec_id, contract, proc, elapsed)
                        self._emit("PAIR_REVIEW_APPROVED", {
                            "task_id": tid,
                            "score": review_report.score,
                        })
                    else:
                        contract.pair_round += 1
                        contract.last_review_report = review_report.to_dict()
                        # Mark coder execution record as completed with CHANGES_REQUESTED
                        self.execution_repo.mark_completed(
                            exec_id, status="COMPLETED", exit_code=0, normalized_outcome="CHANGES_REQUESTED"
                        )
                        # Release write lease locks immediately to prevent OwnershipConflictError on retry
                        self.workspace_mgr.ownership_manager.release_all(exec_id)

                        if contract.pair_round < contract.max_pair_rounds:
                            self.task_repo.update_critique(tid, review_report.to_dict(), contract.pair_round)
                            self._emit("PAIR_REVIEW_REJECTED", {
                                "task_id": tid,
                                "round": contract.pair_round,
                                "feedback": review_report.actionable_feedback,
                            })
                            # Transition to RETRY_WAIT; Decoupled scheduler promotion handles moving to READY
                            TaskStateMachine.transition(
                                self.task_repo, tid, TaskState.RETRY_WAIT,
                                event_repo=self.event_repo, execution_id=exec_id,
                                reason=f"Reviewer requested changes (Round {contract.pair_round})"
                            )
                        else:
                            self._emit("PAIR_REVIEW_EXHAUSTED", {"task_id": tid, "rounds": contract.pair_round})
                            TaskStateMachine.transition(
                                self.task_repo, tid, TaskState.FAILED,
                                event_repo=self.event_repo, execution_id=exec_id,
                                reason="Max pair-programming rounds reached without approval"
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
            self._emit("TASK_DISPATCHED", {
                "task_id": d.task_id,
                "execution_id": exec_id,
                "account_id": d.account_id,
                "model": d.model,
                "pid": proc.pid,
                "title": d.task_contract.title,
            })

        # Periodic Heartbeat (every 15 seconds while workers are active)
        now_ts = time.time()
        if len(self.active_executions) > 0 and (now_ts - self.last_heartbeat_time >= 15.0):
            self.last_heartbeat_time = now_ts
            workers_info = [
                {
                    "task_id": tid,
                    "execution_id": eid,
                    "account_id": aid,
                    "pid": p.pid,
                    "elapsed_seconds": round(now_ts - sts, 1),
                }
                for eid, (tid, p, _, aid, sts) in self.active_executions.items()
            ]
            self._emit("HEARTBEAT", {
                "active_count": len(self.active_executions),
                "workers": workers_info,
            })

        # 3. Check project terminal state
        all_tasks = self.task_repo.list_by_project(project_id)
        if all_tasks:
            if all(t["status"] == "ACCEPTED" for t in all_tasks):
                self.project_repo.update_status(project_id, "COMPLETED")
            elif any(t["status"] == "FAILED" for t in all_tasks) and not any(t["status"] in ("RUNNING", "CLAIMED", "READY", "PENDING", "RETRY_WAIT") for t in all_tasks):
                self.project_repo.update_status(project_id, "FAILED")

        updated_project = self.project_repo.get(project_id)
        if updated_project and updated_project["status"] in ("COMPLETED", "FAILED", "CANCELLED"):
            self._emit("PROJECT_TERMINAL", {
                "project_id": project_id,
                "status": updated_project["status"],
                "total_tasks": len(all_tasks),
            })
        return {
            "status": updated_project["status"] if updated_project else "UNKNOWN",
            "active_executions": len(self.active_executions),
            "total_tasks": len(all_tasks),
        }
