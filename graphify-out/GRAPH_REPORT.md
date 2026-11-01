# Graph Report - multi-agy-tool  (2026-11-01)

## Corpus Check
- 74 files · ~62,485 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: .cmd 3, (none) 1)

## Summary
- 953 nodes · 2552 edges · 57 communities (35 shown, 22 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 638 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f09e41a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- TaskContract
- agy_controller.py
- TaskStateMachine
- PathPolicy
- OwnershipManager
- FileSharingContentionError
- ReviewEngine
- GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
- Database
- MockAdapter
- TaskRepository
- TestStorageLayer
- WindowsFileRetryManager
- ExecutionRepository
- AGYAdapter
- Invocation
- AgentRuntimeAdapter
- .transition
- config.py
- TestWorkspaceCoordination
- MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT
- ARCHITECTURE BASELINE (BEFORE: HIỆN TRẠNG HỆ THỐNG)
- ConfigurableTestAdapter
- GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
- main.py
- ARCHITECTURE PROPOSAL (AFTER: KIẾN TRÚC PAIR-PROGRAMMING)
- Antigravity Controller & Multi-Agent System (`agy-mas`)
- 2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)
- ResourceRepository
- GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
- Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows
- .register_task_artifacts
- .resolve_safe_path
- Verifier
- .fetchone
- 8. CÂU HỎI ÔN TẬP TỔNG HỢP (LIÊN CHUYÊN ĐỀ)
- 2.5. Hệ Thống 7 Repositories Chuyên Biệt
- Orchestrator
- 1.3. Mục Tiêu Học Tập (Learning Outcomes)
- DummyProcess
- CredentialSwitchLock
- 7.2. Integration Acceptance Criteria
- 3. CÁC DESIGN PATTERNS CỐT LÕI
- .test_pair_programming_circuit_breaker
- .test_pair_programming_approval_flow
- ManagedProcess
- recovery_manager.py

## God Nodes (most connected - your core abstractions)
1. `Database` - 68 edges
2. `TaskContract` - 53 edges
3. `ResourceRepository` - 47 edges
4. `TaskRepository` - 44 edges
5. `Orchestrator` - 38 edges
6. `WorkspaceManager` - 37 edges
7. `6.1. Classes & Modules` - 34 edges
8. `MigrationRunner` - 33 edges
9. `QuotaTracker` - 31 edges
10. `EventRepository` - 31 edges

## Surprising Connections (you probably didn't know these)
- `5.3. Lá Chắn Kiến Trúc: Ngăn Chặn Poisoning Xác Thực Chéo` --references--> `get_active_workers_info()`  [INFERRED]
  docs/study_guide/04_orchestrator_quota_and_cli.md → agy_controller.py
- `6.3. Hệ Thống Wrappers Windows & Cài Đặt PATH Người Dùng` --references--> `cmd_install()`  [INFERRED]
  docs/study_guide/04_orchestrator_quota_and_cli.md → agy_controller.py
- `📑 Mục lục` --references--> `AgentRuntimeAdapter`  [INFERRED]
  docs/study_guide/03_agents_workspace_and_process_isolation.md → src/agy_mas/agents/base.py
- `Lab 1: Thử nghiệm Cơ chế Tự sát của Windows Job Objects` --references--> `ManagedProcess`  [INFERRED]
  docs/study_guide/03_agents_workspace_and_process_isolation.md → src/agy_mas/agents/process_manager.py
- `2.2. Nguyên Tắc Modular Monolith` --references--> `Orchestrator`  [INFERRED]
  docs/study_guide/01_architecture_and_design_patterns.md → src/agy_mas/core/orchestrator.py

## Import Cycles
- None detected.

## Communities (57 total, 22 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.08
Nodes (3): IO_COUNTERS, JOBOBJECT_BASIC_LIMIT_INFORMATION, ScheduleDecision

### Community 1 - "TaskContract"
Cohesion: 0.05
Nodes (31): Capstone: Thiết Kế Hệ Thống CI/CD Multi-Agent, Tổng Kết & Bảng Tra Cứu Nhanh, 3.1. Hợp Đồng Tác Vụ Cứng Cáp: `TaskContract`, 3.3. Đồ Thị Ràng Buộc DAG & Thuật Toán Kahn: `DependencyGraph`, 3.4. Bộ Thẩm Định Kế Hoạch 5 Tầng: `PlanValidator`, 3.5. Trình Phân Rã Kế Hoạch Tự Động: `Planner`, 3. CHƯƠNG 2: ĐỘNG CƠ TÁC VỤ & LẬP KẾ HOẠCH (TASK ENGINE - PHASE 2), Biểu diễn nội tại (+23 more)

