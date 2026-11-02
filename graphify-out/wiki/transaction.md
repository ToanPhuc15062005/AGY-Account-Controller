# .transaction

> 24 nodes · cohesion 0.09

## Key Concepts

- **.transaction()** (28 connections) — `src/agy_mas/storage/database.py`
- **.connect()** (9 connections) — `src/agy_mas/storage/database.py`
- **.run_all()** (7 connections) — `src/agy_mas/storage/migrations/runner.py`
- **.execute()** (6 connections) — `src/agy_mas/storage/database.py`
- **.append()** (4 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **Connection** (3 connections)
- **._create_connection()** (3 connections) — `src/agy_mas/storage/database.py`
- **Any** (3 connections)
- **.list_by_project()** (3 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **.update_status()** (3 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/database.py`
- **._apply_v1_0_baseline()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **._apply_v1_1_additions()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **._apply_v1_2_pair_programming()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **Any** (2 connections)
- **.acquire_lock()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_file_ownership()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_lock()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.add_dependency()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Cursor** (1 connections)
- **Context manager yielding a thread-local SQLite connection.** (1 connections) — `src/agy_mas/storage/database.py`
- **Context manager for atomic transaction block.** (1 connections) — `src/agy_mas/storage/database.py`
- **Executes a query directly within an auto-commit or existing transaction.** (1 connections) — `src/agy_mas/storage/database.py`
- **Runs all pending migrations in order and returns applied migration names.** (1 connections) — `src/agy_mas/storage/migrations/runner.py`

## Relationships

- [Database](Database.md) (12 shared connections)
- [TaskRepository](TaskRepository.md) (6 shared connections)
- [ResourceRepository](ResourceRepository.md) (5 shared connections)
- [.fetchone](fetchone.md) (4 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (2 shared connections)
- [ApprovalRepository](ApprovalRepository.md) (2 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [.transition](transition.md) (2 shared connections)
- [TaskContract](TaskContract.md) (2 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (1 shared connections)
- [ManagedProcess](ManagedProcess.md) (1 shared connections)
- [OwnershipManager](OwnershipManager.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/migrations/runner.py`
- `src/agy_mas/storage/repositories/event_repo.py`
- `src/agy_mas/storage/repositories/project_repo.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 38 (57%)
- INFERRED: 29 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*