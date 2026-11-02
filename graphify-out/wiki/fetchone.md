# .fetchone

> 14 nodes · cohesion 0.21

## Key Concepts

- **.fetchone()** (15 connections) — `src/agy_mas/storage/database.py`
- **ReviewRepository** (11 connections) — `src/agy_mas/storage/repositories/review_repo.py`
- **.get()** (5 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **.create()** (4 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **Any** (4 connections)
- **.create()** (4 connections) — `src/agy_mas/storage/repositories/review_repo.py`
- **.get()** (4 connections) — `src/agy_mas/storage/repositories/review_repo.py`
- **.list_all()** (3 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **Any** (3 connections)
- **.get_latest_for_task()** (3 connections) — `src/agy_mas/storage/repositories/review_repo.py`
- **.list_by_task()** (3 connections) — `src/agy_mas/storage/repositories/review_repo.py`
- **Row** (2 connections)
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/review_repo.py`
- **Executes query and returns one row or None.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [Database](Database.md) (7 shared connections)
- [TaskRepository](TaskRepository.md) (4 shared connections)
- [.transaction](transaction.md) (4 shared connections)
- [main.py](main.py.md) (3 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [ResourceRepository](ResourceRepository.md) (2 shared connections)
- [ApprovalRepository](ApprovalRepository.md) (1 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (1 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (1 shared connections)
- [Orchestrator](Orchestrator.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/project_repo.py`
- `src/agy_mas/storage/repositories/review_repo.py`

## Audit Trail

- EXTRACTED: 28 (62%)
- INFERRED: 17 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*