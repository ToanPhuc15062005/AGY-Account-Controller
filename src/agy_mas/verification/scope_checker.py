"""Scope checker verifying that worker modifications remain strictly inside declared write scopes."""

from typing import List, Tuple
from ..planning.plan_schema import PermissionProfile


class ScopeChecker:
    """Verifies that touched paths adhere to task write scopes."""

    def __init__(self, permission_profile: PermissionProfile):
        self.permission_profile = permission_profile

    def check_paths(self, touched_relative_paths: List[str]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        for path in touched_relative_paths:
            if not self.permission_profile.allows_write(path):
                errors.append(
                    f"Out-of-scope write detected: '{path}' is not covered by task write paths: {self.permission_profile.write_paths}"
                )
        return (len(errors) == 0, errors)
