# TestWorkspaceCoordination

> 11 nodes · cohesion 0.25

## Key Concepts

- **TestWorkspaceCoordination** (24 connections) — `tests/unit/test_workspace.py`
- **ArtifactRepository** (23 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.register()** (5 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.get()** (4 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **Any** (4 connections)
- **.list_by_execution()** (3 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.list_by_task()** (3 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.tearDown()** (1 connections) — `tests/unit/test_workspace.py`
- **.test_ownership_conflict_detection()** (1 connections) — `tests/unit/test_workspace.py`
- **.test_path_policy_safety()** (1 connections) — `tests/unit/test_workspace.py`

## Relationships

- [Database](Database.md) (13 shared connections)
- [main.py](main.py.md) (6 shared connections)
- [ResourceRepository](ResourceRepository.md) (5 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (5 shared connections)
- [TaskRepository](TaskRepository.md) (3 shared connections)
- [FileSharingContentionError](FileSharingContentionError.md) (2 shared connections)
- [OwnershipManager](OwnershipManager.md) (2 shared connections)
- [ApprovalRepository](ApprovalRepository.md) (1 shared connections)
- [.fetchone](fetchone.md) (1 shared connections)
- [.transaction](transaction.md) (1 shared connections)
- [.snapshot_file](snapshot_file.md) (1 shared connections)
- [DummyProcess](DummyProcess.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/repositories/artifact_repo.py`
- `tests/unit/test_workspace.py`

## Audit Trail

- EXTRACTED: 27 (47%)
- INFERRED: 30 (53%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*