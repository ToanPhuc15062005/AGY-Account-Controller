# Community 8

> 17 nodes · cohesion 0.12

## Key Concepts

- **resource_repo.py** (13 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **OwnershipManager** (13 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **ownership_manager.py** (12 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **OwnershipConflictError** (6 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.release_all_for_execution()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.claim_ownership()** (4 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.claim_file_ownership()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.check_write_permitted()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.__init__()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.release_all()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **PermissionError** (1 connections)
- **Resource repository for locks, file ownerships, and account-model quotas.** (1 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **File and path ownership manager enforcing lease-based write permissions.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Raised when an execution attempts to claim or write to a path owned by another…** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Manages path pattern leases and verifies file modification privileges.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Claims a path pattern lease for an execution attempt.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Checks if the given execution owns a valid, unexpired write lease for the path.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`

## Relationships

- [Community 11](Community_11.md) (9 shared connections)
- [Community 6](Community_6.md) (8 shared connections)
- [Community 0](Community_0.md) (7 shared connections)
- [Community 4](Community_4.md) (2 shared connections)
- [Community 3](Community_3.md) (2 shared connections)
- [Community 14](Community_14.md) (2 shared connections)
- [Community 16](Community_16.md) (2 shared connections)
- [Community 21](Community_21.md) (1 shared connections)
- [Community 1](Community_1.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/workspace/ownership_manager.py`

## Audit Trail

- EXTRACTED: 42 (82%)
- INFERRED: 9 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*