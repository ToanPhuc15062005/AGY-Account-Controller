# EventRepository

> 8 nodes · cohesion 0.29

## Key Concepts

- **EventRepository** (23 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **init_mas()** (14 connections) — `src/agy_mas/cli/main.py`
- **.__init__()** (6 connections) — `src/agy_mas/core/dispatcher.py`
- **.__init__()** (5 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **.append()** (4 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **.list_by_project()** (3 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **Any** (2 connections)

## Relationships

- [orchestrator.py](orchestrator.py.md) (9 shared connections)
- [ResourceRepository](ResourceRepository.md) (7 shared connections)
- [main.py](main.py.md) (5 shared connections)
- [MigrationRunner](MigrationRunner.md) (4 shared connections)
- [TaskRepository](TaskRepository.md) (4 shared connections)
- [Database](Database.md) (3 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (3 shared connections)
- [config.py](config.py.md) (2 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (1 shared connections)
- [AGYAdapter](AGYAdapter.md) (1 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (1 shared connections)
- [.setUp](setUp.md) (1 shared connections)

## Source Files

- `src/agy_mas/cli/main.py`
- `src/agy_mas/core/dispatcher.py`
- `src/agy_mas/recovery/recovery_manager.py`
- `src/agy_mas/storage/repositories/event_repo.py`

## Audit Trail

- EXTRACTED: 40 (78%)
- INFERRED: 11 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*