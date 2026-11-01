# .fetchone

> 7 nodes · cohesion 0.33

## Key Concepts

- **.fetchone()** (13 connections) — `src/agy_mas/storage/database.py`
- **.get_account_model_resource()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **Any** (3 connections)
- **.get_lock()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.list_account_model_resources()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **Row** (2 connections)
- **Executes query and returns one row or None.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (4 shared connections)
- [TaskRepository](TaskRepository.md) (3 shared connections)
- [Database](Database.md) (3 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [.setUp](setUp.md) (1 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (1 shared connections)
- [MigrationRunner](MigrationRunner.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/resource_repo.py`

## Audit Trail

- EXTRACTED: 13 (59%)
- INFERRED: 9 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*