# TaskContract

> God node · 32 connections · `src/agy_mas/planning/plan_schema.py`

**Community:** [Community 1](Community_1.md)

## Connections by Relation

### calls
- .test_VER_03_all_acceptance_criteria_pass() `EXTRACTED`
- .test_verifier_passes_when_all_conditions_met() `EXTRACTED`
- .test_VER_02_exit_zero_with_missing_artifact() `EXTRACTED`
- .test_VER_01_exit_zero_with_permission_soft_denial() `EXTRACTED`
- .test_plan_validator_detects_conflicts() `EXTRACTED`
- .test_plan_validator_detects_unsafe_paths() `EXTRACTED`
- .test_verifier_missing_artifact_fails_verification() `EXTRACTED`
- .test_verifier_soft_denial_fails_even_with_exit_code_zero() `EXTRACTED`

### contains
- plan_schema.py `EXTRACTED`

### imports
- orchestrator.py `EXTRACTED`
- planner.py `EXTRACTED`
- scheduler.py `EXTRACTED`
- verifier.py `EXTRACTED`
- planning/__init__.py `EXTRACTED`
- plan_validator.py `EXTRACTED`

### method
- .from_dict() `EXTRACTED`
- .to_dict() `EXTRACTED`

### references
- .schedule_next() `EXTRACTED`
- .validate_plan() `EXTRACTED`
- .plan_project() `EXTRACTED`
- ._build_contracts() `EXTRACTED`
- .verify_task() `EXTRACTED`
- ._auto_serialize_collisions() `EXTRACTED`

### uses
- TestTaskEngine `INFERRED`
- Planner `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- Orchestrator `INFERRED`
- TestVerificationAndRecovery `INFERRED`
- Verifier `INFERRED`
- Scheduler `INFERRED`
- PlanValidator `INFERRED`
- ScheduleDecision `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*