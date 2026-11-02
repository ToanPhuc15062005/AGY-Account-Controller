# .transition

> 15 nodes · cohesion 0.15

## Key Concepts

- **.transition()** (20 connections) — `src/agy_mas/core/state_machine.py`
- **InvalidStateTransitionError** (9 connections) — `src/agy_mas/core/state_machine.py`
- **3.2. State Machine Pattern** (4 connections) — `docs/study_guide/01_architecture_and_design_patterns.md`
- **3.2. Cỗ Máy Trạng Thái 12 Bước: `TaskStateMachine`** (4 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **Bảng Tra Cứu Các Lỗi Thường Gặp & Cách Khắc Phục** (4 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **Ma Trận Chuyển Đổi Hợp Lệ (`VALID_TRANSITIONS`)** (4 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **7. TỔNG KẾT & BẢNG TRA CỨU NHANH (CHEAT SHEET)** (3 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **.update_status()** (3 connections) — `src/agy_mas/storage/repositories/task_repo.py`
- **.test_state_machine_invalid_transition_rejected()** (2 connections) — `tests/unit/test_task_engine.py`
- **.test_state_machine_valid_flow()** (2 connections) — `tests/unit/test_task_engine.py`
- **Bảng Tra Cứu 12 Trạng Thái Task** (1 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **Sơ Đồ Chuyển Đổi Trạng Thái (State Transition Diagram)** (1 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **Any** (1 connections)
- **ValueError** (1 connections)
- **Raised when an illegal state transition is attempted.** (1 connections) — `src/agy_mas/core/state_machine.py`

## Relationships

- [TaskContract](TaskContract.md) (6 shared connections)
- [TaskStateMachine](TaskStateMachine.md) (5 shared connections)
- [Database](Database.md) (3 shared connections)
- [TaskRepository](TaskRepository.md) (3 shared connections)
- [main.py](main.py.md) (2 shared connections)
- [.transaction](transaction.md) (2 shared connections)
- [3. CÁC DESIGN PATTERNS CỐT LÕI](3._CÁC_DESIGN_PATTERNS_CỐT_LÕI.md) (1 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (1 shared connections)
- [ManagedProcess](ManagedProcess.md) (1 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (1 shared connections)
- [Orchestrator](Orchestrator.md) (1 shared connections)
- [recovery_manager.py](recovery_manager.py.md) (1 shared connections)

## Source Files

- `docs/study_guide/01_architecture_and_design_patterns.md`
- `docs/study_guide/02_storage_and_task_engine.md`
- `src/agy_mas/core/state_machine.py`
- `src/agy_mas/storage/repositories/task_repo.py`
- `tests/unit/test_task_engine.py`

## Audit Trail

- EXTRACTED: 27 (61%)
- INFERRED: 17 (39%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*