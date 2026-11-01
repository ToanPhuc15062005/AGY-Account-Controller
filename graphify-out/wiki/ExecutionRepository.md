# ExecutionRepository

> 10 nodes · cohesion 0.38

## Key Concepts

- **ExecutionRepository** (24 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.reconcile_startup()** (10 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **.mark_completed()** (6 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.create()** (5 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.get()** (5 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.list_by_task()** (5 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **Any** (5 connections)
- **.get_latest_for_task()** (4 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **Any** (1 connections)
- **Detects dead workers from previous runs, releases locks, and safely resets…** (1 connections) — `src/agy_mas/recovery/recovery_manager.py`

## Relationships

- [orchestrator.py](orchestrator.py.md) (10 shared connections)
- [ResourceRepository](ResourceRepository.md) (6 shared connections)
- [EventRepository](EventRepository.md) (3 shared connections)
- [main.py](main.py.md) (3 shared connections)
- [TaskRepository](TaskRepository.md) (2 shared connections)
- [Database](Database.md) (2 shared connections)
- [.transaction](transaction.md) (2 shared connections)
- [.fetchone](fetchone.md) (2 shared connections)
- [.setUp](setUp.md) (1 shared connections)
- [MigrationRunner](MigrationRunner.md) (1 shared connections)

## Source Files

- `src/agy_mas/recovery/recovery_manager.py`
- `src/agy_mas/storage/repositories/execution_repo.py`

## Audit Trail

- EXTRACTED: 30 (61%)
- INFERRED: 19 (39%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*