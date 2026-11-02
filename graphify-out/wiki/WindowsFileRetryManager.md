# WindowsFileRetryManager

> 25 nodes · cohesion 0.13

## Key Concepts

- **WindowsFileRetryManager** (27 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **SnapshotManager** (18 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **file_lock_manager.py** (17 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **workspace/__init__.py** (15 connections) — `src/agy_mas/workspace/__init__.py`
- **snapshot_manager.py** (15 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **7. Ma trận Kiểm thử & Đối sánh Chuẩn Kiến trúc v1.1** (9 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **4.3. Chuyên Đề 03 — Agents, Workspace & Process Isolation** (8 connections) — `docs/study_guide/00_master_study_guide.md`
- **WindowsFileRetryConfig** (8 connections) — `src/agy_mas/config.py`
- **.__init__()** (8 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **SnapshotTimingError** (7 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **windows_file_retry()** (6 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **.__init__()** (3 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **decorator()** (2 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **.__init__()** (2 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **functools** (1 connections)
- **hashlib** (1 connections)
- **random** (1 connections)
- **RuntimeError** (1 connections)
- **Windows file lock manager with bounded retry and backoff for WinError 32/33.** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Executes file operations with exponential backoff and jitter for Windows…** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Decorator for automatic Windows file contention retry.** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **wrapper()** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Stable snapshot manager calculating artifact hashes only after process exit.** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Raised when an artifact snapshot is attempted while a worker process is still…** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Manages file hashes and artifact snapshots adhering strictly to ADR-016.** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`

## Relationships

- [main.py](main.py.md) (13 shared connections)
- [PathPolicy](PathPolicy.md) (12 shared connections)
- [ResourceRepository](ResourceRepository.md) (8 shared connections)
- [FileSharingContentionError](FileSharingContentionError.md) (8 shared connections)
- [OwnershipManager](OwnershipManager.md) (6 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (5 shared connections)
- [config.py](config.py.md) (4 shared connections)
- [.snapshot_file](snapshot_file.md) (3 shared connections)
- [ManagedProcess](ManagedProcess.md) (2 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (2 shared connections)
- [.resolve_safe_path](resolve_safe_path.md) (2 shared connections)
- [agy_controller.py](agy_controller.py.md) (2 shared connections)

## Source Files

- `docs/study_guide/00_master_study_guide.md`
- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/config.py`
- `src/agy_mas/workspace/__init__.py`
- `src/agy_mas/workspace/file_lock_manager.py`
- `src/agy_mas/workspace/snapshot_manager.py`
- `src/agy_mas/workspace/workspace_manager.py`

## Audit Trail

- EXTRACTED: 76 (66%)
- INFERRED: 40 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*