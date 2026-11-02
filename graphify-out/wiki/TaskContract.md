# TaskContract

> 98 nodes · cohesion 0.05

## Key Concepts

- **TaskContract** (53 connections) — `src/agy_mas/planning/plan_schema.py`
- **plan_schema.py** (27 connections) — `src/agy_mas/planning/plan_schema.py`
- **DependencyGraph** (26 connections) — `src/agy_mas/planning/dependency_graph.py`
- **Planner** (24 connections) — `src/agy_mas/planning/planner.py`
- **planner.py** (23 connections) — `src/agy_mas/planning/planner.py`
- **PlanValidator** (22 connections) — `src/agy_mas/planning/plan_validator.py`
- **TestTaskEngine** (22 connections) — `tests/unit/test_task_engine.py`
- **PermissionProfile** (21 connections) — `src/agy_mas/planning/plan_schema.py`
- **TestArchitectureV11Acceptance** (21 connections) — `tests/integration/test_e2e_acceptance.py`
- **Tổng Kết & Bảng Tra Cứu Nhanh** (20 connections) — `docs/study_guide/01_architecture_and_design_patterns.md`
- **AcceptanceCriterion** (20 connections) — `src/agy_mas/planning/plan_schema.py`
- **ExpectedArtifact** (18 connections) — `src/agy_mas/planning/plan_schema.py`
- **TestVerificationAndRecovery** (16 connections) — `tests/unit/test_verification_recovery.py`
- **planning/__init__.py** (15 connections) — `src/agy_mas/planning/__init__.py`
- **.schedule_next()** (14 connections) — `src/agy_mas/core/scheduler.py`
- **OutputScope** (14 connections) — `src/agy_mas/planning/plan_schema.py`
- **plan_validator.py** (14 connections) — `src/agy_mas/planning/plan_validator.py`
- **.validate_plan()** (12 connections) — `src/agy_mas/planning/plan_validator.py`
- **CycleDetectedError** (11 connections) — `src/agy_mas/planning/dependency_graph.py`
- **.plan_project()** (11 connections) — `src/agy_mas/planning/planner.py`
- **MỤC LỤC TỔNG QUAN** (9 connections) — `docs/study_guide/02_storage_and_task_engine.md`
- **.topological_sort()** (9 connections) — `src/agy_mas/planning/dependency_graph.py`
- **Capstone: Thiết Kế Hệ Thống CI/CD Multi-Agent** (8 connections) — `docs/study_guide/00_master_study_guide.md`
- **dependency_graph.py** (8 connections) — `src/agy_mas/planning/dependency_graph.py`
- **.from_dict()** (8 connections) — `src/agy_mas/planning/plan_schema.py`
- *... and 73 more nodes in this community*

## Relationships

- [main.py](main.py.md) (35 shared connections)
- [PathPolicy](PathPolicy.md) (20 shared connections)
- [Database](Database.md) (17 shared connections)
- [ResourceRepository](ResourceRepository.md) (16 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (12 shared connections)
- [ReviewEngine](ReviewEngine.md) (10 shared connections)
- [Verifier](Verifier.md) (8 shared connections)
- [.transition](transition.md) (6 shared connections)
- [TaskRepository](TaskRepository.md) (6 shared connections)
- [recovery_manager.py](recovery_manager.py.md) (4 shared connections)
- [Orchestrator](Orchestrator.md) (3 shared connections)
- [.resolve_safe_path](resolve_safe_path.md) (3 shared connections)

## Source Files

- `docs/study_guide/00_master_study_guide.md`
- `docs/study_guide/01_architecture_and_design_patterns.md`
- `docs/study_guide/02_storage_and_task_engine.md`
- `src/agy_mas/cli/main.py`
- `src/agy_mas/core/scheduler.py`
- `src/agy_mas/planning/__init__.py`
- `src/agy_mas/planning/dependency_graph.py`
- `src/agy_mas/planning/plan_schema.py`
- `src/agy_mas/planning/plan_validator.py`
- `src/agy_mas/planning/planner.py`
- `src/agy_mas/verification/scope_checker.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_planner.py`
- `tests/unit/test_task_engine.py`
- `tests/unit/test_verification_recovery.py`

## Audit Trail

- EXTRACTED: 252 (62%)
- INFERRED: 156 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*