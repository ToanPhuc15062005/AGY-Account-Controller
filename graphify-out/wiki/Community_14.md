# Community 14

> 11 nodes · cohesion 0.22

## Key Concepts

- **.transaction()** (24 connections) — `src/agy_mas/storage/database.py`
- **.connect()** (9 connections) — `src/agy_mas/storage/database.py`
- **Connection** (3 connections)
- **._create_connection()** (3 connections) — `src/agy_mas/storage/database.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/database.py`
- **.acquire_lock()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_file_ownership()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.release_lock()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.add_dependency()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Context manager yielding a thread-local SQLite connection.** (1 connections) — `src/agy_mas/storage/database.py`
- **Context manager for atomic transaction block.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [Community 0](Community_0.md) (7 shared connections)
- [Community 21](Community_21.md) (4 shared connections)
- [Community 11](Community_11.md) (4 shared connections)
- [Community 10](Community_10.md) (3 shared connections)
- [Community 18](Community_18.md) (2 shared connections)
- [Community 8](Community_8.md) (2 shared connections)
- [Community 4](Community_4.md) (2 shared connections)
- [Community 22](Community_22.md) (1 shared connections)
- [Community 23](Community_23.md) (1 shared connections)
- [Community 19](Community_19.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 19 (49%)
- INFERRED: 20 (51%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*