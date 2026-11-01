# .snapshot_file

> 10 nodes · cohesion 0.20

## Key Concepts

- **.snapshot_file()** (7 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **SnapshotTimingError** (6 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **.register_task_artifacts()** (6 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **RuntimeError** (1 connections)
- **Any** (1 connections)
- **Raised when an artifact snapshot is attempted while a worker process is still…** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Calculates file checksum and metadata after verifying process is terminated.** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **_read_and_hash()** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Any** (1 connections)
- **Snapshots deliverables and commits them to the artifact repository.** (1 connections) — `src/agy_mas/workspace/workspace_manager.py`

## Relationships

- [main.py](main.py.md) (3 shared connections)
- [ResourceRepository](ResourceRepository.md) (2 shared connections)
- [PathPolicy](PathPolicy.md) (1 shared connections)
- [orchestrator.py](orchestrator.py.md) (1 shared connections)
- [ArtifactRepository](ArtifactRepository.md) (1 shared connections)

## Source Files

- `src/agy_mas/workspace/snapshot_manager.py`
- `src/agy_mas/workspace/workspace_manager.py`

## Audit Trail

- EXTRACTED: 11 (65%)
- INFERRED: 6 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*