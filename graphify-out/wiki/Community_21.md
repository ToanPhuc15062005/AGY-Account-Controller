# Community 21

> 8 nodes · cohesion 0.25

## Key Concepts

- **Database** (55 connections) — `src/agy_mas/storage/database.py`
- **.close()** (2 connections) — `src/agy_mas/storage/database.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/artifact_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Manages SQLite database connections and transactions with robust pragmas.** (1 connections) — `src/agy_mas/storage/database.py`
- **Closes thread-local connection if open.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [Community 0](Community_0.md) (13 shared connections)
- [Community 11](Community_11.md) (7 shared connections)
- [Community 19](Community_19.md) (4 shared connections)
- [Community 14](Community_14.md) (4 shared connections)
- [Community 22](Community_22.md) (3 shared connections)
- [Community 3](Community_3.md) (3 shared connections)
- [Community 18](Community_18.md) (3 shared connections)
- [Community 10](Community_10.md) (3 shared connections)
- [Community 1](Community_1.md) (3 shared connections)
- [Community 4](Community_4.md) (2 shared connections)
- [Community 9](Community_9.md) (2 shared connections)
- [Community 2](Community_2.md) (2 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/artifact_repo.py`
- `src/agy_mas/storage/repositories/event_repo.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 42 (70%)
- INFERRED: 18 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*