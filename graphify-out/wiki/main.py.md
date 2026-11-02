# main.py

> 73 nodes · cohesion 0.08

## Key Concepts

- **orchestrator.py** (40 connections) — `src/agy_mas/core/orchestrator.py`
- **typing** (36 connections)
- **dispatcher.py** (29 connections) — `src/agy_mas/core/dispatcher.py`
- **database.py** (27 connections) — `src/agy_mas/storage/database.py`
- **workspace_manager.py** (26 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **repositories/__init__.py** (24 connections) — `src/agy_mas/storage/repositories/__init__.py`
- **process_manager.py** (22 connections) — `src/agy_mas/agents/process_manager.py`
- **test_pair_programming.py** (20 connections) — `tests/unit/test_pair_programming.py`
- **test_workspace.py** (20 connections) — `tests/unit/test_workspace.py`
- **datetime** (19 connections)
- **test_e2e_acceptance.py** (19 connections) — `tests/integration/test_e2e_acceptance.py`
- **pathlib** (18 connections)
- **scheduler.py** (18 connections) — `src/agy_mas/core/scheduler.py`
- **runner.py** (17 connections) — `src/agy_mas/storage/migrations/runner.py`
- **state_machine.py** (16 connections) — `src/agy_mas/core/state_machine.py`
- **quota_tracker.py** (16 connections) — `src/agy_mas/resources/quota_tracker.py`
- **task_repo.py** (15 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **test_orchestrator.py** (15 connections) — `tests/unit/test_orchestrator.py`
- **resource_repo.py** (13 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **shutil** (12 connections)
- **event_repo.py** (12 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **ownership_manager.py** (12 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **test_task_engine.py** (12 connections) — `tests/unit/test_task_engine.py`
- **test_verification_recovery.py** (12 connections) — `tests/unit/test_verification_recovery.py`
- **core/__init__.py** (11 connections) — `src/agy_mas/core/__init__.py`
- *... and 48 more nodes in this community*

## Relationships

- [agy_controller.py](agy_controller.py.md) (32 shared connections)
- [TaskContract](TaskContract.md) (29 shared connections)
- [Database](Database.md) (27 shared connections)
- [ResourceRepository](ResourceRepository.md) (22 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (13 shared connections)
- [PathPolicy](PathPolicy.md) (12 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (12 shared connections)
- [main.py](main.py.md) (11 shared connections)
- [TaskStateMachine](TaskStateMachine.md) (9 shared connections)
- [AGYAdapter](AGYAdapter.md) (7 shared connections)
- [config.py](config.py.md) (7 shared connections)
- [TaskRepository](TaskRepository.md) (6 shared connections)

## Source Files

- `src/agy_mas/agents/process_manager.py`
- `src/agy_mas/core/__init__.py`
- `src/agy_mas/core/dispatcher.py`
- `src/agy_mas/core/orchestrator.py`
- `src/agy_mas/core/scheduler.py`
- `src/agy_mas/core/state_machine.py`
- `src/agy_mas/resources/__init__.py`
- `src/agy_mas/resources/quota_tracker.py`
- `src/agy_mas/storage/__init__.py`
- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/migrations/__init__.py`
- `src/agy_mas/storage/migrations/runner.py`
- `src/agy_mas/storage/repositories/__init__.py`
- `src/agy_mas/storage/repositories/approval_repo.py`
- `src/agy_mas/storage/repositories/artifact_repo.py`
- `src/agy_mas/storage/repositories/event_repo.py`
- `src/agy_mas/storage/repositories/execution_repo.py`
- `src/agy_mas/storage/repositories/project_repo.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/review_repo.py`

## Audit Trail

- EXTRACTED: 427 (99%)
- INFERRED: 5 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*