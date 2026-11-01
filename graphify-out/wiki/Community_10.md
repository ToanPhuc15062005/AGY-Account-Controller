# Community 10

> 15 nodes · cohesion 0.16

## Key Concepts

- **.fetchall()** (16 connections) — `src/agy_mas/storage/database.py`
- **.fetchone()** (13 connections) — `src/agy_mas/storage/database.py`
- **.execute()** (5 connections) — `src/agy_mas/storage/database.py`
- **.get_account_model_resource()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **Any** (3 connections)
- **Any** (3 connections)
- **.get_lock()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **.list_account_model_resources()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **Row** (2 connections)
- **.get_dependency_map()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.get_dependents()** (2 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **Cursor** (1 connections)
- **Executes a query directly within an auto-commit or existing transaction.** (1 connections) — `src/agy_mas/storage/database.py`
- **Executes query and returns one row or None.** (1 connections) — `src/agy_mas/storage/database.py`
- **Executes query and returns all matching rows.** (1 connections) — `src/agy_mas/storage/database.py`

## Relationships

- [Community 0](Community_0.md) (9 shared connections)
- [Community 11](Community_11.md) (6 shared connections)
- [Community 14](Community_14.md) (3 shared connections)
- [Community 21](Community_21.md) (3 shared connections)
- [Community 18](Community_18.md) (2 shared connections)
- [Community 19](Community_19.md) (2 shared connections)
- [Community 4](Community_4.md) (1 shared connections)

## Source Files

- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/storage/repositories/task_repo.py`

## Audit Trail

- EXTRACTED: 24 (56%)
- INFERRED: 19 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*