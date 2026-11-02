# TaskRepository

> 12 nodes · cohesion 0.30

## Key Concepts

- **TaskRepository** (44 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.fetchall()** (17 connections) — `src/agy_mas/storage/database.py`
- **.get()** (7 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.list_by_project()** (7 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.create()** (5 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Any** (4 connections)
- **.get_dependencies()** (4 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.update_critique()** (4 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.get_dependency_map()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.get_dependents()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Executes query and returns all matching rows.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [Database](Database.md) (14 shared connections)
- [ResourceRepository](ResourceRepository.md) (7 shared connections)
- [main.py](main.py.md) (7 shared connections)
- [.transaction](transaction.md) (6 shared connections)
- [TaskContract](TaskContract.md) (6 shared connections)
- [.fetchone](fetchone.md) (4 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (3 shared connections)
- [.transition](transition.md) (3 shared connections)
- [ApprovalRepository](ApprovalRepository.md) (2 shared connections)
- [recovery_manager.py](recovery_manager.py.md) (2 shared connections)
- [Orchestrator](Orchestrator.md) (2 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 42 (53%)
- INFERRED: 37 (47%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*