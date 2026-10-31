"""Acceptance criteria checker evaluating contract verification rules."""

from typing import List, Dict, Any, Tuple
from ..planning.plan_schema import AcceptanceCriterion
from ..workspace.path_policy import PathPolicy


class AcceptanceChecker:
    """Evaluates criteria like EXIT_CODE_ZERO, NO_SOFT_DENIAL, and ARTIFACT_EXISTS."""

    def __init__(self, path_policy: PathPolicy):
        self.path_policy = path_policy

    def evaluate(
        self,
        criteria: List[AcceptanceCriterion],
        exit_code: int,
        has_soft_denial: bool,
    ) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        for c in criteria:
            ctype = c.criterion_type.upper()

            if ctype == "EXIT_CODE_ZERO":
                if exit_code != 0:
                    errors.append(f"Criterion failed: Process exited with code {exit_code} (expected 0).")

            elif ctype == "NO_SOFT_DENIAL":
                if has_soft_denial:
                    errors.append("Criterion failed: Permission soft denial was observed during headless execution.")

            elif ctype == "ARTIFACT_EXISTS":
                target_path = c.params.get("path")
                if not target_path:
                    errors.append("Criterion ARTIFACT_EXISTS missing 'path' parameter.")
                else:
                    try:
                        resolved = self.path_policy.resolve_safe_path(target_path)
                        if not resolved.exists():
                            errors.append(f"Criterion failed: Required artifact '{target_path}' does not exist.")
                    except Exception as e:
                        errors.append(f"Criterion failed resolving path '{target_path}': {e}")

        return (len(errors) == 0, errors)
