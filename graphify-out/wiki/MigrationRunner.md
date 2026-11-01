# MigrationRunner

> God node · 26 connections · `src/agy_mas/storage/migrations/runner.py`

**Community:** [Community 22](Community_22.md)

## Connections by Relation

### calls
- init_mas() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`

### contains
- runner.py `EXTRACTED`

### imports
- main.py `EXTRACTED`
- migrations/__init__.py `EXTRACTED`

### method
- .run_all() `EXTRACTED`
- .__init__() `EXTRACTED`
- ._apply_v1_1_additions() `EXTRACTED`
- ._apply_v1_0_baseline() `EXTRACTED`

### rationale_for
- Manages idempotent schema setup and progressive migrations for AGY-MAS. `EXTRACTED`

### uses
- [Database](Database.md) `INFERRED`
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) `INFERRED`
- TestTaskEngine `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- TestVerificationAndRecovery `INFERRED`
- TestAGYAdapterAndQuota `INFERRED`
- TestStorageLayer `INFERRED`
- TestOrchestrator `INFERRED`
- TestPlanner `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*