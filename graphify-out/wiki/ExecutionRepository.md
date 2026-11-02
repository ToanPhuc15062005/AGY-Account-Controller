# ExecutionRepository

> 9 nodes · cohesion 0.28

## Key Concepts

- **._finalize_acceptance()** (9 connections) — `src/agy_mas/core/orchestrator.py`
- **.mark_completed()** (7 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.create()** (6 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.get()** (5 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.list_by_task()** (5 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **Any** (5 connections)
- **.get_latest_for_task()** (4 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **3.1. Repository Pattern & Data Access Layer** (2 connections) — `docs/study_guide/01_architecture_and_design_patterns.md`
- **Helper to register artifacts, complete execution, release locks, and accept…** (1 connections) — `src/agy_mas/core/orchestrator.py`

## Relationships

- [Orchestrator](Orchestrator.md) (5 shared connections)
- [Database](Database.md) (5 shared connections)
- [recovery_manager.py](recovery_manager.py.md) (3 shared connections)
- [ManagedProcess](ManagedProcess.md) (2 shared connections)
- [.transaction](transaction.md) (2 shared connections)
- [.fetchone](fetchone.md) (2 shared connections)
- [3. CÁC DESIGN PATTERNS CỐT LÕI](3._CÁC_DESIGN_PATTERNS_CỐT_LÕI.md) (1 shared connections)
- [.transition](transition.md) (1 shared connections)
- [TaskContract](TaskContract.md) (1 shared connections)
- [.snapshot_file](snapshot_file.md) (1 shared connections)
- [TaskRepository](TaskRepository.md) (1 shared connections)

## Source Files

- `docs/study_guide/01_architecture_and_design_patterns.md`
- `src/agy_mas/core/orchestrator.py`
- `src/agy_mas/storage/repositories/execution_repo.py`

## Audit Trail

- EXTRACTED: 20 (59%)
- INFERRED: 14 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*