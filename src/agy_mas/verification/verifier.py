"""Verification engine enforcing that process success alone cannot accept a task."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..planning.plan_schema import TaskContract
from ..workspace.path_policy import PathPolicy
from .artifact_checker import ArtifactChecker
from .scope_checker import ScopeChecker
from .acceptance_checker import AcceptanceChecker


@dataclass
class VerificationReport:
    passed: bool
    errors: List[str] = field(default_factory=list)
    artifacts_verified: int = 0


class Verifier:
    """Orchestrates comprehensive task verification according to ADR-014 and ADR-017."""

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.path_policy = PathPolicy(workspace_root)
        self.artifact_checker = ArtifactChecker(self.path_policy)
        self.acceptance_checker = AcceptanceChecker(self.path_policy)

    def verify_task(
        self,
        contract: TaskContract,
        exit_code: int,
        has_soft_denial: bool,
        touched_paths: Optional[List[str]] = None,
    ) -> VerificationReport:
        errors: List[str] = []

        # 1. Soft-denial check (ADR-014)
        if has_soft_denial:
            errors.append("Task cannot be accepted: Permission soft denial was detected in headless mode.")

        # 2. Exit code check
        if exit_code != 0:
            errors.append(f"Task process failed with exit code {exit_code}.")

        # 3. Expected artifacts check
        art_ok, art_errors = self.artifact_checker.check_artifacts(contract.outputs.expected_artifacts)
        if not art_ok:
            errors.extend(art_errors)

        # 4. Scope enforcement check
        if touched_paths:
            scope_checker = ScopeChecker(contract.permission_profile)
            scope_ok, scope_errors = scope_checker.check_paths(touched_paths)
            if not scope_ok:
                errors.extend(scope_errors)

        # 5. Acceptance criteria check
        crit_ok, crit_errors = self.acceptance_checker.evaluate(
            contract.acceptance_criteria, exit_code, has_soft_denial
        )
        if not crit_ok:
            errors.extend(crit_errors)

        return VerificationReport(
            passed=(len(errors) == 0),
            errors=errors,
            artifacts_verified=len(contract.outputs.expected_artifacts),
        )
