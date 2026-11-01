# .setUp

> 8 nodes · cohesion 0.39

## Key Concepts

- **.setUp()** (10 connections) — `tests/unit/test_storage.py`
- **ApprovalRepository** (9 connections) — `src/agy_mas/storage/repositories/approval_repo.py`
- **.get()** (4 connections) — `src/agy_mas/storage/repositories/approval_repo.py`
- **.request_approval()** (4 connections) — `src/agy_mas/storage/repositories/approval_repo.py`
- **Any** (4 connections)
- **.decide()** (3 connections) — `src/agy_mas/storage/repositories/approval_repo.py`
- **.list_pending()** (3 connections) — `src/agy_mas/storage/repositories/approval_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/approval_repo.py`

## Relationships

- [Database](Database.md) (3 shared connections)
- [main.py](main.py.md) (2 shared connections)
- [.transaction](transaction.md) (2 shared connections)
- [TaskRepository](TaskRepository.md) (2 shared connections)
- [MigrationRunner](MigrationRunner.md) (2 shared connections)
- [.fetchone](fetchone.md) (1 shared connections)
- [TestStorageLayer](TestStorageLayer.md) (1 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (1 shared connections)
- [EventRepository](EventRepository.md) (1 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (1 shared connections)
- [ResourceRepository](ResourceRepository.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/repositories/approval_repo.py`
- `tests/unit/test_storage.py`

## Audit Trail

- EXTRACTED: 16 (57%)
- INFERRED: 12 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*