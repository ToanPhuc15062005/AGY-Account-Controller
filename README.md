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
  * Máy trạng thái `TaskStateMachine` kiểm soát nghiêm ngặt 12 trạng thái vòng đời tác vụ.
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

## ⚡ Hướng dẫn chi tiết sử dụng CLI `agy-mas`

Hệ thống cung cấp sẵn các wrapper [agy-mas.cmd](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-mas.cmd) và [agy-mas.ps1](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-mas.ps1) trong thư mục PATH người dùng (`AppData\Local\agy\bin` và `.gemini\antigravity-cli\bin`).

---

### Cách 1: Chạy tự động hoàn toàn với một lệnh duy nhất (`agy-mas run`)

Lệnh `run` là giải pháp mạnh mẽ nhất để giải quyết bài toán: **từ một mục tiêu lớn (Goal) -> tự động lập kế hoạch đa tác vụ độc lập -> phân công nhiều agent chạy song song trên nhiều tài khoản Google khác nhau mà không bị xung đột ghi đè hay vướng quyền**:

```cmd
:: Cú pháp cơ bản
agy-mas run "Xây dựng REST API backend với FastAPI kết nối PostgreSQL và kiểm thử pytest"

:: Cú pháp đầy đủ với tùy chọn nâng cao
agy-mas run "Xây dựng hệ thống Authentication và thanh toán Stripe" ^
    --name "Auth & Payment System" ^
    --workspace "C:\projects\my-ecommerce" ^
    --accounts default,toanphucnguyena1,toanphucnguyena2,n23dccn115 ^
    --concurrency 3 ^
    --model gemini-3.8-flash
```

#### Các tùy chọn của `agy-mas run`:
* `goal` *(bắt buộc)*: Mô tả mục tiêu tổng quát của dự án cần hoàn thành.
* `--name`: Tên định danh gợi nhớ cho dự án (mặc định lấy theo 30 ký tự đầu của mục tiêu).
* `--id`: Mã ID dự án duy nhất (mặc định sinh ngẫu nhiên dạng `proj_xxxxxx`).
* `--workspace`: Đường dẫn thư mục làm việc của dự án (mặc định lấy thư mục hiện tại `.`).
* `--accounts`: Danh sách các tài khoản phân tách bằng dấu phẩy dùng để luân phiên chạy tác vụ (mặc định: `default`).
* `--concurrency`: Số lượng agent được phép chạy đồng thời tối đa (mặc định: `4`).
* `--model`: Mô hình LLM được sử dụng trong Google Antigravity (mặc định: `gemini-3.8-flash`).
  * Danh sách mô hình Antigravity hỗ trợ:
    * `gemini-3.8-flash` *(Mặc định)*
    * `claude-sonnet-4-6`
    * `claude-opus-4-6-thinking`
    * `gpt-oss-120b-medium`
* `--effort`: Mức độ suy luận (Reasoning Effort) mặc định cho các agent: `low`, `medium`, `high`, `xhigh`, `max` (mặc định: `medium`).

---

### ⚙️ Thiết lập Model và Effort cho Orchestrator & Worker (3 cấp độ ưu tiên)

Hệ thống hỗ trợ cơ chế phân cấp (hierarchical fallback) linh hoạt để bạn kiểm soát mô hình và mức suy luận:

```text
Cấp 3: Task Contract (--model, --effort trong task create)    [ƯU TIÊN CAO NHẤT]
       ▲
       │ (nếu task không ghi đè)
Cấp 2: Account Profile (Cấu hình riêng của từng tài khoản)
       ▲
       │ (nếu account để mặc định)
Cấp 1: Orchestrator Policy (--model, --effort trong agy-mas run)
```

1. **Cấp 1 - Toàn cục cho phiên chạy (`Orchestrator Level`)**:
   * Thiết lập qua cờ `--model` và `--effort` ngay khi gọi `agy-mas run`:
     ```cmd
     agy-mas run "Xây dựng microservice" --model claude-sonnet-4-6 --effort high
     ```
   * Sẽ áp dụng cho bộ Planner lập kế hoạch và làm giá trị mặc định cho toàn bộ các worker trong phiên.

