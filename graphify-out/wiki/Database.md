# Database

> 30 nodes · cohesion 0.17

## Key Concepts

- **Database** (68 connections) — `src/agy_mas/storage/database.py`
- **MigrationRunner** (33 connections) — `src/agy_mas/storage/migrations/runner.py`
- **EventRepository** (31 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **ExecutionRepository** (28 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **ProjectRepository** (25 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- **TestPairProgramming** (17 connections) — `tests/unit/test_pair_programming.py`
- **init_mas()** (14 connections) — `src/agy_mas/cli/main.py`
- **.setUp()** (13 connections) — `tests/integration/test_e2e_acceptance.py`
- **.setUp()** (12 connections) — `tests/unit/test_pair_programming.py`
- **.setUp()** (12 connections) — `tests/unit/test_workspace.py`
- **.setUp()** (11 connections) — `tests/unit/test_orchestrator.py`
- **TestPlanner** (10 connections) — `tests/unit/test_planner.py`
- **.setUp()** (10 connections) — `tests/unit/test_storage.py`
- **.setUp()** (10 connections) — `tests/unit/test_verification_recovery.py`
- **.setUp()** (6 connections) — `tests/unit/test_agy_adapter.py`
- **.setUp()** (6 connections) — `tests/unit/test_planner.py`
- **.setUp()** (6 connections) — `tests/unit/test_task_engine.py`
- **.__init__()** (5 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **2.2. Điều Phối Migration Tự Động & Idempotent: `MigrationRunner`** (3 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **Chiến lược mở rộng schema an toàn (Schema Evolution Safety)** (2 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **.close()** (2 connections) — `src/agy_mas/storage/database.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/migrations/runner.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/event_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **.__init__()** (2 connections) — `src/agy_mas/storage/repositories/project_repo.py`
- *... and 5 more nodes in this community*

## Relationships

- [ResourceRepository](ResourceRepository.md) (38 shared connections)
- [main.py](main.py.md) (34 shared connections)
- [TaskContract](TaskContract.md) (17 shared connections)
- [TaskRepository](TaskRepository.md) (14 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (13 shared connections)
- [.transaction](transaction.md) (12 shared connections)
- [.fetchone](fetchone.md) (7 shared connections)
- [AGYAdapter](AGYAdapter.md) (6 shared connections)
- [ApprovalRepository](ApprovalRepository.md) (6 shared connections)
- [Orchestrator](Orchestrator.md) (6 shared connections)
- [recovery_manager.py](recovery_manager.py.md) (5 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (5 shared connections)

## Source Files

- `docs/study_guide/02_storage_and_task_engine.md`
- `src/agy_mas/cli/main.py`
- `src/agy_mas/recovery/recovery_manager.py`
- `src/agy_mas/storage/database.py`
- `src/agy_mas/storage/migrations/runner.py`
- `src/agy_mas/storage/repositories/event_repo.py`
- `src/agy_mas/storage/repositories/execution_repo.py`
- `src/agy_mas/storage/repositories/project_repo.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_agy_adapter.py`
- `tests/unit/test_orchestrator.py`
- `tests/unit/test_pair_programming.py`
- `tests/unit/test_planner.py`
- `tests/unit/test_storage.py`
- `tests/unit/test_task_engine.py`
- `tests/unit/test_verification_recovery.py`
- `tests/unit/test_workspace.py`

## Audit Trail

- EXTRACTED: 163 (62%)
- INFERRED: 101 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*