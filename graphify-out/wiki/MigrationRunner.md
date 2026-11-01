# MigrationRunner

> 20 nodes · cohesion 0.15

## Key Concepts

- **MigrationRunner** (26 connections) — `src/agy_mas/storage/migrations/runner.py`
- **ProjectRepository** (22 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **TestPlanner** (10 connections) — `tests/unit/test_planner.py`
- **.setUp()** (10 connections) — `tests/unit/test_verification_recovery.py`
- **.setUp()** (6 connections) — `tests/unit/test_planner.py`
- **.setUp()** (6 connections) — `tests/unit/test_task_engine.py`
- **.run_all()** (5 connections) — `src/agy_mas/storage/migrations/runner.py`
- **.get()** (5 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **.create()** (4 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **.list_all()** (3 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **.update_status()** (3 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **Any** (3 connections)
- **migrations/__init__.py** (2 connections) — `src/agy_mas/storage/migrations/__init__.py`
- **._apply_v1_0_baseline()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **._apply_v1_1_additions()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **Runs all pending migrations in order and returns applied migration names.** (1 connections) — `src/agy_mas/storage/migrations/runner.py`
- **Manages idempotent schema setup and progressive migrations for AGY-MAS.** (1 connections) — `src/agy_mas/storage/migrations/runner.py`
- **.tearDown()** (1 connections) — `tests/unit/test_planner.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (11 shared connections)
- [TaskContract](TaskContract.md) (10 shared connections)
- [Database](Database.md) (8 shared connections)
- [main.py](main.py.md) (7 shared connections)
- [orchestrator.py](orchestrator.py.md) (5 shared connections)
- [TaskRepository](TaskRepository.md) (5 shared connections)
- [EventRepository](EventRepository.md) (4 shared connections)
- [.transaction](transaction.md) (3 shared connections)
- [.setUp](setUp.md) (2 shared connections)
- [TestAGYAdapterAndQuota](TestAGYAdapterAndQuota.md) (1 shared connections)
- [TestStorageLayer](TestStorageLayer.md) (1 shared connections)
- [.fetchone](fetchone.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/migrations/__init__.py`
- `src/agy_mas/storage/migrations/runner.py`
- `src/agy_mas/storage/repositories/project_repo.py`
- `tests/unit/test_planner.py`
- `tests/unit/test_task_engine.py`
- `tests/unit/test_verification_recovery.py`

## Audit Trail

- EXTRACTED: 56 (64%)
- INFERRED: 32 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*