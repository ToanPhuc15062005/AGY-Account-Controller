# Database

> God node · 68 connections · `src/agy_mas/storage/database.py`

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
- database.py `EXTRACTED`

### imports
- [main.py](main.py.md) `EXTRACTED`
- runner.py `EXTRACTED`
- task_repo.py `EXTRACTED`
- resource_repo.py `EXTRACTED`
- event_repo.py `EXTRACTED`
- artifact_repo.py `EXTRACTED`
- project_repo.py `EXTRACTED`
- execution_repo.py `EXTRACTED`
- approval_repo.py `EXTRACTED`
- review_repo.py `EXTRACTED`
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
- [6.1. Classes & Modules](6.1._Classes_&_Modules.md) `INFERRED`
- MỤC LỤC TỔNG QUAN `INFERRED`
- 5. GOD NODES & ĐIỂM KẾT NỐI TRUNG TÂM `INFERRED`
- 2.1. Quản Lý Kết Nối & Transaction Context: `Database` `INFERRED`
- Lab 1: Khám Phá Knowledge Graph (15 phút) `INFERRED`
- 4.1. Chuyên Đề 01 — Kiến Trúc & Design Patterns `INFERRED`
- Câu hỏi mức Hiểu (Understanding) `INFERRED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- 1.2. Các Con Số Quan Trọng `INFERRED`

### uses
- [ResourceRepository](ResourceRepository.md) `INFERRED`
- [TaskRepository](TaskRepository.md) `INFERRED`
- [MigrationRunner](MigrationRunner.md) `INFERRED`
- EventRepository `INFERRED`
- [ExecutionRepository](ExecutionRepository.md) `INFERRED`
- ProjectRepository `INFERRED`
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) `INFERRED`
- ArtifactRepository `INFERRED`
- TestTaskEngine `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- TestPairProgramming `INFERRED`
- TestVerificationAndRecovery `INFERRED`
- TestAGYAdapterAndQuota `INFERRED`
- [TestStorageLayer](TestStorageLayer.md) `INFERRED`
- [ApprovalRepository](ApprovalRepository.md) `INFERRED`
- ReviewRepository `INFERRED`
- TestOrchestrator `INFERRED`
- TestPlanner `INFERRED`
- get_active_workers_info() `INFERRED`
- check_account_status() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*