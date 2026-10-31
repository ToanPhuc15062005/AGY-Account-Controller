"""Stable snapshot manager calculating artifact hashes only after process exit."""

import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from .path_policy import PathPolicy
from .file_lock_manager import WindowsFileRetryManager
from ..agents.process_manager import ManagedProcess


class SnapshotTimingError(RuntimeError):
    """Raised when an artifact snapshot is attempted while a worker process is still alive."""
    pass


class SnapshotManager:
    """Manages file hashes and artifact snapshots adhering strictly to ADR-016."""

    def __init__(self, path_policy: PathPolicy, retry_manager: Optional[WindowsFileRetryManager] = None):
        self.path_policy = path_policy
        self.retry_manager = retry_manager or WindowsFileRetryManager()

    def snapshot_file(self, relative_path: str, process: Optional[Any] = None) -> Dict[str, Any]:
        """Calculates file checksum and metadata after verifying process is terminated."""
        if process and hasattr(process, "is_alive") and process.is_alive():
            raise SnapshotTimingError(
                f"Cannot snapshot '{relative_path}': process tree is still running. "
                "ADR-016 requires process-tree exit before workspace snapshot."
            )

        full_path = self.path_policy.resolve_safe_path(relative_path)
        if not full_path.exists():
            return {
                "path": relative_path,
                "exists": False,
                "size_bytes": 0,
                "checksum": None,
            }

        def _read_and_hash():
            hasher = hashlib.sha256()
            total_size = 0
            with open(full_path, "rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
                    total_size += len(chunk)
            return hasher.hexdigest(), total_size

        # Wrap in Windows bounded retry to prevent sharing violations during compiler teardown
        checksum, size = self.retry_manager.execute_with_retry(_read_and_hash)

        return {
            "path": relative_path,
            "exists": True,
            "size_bytes": size,
            "checksum": checksum,
        }
