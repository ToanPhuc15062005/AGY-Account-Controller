"""Workspace manager coordinating path policies, ownership leases, and artifact snapshots."""

from pathlib import Path
from typing import Optional, Dict, Any, List
from .path_policy import PathPolicy
from .file_lock_manager import WindowsFileRetryManager
from .ownership_manager import OwnershipManager
from .snapshot_manager import SnapshotManager
from ..storage.repositories.resource_repo import ResourceRepository
from ..storage.repositories.artifact_repo import ArtifactRepository
from ..config import WorkspaceConfig


class WorkspaceManager:
    """Central interface for shared workspace safety, file locks, and artifacts."""

    def __init__(
        self,
        workspace_root: str,
        resource_repo: ResourceRepository,
        artifact_repo: ArtifactRepository,
        config: Optional[WorkspaceConfig] = None,
    ):
        self.workspace_root = workspace_root
        self.resource_repo = resource_repo
        self.artifact_repo = artifact_repo
        self.config = config or WorkspaceConfig()

        self.path_policy = PathPolicy(workspace_root)
        self.retry_manager = WindowsFileRetryManager(self.config.windows_file_retry)
        self.ownership_manager = OwnershipManager(resource_repo)
        self.snapshot_manager = SnapshotManager(self.path_policy, self.retry_manager)

    def register_task_artifacts(
        self,
        project_id: str,
        task_id: str,
        execution_id: str,
        expected_artifacts: List[Dict[str, Any]],
        process: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        """Snapshots deliverables and commits them to the artifact repository."""
        registered = []
        for art_spec in expected_artifacts:
            path_str = art_spec.get("path")
            if not path_str:
                continue

            snap = self.snapshot_manager.snapshot_file(path_str, process=process)
            if snap["exists"]:
                record = self.artifact_repo.register(
                    project_id=project_id,
                    task_id=task_id,
                    execution_id=execution_id,
                    path=snap["path"],
                    artifact_type=art_spec.get("artifact_type", "FILE"),
                    checksum=snap["checksum"],
                    metadata={"size_bytes": snap["size_bytes"]},
                )
                registered.append(record)
        return registered
