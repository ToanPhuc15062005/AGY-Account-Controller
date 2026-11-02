# MigrationRunner

> God node · 33 connections · `src/agy_mas/storage/migrations/runner.py`

**Community:** [Database](Database.md)

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
- .setUp() `EXTRACTED`

### contains
- runner.py `EXTRACTED`

### imports
- [main.py](main.py.md) `EXTRACTED`
- migrations/__init__.py `EXTRACTED`

### method
- .run_all() `EXTRACTED`
- .__init__() `EXTRACTED`
- ._apply_v1_1_additions() `EXTRACTED`
- ._apply_v1_2_pair_programming() `EXTRACTED`
- ._apply_v1_0_baseline() `EXTRACTED`

### rationale_for
- Manages idempotent schema setup and progressive migrations for AGY-MAS. `EXTRACTED`

### references
- [6.1. Classes & Modules](6.1._Classes_&_Modules.md) `INFERRED`
- MỤC LỤC TỔNG QUAN `INFERRED`
- 2.2. Điều Phối Migration Tự Động & Idempotent: `MigrationRunner` `INFERRED`
- Chiến lược mở rộng schema an toàn (Schema Evolution Safety) `INFERRED`

### uses
- [Database](Database.md) `INFERRED`
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) `INFERRED`
- TestTaskEngine `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- TestPairProgramming `INFERRED`
- TestVerificationAndRecovery `INFERRED`
- TestAGYAdapterAndQuota `INFERRED`
- [TestStorageLayer](TestStorageLayer.md) `INFERRED`
- TestOrchestrator `INFERRED`
- TestPlanner `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*