2. **Cấp 2 - Kế thừa theo Tài khoản (`Account Profile Level`)**:
   * Thiết lập độc lập cho từng tài khoản qua `agy-controller config` hoặc giao diện TUI:
     ```cmd
     :: Tài khoản 1 dùng Flash để xử lý tác vụ nhẹ, tiết kiệm
     agy-controller config 1 --model gemini-3.8-flash --effort medium

     :: Tài khoản 2 chuyên dùng Sonnet mức suy luận cao
     agy-controller config 2 --model claude-sonnet-4-6 --effort high --mode turbo
     ```
   * **Khi Orchestrator phân công Task cho Tài khoản 2**, worker sẽ **tự động chạy bằng `claude-sonnet-4-6` với effort `high`** mà bạn không cần cấu hình lại!

3. **Cấp 3 - Tác vụ chuyên biệt (`Task Level - Ghi đè tuyệt đối`)**:
   * Khi tạo task thủ công trong Cách 2 (`agy-mas task create`), bạn có thể chỉ định model/effort riêng cho từng task:
     ```cmd
     :: Tác vụ giải thuật khó: Ép dùng Claude Opus với mức suy luận max
     agy-mas task create proj_1 task_algo "Thiết kế giải thuật mã hóa" --model claude-opus-4-6-thinking --effort max

     :: Tác vụ viết tài liệu: Ép dùng Gemini Flash với effort low
     agy-mas task create proj_1 task_docs "Viết API documentation" --model gemini-3.8-flash --effort low
     ```

#### Quy trình 3 bước tự động thực thi:
1. **[1/3] Khởi tạo Dự án & Database**: Đăng ký dự án vào SQLite WAL, gắn kết `workspace_root` và chuẩn bị snapshot baseline.
2. **[2/3] Phân rã mục tiêu (Planner & Validator)**:
   * Tự động sinh danh sách các hợp đồng tác vụ (`TaskContract`).
   * Phân tách phạm vi ghi (`write_paths`) độc lập cho từng tác vụ để tránh ghi đè đồng thời.
   * Xây dựng đồ thị có hướng không chu trình (DAG) bằng thuật toán Kahn's Topological Sort.
3. **[3/3] Điều phối đa Agent (Multi-Agent Orchestrator)**:
   * Khởi chạy vòng lặp điều phối tập trung (Central Tick Loop).
   * Cấp phát tài khoản khả dụng cho từng tác vụ, khởi chạy headless agent trong Windows Job Objects.
   * Giám sát, kiểm định artifact hoàn thành, tự động chuyển đổi tài khoản (failover) nếu phát hiện cạn hạn ngạch (quota cooldown).

---

### Cách 2: Quy trình quản lý thủ công & kiểm soát chi tiết

Nếu bạn muốn tự tay định nghĩa các tác vụ hoặc kiểm tra từng giai đoạn, bạn có thể sử dụng các nhóm lệnh chuyên biệt:

#### 1. Quản lý dự án (`project`)
```cmd
:: Tạo dự án mới với đường dẫn workspace chỉ định
agy-mas project create "Payment Module" "Build Stripe webhook integration" --workspace "C:\projects\payment" --id proj_pay

:: Liệt kê toàn bộ các dự án trong hệ thống
agy-mas project list

:: Xem chi tiết cấu hình và trạng thái dự án dưới dạng JSON
agy-mas project inspect proj_pay
```

#### 2. Tự động sinh kế hoạch cho dự án đã có (`plan`)
```cmd
:: Phân rã mục tiêu của dự án đã đăng ký thành các tác vụ hợp lệ
agy-mas plan proj_pay --model gemini-3.8-flash
```

#### 3. Quản lý tác vụ tùy chỉnh (`task`)
```cmd
:: Tạo tác vụ gốc (chạy đầu tiên)
agy-mas task create proj_pay task_schema "Design database schema & migration models" --priority 100

:: Tạo tác vụ phụ thuộc (chỉ chạy sau khi task_schema hoàn thành)
agy-mas task create proj_pay task_api "Implement webhook endpoint" --depends-on task_schema --priority 80

:: Tạo tác vụ kiểm thử (chạy sau task_api)
agy-mas task create proj_pay task_test "Write unit tests for webhook" --depends-on task_api --priority 50

:: Liệt kê các tác vụ của dự án kèm trạng thái DAG và phụ thuộc
agy-mas task list proj_pay
```