### Community 2 - "agy_controller.py"
Cohesion: 0.06
Nodes (54): build_table_lines(), check_account_status(), cmd_check(), cmd_check_all(), cmd_config(), cmd_current(), cmd_delete(), cmd_install() (+46 more)

### Community 4 - "PathPolicy"
Cohesion: 0.16
Nodes (7): 1. `ArtifactChecker` ([artifact_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/artifact_checker.py)), 🚀 Tính năng cốt lõi của Multi-Agent System (`agy-mas`), AcceptanceChecker, ArtifactChecker, ScopeChecker, VerificationReport, PathPolicy

### Community 5 - "OwnershipManager"
Cohesion: 0.12
Nodes (7): 1. Tổng quan & Mục tiêu đào tạo (Overview & Objectives), 2. Kiến trúc Tổng thể: Agents - Workspace - Verification Pipeline, Luồng tương tác 6 bước chuẩn hóa, Mục tiêu học tập (Learning Objectives), Sơ đồ tương tác kiến trúc hệ thống, OwnershipConflictError, OwnershipManager

### Community 6 - "FileSharingContentionError"
Cohesion: 0.11
Nodes (5): 4.2. Xử lý Xung đột Khóa File Windows: WinError 32/33 (`file_lock_manager.py`), Bản chất kỹ thuật của `WinError 32` & `WinError 33`:, Giải pháp trong `WindowsFileRetryManager`:, FileSharingContentionError, is_windows_sharing_violation()

### Community 7 - "ReviewEngine"
Cohesion: 0.16
Nodes (3): ReviewEngine, ReviewReport, ReviewVerdict

### Community 8 - "GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS"
Cohesion: 0.08
Nodes (24): 10. BÀI TẬP THỰC HÀNH, 1. GIỚI THIỆU & BỐI CẢNH BÀI TOÁN, 2.1. Sơ Đồ Tổng Thể & Vai Trò Từng Tầng, 2.2. Nguyên Tắc Modular Monolith, 2. KIẾN TRÚC PHÂN TẦNG 6 PHASE, 4. CÁC QUYẾT ĐỊNH KIẾN TRÚC (ADR), 6. SƠ ĐỒ QUAN HỆ THỰC THỂ (ERD TỔNG QUÁT), 7.1. Bốn Trụ Cột Kiến Trúc (+16 more)

### Community 9 - "Database"
Cohesion: 0.17
Nodes (10): 2.2. Điều Phối Migration Tự Động & Idempotent: `MigrationRunner`, Chiến lược mở rộng schema an toàn (Schema Evolution Safety), init_mas(), Database, MigrationRunner, EventRepository, ExecutionRepository, ProjectRepository (+2 more)

### Community 13 - "WindowsFileRetryManager"
Cohesion: 0.13
Nodes (8): 4.3. Chuyên Đề 03 — Agents, Workspace & Process Isolation, 7. Ma trận Kiểm thử & Đối sánh Chuẩn Kiến trúc v1.1, WindowsFileRetryConfig, windows_file_retry(), decorator(), WindowsFileRetryManager, SnapshotManager, SnapshotTimingError

### Community 15 - "AGYAdapter"
Cohesion: 0.15
Nodes (6): 1. Biên dịch cờ lệnh dòng lệnh (`build_invocation`):, 2. Phân loại lỗi theo bảng phân loại (Section 10 Error Taxonomy):, 3.4. Headless AGY Adapter (`adapters/agy_adapter.py`) & Phân loại lỗi đa tầng, AGYAdapter, RuntimeEvent, TestAGYAdapterAndQuota

### Community 16 - "Invocation"
Cohesion: 0.15
Nodes (3): 7.2. Rào Cản Cờ `--effort` Giữa Các Dòng Mô Hình, Invocation, MockPairAdapter

### Community 18 - "AgentRuntimeAdapter"
Cohesion: 0.25
Nodes (4): 3.1. Hợp đồng trừu tượng `AgentRuntimeAdapter` & Event Model, Các Data Transfer Objects (DTO) cốt lõi:, AgentRuntimeAdapter, TerminationResult

### Community 19 - ".transition"
Cohesion: 0.15
Nodes (8): 3.2. State Machine Pattern, 3.2. Cỗ Máy Trạng Thái 12 Bước: `TaskStateMachine`, 7. TỔNG KẾT & BẢNG TRA CỨU NHANH (CHEAT SHEET), Bảng Tra Cứu 12 Trạng Thái Task, Bảng Tra Cứu Các Lỗi Thường Gặp & Cách Khắc Phục, Ma Trận Chuyển Đổi Hợp Lệ (`VALID_TRANSITIONS`), Sơ Đồ Chuyển Đổi Trạng Thái (State Transition Diagram), InvalidStateTransitionError

