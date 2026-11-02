# ReviewEngine

> 19 nodes · cohesion 0.16

## Key Concepts

- **ReviewEngine** (18 connections) — `src/agy_mas/agents/review_engine.py`
- **ReviewReport** (14 connections) — `src/agy_mas/planning/plan_schema.py`
- **review_engine.py** (13 connections) — `src/agy_mas/agents/review_engine.py`
- **ReviewVerdict** (9 connections) — `src/agy_mas/planning/plan_schema.py`
- **.execute_review()** (8 connections) — `src/agy_mas/agents/review_engine.py`
- **.__init__()** (4 connections) — `src/agy_mas/agents/review_engine.py`
- **Any** (4 connections)
- **._run_acceptance_tests()** (3 connections) — `src/agy_mas/agents/review_engine.py`
- **.from_dict()** (3 connections) — `src/agy_mas/planning/plan_schema.py`
- **.to_dict()** (3 connections) — `src/agy_mas/planning/plan_schema.py`
- **._collect_diff()** (2 connections) — `src/agy_mas/agents/review_engine.py`
- **Enum** (2 connections)
- **.to_dict()** (2 connections) — `src/agy_mas/planning/plan_schema.py`
- **Any** (1 connections)
- **ReviewEngine implementing Hybrid (Fast-path automated checks + Reviewer Agent)…** (1 connections) — `src/agy_mas/agents/review_engine.py`
- **Executes active quality review for task executions in Pair-Programming mode.** (1 connections) — `src/agy_mas/agents/review_engine.py`
- **Executes hybrid quality review: Fast-path tests first, then Reviewer Agent.** (1 connections) — `src/agy_mas/agents/review_engine.py`
- **str** (1 connections)
- **Biên bản đánh giá chất lượng code do Reviewer tạo ra.** (1 connections) — `src/agy_mas/planning/plan_schema.py`

## Relationships

- [TaskContract](TaskContract.md) (10 shared connections)
- [main.py](main.py.md) (6 shared connections)
- [Orchestrator](Orchestrator.md) (5 shared connections)
- [Verifier](Verifier.md) (4 shared connections)
- [Database](Database.md) (3 shared connections)
- [agy_controller.py](agy_controller.py.md) (2 shared connections)
- [.test_pair_programming_approval_flow](test_pair_programming_approval_flow.md) (2 shared connections)
- [.test_pair_programming_circuit_breaker](test_pair_programming_circuit_breaker.md) (2 shared connections)
- [PathPolicy](PathPolicy.md) (1 shared connections)
- [ResourceRepository](ResourceRepository.md) (1 shared connections)
- [ARCHITECTURE PROPOSAL (AFTER: KIẾN TRÚC PAIR-PROGRAMMING)](ARCHITECTURE_PROPOSAL_AFTER-_KIẾN_TRÚC_PAIR-PROGRAMMING.md) (1 shared connections)

## Source Files

- `src/agy_mas/agents/review_engine.py`
- `src/agy_mas/planning/plan_schema.py`

## Audit Trail

- EXTRACTED: 53 (83%)
- INFERRED: 11 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*