#### 4. Khởi chạy điều phối Multi-Agent (`orchestrate`)
```cmd
:: Bắt đầu điều phối dự án với danh sách tài khoản xoay vòng và giới hạn 3 agent song song
agy-mas orchestrate start proj_pay --accounts default,toanphucnguyena1,toanphucnguyena2 --concurrency 3
```

#### 5. Giám sát hạn ngạch & tài nguyên (`resource`)
```cmd
:: Kiểm tra các cặp (tài khoản, mô hình) đang trong thời gian cooldown hạn ngạch (Quota Cooldown)
agy-mas resource status
```

---

## 🧪 Bộ kiểm thử tự động (Test Suite)

Hệ thống đi kèm bộ kiểm thử toàn diện với **37/37 tests** đạt 100%:
* `tests/unit/test_storage.py`: Kiểm thử migrations, foreign keys, transaction rollback và 7 repositories.
* `tests/unit/test_task_engine.py`: Kiểm thử hợp đồng tác vụ, chu trình phụ thuộc, xung đột ghi đè.
* `tests/unit/test_planner.py`: Kiểm thử bộ phân rã mục tiêu tự động, tính hợp lệ của hợp đồng và phát hiện chu trình DAG.
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

Trình điều khiển và giao diện động tương tác (TUI) quản lý session cá nhân và cấu hình môi trường:

```cmd
:: Mở giao diện TUI tương tác (phím mũi tên, Enter để chuyển tài khoản)
agy-controller

:: Liệt kê danh sách tài khoản kèm Model, Effort và Mode
agy-controller list

:: Chuyển đổi nhanh sang tài khoản số 2 (hoặc theo tên/email)
agy-controller switch 2

:: Cấu hình Model, Effort và Turbo Mode cho tài khoản cụ thể
agy-controller config 1 --model claude-sonnet-4-6 --effort high --mode turbo

:: Chạy song song nhiều worker với cơ chế Staggered Startup chống xung đột Credential Manager
agy-controller run-many -w 1 "Viết file auth.py" -w 2 "Viết file test_auth.py"
```

---

## 🔍 Kiểm tra tình trạng xác thực tài khoản (`check` & `check-all`)

### Vì sao cần tính năng này?
1. **Chu kỳ sống của Google OAuth**: `access_token` có hiệu lực trong **1 giờ (3600s)**, trong khi `refresh_token` được lưu bền vững trên máy để tự động cấp mới `access_token` trong ~1 giây khi chạy lệnh `agy`.
2. **Hiện tượng hiểu lầm "Hết hạn"**: Nếu gọi `agy` độc lập mà Credential Manager chưa tải đúng session của tài khoản đó, Google CLI sẽ báo `Authentication required...` khiến người dùng lầm tưởng token đã mất.
3. **Phát hiện sự cố sớm**: Kiểm tra trước xem Refresh Token có bị Google thu hồi (hết hạn 7 ngày / đổi mật khẩu) hay tài khoản có đang bị dính hạn ngạch (Quota Cooldown) trước khi khởi chạy các đợt điều phối song song lớn.

### 1. Kiểm tra tổng quan toàn bộ tài khoản (`check-all` hoặc `check`)
```cmd
agy-controller check-all
:: hoặc gõ ngắn gọn:
agy-controller check
```

