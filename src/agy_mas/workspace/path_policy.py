"""Workspace path security and normalization policy."""

from pathlib import Path
from typing import Union


class PathPolicyError(ValueError):
    """Raised when an unsafe path attempts to escape the workspace root."""
    pass


class PathPolicy:
    """Enforces that all file operations are strictly confined within the workspace root."""

    def __init__(self, workspace_root: Union[str, Path]):
        self.workspace_root = Path(workspace_root).resolve()

    def resolve_safe_path(self, relative_or_absolute: Union[str, Path]) -> Path:
        """Resolves path and verifies it resides inside the workspace root without escaping."""
        target = Path(relative_or_absolute)
        if not target.is_absolute():
            resolved = (self.workspace_root / target).resolve()
        else:
            resolved = target.resolve()

        try:
            # Python 3.9+ is_relative_to
            is_inside = resolved.is_relative_to(self.workspace_root)
        except AttributeError:
            try:
                resolved.relative_to(self.workspace_root)
                is_inside = True
            except ValueError:
                is_inside = False

        if not is_inside:
            raise PathPolicyError(
                f"Path '{relative_or_absolute}' escapes workspace root '{self.workspace_root}'"
            )

        return resolved

    def get_relative_path(self, path: Union[str, Path]) -> str:
        """Returns clean forward-slash relative path within workspace."""
        resolved = self.resolve_safe_path(path)
        rel = resolved.relative_to(self.workspace_root)
        return str(rel).replace("\\", "/")
