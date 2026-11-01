"""Dispatcher executing scheduled tasks via runtime adapters and tracking process state."""

import uuid
import datetime
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from ..agents.base import AgentRuntimeAdapter
from ..agents.process_manager import ManagedProcess
from ..storage.repositories.task_repo import TaskRepository
from ..storage.repositories.execution_repo import ExecutionRepository
from ..storage.repositories.event_repo import EventRepository
from ..workspace.workspace_manager import WorkspaceManager
from ..accounts.credential_provider import CredentialSwitchLock, switch_credential_to_account
from .state_machine import TaskStateMachine, TaskState
from .scheduler import ScheduleDecision


class Dispatcher:
    """Dispatches scheduled tasks, creates execution attempts, and tracks processes."""

    def __init__(
        self,
        task_repo: TaskRepository,
        execution_repo: ExecutionRepository,
        event_repo: EventRepository,
        workspace_mgr: WorkspaceManager,
        adapter: AgentRuntimeAdapter,
    ):
        self.task_repo = task_repo
        self.execution_repo = execution_repo
        self.event_repo = event_repo
        self.workspace_mgr = workspace_mgr
        self.adapter = adapter

    def dispatch(
        self,
        project_id: str,
        decision: ScheduleDecision,
        policy: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, ManagedProcess]:
        task_id = decision.task_id
        contract = decision.task_contract

        # 1. State transition PENDING/BLOCKED -> READY -> CLAIMED
        current_status = self.task_repo.get(task_id)["status"]
        if current_status in (TaskState.PENDING.value, TaskState.BLOCKED.value):
            TaskStateMachine.transition(
                self.task_repo, task_id, TaskState.READY,
                event_repo=self.event_repo,
                reason="Dependencies satisfied; marked ready for scheduling"
            )

        TaskStateMachine.transition(
            self.task_repo, task_id, TaskState.CLAIMED,
            event_repo=self.event_repo,
            reason=f"Claimed by scheduler for account {decision.account_id}"
        )

        # 2. Create immutable execution record
        execution_id = f"exec_{uuid.uuid4().hex[:12]}"
        log_dir = Path.home() / ".gemini" / "antigravity-cli" / "logs" / project_id
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = str(log_dir / f"{task_id}_{execution_id}.log")
        except Exception:
            log_path = None

        exec_record = self.execution_repo.create(
            execution_id=execution_id,
            task_id=task_id,
            runtime_type="agy",
            account_id=decision.account_id,
            model=decision.model,
            status="PENDING",
            agent_print_timeout_seconds=contract.timeout_seconds,
            metadata={"account_id": decision.account_id, "log_path": log_path},
        )

        # 3. Claim write scope leases for expected output targets
        for write_path in contract.permission_profile.write_paths:
            self.workspace_mgr.ownership_manager.claim_ownership(
                project_id=project_id,
                path_pattern=write_path,
                owner_execution_id=execution_id,
                duration_seconds=contract.timeout_seconds + 60,
            )

        # 4. Build invocation and create managed process
        inv_policy = dict(policy or {})
        inv_policy["workspace_root"] = self.workspace_mgr.workspace_root
        invocation = self.adapter.build_invocation(contract.to_dict(), exec_record, inv_policy)

        # Atomic credential switch with startup grace period to prevent cross-account race conditions
        with CredentialSwitchLock():
            if decision.account_id:
                switch_credential_to_account(decision.account_id)
            process = ManagedProcess(invocation, log_path=log_path)
            process.start()
            if decision.account_id:
                time.sleep(0.4)

        # 5. Record PID and mark RUNNING
        self.execution_repo.mark_process_started(
            execution_id=execution_id,
            pid=process.pid,
            command_fingerprint=" ".join(invocation.command_args[:3]),
        )

        TaskStateMachine.transition(
            self.task_repo, task_id, TaskState.RUNNING,
            event_repo=self.event_repo,
            execution_id=execution_id,
            reason=f"Subprocess started with PID {process.pid}",
        )

        return execution_id, process
