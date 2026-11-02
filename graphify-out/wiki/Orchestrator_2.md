# Orchestrator

> God node · 38 connections · `src/agy_mas/core/orchestrator.py`

**Community:** [Orchestrator](Orchestrator.md)

## Connections by Relation

### calls
- cmd_orchestrate() `EXTRACTED`
- .test_pair_programming_approval_flow() `EXTRACTED`
- .test_pair_programming_circuit_breaker() `EXTRACTED`
- .test_pair_programming_feedback_loop_retry() `EXTRACTED`
- .test_pair_programming_reviewer_fault_tolerance() `EXTRACTED`
- .test_orchestrator_events_and_log_streaming() `EXTRACTED`
- .test_orchestrator_quota_failover_to_alternative_account() `EXTRACTED`
- .test_orchestrator_two_task_dag_execution() `EXTRACTED`

### contains
- orchestrator.py `EXTRACTED`

### imports
- [main.py](main.py.md) `EXTRACTED`
- core/__init__.py `EXTRACTED`

### method
- .tick() `EXTRACTED`
- .__init__() `EXTRACTED`
- ._finalize_acceptance() `EXTRACTED`
- ._emit() `EXTRACTED`

### rationale_for
- The central authority governing project execution, concurrency, and dispatch. `EXTRACTED`

### references
- [6.1. Classes & Modules](6.1._Classes_&_Modules.md) `INFERRED`
- 🚀 Tính năng cốt lõi của Multi-Agent System (`agy-mas`) `INFERRED`
- MỤC LỤC TỔNG QUAN `INFERRED`
- [2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)](2._CHƯƠNG_1-_VÒNG_LẶP_ĐIỀU_PHỐI_TRUNG_TÂM_CENTRAL_ORCHESTRATOR.md) `INFERRED`
- Nhóm A — Kiến Trúc Tổng Thể `INFERRED`
- Bộ 10 Câu Hỏi Trắc Nghiệm Kiến Trúc Chuyên Sâu (Kèm Lời Giải) `INFERRED`
- 2.2. Nguyên Tắc Modular Monolith `INFERRED`
- Lab 4: Thiết Kế Adapter Mới (30 phút) `INFERRED`
- 2.1. Cấu Trúc và Trách Nhiệm Của `Orchestrator` `INFERRED`

### uses
- [TaskContract](TaskContract.md) `INFERRED`
- [WorkspaceManager](WorkspaceManager.md) `INFERRED`
- [QuotaTracker](QuotaTracker.md) `INFERRED`
- [ManagedProcess](ManagedProcess.md) `INFERRED`
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) `INFERRED`
- Dispatcher `INFERRED`
- [TaskStateMachine](TaskStateMachine.md) `INFERRED`
- Scheduler `INFERRED`
- [ReviewEngine](ReviewEngine.md) `INFERRED`
- TestPairProgramming `INFERRED`
- TaskState `INFERRED`
- TestOrchestrator `INFERRED`
- ReviewVerdict `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*