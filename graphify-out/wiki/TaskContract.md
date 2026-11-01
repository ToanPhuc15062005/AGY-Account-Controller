# TaskContract

> 83 nodes · cohesion 0.06

## Key Concepts

- **TaskContract** (32 connections) — `src/agy_mas/planning/plan_schema.py`
- **planner.py** (23 connections) — `src/agy_mas/planning/planner.py`
- **plan_schema.py** (22 connections) — `src/agy_mas/planning/plan_schema.py`
- **TestTaskEngine** (22 connections) — `tests/unit/test_task_engine.py`
- **Planner** (21 connections) — `src/agy_mas/planning/planner.py`
- **TestArchitectureV11Acceptance** (21 connections) — `tests/integration/test_e2e_acceptance.py`
- **DependencyGraph** (19 connections) — `src/agy_mas/planning/dependency_graph.py`
- **PermissionProfile** (17 connections) — `src/agy_mas/planning/plan_schema.py`
- **TestVerificationAndRecovery** (16 connections) — `tests/unit/test_verification_recovery.py`
- **planning/__init__.py** (15 connections) — `src/agy_mas/planning/__init__.py`
- **AcceptanceCriterion** (15 connections) — `src/agy_mas/planning/plan_schema.py`
- **ExpectedArtifact** (15 connections) — `src/agy_mas/planning/plan_schema.py`
- **plan_validator.py** (14 connections) — `src/agy_mas/planning/plan_validator.py`
- **PlanValidator** (13 connections) — `src/agy_mas/planning/plan_validator.py`
- **OutputScope** (12 connections) — `src/agy_mas/planning/plan_schema.py`
- **.schedule_next()** (11 connections) — `src/agy_mas/core/scheduler.py`
- **.validate_plan()** (11 connections) — `src/agy_mas/planning/plan_validator.py`
- **.plan_project()** (11 connections) — `src/agy_mas/planning/planner.py`
- **CycleDetectedError** (9 connections) — `src/agy_mas/planning/dependency_graph.py`
- **dependency_graph.py** (8 connections) — `src/agy_mas/planning/dependency_graph.py`
- **.from_dict()** (8 connections) — `src/agy_mas/planning/plan_schema.py`
- **._build_contracts()** (8 connections) — `src/agy_mas/planning/planner.py`
- **.topological_sort()** (7 connections) — `src/agy_mas/planning/dependency_graph.py`
- **.test_VER_03_all_acceptance_criteria_pass()** (7 connections) — `tests/integration/test_e2e_acceptance.py`
- **.add_task()** (6 connections) — `src/agy_mas/planning/dependency_graph.py`
- *... and 58 more nodes in this community*

## Relationships

- [main.py](main.py.md) (28 shared connections)
- [orchestrator.py](orchestrator.py.md) (21 shared connections)
- [PathPolicy](PathPolicy.md) (19 shared connections)
- [MigrationRunner](MigrationRunner.md) (10 shared connections)
- [TaskRepository](TaskRepository.md) (6 shared connections)
- [ResourceRepository](ResourceRepository.md) (4 shared connections)
- [Database](Database.md) (3 shared connections)
- [config.py](config.py.md) (2 shared connections)
- [agy_controller.py](agy_controller.py.md) (1 shared connections)
- [EventRepository](EventRepository.md) (1 shared connections)

## Source Files

- `src/agy_mas/cli/main.py`
- `src/agy_mas/core/scheduler.py`
- `src/agy_mas/planning/__init__.py`
- `src/agy_mas/planning/dependency_graph.py`
- `src/agy_mas/planning/plan_schema.py`
- `src/agy_mas/planning/plan_validator.py`
- `src/agy_mas/planning/planner.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_planner.py`
- `tests/unit/test_task_engine.py`
- `tests/unit/test_verification_recovery.py`

## Audit Trail

- EXTRACTED: 224 (76%)
- INFERRED: 70 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*