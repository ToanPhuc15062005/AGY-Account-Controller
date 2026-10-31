# Antigravity Controller & Multi-Agent System (`agy-mas`)

Bộ công cụ toàn diện gồm:
1. **`agy-controller`**: Trình quản lý đa tài khoản, cấu hình độc lập Model / Effort / Turbo Mode và TUI tương tác cho Google Antigravity CLI (`agy`) trên Windows.
2. **`agy-mas`**: Hệ thống Multi-Agent System (MAS) tập trung theo chuẩn kiến trúc **Architecture Specification v1.1**, điều phối song song nhiều tác tử, kiểm soát xung đột tài nguyên Windows, theo dõi hạn ngạch (quota) và tự động phục hồi.

---

## 🚀 Tính năng cốt lõi của Multi-Agent System (`agy-mas`)

Hệ thống được thiết kế theo mô hình **Modular Monolith**, hướng sự kiện và tuân thủ các quyết định kiến trúc cứng cáp (hardened) cho môi trường Windows:

* **Persistence Core & SQLite Migrations (Phase 1)**:
  * Lưu trữ bền vững toàn bộ trạng thái qua SQLite (`WAL` mode, `PRAGMA foreign_keys = ON`, `busy_timeout = 5000ms`).
  * Hệ thống migration tự động kiểm tra `PRAGMA table_info` trước khi bổ sung cột.
  * Bộ repositories chuyên biệt: `projects`, `tasks`, `task_dependencies`, `executions` (lịch sử bất biến), `events` (log đơn điệu), `artifacts`, `resource_locks`, `file_ownerships`, `approvals`, `account_model_resources`.
