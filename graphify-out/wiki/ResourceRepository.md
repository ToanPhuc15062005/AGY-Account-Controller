# ResourceRepository

> 35 nodes · cohesion 0.10

## Key Concepts

- **ResourceRepository** (41 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **WorkspaceManager** (25 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **QuotaTracker** (24 connections) — `src/agy_mas/resources/quota_tracker.py`
- **TestWorkspaceCoordination** (24 connections) — `tests/unit/test_workspace.py`
- **.__init__()** (13 connections) — `src/agy_mas/core/orchestrator.py`
- **OwnershipManager** (13 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.setUp()** (13 connections) — `tests/integration/test_e2e_acceptance.py`
- **.setUp()** (12 connections) — `tests/unit/test_workspace.py`
- **.setUp()** (11 connections) — `tests/unit/test_orchestrator.py`
- **.__init__()** (8 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **.setUp()** (6 connections) — `tests/unit/test_agy_adapter.py`
- **.__init__()** (4 connections) — `src/agy_mas/core/scheduler.py`
- **.is_available()** (4 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.select_eligible_account()** (4 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.clear_account_model_cooldown()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.is_in_cooldown()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_all_for_execution()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.claim_ownership()** (4 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.__init__()** (3 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.claim_file_ownership()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **resources/__init__.py** (2 connections) — `src/agy_mas/resources/__init__.py`
- **.clear_cooldown()** (2 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.check_write_permitted()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.__init__()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.release_all()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- *... and 10 more nodes in this community*

## Relationships

- [main.py](main.py.md) (26 shared connections)
- [orchestrator.py](orchestrator.py.md) (20 shared connections)
- [MigrationRunner](MigrationRunner.md) (11 shared connections)
- [.transaction](transaction.md) (8 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (7 shared connections)
- [EventRepository](EventRepository.md) (7 shared connections)
- [config.py](config.py.md) (7 shared connections)
- [Database](Database.md) (7 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (6 shared connections)
- [TaskRepository](TaskRepository.md) (6 shared connections)
- [PathPolicy](PathPolicy.md) (6 shared connections)
- [TaskContract](TaskContract.md) (4 shared connections)

## Source Files

- `src/agy_mas/core/orchestrator.py`
- `src/agy_mas/core/scheduler.py`
- `src/agy_mas/resources/__init__.py`
- `src/agy_mas/resources/quota_tracker.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/workspace/ownership_manager.py`
- `src/agy_mas/workspace/workspace_manager.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_agy_adapter.py`
- `tests/unit/test_orchestrator.py`
- `tests/unit/test_workspace.py`

## Audit Trail

- EXTRACTED: 125 (67%)
- INFERRED: 61 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*