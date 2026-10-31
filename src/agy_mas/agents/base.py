"""Base classes and contracts for MAS Agent Runtime Adapters (Section 9 & Section 13)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Iterator


@dataclass
class RuntimeCapabilities:
    runtime_name: str
    version: str
    supports_print_mode: bool = True
    supports_stream_json: bool = True
    supports_scoped_permissions: bool = True
    supported_models: List[str] = field(default_factory=list)


@dataclass
class Invocation:
    command_args: List[str]
    env: Dict[str, str] = field(default_factory=dict)
    cwd: Optional[str] = None
    timeout_seconds: int = 900
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeEvent:
    event_type: str
    timestamp: str
    raw_data: Any = None
    message: Optional[str] = None
    error_type: Optional[str] = None
    structured_payload: Optional[Dict[str, Any]] = None


@dataclass
class FailureClassification:
    error_type: str
    retryable: bool
    cooldown_required: bool
    reason: str
    cooldown_seconds: Optional[int] = None
    retry_after_seconds: Optional[int] = None
    evidence_source: str = "structured"  # structured or pattern


@dataclass
class TerminationResult:
    success: bool
    processes_terminated: int
    residual_processes: int
    termination_reason: str


class AgentRuntimeAdapter(ABC):
    """Abstract contract isolating provider-specific CLI behavior behind adapters."""

    @abstractmethod
    def validate_runtime(self) -> RuntimeCapabilities:
        """Validates runtime CLI availability, version, and supported flags."""
        pass

    @abstractmethod
    def build_invocation(
        self,
        task_contract: Dict[str, Any],
        execution_record: Dict[str, Any],
        policy: Optional[Dict[str, Any]] = None,
    ) -> Invocation:
        """Constructs safe CLI invocation arguments according to task contract and policy."""
        pass

    @abstractmethod
    def classify_failure(
        self,
        exit_code: int,
        stdout_tail: str,
        stderr_tail: str,
        events: Optional[List[RuntimeEvent]] = None,
    ) -> FailureClassification:
        """Maps process exit and runtime output into the typed error taxonomy."""
        pass

    @abstractmethod
    def parse_line(self, line: str) -> Optional[RuntimeEvent]:
        """Parses a single stdout/stderr line into a typed RuntimeEvent."""
        pass