### Community 20 - "config.py"
Cohesion: 0.20
Nodes (9): get_active_workers_info(), FailoverConfig, MASConfig, QuotaConfig, QuotaCooldownConfig, QuotaDetectionConfig, RuntimeConfig, StorageConfig (+1 more)

### Community 22 - "MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT"
Cohesion: 0.15
Nodes (13): 2. BẢN ĐỒ KIẾN TRÚC & QUAN HỆ GIỮA CÁC CHUYÊN ĐỀ, 3.1. Lộ Trình Nhanh (4 giờ) — Nắm bắt toàn cảnh, 3.2. Lộ Trình Chuyên Sâu (12-16 giờ) — Hiểu toàn diện, 3.3. Thứ Tự Ưu Tiên Đọc Code, 3. LỘ TRÌNH HỌC TẬP KHUYẾN NGHỊ, 5. SƠ ĐỒ TỔNG HỢP KIẾN TRÚC ĐẦY ĐỦ, 6.2. Lệnh CLI Tra Cứu Nhanh, 6.3. ADR Quick Reference (+5 more)

### Community 23 - "ARCHITECTURE BASELINE (BEFORE: HIỆN TRẠNG HỆ THỐNG)"
Cohesion: 0.18
Nodes (10): 1. Cấu trúc Hợp đồng Tác vụ Hiện tại (`plan_schema.py`), 2. Vòng đời Tác vụ & Khâu Thẩm định Hiện tại (`orchestrator.py`), 3. Cơ chế Khởi tạo Prompt và Thử lại Hiện tại (`agy_adapter.py`), 4. Mô hình Lưu trữ Database Hiện tại (`schema.sql`), ARCHITECTURE BASELINE (BEFORE: HIỆN TRẠNG HỆ THỐNG), Hạn chế:, Hạn chế hiện tại:, Hạn chế hiện tại: (+2 more)

### Community 25 - "GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS"
Cohesion: 0.05
Nodes (38): 10. ĐÁP ÁN GỢI Ý & HƯỚNG DẪN TỰ ĐÁNH GIÁ, Rubric Tự Đánh Giá, Đáp Án Câu Hỏi Ôn Tập (Chọn Lọc), 1.1. Vị Trí Của Orchestrator, Quota Tracker và CLI Trong Hệ Thống Multi-Agent, 1.2. Thách Thức Kỹ Thuật Cốt Lõi Trên Môi Trường Windows, 1.3. 4 Trụ Cột Kiến Trúc (Architecture Tenets), 1. TỔNG QUAN KIẾN TRÚC & TRIẾT LÝ ĐIỀU PHỐI, 3.1. Bộ Lập Lịch Đồ Thị `Scheduler` (+30 more)

### Community 34 - "main.py"
Cohesion: 0.36
Nodes (6): cmd_orchestrate(), cmd_project(), cmd_resource(), cmd_run(), cmd_task(), main()

### Community 35 - "ARCHITECTURE PROPOSAL (AFTER: KIẾN TRÚC PAIR-PROGRAMMING)"
Cohesion: 0.18
Nodes (10): 1. Cấu trúc Hợp đồng Tác vụ Mở rộng (`plan_schema.py`), 2. Nâng cấp Vòng đời Tác vụ: Khâu Thẩm định Chủ động (`orchestrator.py`), 3. Bơm Phản hồi (Feedback Injection) vào Prompt (`agy_adapter.py`), 4. Mở rộng Cơ sở Dữ liệu (`schema.sql` Evolution), 5. Bảng Đối chiếu Trực tiếp: BEFORE vs AFTER, 6. Lưu ý Triển khai Thực tế (Implementation & Runtime Safeguards), A. Đối với Coder khi chạy lại từ Vòng 2 trở đi (`pair_round > 0`):, ARCHITECTURE PROPOSAL (AFTER: KIẾN TRÚC PAIR-PROGRAMMING) (+2 more)

### Community 36 - "Antigravity Controller & Multi-Agent System (`agy-mas`)"
Cohesion: 0.10
Nodes (20): 1. Kiểm tra tổng quan toàn bộ tài khoản (`check-all` hoặc `check`), 1. Quản lý dự án (`project`), 2. Kiểm tra sâu & Tự động Refresh Token (`check <STT / Tên>`), 2. Tự động sinh kế hoạch cho dự án đã có (`plan`), 3. Bảng giải thích chi tiết ký hiệu trạng thái:, 3. Quản lý tác vụ tùy chỉnh (`task`), 4. Khởi chạy điều phối Multi-Agent (`orchestrate`), 5. Giám sát hạn ngạch & tài nguyên (`resource`) (+12 more)