* **Task Engine & DAG Validation (Phase 2)**:
  * Hợp đồng tác vụ `TaskContract` quy định phạm vi đầu vào, đầu ra, quyền truy cập đường dẫn (`PermissionProfile`) và tiêu chí chấp nhận (`AcceptanceCriterion`).
  * Máy trạng thái `TaskStateMachine` kiểm soát nghiêm ngặt 11 trạng thái vòng đời tác vụ.
  * `DependencyGraph` (Kahn's Topological Sort) phát hiện chu trình phụ thuộc và tính toán các tác vụ sẵn sàng chạy.
  * `PlanValidator` tự động phát hiện xung đột ghi đè song song (write collisions) giữa các tác vụ độc lập và ngăn chặn thoát workspace root.
* **Headless AGY Adapter & Process Supervisor (Phase 3)**:
  * Triển khai `AgentRuntimeAdapter` cho `agy` ở chế độ headless print mode (`agy -p --output-format stream-json`).
  * Thu thập độc lập stdout/stderr và phân loại lỗi theo bảng phân loại (Section 10 Error Taxonomy: `QUOTA_EXHAUSTED`, `RATE_LIMITED`, `AUTHENTICATION_FAILED`, `PERMISSION_SOFT_DENIED`, `FILE_BUSY`).
  * Quản lý vòng đời tiến trình qua **Windows Job Objects** (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`), đảm bảo dọn sạch toàn bộ cây tiến trình con khi hủy bỏ hoặc hết thời gian chờ (timeout).
  * `QuotaTracker` kiểm soát cooldown và hạn ngạch riêng biệt theo từng cặp `(account_id, model_key)`.
* **Shared Workspace & Windows Hardening (Phase 4)**:
  * `PathPolicy` cô lập tuyệt đối đường dẫn trong thư mục dự án.
  * `WindowsFileRetryManager` tự động xử lý lỗi khóa file chia sẻ Windows (`WinError 32` / `WinError 33`) bằng exponential backoff kèm jitter.
  * `OwnershipManager` quản lý quyền ghi đè theo mẫu đường dẫn (path pattern lease).
  * `SnapshotManager` tuân thủ ADR-016: chỉ tính checksum SHA256 của deliverables sau khi cây tiến trình worker đã thoát hoàn toàn.
* **Deterministic Central Scheduler & Orchestrator (Phase 5)**:
  * `Scheduler` lựa chọn các tác vụ sẵn sàng, thỏa mãn phụ thuộc, tài khoản khả dụng và giới hạn concurrency.
  * `Orchestrator` tick loop tự động phát hiện tài khoản cạn hạn ngạch và tự động chuyển đổi tác vụ (failover) sang tài khoản thay thế.
* **Verification Pipeline & Crash Recovery (Phase 6)**:
  * Bộ kiểm tra xác minh độc lập: `ArtifactChecker`, `ScopeChecker`, `AcceptanceChecker`, `Verifier`.
  * Tuân thủ ADR-014 (lỗi soft-denial không được chấp nhận dù exit code là 0) và ADR-017 (chỉ chấp nhận tác vụ khi toàn bộ artifacts hợp lệ).
  * `RecoveryManager` tự động rà soát lúc khởi động (startup reconciliation), dọn dẹp các worker đã chết ngắt quãng và mở khóa tài nguyên mồ côi.

---

## 📦 Cấu trúc gói mã nguồn (`src/agy_mas`)

```text
src/
└── agy_mas/
    ├── __init__.py
    ├── config.py                  # Cấu hình runtime, quota, retry, storage
    ├── storage/
    │   ├── database.py            # SQLite connection, transaction context, pragmas
    │   ├── migrations/            # Migration runner (v1.0 baseline + v1.1 additions)
    │   └── repositories/          # Project, Task, Execution, Event, Artifact, Resource, Approval
    ├── core/
    │   ├── state_machine.py       # Task lifecycle state machine & transitions
    │   ├── scheduler.py           # Deterministic DAG scheduler
    │   ├── dispatcher.py          # Process invocation & execution launcher
    │   └── orchestrator.py        # Central orchestration tick loop
    ├── planning/
    │   ├── plan_schema.py         # TaskContract, scopes, acceptance criteria
    │   ├── dependency_graph.py    # DAG topological sort, cycle detection
    │   └── plan_validator.py      # Write scope collision & path safety validator
    ├── agents/
    │   ├── base.py                # AgentRuntimeAdapter contract & event schemas
    │   ├── process_manager.py     # Process supervisor & Windows Job Objects
    │   └── adapters/
    │       └── agy_adapter.py     # Headless stream-json adapter for AGY
    ├── accounts/
    │   └── credential_provider.py # Thread/process-safe atomic file lock for credentials
    ├── workspace/
    │   ├── path_policy.py         # Workspace path safety & traversal prevention
    │   ├── file_lock_manager.py   # Windows WinError 32/33 bounded retry with jitter
    │   ├── ownership_manager.py   # Path lease & write permission verification
    │   ├── snapshot_manager.py    # Post-exit stable SHA256 artifact snapshots
    │   └── workspace_manager.py   # Workspace coordination facade
    ├── resources/
    │   └── quota_tracker.py       # (account_id, model_key) cooldown tracker
    ├── verification/
    │   ├── artifact_checker.py    # Existence, min-size & checksum verification
    │   ├── scope_checker.py       # Out-of-scope write verification
    │   ├── acceptance_checker.py  # Criteria evaluator
    │   └── verifier.py            # Comprehensive verification pipeline
    ├── recovery/
    │   └── recovery_manager.py    # Startup reconciliation & dead PID recovery
    └── cli/
        └── main.py                # agy-mas CLI entrypoint
```

---

## ⚡ Hướng dẫn sử dụng CLI `agy-mas`

Hệ thống cung cấp sẵn các wrapper [agy-mas.cmd](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-mas.cmd) và [agy-mas.ps1](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-mas.ps1).

### 1. Quản lý dự án (Project)
```cmd
:: Tạo dự án mới
agy-mas project create "Payment Module" "Build Stripe webhook integration" --workspace "C:\projects\payment" --id proj_pay

:: Liệt kê các dự án
agy-mas project list

:: Xem chi tiết cấu hình dự án
agy-mas project inspect proj_pay
```

### 2. Quản lý tác vụ (Task)
```cmd
:: Tạo tác vụ gốc
agy-mas task create proj_pay task_schema "Design database schema"

:: Tạo tác vụ phụ thuộc (chạy sau task_schema)
agy-mas task create proj_pay task_api "Implement webhook endpoint" --depends-on task_schema

:: Liệt kê các tác vụ của dự án kèm trạng thái DAG
agy-mas task list proj_pay
```

### 3. Kiểm tra hạn ngạch & tài nguyên (Resource)
```cmd
:: Xem trạng thái cooldown của các tài khoản và mô hình
agy-mas resource status
```

### 4. Khởi chạy điều phối Multi-Agent (Orchestrate)
```cmd
:: Chạy điều phối dự án với danh sách tài khoản chỉ định và giới hạn song song
agy-mas orchestrate start proj_pay --accounts default,toanphucnguyena1,toanphucnguyena2 --concurrency 4
```

---

## 🧪 Bộ kiểm thử tự động (Test Suite)

Hệ thống đi kèm bộ kiểm thử toàn diện với **36/36 tests** đạt 100%:
* `tests/unit/test_storage.py`: Kiểm thử migrations, foreign keys, transaction rollback và 7 repositories.
* `tests/unit/test_task_engine.py`: Kiểm thử hợp đồng tác vụ, chu trình phụ thuộc, xung đột ghi đè.
* `tests/unit/test_agy_adapter.py`: Kiểm thử headless flags, stream-json parsing, taxonomy phân loại lỗi.
* `tests/unit/test_workspace.py`: Kiểm thử cô lập đường dẫn, retry `WinError 32`, snapshot timing.
* `tests/unit/test_orchestrator.py`: Kiểm thử vòng lặp điều phối DAG 2 tác vụ và tự động failover khi quota cạn.
* `tests/unit/test_verification_recovery.py`: Kiểm thử pipeline kiểm định và phục hồi tiến trình mồ côi.
* `tests/integration/test_e2e_acceptance.py`: Kiểm thử chấp nhận E2E v1.1 (VER-01, VER-02, VER-03, QUOTA-01, WIN-01, REC-01).

Chạy toàn bộ kiểm thử:
```powershell
$env:PYTHONPATH="src"; python -m unittest discover -s tests -p "test_*.py"
```

---

## 🎮 Antigravity Controller (`agy-controller`)

Trình điều khiển và giao diện động tương tác (TUI) quản lý session cá nhân:

```cmd
:: Mở giao diện TUI tương tác
agy-controller

:: Liệt kê tài khoản
agy-controller list

:: Kiểm tra trạng thái xác thực toàn bộ tài khoản (bảng trực quan)
agy-controller check-all
:: hoặc
agy-controller check

:: Kiểm tra sâu & tự động refresh token cho 1 tài khoản cụ thể
agy-controller check 1
agy-controller check toanphucnguyena1

:: Chuyển đổi tài khoản nhanh
agy-controller switch 2

:: Chạy song song nhiều worker với bảo vệ chống xung đột Windows Credential Manager
agy-controller run-many -w 1 "Prompt worker 1" -w 2 "Prompt worker 2"
```

### Ký hiệu trạng thái Token (`agy-controller check`):
| Ký hiệu | Màu sắc | Ý nghĩa |
| :---: | :---: | :--- |
| `+` | Xanh lá | **VALID**: Access Token còn hạn và sẵn sàng thực thi ngay lập tức. |
| `!` | Vàng | **NEED_REFRESH**: Access Token hết hạn, có sẵn Refresh Token (tự động làm mới khi chạy hoặc qua `check <STT>`). |
| `-` | Đỏ | **EXPIRED / NO_TOKEN**: Hết hạn hoàn toàn hoặc thiếu Refresh Token (Cần chạy `agy-controller login <tên>`). |
| `#` | Tím | **COOLDOWN**: Tài khoản đang bị giới hạn hạn ngạch (Quota Rate Limit) trong SQLite. |

