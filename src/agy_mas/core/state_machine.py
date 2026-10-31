"""Authoritative Task State Machine for AGY-MAS, enforcing strict lifecycle rules."""

from enum import Enum
from typing import Set, Dict, Optional, Any
from ..storage.repositories.task_repo import TaskRepository
from ..storage.repositories.event_repo import EventRepository


class TaskState(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    BLOCKED = "BLOCKED"
    CLAIMED = "CLAIMED"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    RETRY_WAIT = "RETRY_WAIT"
    ACCEPTED = "ACCEPTED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"


class InvalidStateTransitionError(ValueError):
    """Raised when an illegal state transition is attempted."""
    pass


class TaskStateMachine:
    """Enforces state transition rules and logs lifecycle events."""

    VALID_TRANSITIONS: Dict[TaskState, Set[TaskState]] = {
        TaskState.PENDING: {TaskState.READY, TaskState.BLOCKED, TaskState.CANCELLED},
        TaskState.BLOCKED: {TaskState.READY, TaskState.CANCELLED},
        TaskState.READY: {TaskState.CLAIMED, TaskState.CANCELLED},
        TaskState.CLAIMED: {TaskState.RUNNING, TaskState.RETRY_WAIT, TaskState.CANCELLED},
        TaskState.RUNNING: {
            TaskState.VERIFYING,
            TaskState.RETRY_WAIT,
            TaskState.FAILED,
            TaskState.TIMEOUT,
            TaskState.CANCELLED,
        },
        TaskState.VERIFYING: {TaskState.ACCEPTED, TaskState.RETRY_WAIT, TaskState.FAILED},
        TaskState.RETRY_WAIT: {TaskState.READY, TaskState.FAILED, TaskState.CANCELLED},
        TaskState.TIMEOUT: {TaskState.RETRY_WAIT, TaskState.FAILED},
        TaskState.ACCEPTED: set(),  # terminal
        TaskState.FAILED: set(),    # terminal
        TaskState.CANCELLED: set(), # terminal
    }

    TERMINAL_STATES = {TaskState.ACCEPTED, TaskState.FAILED, TaskState.CANCELLED}

    @classmethod
    def can_transition(cls, current_state: str, target_state: str) -> bool:
        try:
            curr = TaskState(current_state)
            target = TaskState(target_state)
        except ValueError:
            return False

        return target in cls.VALID_TRANSITIONS.get(curr, set())

    @classmethod
    def is_terminal(cls, state: str) -> bool:
        try:
            return TaskState(state) in cls.TERMINAL_STATES
        except ValueError:
            return False

    @classmethod
    def transition(
        cls,
        task_repo: TaskRepository,
        task_id: str,
        target_state: str,
        event_repo: Optional[EventRepository] = None,
        reason: Optional[str] = None,
        execution_id: Optional[str] = None,
        extra_payload: Optional[Dict[str, Any]] = None,
    ) -> bool:
        task = task_repo.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        current_state = task["status"]
        if current_state == target_state:
            return True  # Idempotent no-op

        if not cls.can_transition(current_state, target_state):
            raise InvalidStateTransitionError(
                f"Invalid transition for task '{task_id}': cannot move from '{current_state}' to '{target_state}'"
            )

        updated = task_repo.update_status(task_id, target_state)
        if updated and event_repo:
            payload = {
                "task_id": task_id,
                "previous_state": current_state,
                "new_state": target_state,
                "reason": reason,
            }
            if extra_payload:
                payload.update(extra_payload)

            event_repo.append(
                project_id=task["project_id"],
                event_type=f"TASK_STATE_{target_state}",
                payload=payload,
                task_id=task_id,
                execution_id=execution_id,
            )

        return updated
