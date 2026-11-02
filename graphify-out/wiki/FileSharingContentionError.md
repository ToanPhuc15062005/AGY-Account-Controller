# FileSharingContentionError

> 18 nodes · cohesion 0.11

## Key Concepts

- **FileSharingContentionError** (8 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **.execute_with_retry()** (7 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **.test_windows_file_retry_backoff()** (6 connections) — `tests/unit/test_workspace.py`
- **.test_WIN_01_windows_file_sharing_retry()** (5 connections) — `tests/integration/test_e2e_acceptance.py`
- **is_windows_sharing_violation()** (4 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **4.2. Xử lý Xung đột Khóa File Windows: WinError 32/33 (`file_lock_manager.py`)** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Giải pháp trong `WindowsFileRetryManager`:** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Bản chất kỹ thuật của `WinError 32` & `WinError 33`:** (1 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Exception** (1 connections)
- **IOError** (1 connections)
- **Any** (1 connections)
- **Raised when file access retries are exhausted due to concurrent Windows file…** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Checks if exception is WinError 32 (sharing violation) or 33 (lock violation).** (1 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **T** (1 connections)
- **WIN-01: Windows file sharing retry overcomes transient lock contention.** (1 connections) — `tests/integration/test_e2e_acceptance.py`
- **transient_locked_read()** (1 connections) — `tests/integration/test_e2e_acceptance.py`
- **always_locked()** (1 connections) — `tests/unit/test_workspace.py`
- **flaky_file_op()** (1 connections) — `tests/unit/test_workspace.py`

## Relationships

- [WindowsFileRetryManager](WindowsFileRetryManager.md) (8 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (2 shared connections)
- [.snapshot_file](snapshot_file.md) (1 shared connections)
- [7.2. Integration Acceptance Criteria](7.2._Integration_Acceptance_Criteria.md) (1 shared connections)
- [TaskContract](TaskContract.md) (1 shared connections)

## Source Files

- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/workspace/file_lock_manager.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_workspace.py`

## Audit Trail

- EXTRACTED: 21 (70%)
- INFERRED: 9 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*