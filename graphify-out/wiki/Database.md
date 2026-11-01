# Database

> 16 nodes · cohesion 0.16

## Key Concepts

- **Database** (55 connections) — `src/agy_mas/storage/database.py`
- **.connect()** (9 connections) — `src/agy_mas/storage/database.py`
- **.execute()** (5 connections) — `src/agy_mas/storage/database.py`
- **Connection** (3 connections)
- **._create_connection()** (3 connections) — `src/agy_mas/storage/database.py`
- **Any** (3 connections)
- **.close()** (2 connections) — `src/agy_mas/storage/database.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/database.py`
- **storage/__init__.py** (2 connections) — `src/agy_mas/storage/__init__.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **Cursor** (1 connections)
- **Manages SQLite database connections and transactions with robust pragmas.** (1 connections) — `src/agy_mas/storage/database.py`
- **Context manager yielding a thread-local SQLite connection.** (1 connections) — `src/agy_mas/storage/database.py`
- **Executes a query directly within an auto-commit or existing transaction.** (1 connections) — `src/agy_mas/storage/database.py`
- **Closes thread-local connection if open.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [main.py](main.py.md) (11 shared connections)
- [MigrationRunner](MigrationRunner.md) (8 shared connections)
- [ResourceRepository](ResourceRepository.md) (7 shared connections)
- [TaskRepository](TaskRepository.md) (5 shared connections)
- [.transaction](transaction.md) (3 shared connections)
- [EventRepository](EventRepository.md) (3 shared connections)
- [.setUp](setUp.md) (3 shared connections)
- [.fetchone](fetchone.md) (3 shared connections)
- [TaskContract](TaskContract.md) (3 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (2 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [agy_controller.py](agy_controller.py.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/__init__.py`
- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/execution_repo.py`
- `src/agy_mas/storage/repositories/resource_repo.py`

## Audit Trail

- EXTRACTED: 56 (76%)
- INFERRED: 18 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*