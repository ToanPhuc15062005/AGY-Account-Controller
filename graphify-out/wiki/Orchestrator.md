# Orchestrator

> 20 nodes · cohesion 0.15

## Key Concepts

- **Orchestrator** (38 connections) — `src/agy_mas/core/orchestrator.py`
- **.tick()** (29 connections) — `src/agy_mas/core/orchestrator.py`
- **TestOrchestrator** (11 connections) — `tests/unit/test_orchestrator.py`
- **.test_pair_programming_feedback_loop_retry()** (7 connections) — `tests/unit/test_pair_programming.py`
- **.test_pair_programming_reviewer_fault_tolerance()** (7 connections) — `tests/unit/test_pair_programming.py`
- **.test_orchestrator_events_and_log_streaming()** (6 connections) — `tests/unit/test_orchestrator.py`
- **._emit()** (5 connections) — `src/agy_mas/core/orchestrator.py`
- **.test_orchestrator_quota_failover_to_alternative_account()** (4 connections) — `tests/unit/test_orchestrator.py`
- **.test_orchestrator_two_task_dag_execution()** (4 connections) — `tests/unit/test_orchestrator.py`
- **Any** (3 connections)
- **dynamic_reviewer()** (2 connections) — `tests/unit/test_pair_programming.py`
- **Performs a single evaluation tick over the project lifecycle.** (1 connections) — `src/agy_mas/core/orchestrator.py`
- **The central authority governing project execution, concurrency, and dispatch.** (1 connections) — `src/agy_mas/core/orchestrator.py`
- **Emits telemetry events safely without interfering with core loop.** (1 connections) — `src/agy_mas/core/orchestrator.py`
- **Verify on_event callback receives lifecycle events and logs are written to disk.** (1 connections) — `tests/unit/test_orchestrator.py`
- **.tearDown()** (1 connections) — `tests/unit/test_orchestrator.py`
- **event_listener()** (1 connections) — `tests/unit/test_orchestrator.py`
- **Round 1: Reviewer rejects -> RETRY_WAIT -> Decoupled promotion to READY ->…** (1 connections) — `tests/unit/test_pair_programming.py`
- **Reviewer crashes or times out -> Orchestrator catches error, handles safely and…** (1 connections) — `tests/unit/test_pair_programming.py`
- **crashing_reviewer()** (1 connections) — `tests/unit/test_pair_programming.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (11 shared connections)
- [main.py](main.py.md) (6 shared connections)
- [Database](Database.md) (6 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (5 shared connections)
- [ReviewEngine](ReviewEngine.md) (5 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (4 shared connections)
- [MockAdapter](MockAdapter.md) (4 shared connections)
- [TaskContract](TaskContract.md) (3 shared connections)
- [.test_pair_programming_approval_flow](test_pair_programming_approval_flow.md) (2 shared connections)
- [.test_pair_programming_circuit_breaker](test_pair_programming_circuit_breaker.md) (2 shared connections)
- [2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)](2._CHƯƠNG_1-_VÒNG_LẶP_ĐIỀU_PHỐI_TRUNG_TÂM_CENTRAL_ORCHESTRATOR.md) (2 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (2 shared connections)

## Source Files

- `src/agy_mas/core/orchestrator.py`
- `tests/unit/test_orchestrator.py`
- `tests/unit/test_pair_programming.py`

## Audit Trail

- EXTRACTED: 44 (46%)
- INFERRED: 52 (54%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*