### Community 37 - "2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)"
Cohesion: 0.29
Nodes (7): 2.1. Cấu Trúc và Trách Nhiệm Của `Orchestrator`, 2.2. Chu Trình Tick Loop (`.tick()`): 3 Giai Đoạn Vận Hành, 2.3. Đối Soát Tiến Trình (Active Executions Reconciliation), 2.4. Phân Loại Thất Bại & Cooldown Hạn Ngạch, 2.5. Thẩm Định Nghiệm Thu Artifacts (Verification & Acceptance), 2.6. Đánh Giá Trạng Thái Kết Thúc Dự Án, 2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)

### Community 38 - "ResourceRepository"
Cohesion: 0.11
Nodes (14): 4.1. Chuyên Đề 01 — Kiến Trúc & Design Patterns, 4.2. Chuyên Đề 02 — Storage Layer & Task Engine, 4.4. Chuyên Đề 04 — Orchestrator, Quota & CLI, 4. TÓM TẮT NỘI DUNG TỪNG CHUYÊN ĐỀ, 6.1. Classes & Modules, 5. GOD NODES & ĐIỂM KẾT NỐI TRUNG TÂM, Câu hỏi mức Hiểu (Understanding), Lab 1: Khám Phá Knowledge Graph (15 phút) (+6 more)

### Community 39 - "GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS"
Cohesion: 0.07
Nodes (27): 1.1. Bối Cảnh Bài Toán và Vị Trí Của Storage & Task Engine, 1.2. Các Thách Thức Kỹ Thuật Trên Môi Trường Windows, 1.3. Các Nguyên Lý Cốt Lõi, 1. TỔNG QUAN KIẾN TRÚC & TRIẾT LÝ THIẾT KẾ, 2.1. Quản Lý Kết Nối & Transaction Context: `Database`, 2.3. Lược Đồ Cơ Sở Dữ Liệu & Entity Relationship Diagram (ERD), 2.4. Phân Tích 10 Bảng Dữ Liệu Chi Tiết, 2. CHƯƠNG 1: TẦNG LƯU TRỮ BỀN VỮNG (STORAGE LAYER - PHASE 1) (+19 more)

### Community 40 - "Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows"
Cohesion: 0.12
Nodes (17): 2. `ScopeChecker` ([scope_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/scope_checker.py)), 3. `AcceptanceChecker` ([acceptance_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/acceptance_checker.py)), 5.1. Triết lý "Exit Code 0 không đồng nghĩa với Thành công", 5.2. Các Bộ kiểm định Chuyên biệt: Artifact, Scope và Acceptance Criteria, 5. Đường ống Thẩm định & Xác minh Tác vụ Độc lập (`verification/`), 6.1. Sequence Diagram: Vòng đời Thực thi Một Tác vụ, 6.2. Cô lập Tài khoản Đa tiến trình với `CredentialSwitchLock`, 6.3. Khắc phục Sự cố Sập nguồn & Dọn rác Tiến trình Chết (`recovery/`) (+9 more)

### Community 41 - ".register_task_artifacts"
Cohesion: 0.14
Nodes (8): 3.4. Facade Pattern — `WorkspaceManager`, 4.1. Chính sách An toàn Đường dẫn (`path_policy.py`), 4.3. Quản trị Quyền Ghi theo Lease Mẫu Đường dẫn (`ownership_manager.py`), 4.4. Snapshot Deliverables & Quyết định Kiến trúc ADR-016 (`snapshot_manager.py`), 4.5. Facade Điều phối Workspace (`workspace_manager.py`), 4. Phân hệ Quản trị Workspace & Windows Hardening (`workspace/`), Quy tắc kiểm tra xung đột:, Vì sao quy tắc này sống còn?

### Community 43 - "Verifier"
Cohesion: 0.38
Nodes (3): 5.3. Verification Engine: Thực thi ADR-014 và ADR-017, Lab 3: Thiết lập Pipeline Xác minh cho Tác vụ Sinh Code, Verifier

### Community 45 - "8. CÂU HỎI ÔN TẬP TỔNG HỢP (LIÊN CHUYÊN ĐỀ)"
Cohesion: 0.40
Nodes (5): 8. CÂU HỎI ÔN TẬP TỔNG HỢP (LIÊN CHUYÊN ĐỀ), Nhóm A — Kiến Trúc Tổng Thể, Nhóm B — Data Flow & State, Nhóm C — Windows Hardening, Nhóm E — Design & Trade-offs

