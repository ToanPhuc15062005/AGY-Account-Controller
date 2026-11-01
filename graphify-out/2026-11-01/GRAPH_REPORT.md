# Graph Report - multi-agy-tool  (2026-11-01)

## Corpus Check
- 69 files · ~57,709 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: .cmd 3, (none) 1)

## Summary
- 876 nodes · 2348 edges · 59 communities (30 shown, 29 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 592 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `707f6fc6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- TaskContract
- agy_controller.py
- orchestrator.py
- PathPolicy
- WorkspaceManager
- config.py
- MigrationRunner
- GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
- Database
- base.py
- TestStorageLayer
- .snapshot_file
- AGYAdapter
- Invocation
- RuntimeEvent
- .transition
- .setUp
- MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT
- TestAGYAdapterAndQuota
- ConfigurableTestAdapter
- GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
- main.py
- DependencyGraph
- Antigravity Controller & Multi-Agent System (`agy-mas`)
- planner.py
- ResourceRepository
- GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
- Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows
- .register_task_artifacts
- .resolve_safe_path
- Verifier
- 3. CHƯƠNG 2: ĐỘNG CƠ TÁC VỤ & LẬP KẾ HOẠCH (TASK ENGINE - PHASE 2)
- 2.5. Hệ Thống 7 Repositories Chuyên Biệt
- MockAdapter
- .dispatch
- 2. CHƯƠNG 1: TẦNG LƯU TRỮ BỀN VỮNG (STORAGE LAYER - PHASE 1)
- CredentialSwitchLock
- 00_master_study_guide.md
- 3. CÁC DESIGN PATTERNS CỐT LÕI
- 6. CHƯƠNG 5: THỰC HÀNH & BÀI TẬP CHUYÊN SÂU (HANDS-ON LAB)
- 1. `ArtifactChecker` ([artifact_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/artifact_checker.py))
- Các Data Transfer Objects (DTO) cốt lõi:
- recovery_manager.py

## God Nodes (most connected - your core abstractions)
1. `Database` - 63 edges
2. `TaskContract` - 48 edges
3. `ResourceRepository` - 46 edges
4. `TaskRepository` - 42 edges
5. `WorkspaceManager` - 35 edges
6. `6.1. Classes & Modules` - 34 edges
7. `PathPolicy` - 31 edges
8. `Orchestrator` - 30 edges
9. `MigrationRunner` - 30 edges
10. `EventRepository` - 30 edges

## Surprising Connections (you probably didn't know these)
- `6.3. Hệ Thống Wrappers Windows & Cài Đặt PATH Người Dùng` --references--> `cmd_install()`  [INFERRED]
  docs/study_guide/04_orchestrator_quota_and_cli.md → agy_controller.py
- `📑 Mục lục` --references--> `AgentRuntimeAdapter`  [INFERRED]
  docs/study_guide/03_agents_workspace_and_process_isolation.md → src/agy_mas/agents/base.py
- `Lab 1: Thử nghiệm Cơ chế Tự sát của Windows Job Objects` --references--> `ManagedProcess`  [INFERRED]
  docs/study_guide/03_agents_workspace_and_process_isolation.md → src/agy_mas/agents/process_manager.py
- `2.2. Nguyên Tắc Modular Monolith` --references--> `Orchestrator`  [INFERRED]
  docs/study_guide/01_architecture_and_design_patterns.md → src/agy_mas/core/orchestrator.py
- `Lab 4: Thiết Kế Adapter Mới (30 phút)` --references--> `Orchestrator`  [INFERRED]
  docs/study_guide/01_architecture_and_design_patterns.md → src/agy_mas/core/orchestrator.py

## Import Cycles
- None detected.

## Communities (59 total, 29 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (3): IO_COUNTERS, JOBOBJECT_BASIC_LIMIT_INFORMATION, DummyProcess

### Community 1 - "TaskContract"
Cohesion: 0.20
Nodes (10): Capstone: Thiết Kế Hệ Thống CI/CD Multi-Agent, 3.1. Hợp Đồng Tác Vụ Cứng Cáp: `TaskContract`, Các thành phần chi tiết trong Hợp Đồng, AcceptanceCriterion, ExpectedArtifact, OutputScope, PermissionProfile, TaskContract (+2 more)

### Community 2 - "agy_controller.py"
Cohesion: 0.06
Nodes (53): build_table_lines(), check_account_status(), cmd_check(), cmd_check_all(), cmd_config(), cmd_current(), cmd_delete(), cmd_install() (+45 more)

### Community 3 - "orchestrator.py"
Cohesion: 0.17
Nodes (9): 1.3. Mục Tiêu Học Tập (Learning Outcomes), 3.2. State Machine Pattern, Luồng tương tác 6 bước chuẩn hóa, 3.2. Bộ Khởi Chạy `Dispatcher`, ManagedProcess, Dispatcher, ScheduleDecision, TaskState (+1 more)

### Community 4 - "PathPolicy"
Cohesion: 0.20
Nodes (4): AcceptanceChecker, ArtifactChecker, VerificationReport, PathPolicy

### Community 5 - "WorkspaceManager"
Cohesion: 0.11
Nodes (17): 4.1. Chuyên Đề 01 — Kiến Trúc & Design Patterns, 4.2. Chuyên Đề 02 — Storage Layer & Task Engine, 4.3. Chuyên Đề 03 — Agents, Workspace & Process Isolation, 4. TÓM TẮT NỘI DUNG TỪNG CHUYÊN ĐỀ, 6.1. Classes & Modules, 3.4. Facade Pattern — `WorkspaceManager`, 9. CÂU HỎI ÔN TẬP, Câu hỏi mức Hiểu (Understanding) (+9 more)

### Community 6 - "config.py"
Cohesion: 0.05
Nodes (20): get_active_workers_info(), 4.2. Xử lý Xung đột Khóa File Windows: WinError 32/33 (`file_lock_manager.py`), Bản chất kỹ thuật của `WinError 32` & `WinError 33`:, Giải pháp trong `WindowsFileRetryManager`:, 5.3. Lá Chắn Kiến Trúc: Ngăn Chặn Poisoning Xác Thực Chéo, FailoverConfig, MASConfig, QuotaConfig (+12 more)

### Community 7 - "MigrationRunner"
Cohesion: 0.27
Nodes (3): 2.2. Điều Phối Migration Tự Động & Idempotent: `MigrationRunner`, Chiến lược mở rộng schema an toàn (Schema Evolution Safety), MigrationRunner

### Community 8 - "GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS"
Cohesion: 0.06
Nodes (25): 10. BÀI TẬP THỰC HÀNH, 1. GIỚI THIỆU & BỐI CẢNH BÀI TOÁN, 2.1. Sơ Đồ Tổng Thể & Vai Trò Từng Tầng, 2.2. Nguyên Tắc Modular Monolith, 2. KIẾN TRÚC PHÂN TẦNG 6 PHASE, 4. CÁC QUYẾT ĐỊNH KIẾN TRÚC (ADR), 5. GOD NODES & ĐIỂM KẾT NỐI TRUNG TÂM, 6. SƠ ĐỒ QUAN HỆ THỰC THỂ (ERD TỔNG QUÁT) (+17 more)

### Community 9 - "Database"
Cohesion: 0.18
Nodes (8): init_mas(), RecoveryManager, Database, EventRepository, ExecutionRepository, ProjectRepository, TaskRepository, TestPlanner

### Community 15 - "AGYAdapter"
Cohesion: 0.24
Nodes (4): 1. Biên dịch cờ lệnh dòng lệnh (`build_invocation`):, 2. Phân loại lỗi theo bảng phân loại (Section 10 Error Taxonomy):, 3.4. Headless AGY Adapter (`adapters/agy_adapter.py`) & Phân loại lỗi đa tầng, AGYAdapter

### Community 19 - ".transition"
Cohesion: 0.13
Nodes (7): 3.2. Cỗ Máy Trạng Thái 12 Bước: `TaskStateMachine`, 7. TỔNG KẾT & BẢNG TRA CỨU NHANH (CHEAT SHEET), Bảng Tra Cứu 12 Trạng Thái Task, Bảng Tra Cứu Các Lỗi Thường Gặp & Cách Khắc Phục, Ma Trận Chuyển Đổi Hợp Lệ (`VALID_TRANSITIONS`), Sơ Đồ Chuyển Đổi Trạng Thái (State Transition Diagram), InvalidStateTransitionError

### Community 22 - "MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT"
Cohesion: 0.05
Nodes (34): 10. ĐÁP ÁN GỢI Ý & HƯỚNG DẪN TỰ ĐÁNH GIÁ, 1.1. AGY-MAS Là Gì?, 1.2. Các Con Số Quan Trọng, 1. TỔNG QUAN HỆ THỐNG & MỤC TIÊU HỌC TẬP, 2. BẢN ĐỒ KIẾN TRÚC & QUAN HỆ GIỮA CÁC CHUYÊN ĐỀ, 3.1. Lộ Trình Nhanh (4 giờ) — Nắm bắt toàn cảnh, 3.2. Lộ Trình Chuyên Sâu (12-16 giờ) — Hiểu toàn diện, 3.3. Thứ Tự Ưu Tiên Đọc Code (+26 more)

### Community 25 - "GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS"
Cohesion: 0.07
Nodes (30): 1.1. Vị Trí Của Orchestrator, Quota Tracker và CLI Trong Hệ Thống Multi-Agent, 1.2. Thách Thức Kỹ Thuật Cốt Lõi Trên Môi Trường Windows, 1.3. 4 Trụ Cột Kiến Trúc (Architecture Tenets), 1. TỔNG QUAN KIẾN TRÚC & TRIẾT LÝ ĐIỀU PHỐI, 2.1. Cấu Trúc và Trách Nhiệm Của `Orchestrator`, 2.2. Chu Trình Tick Loop (`.tick()`): 3 Giai Đoạn Vận Hành, 2.3. Đối Soát Tiến Trình (Active Executions Reconciliation), 2.4. Phân Loại Thất Bại & Cooldown Hạn Ngạch (+22 more)

### Community 34 - "main.py"
Cohesion: 0.16
Nodes (9): 3.5. Trình Phân Rã Kế Hoạch Tự Động: `Planner`, cmd_orchestrate(), cmd_plan(), cmd_project(), cmd_resource(), cmd_run(), cmd_task(), main() (+1 more)

### Community 35 - "DependencyGraph"
Cohesion: 0.16
Nodes (4): Tổng Kết & Bảng Tra Cứu Nhanh, Hướng Dẫn Giải:, DependencyGraph, TestTaskEngine

### Community 36 - "Antigravity Controller & Multi-Agent System (`agy-mas`)"
Cohesion: 0.10
Nodes (20): 1. Kiểm tra tổng quan toàn bộ tài khoản (`check-all` hoặc `check`), 1. Quản lý dự án (`project`), 2. Kiểm tra sâu & Tự động Refresh Token (`check <STT / Tên>`), 2. Tự động sinh kế hoạch cho dự án đã có (`plan`), 3. Bảng giải thích chi tiết ký hiệu trạng thái:, 3. Quản lý tác vụ tùy chỉnh (`task`), 4. Khởi chạy điều phối Multi-Agent (`orchestrate`), 5. Giám sát hạn ngạch & tài nguyên (`resource`) (+12 more)

### Community 37 - "planner.py"
Cohesion: 0.17
Nodes (4): CycleDetectedError, InputScope, PlanValidationError, PlanValidator

### Community 38 - "ResourceRepository"
Cohesion: 0.24
Nodes (7): MỤC LỤC TỔNG QUAN, 🚀 Tính năng cốt lõi của Multi-Agent System (`agy-mas`), Orchestrator, Scheduler, QuotaTracker, ResourceRepository, TestOrchestrator

### Community 39 - "GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS"
Cohesion: 0.12
Nodes (16): 1.1. Bối Cảnh Bài Toán và Vị Trí Của Storage & Task Engine, 1.2. Các Thách Thức Kỹ Thuật Trên Môi Trường Windows, 1.3. Các Nguyên Lý Cốt Lõi, 1. TỔNG QUAN KIẾN TRÚC & TRIẾT LÝ THIẾT KẾ, 4.1. Cơ Chế Phối Hợp Với `Scheduler`, 4.2. Dòng Chảy Dữ Liệu Từ Task Creation Đến Accepted / Failed, 4.3. Bất Biến Trong Ghi Nhận Lịch Sử Thực Thi (Immutable Executions), 4. CHƯƠNG 3: GIAO THOA GIỮA STORAGE LAYER & TASK ENGINE (+8 more)

### Community 40 - "Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows"
Cohesion: 0.13
Nodes (15): 1. Tổng quan & Mục tiêu đào tạo (Overview & Objectives), 2. Kiến trúc Tổng thể: Agents - Workspace - Verification Pipeline, 6.1. Sequence Diagram: Vòng đời Thực thi Một Tác vụ, 6.2. Cô lập Tài khoản Đa tiến trình với `CredentialSwitchLock`, 6.3. Khắc phục Sự cố Sập nguồn & Dọn rác Tiến trình Chết (`recovery/`), 6. Phối hợp Điều phối, Đa tài khoản & Tự động Phục hồi, 8. Bài tập Thực hành & Kịch bản Tự luyện (Hands-on Labs), 9. Câu hỏi Ôn tập & Hướng dẫn Đọc tiếp (+7 more)

### Community 41 - ".register_task_artifacts"
Cohesion: 0.14
Nodes (11): 4.3. Quản trị Quyền Ghi theo Lease Mẫu Đường dẫn (`ownership_manager.py`), 4.4. Snapshot Deliverables & Quyết định Kiến trúc ADR-016 (`snapshot_manager.py`), 4.5. Facade Điều phối Workspace (`workspace_manager.py`), 4. Phân hệ Quản trị Workspace & Windows Hardening (`workspace/`), Quy tắc kiểm tra xung đột:, Vì sao quy tắc này sống còn?, 7.1. Chống Race Condition Khi Tráo Đổi Credential Giữa Nhiều Workers, 7.3. Triệt Tiêu Tiến Trình Con Mồ Côi Bằng Windows Job Objects (+3 more)

### Community 43 - "Verifier"
Cohesion: 0.29
Nodes (4): 5.3. Verification Engine: Thực thi ADR-014 và ADR-017, Lab 3: Thiết lập Pipeline Xác minh cho Tác vụ Sinh Code, ScopeChecker, Verifier

### Community 45 - "3. CHƯƠNG 2: ĐỘNG CƠ TÁC VỤ & LẬP KẾ HOẠCH (TASK ENGINE - PHASE 2)"
Cohesion: 0.22
Nodes (7): 3.3. Đồ Thị Ràng Buộc DAG & Thuật Toán Kahn: `DependencyGraph`, 3.4. Bộ Thẩm Định Kế Hoạch 5 Tầng: `PlanValidator`, 3. CHƯƠNG 2: ĐỘNG CƠ TÁC VỤ & LẬP KẾ HOẠCH (TASK ENGINE - PHASE 2), Biểu diễn nội tại, Thuật toán Kahn trong sắp xếp Topo & Phát hiện Chu trình, Thuật toán phát hiện Xung Đột Ghi Đè Song Song (Concurrent Write Scope Collisions), Tính Toán Tác Vụ Sẵn Sàng (`get_ready_tasks`)

### Community 46 - "2.5. Hệ Thống 7 Repositories Chuyên Biệt"
Cohesion: 0.25
Nodes (8): 1. [`ProjectRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/project_repo.py#L9), 2.5. Hệ Thống 7 Repositories Chuyên Biệt, 2. [`TaskRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/task_repo.py#L9), 3. [`ExecutionRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/execution_repo.py#L9), 4. [`EventRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/event_repo.py#L10), 5. [`ArtifactRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/artifact_repo.py#L10), 6. [`ResourceRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/resource_repo.py#L8), 7. [`ApprovalRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/approval_repo.py#L10)

### Community 49 - "2. CHƯƠNG 1: TẦNG LƯU TRỮ BỀN VỮNG (STORAGE LAYER - PHASE 1)"
Cohesion: 0.29
Nodes (7): 2.1. Quản Lý Kết Nối & Transaction Context: `Database`, 2.3. Lược Đồ Cơ Sở Dữ Liệu & Entity Relationship Diagram (ERD), 2.4. Phân Tích 10 Bảng Dữ Liệu Chi Tiết, 2. CHƯƠNG 1: TẦNG LƯU TRỮ BỀN VỮNG (STORAGE LAYER - PHASE 1), Cấu hình Pragmas gia cố (Hardened Pragmas), Thread-Local Connection Pattern, Transaction Context Manager

### Community 52 - "3. CÁC DESIGN PATTERNS CỐT LÕI"
Cohesion: 0.33
Nodes (5): 3.1. Repository Pattern & Data Access Layer, 3.3. Adapter Pattern — `AgentRuntimeAdapter`, 3.5. Strategy Pattern — Error Taxonomy, 3.6. Observer Pattern — Event Sourcing, 3. CÁC DESIGN PATTERNS CỐT LÕI

### Community 53 - "6. CHƯƠNG 5: THỰC HÀNH & BÀI TẬP CHUYÊN SÂU (HANDS-ON LAB)"
Cohesion: 0.33
Nodes (6): 6. CHƯƠNG 5: THỰC HÀNH & BÀI TẬP CHUYÊN SÂU (HANDS-ON LAB), Bài Tập Tự Luyện (Comprehensive Exercises), Lab 1: Khởi Tạo Storage, Nạp Schema, Thiết Lập DAG Tasks Đa Tầng, Lab 2: Thực Thi Vòng Đời State Machine Với Monotonic Event Logging, Lab 3: Thẩm Định Kế Hoạch Và Tự Động Phát Hiện Write Collisions, Đề Bài: Thiết Kế DAG Cho Hệ Thống Microservices

### Community 54 - "1. `ArtifactChecker` ([artifact_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/artifact_checker.py))"
Cohesion: 0.33
Nodes (6): 1. `ArtifactChecker` ([artifact_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/artifact_checker.py)), 2. `ScopeChecker` ([scope_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/scope_checker.py)), 3. `AcceptanceChecker` ([acceptance_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/acceptance_checker.py)), 5.1. Triết lý "Exit Code 0 không đồng nghĩa với Thành công", 5.2. Các Bộ kiểm định Chuyên biệt: Artifact, Scope và Acceptance Criteria, 5. Đường ống Thẩm định & Xác minh Tác vụ Độc lập (`verification/`)

### Community 55 - "Các Data Transfer Objects (DTO) cốt lõi:"
Cohesion: 0.33
Nodes (6): 3.1. Hợp đồng trừu tượng `AgentRuntimeAdapter` & Event Model, 3.2. Giám sát tiến trình cấp thấp & Windows Job Objects (`process_manager.py`), 3. Phân hệ Agent Runtime & Process Supervision (`agents/`), Các Data Transfer Objects (DTO) cốt lõi:, Cơ chế thiết lập Win32 Job Object:, JOBOBJECT_EXTENDED_LIMIT_INFORMATION

## Knowledge Gaps
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Database` connect `Database` to `main.py`, `TaskContract`, `agy_controller.py`, `main.py`, `DependencyGraph`, `WorkspaceManager`, `config.py`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`, `MigrationRunner`, `ResourceRepository`, `TestStorageLayer`, `2. CHƯƠNG 1: TẦNG LƯU TRỮ BỀN VỮNG (STORAGE LAYER - PHASE 1)`, `.transaction`, `.setUp`, `.fetchall`, `MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT`, `TestAGYAdapterAndQuota`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `Database` (e.g. with `check_account_status()` and `get_active_workers_info()`) actually correct?**
  _`Database` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07272727272727272 - nodes in this community are weakly interconnected._
- **Why does `6.1. Classes & Modules` connect `WorkspaceManager` to `TaskContract`, `main.py`, `DependencyGraph`, `orchestrator.py`, `planner.py`, `ResourceRepository`, `MigrationRunner`, `PathPolicy`, `Database`, `config.py`, `Verifier`, `AGYAdapter`, `.setUp`, `MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `TaskContract` (e.g. with `1.3. Mục Tiêu Học Tập (Learning Outcomes)` and `6.1. Classes & Modules`) actually correct?**
  _`TaskContract` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Should `agy_controller.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._
- **Why does `TaskContract` connect `TaskContract` to `main.py`, `DependencyGraph`, `orchestrator.py`, `WorkspaceManager`, `Antigravity Controller & Multi-Agent System (`agy-mas`)`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`, `Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows`, `ResourceRepository`, `Verifier`, `planner.py`, `3. CHƯƠNG 2: ĐỘNG CƠ TÁC VỤ & LẬP KẾ HOẠCH (TASK ENGINE - PHASE 2)`, `6. CHƯƠNG 5: THỰC HÀNH & BÀI TẬP CHUYÊN SÂU (HANDS-ON LAB)`, `PathPolicy`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._