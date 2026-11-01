# Community 6

> 24 nodes · cohesion 0.14

## Key Concepts

- **workspace_manager.py** (25 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **test_workspace.py** (20 connections) — `tests/unit/test_workspace.py`
- **file_lock_manager.py** (17 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **WindowsFileRetryManager** (17 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **pathlib** (15 connections)
- **workspace/__init__.py** (15 connections) — `src/agy_mas/workspace/__init__.py`
- **snapshot_manager.py** (15 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **SnapshotManager** (12 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **artifact_repo.py** (11 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **windows_file_retry()** (6 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **.__init__()** (3 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **decorator()** (2 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **functools** (1 connections)
- **hashlib** (1 connections)
- **random** (1 connections)
- **Artifact repository for tracking deliverables, logs, and output products.** (1 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **Windows file lock manager with bounded retry and backoff for WinError 32/33.** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Executes file operations with exponential backoff and jitter for Windows…** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Decorator for automatic Windows file contention retry.** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **wrapper()** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Stable snapshot manager calculating artifact hashes only after process exit.** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Manages file hashes and artifact snapshots adhering strictly to ADR-016.** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Workspace manager coordinating path policies, ownership leases, and artifact…** (1 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **Unit tests for Phase 4: Shared Workspace, Path Policy, Windows Retries,…** (1 connections) — `tests/unit/test_workspace.py`

## Relationships

- [Community 3](Community_3.md) (16 shared connections)
- [Community 5](Community_5.md) (12 shared connections)
- [Community 4](Community_4.md) (11 shared connections)
- [Community 0](Community_0.md) (11 shared connections)
- [Community 11](Community_11.md) (11 shared connections)
- [Community 8](Community_8.md) (8 shared connections)
- [Community 13](Community_13.md) (5 shared connections)
- [Community 16](Community_16.md) (5 shared connections)
- [Community 17](Community_17.md) (3 shared connections)
- [Community 2](Community_2.md) (2 shared connections)
- [Community 1](Community_1.md) (2 shared connections)
- [Community 7](Community_7.md) (2 shared connections)

## Source Files

- `src/agy_mas/storage/repositories/artifact_repo.py`
- `src/agy_mas/workspace/__init__.py`
- `src/agy_mas/workspace/file_lock_manager.py`
- `src/agy_mas/workspace/snapshot_manager.py`
- `src/agy_mas/workspace/workspace_manager.py`
- `tests/unit/test_workspace.py`

## Audit Trail

- EXTRACTED: 119 (92%)
- INFERRED: 11 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*