### Community 46 - "2.5. Hệ Thống 7 Repositories Chuyên Biệt"
Cohesion: 0.17
Nodes (9): 1. [`ProjectRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/project_repo.py#L9), 2.5. Hệ Thống 7 Repositories Chuyên Biệt, 2. [`TaskRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/task_repo.py#L9), 3. [`ExecutionRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/execution_repo.py#L9), 4. [`EventRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/event_repo.py#L10), 5. [`ArtifactRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/artifact_repo.py#L10), 6. [`ResourceRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/resource_repo.py#L8), 7. [`ApprovalRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/approval_repo.py#L10) (+1 more)

### Community 47 - "Orchestrator"
Cohesion: 0.15
Nodes (3): Orchestrator, TestOrchestrator, dynamic_reviewer()

### Community 48 - "1.3. Mục Tiêu Học Tập (Learning Outcomes)"
Cohesion: 0.50
Nodes (4): 1.1. AGY-MAS Là Gì?, 1.2. Các Con Số Quan Trọng, 1.3. Mục Tiêu Học Tập (Learning Outcomes), 1. TỔNG QUAN HỆ THỐNG & MỤC TIÊU HỌC TẬP

### Community 51 - "7.2. Integration Acceptance Criteria"
Cohesion: 0.67
Nodes (3): 7.1. Bộ Test Suite (37/37 Passing), 7.2. Integration Acceptance Criteria, 7. MA TRẬN KIỂM THỬ & ACCEPTANCE CRITERIA

### Community 52 - "3. CÁC DESIGN PATTERNS CỐT LÕI"
Cohesion: 0.50
Nodes (4): 3.3. Adapter Pattern — `AgentRuntimeAdapter`, 3.5. Strategy Pattern — Error Taxonomy, 3.6. Observer Pattern — Event Sourcing, 3. CÁC DESIGN PATTERNS CỐT LÕI

### Community 55 - "ManagedProcess"
Cohesion: 0.14
Nodes (7): 3.2. Giám sát tiến trình cấp thấp & Windows Job Objects (`process_manager.py`), 3.3. Thu thập Stream bất đồng bộ Non-blocking & Bộ ngắt tiến trình 2 lớp, 3. Phân hệ Agent Runtime & Process Supervision (`agents/`), Cơ chế thiết lập Win32 Job Object:, Cơ chế tiêu diệt tiến trình 2 lớp (Two-Layer Defense Termination):, JOBOBJECT_EXTENDED_LIMIT_INFORMATION, ManagedProcess

### Community 56 - "recovery_manager.py"
Cohesion: 0.19
Nodes (3): Nhóm D — Error Handling & Recovery, is_pid_alive(), RecoveryManager

## Knowledge Gaps
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Database` connect `Database` to `main.py`, `TaskContract`, `agy_controller.py`, `main.py`, `ResourceRepository`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`, `TaskRepository`, `.fetchone`, `TestStorageLayer`, `2.5. Hệ Thống 7 Repositories Chuyên Biệt`, `AGYAdapter`, `1.3. Mục Tiêu Học Tập (Learning Outcomes)`, `.transaction`, `Orchestrator`, `config.py`, `TestWorkspaceCoordination`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `Database` (e.g. with `check_account_status()` and `get_active_workers_info()`) actually correct?**
  _`Database` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07686453576864535 - nodes in this community are weakly interconnected._
- **Why does `6.1. Classes & Modules` connect `ResourceRepository` to `TaskContract`, `TaskStateMachine`, `PathPolicy`, `OwnershipManager`, `Database`, `Verifier`, `TaskRepository`, `WindowsFileRetryManager`, `2.5. Hệ Thống 7 Repositories Chuyên Biệt`, `Orchestrator`, `AGYAdapter`, `AgentRuntimeAdapter`, `TestWorkspaceCoordination`, `MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT`, `ManagedProcess`, `recovery_manager.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `TaskContract` (e.g. with `1.3. Mục Tiêu Học Tập (Learning Outcomes)` and `6.1. Classes & Modules`) actually correct?**
  _`TaskContract` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Should `TaskContract` be split into smaller, more focused modules?**
  _Cohesion score 0.05154639175257732 - nodes in this community are weakly interconnected._
- **Why does `TaskContract` connect `TaskContract` to `main.py`, `Antigravity Controller & Multi-Agent System (`agy-mas`)`, `OwnershipManager`, `ResourceRepository`, `PathPolicy`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`, `ReviewEngine`, `Verifier`, `ExecutionRepository`, `Orchestrator`, `1.3. Mục Tiêu Học Tập (Learning Outcomes)`, `GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._