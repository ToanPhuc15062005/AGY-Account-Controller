# .transaction

> 9 nodes · cohesion 0.22

## Key Concepts

- **.transaction()** (24 connections) — `src/agy_mas/storage/database.py`
- **.record_quota_exhaustion()** (3 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.set_account_model_cooldown()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.acquire_lock()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_file_ownership()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_lock()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.add_dependency()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Sets cooldown for the specific (account_id, model_key) pair.** (1 connections) — `src/agy_mas/resources/quota_tracker.py`
- **Context manager for atomic transaction block.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (8 shared connections)
- [Database](Database.md) (3 shared connections)
- [MigrationRunner](MigrationRunner.md) (3 shared connections)
- [.setUp](setUp.md) (2 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [orchestrator.py](orchestrator.py.md) (2 shared connections)
- [TaskRepository](TaskRepository.md) (2 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (1 shared connections)
- [EventRepository](EventRepository.md) (1 shared connections)

## Source Files

- `src/agy_mas/resources/quota_tracker.py`
- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 11 (34%)
- INFERRED: 21 (66%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*