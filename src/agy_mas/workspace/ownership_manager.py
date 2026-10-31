"""File and path ownership manager enforcing lease-based write permissions."""

import fnmatch
import uuid
import datetime
from typing import Optional, List, Dict, Any
from ..storage.repositories.resource_repo import ResourceRepository


class OwnershipConflictError(PermissionError):
    """Raised when an execution attempts to claim or write to a path owned by another execution."""
    pass


class OwnershipManager:
    """Manages path pattern leases and verifies file modification privileges."""

    def __init__(self, resource_repo: ResourceRepository):
        self.resource_repo = resource_repo

    def claim_ownership(
        self,
        project_id: str,
        path_pattern: str,
        owner_execution_id: str,
        duration_seconds: int = 900,
        access_mode: str = "WRITE",
        lease_version: int = 1,
    ) -> str:
        """Claims a path pattern lease for an execution attempt."""
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        expires_at = (now_dt + datetime.timedelta(seconds=duration_seconds)).isoformat()
        ownership_id = f"own_{uuid.uuid4().hex[:12]}"

        # Check existing active ownerships in this project
        rows = self.resource_repo.db.fetchall(
            """
            SELECT * FROM file_ownerships
            WHERE project_id = ? AND expires_at > ?;
            """,
            (project_id, now_dt.isoformat()),
        )

        norm_pattern = path_pattern.replace("\\", "/").strip("/")
        for r in rows:
            if r["owner_execution_id"] != owner_execution_id and r["access_mode"] == "WRITE":
                existing_pattern = r["path_pattern"].replace("\\", "/").strip("/")
                if (
                    norm_pattern == existing_pattern
                    or fnmatch.fnmatch(norm_pattern, existing_pattern)
                    or fnmatch.fnmatch(existing_pattern, norm_pattern)
                    or norm_pattern.startswith(existing_pattern + "/")
                    or existing_pattern.startswith(norm_pattern + "/")
                ):
                    raise OwnershipConflictError(
                        f"Path '{path_pattern}' conflicts with active write lease by execution '{r['owner_execution_id']}'"
                    )

        self.resource_repo.claim_file_ownership(
            ownership_id=ownership_id,
            project_id=project_id,
            path_pattern=path_pattern,
            access_mode=access_mode,
            owner_execution_id=owner_execution_id,
            expires_at=expires_at,
            lease_version=lease_version,
        )
        return ownership_id

    def check_write_permitted(self, project_id: str, execution_id: str, relative_path: str) -> bool:
        """Checks if the given execution owns a valid, unexpired write lease for the path."""
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rows = self.resource_repo.db.fetchall(
            """
            SELECT * FROM file_ownerships
            WHERE project_id = ? AND owner_execution_id = ? AND access_mode = 'WRITE' AND expires_at > ?;
            """,
            (project_id, execution_id, now_str),
        )
        norm_path = relative_path.replace("\\", "/").strip("/")
        for r in rows:
            pattern = r["path_pattern"].replace("\\", "/").strip("/")
            if fnmatch.fnmatch(norm_path, pattern) or norm_path.startswith(pattern.rstrip("*").rstrip("/")):
                return True
        return False

    def release_all(self, execution_id: str) -> None:
        self.resource_repo.release_all_for_execution(execution_id)
