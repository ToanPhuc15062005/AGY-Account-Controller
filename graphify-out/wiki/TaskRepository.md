# TaskRepository

> 11 nodes · cohesion 0.33

## Key Concepts

- **TaskRepository** (39 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.fetchall()** (16 connections) — `src/agy_mas/storage/database.py`
- **.get()** (7 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.list_by_project()** (7 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.create()** (5 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.get_dependencies()** (4 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Any** (3 connections)
- **.get_dependency_map()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.get_dependents()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Executes query and returns all matching rows.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [orchestrator.py](orchestrator.py.md) (12 shared connections)
- [ResourceRepository](ResourceRepository.md) (6 shared connections)
- [TaskContract](TaskContract.md) (6 shared connections)
- [Database](Database.md) (5 shared connections)
- [MigrationRunner](MigrationRunner.md) (5 shared connections)
- [EventRepository](EventRepository.md) (4 shared connections)
- [.fetchone](fetchone.md) (3 shared connections)
- [main.py](main.py.md) (3 shared connections)
- [.setUp](setUp.md) (2 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (2 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [.transaction](transaction.md) (2 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 40 (57%)
- INFERRED: 30 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*