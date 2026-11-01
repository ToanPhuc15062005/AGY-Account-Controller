# main.py

> 86 nodes · cohesion 0.06

## Key Concepts

- **main.py** (38 connections) — `src/agy_mas/cli/main.py`
- **typing** (34 connections)
- **database.py** (25 connections) — `src/agy_mas/storage/database.py`
- **workspace_manager.py** (25 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **repositories/__init__.py** (21 connections) — `src/agy_mas/storage/repositories/__init__.py`
- **test_workspace.py** (20 connections) — `tests/unit/test_workspace.py`
- **test_e2e_acceptance.py** (19 connections) — `tests/integration/test_e2e_acceptance.py`
- **json** (18 connections)
- **agy_adapter.py** (18 connections) — `src/agy_mas/agents/adapters/agy_adapter.py`
- **base.py** (18 connections) — `src/agy_mas/agents/base.py`
- **datetime** (17 connections)
- **file_lock_manager.py** (17 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **WindowsFileRetryManager** (17 connections) — `src/agy_mas/workspace/file_lock_manager.py`
- **runner.py** (16 connections) — `src/agy_mas/storage/migrations/runner.py`
- **pathlib** (15 connections)
- **quota_tracker.py** (15 connections) — `src/agy_mas/resources/quota_tracker.py`
- **task_repo.py** (15 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **workspace/__init__.py** (15 connections) — `src/agy_mas/workspace/__init__.py`
- **snapshot_manager.py** (15 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **test_orchestrator.py** (15 connections) — `tests/unit/test_orchestrator.py`
- **resource_repo.py** (13 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **event_repo.py** (12 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **ownership_manager.py** (12 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **path_policy.py** (12 connections) — `src/agy_mas/workspace/path_policy.py`
- **SnapshotManager** (12 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- *... and 61 more nodes in this community*

## Relationships

- [orchestrator.py](orchestrator.py.md) (41 shared connections)
- [TaskContract](TaskContract.md) (28 shared connections)
- [ResourceRepository](ResourceRepository.md) (26 shared connections)
- [config.py](config.py.md) (22 shared connections)
- [PathPolicy](PathPolicy.md) (18 shared connections)
- [agy_controller.py](agy_controller.py.md) (13 shared connections)
- [Database](Database.md) (11 shared connections)
- [process_manager.py](process_manager.py.md) (9 shared connections)
- [MigrationRunner](MigrationRunner.md) (7 shared connections)
- [MockAdapter](MockAdapter.md) (5 shared connections)
- [EventRepository](EventRepository.md) (5 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (4 shared connections)

## Source Files

- `src/agy_mas/agents/adapters/agy_adapter.py`
- `src/agy_mas/agents/base.py`
- `src/agy_mas/cli/main.py`
- `src/agy_mas/resources/quota_tracker.py`
- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/migrations/runner.py`
- `src/agy_mas/storage/repositories/__init__.py`
- `src/agy_mas/storage/repositories/approval_repo.py`
- `src/agy_mas/storage/repositories/artifact_repo.py`
- `src/agy_mas/storage/repositories/event_repo.py`
- `src/agy_mas/storage/repositories/execution_repo.py`
- `src/agy_mas/storage/repositories/project_repo.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`
- `src/agy_mas/workspace/__init__.py`
- `src/agy_mas/workspace/file_lock_manager.py`
- `src/agy_mas/workspace/ownership_manager.py`
- `src/agy_mas/workspace/path_policy.py`
- `src/agy_mas/workspace/snapshot_manager.py`
- `src/agy_mas/workspace/workspace_manager.py`

## Audit Trail

- EXTRACTED: 428 (97%)
- INFERRED: 14 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*