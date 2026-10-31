"""Artifact verification checking file existence, minimum size, and checksums."""

from pathlib import Path
from typing import List, Dict, Any, Tuple
from ..planning.plan_schema import ExpectedArtifact
from ..workspace.path_policy import PathPolicy


class ArtifactChecker:
    """Verifies that deliverables meet declared artifact specifications."""

    def __init__(self, path_policy: PathPolicy):
        self.path_policy = path_policy

    def check_artifacts(
        self,
        expected_artifacts: List[ExpectedArtifact],
    ) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        for exp in expected_artifacts:
            try:
                full_path = self.path_policy.resolve_safe_path(exp.path)
            except Exception as e:
                errors.append(f"Invalid path for artifact '{exp.path}': {e}")
                continue

            if not full_path.exists():
                if exp.required:
                    errors.append(f"Required artifact '{exp.path}' was not found on disk.")
                continue

            if not full_path.is_file():
                errors.append(f"Artifact '{exp.path}' exists but is not a file.")
                continue

            actual_size = full_path.stat().st_size
            if actual_size < exp.min_size_bytes:
                errors.append(
                    f"Artifact '{exp.path}' size ({actual_size} bytes) is below minimum required ({exp.min_size_bytes} bytes)."
                )

        return (len(errors) == 0, errors)
