# recovery_manager.py

> 13 nodes · cohesion 0.19

## Key Concepts

- **recovery_manager.py** (18 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **RecoveryManager** (18 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **.reconcile_startup()** (10 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **is_pid_alive()** (6 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **.release_all_for_execution()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **Nhóm D — Error Handling & Recovery** (3 connections) — `docs/study_guide/00_master_study_guide.md`
- **recovery/__init__.py** (3 connections) — `src/agy_mas/recovery/__init__.py`
- **.release_all()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Any** (1 connections)
- **Recovery manager handling startup reconciliation, stale worker cleanup, and…** (1 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **Checks whether a process with given PID is currently alive on the host.** (1 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **Reconciles interrupted state after orchestrator restart and recovers orphaned…** (1 connections) — `src/agy_mas/recovery/recovery_manager.py`
- **Detects dead workers from previous runs, releases locks, and safely resets…** (1 connections) — `src/agy_mas/recovery/recovery_manager.py`

## Relationships

- [agy_controller.py](agy_controller.py.md) (5 shared connections)
- [Database](Database.md) (5 shared connections)
- [main.py](main.py.md) (5 shared connections)
- [TaskContract](TaskContract.md) (4 shared connections)
- [TaskStateMachine](TaskStateMachine.md) (4 shared connections)
- [ResourceRepository](ResourceRepository.md) (3 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (3 shared connections)
- [TaskRepository](TaskRepository.md) (2 shared connections)
- [8. CÂU HỎI ÔN TẬP TỔNG HỢP (LIÊN CHUYÊN ĐỀ)](8._CÂU_HỎI_ÔN_TẬP_TỔNG_HỢP_LIÊN_CHUYÊN_ĐỀ.md) (1 shared connections)
- [7.2. Integration Acceptance Criteria](7.2._Integration_Acceptance_Criteria.md) (1 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (1 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (1 shared connections)

## Source Files

- `docs/study_guide/00_master_study_guide.md`
- `src/agy_mas/recovery/__init__.py`
- `src/agy_mas/recovery/recovery_manager.py`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/workspace/ownership_manager.py`

## Audit Trail

- EXTRACTED: 35 (65%)
- INFERRED: 19 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*