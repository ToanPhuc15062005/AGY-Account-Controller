# orchestrator.py

> 64 nodes · cohesion 0.06

## Key Concepts

- **orchestrator.py** (34 connections) — `src/agy_mas/core/orchestrator.py`
- **dispatcher.py** (28 connections) — `src/agy_mas/core/dispatcher.py`
- **Orchestrator** (19 connections) — `src/agy_mas/core/orchestrator.py`
- **scheduler.py** (18 connections) — `src/agy_mas/core/scheduler.py`
- **recovery_manager.py** (18 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **.tick()** (17 connections) — `src/agy_mas/core/orchestrator.py`
- **credential_provider.py** (16 connections) — `src/agy_mas/accounts/credential_provider.py`
- **state_machine.py** (15 connections) — `src/agy_mas/core/state_machine.py`
- **.transition()** (15 connections) — `src/agy_mas/core/state_machine.py`
- **TaskStateMachine** (14 connections) — `src/agy_mas/core/state_machine.py`
- **.dispatch()** (13 connections) — `src/agy_mas/core/dispatcher.py`
- **Scheduler** (13 connections) — `src/agy_mas/core/scheduler.py`
- **TaskState** (13 connections) — `src/agy_mas/core/state_machine.py`
- **CredentialSwitchLock** (11 connections) — `src/agy_mas/accounts/credential_provider.py`
- **core/__init__.py** (11 connections) — `src/agy_mas/core/__init__.py`
- **RecoveryManager** (11 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **TestOrchestrator** (10 connections) — `tests/unit/test_orchestrator.py`
- **Dispatcher** (9 connections) — `src/agy_mas/core/dispatcher.py`
- **os** (7 connections)
- **ScheduleDecision** (7 connections) — `src/agy_mas/core/scheduler.py`
- **subprocess** (7 connections)
- **InvalidStateTransitionError** (6 connections) — `src/agy_mas/core/state_machine.py`
- **is_pid_alive()** (6 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **time** (6 connections)
- **.test_orchestrator_quota_failover_to_alternative_account()** (4 connections) — `tests/unit/test_orchestrator.py`
- *... and 39 more nodes in this community*

## Relationships

- [main.py](main.py.md) (41 shared connections)
- [TaskContract](TaskContract.md) (21 shared connections)
- [ResourceRepository](ResourceRepository.md) (20 shared connections)
- [agy_controller.py](agy_controller.py.md) (12 shared connections)
- [TaskRepository](TaskRepository.md) (12 shared connections)
- [process_manager.py](process_manager.py.md) (10 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (10 shared connections)
- [EventRepository](EventRepository.md) (9 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (5 shared connections)
- [MigrationRunner](MigrationRunner.md) (5 shared connections)
- [MockAdapter](MockAdapter.md) (3 shared connections)
- [config.py](config.py.md) (2 shared connections)

## Source Files

- `src/agy_mas/accounts/__init__.py`
- `src/agy_mas/accounts/credential_provider.py`
- `src/agy_mas/core/__init__.py`
- `src/agy_mas/core/dispatcher.py`
- `src/agy_mas/core/orchestrator.py`
- `src/agy_mas/core/scheduler.py`
- `src/agy_mas/core/state_machine.py`
- `src/agy_mas/recovery/__init__.py`
- `src/agy_mas/recovery/recovery_manager.py`
- `src/agy_mas/storage/repositories/execution_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`
- `tests/unit/test_orchestrator.py`
- `tests/unit/test_task_engine.py`

## Audit Trail

- EXTRACTED: 220 (81%)
- INFERRED: 53 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*