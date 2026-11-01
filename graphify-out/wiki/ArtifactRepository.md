# ArtifactRepository

> 7 nodes · cohesion 0.48

## Key Concepts

- **ArtifactRepository** (20 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.register()** (5 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.get()** (4 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **Any** (4 connections)
- **.list_by_execution()** (3 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.list_by_task()** (3 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (7 shared connections)
- [main.py](main.py.md) (4 shared connections)
- [Database](Database.md) (2 shared connections)
- [TaskRepository](TaskRepository.md) (2 shared connections)
- [EventRepository](EventRepository.md) (1 shared connections)
- [orchestrator.py](orchestrator.py.md) (1 shared connections)
- [.setUp](setUp.md) (1 shared connections)
- [.fetchone](fetchone.md) (1 shared connections)
- [.transaction](transaction.md) (1 shared connections)
- [.snapshot_file](snapshot_file.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/repositories/artifact_repo.py`

## Audit Trail

- EXTRACTED: 20 (65%)
- INFERRED: 11 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*