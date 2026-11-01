# config.py

> 34 nodes · cohesion 0.08

## Key Concepts

- **config.py** (20 connections) — `src/agy_mas/config.py`
- **.from_dict()** (11 connections) — `src/agy_mas/config.py`
- **WindowsFileRetryConfig** (8 connections) — `src/agy_mas/config.py`
- **MASConfig** (7 connections) — `src/agy_mas/config.py`
- **.execute_with_retry()** (7 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **get_active_workers_info()** (6 connections) — `agy_controller.py`
- **.load()** (6 connections) — `src/agy_mas/config.py`
- **FileSharingContentionError** (6 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **.test_windows_file_retry_backoff()** (6 connections) — `tests/unit/test_workspace.py`
- **dataclasses** (5 connections)
- **QuotaConfig** (5 connections) — `src/agy_mas/config.py`
- **WorkspaceConfig** (5 connections) — `src/agy_mas/config.py`
- **.test_WIN_01_windows_file_sharing_retry()** (5 connections) — `tests/integration/test_e2e_acceptance.py`
- **is_windows_sharing_violation()** (4 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **FailoverConfig** (2 connections) — `src/agy_mas/config.py`
- **QuotaCooldownConfig** (2 connections) — `src/agy_mas/config.py`
- **QuotaDetectionConfig** (2 connections) — `src/agy_mas/config.py`
- **RuntimeConfig** (2 connections) — `src/agy_mas/config.py`
- **StorageConfig** (2 connections) — `src/agy_mas/config.py`
- **.__init__()** (2 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **Kiểm tra xem hiện tại có worker MAS hoặc tiến trình song song nào đang chạy…** (1 connections) — `agy_controller.py`
- **Exception** (1 connections)
- **IOError** (1 connections)
- **Any** (1 connections)
- **Configuration module for AGY-MAS (Multi-Agent System). Defines configuration…** (1 connections) — `src/agy_mas/config.py`
- *... and 9 more nodes in this community*

## Relationships

- [main.py](main.py.md) (22 shared connections)
- [ResourceRepository](ResourceRepository.md) (7 shared connections)
- [agy_controller.py](agy_controller.py.md) (4 shared connections)
- [orchestrator.py](orchestrator.py.md) (2 shared connections)
- [TaskContract](TaskContract.md) (2 shared connections)
- [EventRepository](EventRepository.md) (2 shared connections)
- [Database](Database.md) (1 shared connections)
- [PathPolicy](PathPolicy.md) (1 shared connections)

## Source Files

- `agy_controller.py`
- `src/agy_mas/config.py`
- `src/agy_mas/workspace/file_lock_manager.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_workspace.py`

## Audit Trail

- EXTRACTED: 69 (82%)
- INFERRED: 15 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*