**Kết quả hiển thị trực quan:**
```text
Bảng trạng thái xác thực tài khoản Antigravity:

┌─────┬──────────────────┬─────────────────────────────────────┬────────────────────────────┬────────────────────────────┐
│ STT │    Tài khoản     │                Email                │      Tình trạng Token      │          Kết luận          │
├─────┼──────────────────┼─────────────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ 1*  │ default          │ phucnguyentenda@gmail.com           │ + Còn hạn (0h 59m)         │ Sẵn sàng                   │
│  2  │ n23dccn115       │ n23dccn115@student.ptithcm.edu.vn   │ ! Cần refresh (có sẵn RT)  │ Sẵn sàng (Auto-refresh)    │
│  3  │ phucnguyentenda  │ phucnguyentenda@gmail.com           │ ! Cần refresh (có sẵn RT)  │ Sẵn sàng (Auto-refresh)    │
│  4  │ toanphucnguyena1 │ toanphucnguyena1@gmail.com          │ ! Cần refresh (có sẵn RT)  │ Sẵn sàng (Auto-refresh)    │
│  5  │ toanphucnguyena2 │ toanphucnguyena2@gmail.com          │ ! Cần refresh (có sẵn RT)  │ Sẵn sàng (Auto-refresh)    │
│  6  │ toanphucnguyena3 │ toanphucnguyena3@gmail.com          │ ! Cần refresh (có sẵn RT)  │ Sẵn sàng (Auto-refresh)    │
└─────┴──────────────────┴─────────────────────────────────────┴────────────────────────────┴────────────────────────────┘

  *         : Tài khoản đang kích hoạt (Active)
  + (Xanh lá) : Access Token còn hạn, sẵn sàng
  ! (Vàng)    : Access Token hết hạn, có sẵn Refresh Token (tự động làm mới khi chạy)
  - (Đỏ)      : Hết hạn hoàn toàn / Thiếu token (Cần: agy-controller login <tên>)
  # (Tím)     : Đang trong thời gian cooldown hạn ngạch (Quota Limit)

  Kiểm tra sâu & tự động refresh: agy-controller check <STT hoặc Tên>
```

### 2. Kiểm tra sâu & Tự động Refresh Token (`check <STT / Tên>`)
Khi muốn làm mới ngay lập tức một tài khoản cụ thể mà không cần chờ tới lúc chạy tác vụ:

```cmd
:: Kiểm tra theo số thứ tự (STT)
agy-controller check 1

:: Kiểm tra theo tên profile
agy-controller check toanphucnguyena1
```

**Cơ chế hoạt động:**
* Tự động khóa luồng với `CredentialSwitchLock` để tránh tranh chấp Windows Credential Manager.
* Tạm lưu phiên hiện tại và nạp profile chỉ định vào `gemini:antigravity`.
* Gửi yêu cầu Live Probe `agy -p ping` tới Google CLI.
* Nếu thành công: đọc `access_token` mới nhất, cập nhật file profile JSON trên đĩa (kéo dài thêm 1 giờ hạn dùng) và khôi phục lại tài khoản ban đầu cho hệ thống.
* Nếu Google trả về lỗi `invalid_grant` hoặc `authentication required`: thông báo tài khoản cần đăng nhập lại với `agy-controller login <tên>`.
* **Cơ chế an toàn (Pre-flight Concurrency Guard):** Trước khi hoán đổi Credential Manager, hệ thống tự động kiểm tra `executions` trong SQLite và tiến trình qua `psutil`. Nếu phát hiện có bất kỳ worker nào đang chạy song song, lệnh `check <STT>` sẽ **tự động từ chối thực hiện live probe** để bảo vệ credential của worker đang chạy không bị ghi đè, tránh hoàn toàn lỗi race condition trên Windows.

### 3. Bảng giải thích chi tiết ký hiệu trạng thái:

| Ký hiệu | Màu sắc | Trạng thái kỹ thuật | Ý nghĩa & Hành động xử lý |
| :---: | :---: | :--- | :--- |
| **`+`** | Xanh lá | **VALID** (Sẵn sàng) | Access Token còn hạn sử dụng. Sẵn sàng thực thi lệnh và tác vụ ngay tức thì. |
| **`!`** | Vàng | **NEED_REFRESH** (Tự động) | Access Token đã quá 1 giờ nhưng có sẵn Refresh Token hợp lệ. Khi khởi chạy tác vụ hoặc chạy `check <STT>`, hệ thống sẽ tự động silent-refresh thành `+` trong 1 giây mà **không cần người dùng can thiệp**. |
| **`-`** | Đỏ | **EXPIRED / NO_TOKEN** (Hết hạn) | Không tìm thấy Refresh Token hoặc token đã bị Google vô hiệu hóa (do đổi pass/thu hồi/quá 7 ngày đối với app thử nghiệm). Cần chạy: `agy-controller login <tên_profile>` để đăng nhập lại qua trình duyệt. |
| **`#`** | Tím | **COOLDOWN** (Hạn ngạch) | Tài khoản đang trong thời gian hạ nhiệt hạn ngạch (Quota Rate Limit) được theo dõi tự động bởi SQLite WAL. Không nên gán tác vụ mới cho tới khi hết thời gian cooldown. |


