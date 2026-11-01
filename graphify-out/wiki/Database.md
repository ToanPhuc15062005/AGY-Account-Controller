# Database

> God node · 55 connections · `src/agy_mas/storage/database.py`

**Community:** [Community 21](Community_21.md)

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
- database.py `EXTRACTED`

### imports
- main.py `EXTRACTED`
- runner.py `EXTRACTED`
- task_repo.py `EXTRACTED`
- resource_repo.py `EXTRACTED`
- event_repo.py `EXTRACTED`
- artifact_repo.py `EXTRACTED`
- project_repo.py `EXTRACTED`
- execution_repo.py `EXTRACTED`
- approval_repo.py `EXTRACTED`
- storage/__init__.py `EXTRACTED`

### method
- .transaction() `EXTRACTED`
- .fetchall() `EXTRACTED`
- .fetchone() `EXTRACTED`
- .connect() `EXTRACTED`
- .execute() `EXTRACTED`
- ._create_connection() `EXTRACTED`
- .__init__() `EXTRACTED`
- .close() `EXTRACTED`

### rationale_for
- Manages SQLite database connections and transactions with robust pragmas. `EXTRACTED`

### references
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [ResourceRepository](ResourceRepository.md) `INFERRED`
- [TaskRepository](TaskRepository.md) `INFERRED`
- [MigrationRunner](MigrationRunner.md) `INFERRED`
- [ExecutionRepository](ExecutionRepository.md) `INFERRED`
- [EventRepository](EventRepository.md) `INFERRED`
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) `INFERRED`
- ProjectRepository `INFERRED`
- TestTaskEngine `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- ArtifactRepository `INFERRED`
- TestVerificationAndRecovery `INFERRED`
- TestAGYAdapterAndQuota `INFERRED`
- TestStorageLayer `INFERRED`
- TestOrchestrator `INFERRED`
- TestPlanner `INFERRED`
- ApprovalRepository `INFERRED`
- check_account_status() `INFERRED`
- get_active_workers_info() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*