# GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS
## CHUYÊN ĐỀ 04: ORCHESTRATOR, QUOTA TRACKER VÀ CLI CONTROLLER

> **Phiên bản tài liệu:** 1.1.0  
> **Phạm vi mã nguồn:** [`src/agy_mas/core/`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/), [`src/agy_mas/resources/`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/resources/), [`src/agy_mas/cli/`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/cli/), [`src/agy_mas/accounts/`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/accounts/), [`agy_controller.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py)  
> **Mục tiêu chuyên đề:** Đào tạo chuyên sâu về kiến trúc vòng lặp điều phối tập trung (Central Orchestration Loop), cỗ máy lập lịch đồ thị tất định (Deterministic DAG Scheduler), quản lý hạn ngạch & cách ly tài nguyên theo cặp `(account, model)`, cơ chế tráo đổi phiên an toàn chống race condition (Atomic Credential Switching), giám sát tiến trình qua Windows Job Objects, và bộ công cụ CLI/TUI đa tài khoản toàn diện (`agy-controller`, `agy-mas`).

---

## MỤC LỤC TỔNG QUAN

1. [Tổng Quan Kiến Trúc & Triết Lý Điều Phối](#1-tổng-quan-kiến-trúc--triết-lý-điều-phối)
   - 1.1. Vị trí của Orchestrator, Quota Tracker và CLI trong hệ thống Multi-Agent
   - 1.2. Thách thức kỹ thuật cốt lõi: Concurrency, Quota Limits và Quản lý Định danh OS trên Windows
   - 1.3. 4 Trụ cột kiến trúc: Determinism, Resiliency, Isolation, Zero-Contention
2. [Chương 1: Vòng Lặp Điều Phối Trung Tâm (Central Orchestrator)](#2-chương-1-vòng-lặp-điều-phối-trung-tâm-central-orchestrator)
   - 2.1. Cấu trúc và Trách nhiệm của [`Orchestrator`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py#L24)
   - 2.2. Chu trình Tick Loop ([`.tick()`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py#L58)): 3 Giai đoạn vận hành cốt lõi
   - 2.3. Đối soát & Giám sát tiến trình đang chạy (Active Executions Reconciliation)
   - 2.4. Cơ chế xử lý Timeout và Dọn dẹp Cây tiến trình (Windows Job Objects & Taskkill)
   - 2.5. Phân loại lỗi hoàn tất và Cơ chế Retry / Quota Cooldown
   - 2.6. Thẩm định nghiệm thu Artifact và Chuyển dịch Trạng thái Tác vụ
   - 2.7. Đánh giá trạng thái kết thúc dự án (Terminal Project Evaluation)
3. [Chương 2: Bộ Lập Lịch Tất Định & Phân Phối Tác Vụ (Scheduler & Dispatcher)](#3-chương-2-bộ-lập-lịch-tất-định--phân-phối-tác-vụ-scheduler--dispatcher)
   - 3.1. Bộ Lập Lịch Đồ Thị [`Scheduler`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/scheduler.py#L20):
     - Giải thuật trích xuất Ready Tasks từ DAG
     - Tính toán Concurrency Slots khả dụng
     - Ra quyết định điều phối [`ScheduleDecision`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/scheduler.py#L13)
   - 3.2. Bộ Khởi Chạy [`Dispatcher`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/dispatcher.py#L18):
     - Chuyển dịch trạng thái: `PENDING` -> `READY` -> `CLAIMED`
     - Khởi tạo Bản ghi thực thi bất biến (`ExecutionRecord`)
     - Xác lập quyền sở hữu vùng ghi độc quyền (`OwnershipManager` Lease)
     - Xây dựng lệnh gọi thực thi [`Invocation`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/agents/base.py#L19)
     - Tráo đổi credential nguyên tử (`CredentialSwitchLock`) & Khởi động tiến trình
     - Ghi nhận PID và chuyển trạng thái `RUNNING`
4. [Chương 3: Quản Lý Hạn Ngạch & Tự Động Chuyển Giao (QuotaTracker & Resource Management)](#4-chương-3-quản-lý-hạn-ngạch--tự-động-chuyển-giao-quotatracker--resource-management)
   - 4.1. Mô hình Hạn ngạch Phân tầng theo cặp `(account_id, model_key)`
   - 4.2. Cơ chế ghi nhận cạn hạn ngạch [`record_quota_exhaustion`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/resources/quota_tracker.py#L16)
   - 4.3. Cơ chế hết hạn Cooldown lười (`Lazy Expiration`) trong [`ResourceRepository`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/resource_repo.py#L75)
   - 4.4. Thuật toán lựa chọn tài khoản khả dụng [`select_eligible_account`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/resources/quota_tracker.py#L46)
   - 4.5. Cơ chế Tự động Failover tức thì giữa các tài khoản khi gặp lỗi Quota (QUOTA-01)
   - 4.6. Phân định Taxonomy lỗi thực thi: QUOTA_EXHAUSTED vs RATE_LIMITED vs AUTHENTICATION_FAILED vs PERMISSION_SOFT_DENIED vs FILE_BUSY
5. [Chương 4: Bộ Điều Khiển Đa Tài Khoản `agy-controller`](#5-chương-4-bộ-điều-khiển-đa-tài-khoản-agy-controller)
   - 5.1. Cơ chế Tương tác Win32 Credential Manager (`advapi32.dll` qua `ctypes`)
   - 5.2. Giải pháp Đột phá: Đa tiến trình song song trên một ô nhớ Credential duy nhất (`gemini:antigravity`)
   - 5.3. Khóa đồng bộ liên tiến trình [`CredentialSwitchLock`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L77) & Chiến lược Khởi động so le (`Staggered Startup 0.4s`)
   - 5.4. Chế độ Chạy song song nhiều Worker [`cmd_run_many`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L1125) & Multi-threaded Stream Demuxing
   - 5.5. Cơ chế Kiểm tra Sức khỏe Tài khoản (Pre-flight Live Probe vs Bảng Tĩnh Check-All)
   - 5.6. Lá chắn Kiến trúc: Ngăn chặn Poisoning Xác thực chéo [`get_active_workers_info()`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L1598)
   - 5.7. Giao diện Tương tác Động TUI: State Machine điều khiển bảng, tìm kiếm và chỉnh sửa thuộc tính
   - 5.8. Cấu hình phân cấp 3 tầng (3-Tier Hierarchical Configuration: Model / Effort / Turbo Mode)
6. [Chương 5: Giao Diện Dòng Lệnh `agy-mas` CLI & Hệ Thống Wrappers](#6-chương-5-giao-diện-dòng-lệnh-agy-mas-cli--hệ-thống-wrappers)
   - 6.1. Kiến trúc CLI `agy-mas`: Subcommand Hierarchy (`project`, `task`, `resource`, `plan`, `orchestrate`, `run`)
   - 6.2. Luồng tự trị một lệnh duy nhất: `agy-mas run "<goal>"`
   - 6.3. Hệ thống wrapper đa nền tảng Windows: `.cmd` và `.ps1` (CMD & PowerShell)
   - 6.4. Cơ chế Cài đặt tự động vào PATH Người dùng và Dọn dẹp Legacy Wrappers (`cmd_install`)
7. [Chương 6: Các Ca Biên (Edge Cases), Bẫy Kỹ Thuật & Giải Pháp Gia Cố Trên Windows](#7-chương-6-các-ca-biên-edge-cases-bẫy-kỹ-thuật--giải-pháp-gia-cố-trên-windows)
   - 7.1. Chống Race Condition khi tráo đổi Credential giữa nhiều Workers
   - 7.2. Rào cản cờ `--effort` giữa họ Gemini và Claude/GPT trên Google Antigravity CLI
   - 7.3. Triệt tiêu tiến trình con mồ côi bằng Windows Job Objects (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`)
   - 7.4. Đảm bảo an toàn Snapshot Deliverables tuân thủ ADR-016 (Hậu tiến trình thoát hoàn toàn)
   - 7.5. Phòng chống lỗi Soft Denial (ADR-014) trong chế độ Headless Print Mode
8. [Chương 7: Thực Hành & Bài Tập Chuyên Sâu (Hands-On Lab)](#8-chương-7-thực-hành--bài-tập-chuyên-sâu-hands-on-lab)
   - Lab 1: Tương tác Win32 Credential Manager và Atomic Locking qua Python
   - Lab 2: Thiết lập Quota Tracker, mô phỏng cạn hạn ngạch và kiểm thử Failover tự động
   - Lab 3: Triển khai Vòng lặp Orchestration Tick Loop hoàn chỉnh với Mock Adapter
   - Lab 4: Khởi chạy Song song Đa tác tử thực chiến với `agy-mas run` và Giám sát Tài nguyên
   - Bài tập tự luyện chuyên sâu: Thiết kế bộ điều phối phân tán chịu lỗi cao
9. [Tổng Kết & Bảng Tra Cứu Nhanh (Cheat Sheet)](#9-tổng-kết--bảng-tra-cứu-nhanh-cheat-sheet)
   - Bảng tra cứu lệnh `agy-controller`
   - Bảng tra cứu lệnh `agy-mas`
   - Bảng quy tắc State Transitions & Error Taxonomy
   - Bộ 10 câu hỏi trắc nghiệm kiến trúc chuyên sâu có đáp án giải thích

---

## 1. TỔNG QUAN KIẾN TRÚC & TRIẾT LÝ ĐIỀU PHỐI

### 1.1. Vị Trí Của Orchestrator, Quota Tracker và CLI Trong Hệ Thống Multi-Agent

Trong hệ thống **AGY-MAS**, nếu tầng **Storage Layer (Phase 1)** đóng vai trò là "bộ nhớ bền vững" lưu lại lịch sử, và **Task Engine (Phase 2)** đóng vai trò là "bộ quy tắc logic và cấu trúc đồ thị", thì:

- **Orchestrator (Phase 5)** chính là **"Trái tim vận hành"** (The Executive Heartbeat) liên tục bơm nhịp đập (`tick()`), giám sát các tác tử đang chạy ngầm, phát hiện sự cố, đánh giá nghiệm thu và kích hoạt các tác vụ tiếp theo theo đúng thứ tự topo.
- **Quota Tracker (Phase 3 & Phase 5)** là **"Cảm biến tài nguyên & Van điều tiết"** (Resource Governor) bảo vệ hệ thống không bị nghẽn do giới hạn API của nhà cung cấp LLM, cho phép luân chuyển thông minh giữa nhiều tài khoản.
- **CLI & TUI Controllers (`agy-mas` & `agy_controller.py`)** là **"Bảng điều khiển chỉ huy"** (Command & Control Plane) giúp người dùng giao tiếp với hệ thống, thiết lập cấu hình đa cấp độ, theo dõi tiến độ thời gian thực và tự động hóa toàn diện từ ý tưởng đến mã nguồn hoàn chỉnh.

Sơ đồ quan hệ kiến trúc tổng thể giữa các tầng:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                               USER / COMMAND INTERFACE                           │
│     agy-controller (TUI / Multi-Account CLI)   │    agy-mas run / orchestrate    │
└──────────────────────────┬─────────────────────┴─────────────────┬───────────────┘
                           │                                       │
                           ▼                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           CENTRAL ORCHESTRATION LAYER                            │
│                                                                                  │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │                         Orchestrator (core/orchestrator.py)              │   │
│   │   - Active Execution Reconciliation                                      │   │
│   │   - Process Timeout Guard (Job Objects)                                  │   │
│   │   - Failure Classification & Quota Trigger                               │   │
│   │   - Artifact Verification & State Machine Transition                     │   │
│   └──────────────────────┬───────────────────────────────────▲───────────────┘   │
│                          │                                   │                   │
│         Tick: Schedule   │                  Feedback: Status │                   │
│                          ▼                                   │                   │
│   ┌──────────────────────────────┐        ┌──────────────────┴───────────────┐   │
│   │  Scheduler (core/scheduler)  │        │   QuotaTracker (resources/quota) │   │
│   │  - DependencyGraph check     │        │   - (account, model) cooldown    │   │
│   │  - Concurrency slot budget   │        │   - Lazy cooldown expiration     │   │
│   │  - Select eligible account   │◄───────┤   - Failover account selection   │   │
│   └──────────────┬───────────────┘        └──────────────────────────────────┘   │
│                  │                                                               │
│                  │ ScheduleDecision                                              │
│                  ▼                                                               │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │                         Dispatcher (core/dispatcher.py)                  │   │
│   │   - State transition: PENDING -> READY -> CLAIMED                        │   │
│   │   - Create immutable ExecutionRecord                                     │   │
│   │   - Path Lease Claim (OwnershipManager)                                  │   │
│   │   - Atomic Credential Switching (CredentialSwitchLock)                   │   │
│   │   - Staggered Startup (0.4s RAM Grace Period)                            │   │
│   │   - Subprocess launch & Windows Job Object attachment                    │   │
│   └──────────────────────┬───────────────────────────────────────────────────┘   │
└──────────────────────────┼───────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             RUNTIME EXECUTION AGENTS                             │
│   ┌──────────────────────────────┐        ┌──────────────────────────────────┐   │
│   │   Agent Worker 1 (agy CLI)   │        │     Agent Worker 2 (agy CLI)     │   │
│   │   PID: 10420 | Acc: default  │        │     PID: 18532 | Acc: profile_2  │   │
│   │   Model: gemini-3.8-flash    │        │     Model: claude-sonnet-4-6     │   │
│   │   Job Object Sandboxed       │        │     Job Object Sandboxed         │   │
│   └──────────────────────────────┘        └──────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1.2. Thách Thức Kỹ Thuật Cốt Lõi Trên Môi Trường Windows

Khi xây dựng một hệ thống Multi-Agent chạy đồng thời nhiều tiến trình độc lập trên hệ điều hành Windows, có 3 rào cản kỹ thuật rất đặc thù mà các hệ thống trên Linux/macOS không gặp phải:

1. **Điểm Nghẽn Độc Nhất Của Windows Credential Manager (`gemini:antigravity`)**:
   - Google Antigravity CLI (`agy`) lưu token OAuth2 đăng nhập tại duy nhất một mục Generic Credential trên Windows mang tên `gemini:antigravity`.
   - Nếu khởi chạy 4 agent chạy trên 4 tài khoản Google khác nhau mà không có cơ chế khóa đồng bộ, các tiến trình sẽ ghi đè credential của nhau trong Win32 Credential Manager, dẫn tới hiện tượng **Cross-Account Credential Poisoning** (Tiến trình A dùng token của Tài khoản B, sinh lỗi xác thực hoặc cạn quota chéo).
2. **Khóa Độc Quyền Tệp Tin & Tiến Trình Con Mồ Côi (Orphaned Child Processes)**:
   - Khi một CLI chạy trong console (`agy`), nó có thể sinh ra các tiến trình phụ thuộc (Node.js engine, git, Python child processes).
   - Nếu agent bị timeout hoặc gặp lỗi, việc chỉ gọi hàm `terminate()` chuẩn của Python (`os.kill`) trên Windows chỉ giết tiến trình vỏ ngoài, bỏ rơi các tiến trình con bên dưới. Các tiến trình mồ côi này tiếp tục giữ khóa tệp (`WinError 32: The process cannot access the file because it is being used by another process`), khiến các worker tiếp theo bị chặn hoàn toàn.
3. **Cạn Kiệt Hạn Ngạch Đột Ngột & Sự Khác Biệt Giữa Các Nhà Cung Cấp Model**:
   - Các tài khoản AI có giới hạn ngặt nghèo về TPM (Tokens Per Minute) và RPD (Requests Per Day). Khi tài khoản chạm trần hạn ngạch, lệnh CLI sẽ thất bại. Nếu hệ thống lập tức đánh trượt toàn bộ dự án, hiệu suất tự động hóa sẽ sụp đổ.
   - Hơn nữa, cờ `--effort` (mức độ suy luận reasoning) chỉ được Antigravity CLI hỗ trợ trên các mô hình của Google Gemini (`gemini-3.8-flash`). Khi truyền cờ `--effort` cho các model Anthropic Claude (`claude-sonnet-4-6`, `claude-opus-4-6-thinking`) hoặc OpenAI GPT (`gpt-oss-120b-medium`), CLI Antigravity sẽ bị văng lỗi với mã thoát `exit code 1`.

---

### 1.3. 4 Trụ Cột Kiến Trúc (Architecture Tenets)

Hệ thống Orchestrator & CLI được xây dựng dựa trên 4 nguyên lý bất di bất dịch:

1. **Determinism (Tính Tất Định)**:
   - Việc phân công tác vụ và lựa chọn tài khoản hoàn toàn dựa trên quy tắc toán học (Kahn DAG sort, danh sách ưu tiên, trạng thái cooldown). Không tồn tại điều kiện tranh chấp ngẫu nhiên (no race-condition-based dispatching).
2. **Resiliency & Auto-Failover (Khả Năng Chịu Lỗi & Tự Động Phục Hồi)**:
   - Khi một tác tử gặp lỗi cạn hạn ngạch (`QUOTA_EXHAUSTED`), hệ thống không dừng lại. QuotaTracker lập tức khóa tạm thời cặp `(account, model)` đó và kích hoạt **tự động chuyển giao (failover)** sang tài khoản khả dụng tiếp theo ngay trong cùng một nhịp tick.
3. **Isolation (Cô Lập Hoàn Toàn)**:
   - Mọi tiến trình worker đều được giam giữ trong một **Windows Job Object** riêng biệt với cờ `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Khi worker kết thúc hoặc bị hủy, toàn bộ cây tiến trình con bị hệ điều hành tiêu diệt 100%, không để lại bất kỳ tiến trình rác nào.
4. **Zero-Contention Credential Switching (Tráo Đổi Định Danh Không Xung Đột)**:
   - Tận dụng cơ chế **Staggered Startup** kèm khóa tệp liên tiến trình (`CredentialSwitchLock`). Mỗi worker nạp token vào bộ nhớ RAM của tiến trình trong 0.4 giây đầu tiên, sau đó nhường lại Credential Manager cho worker kế tiếp, cho phép **hàng chục tiến trình chạy song song hoàn toàn độc lập về tài khoản**.

---

## 2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)

Toàn bộ logic chỉ huy trung tâm được đóng gói tại lớp [`Orchestrator`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py#L24) trong tệp [`src/agy_mas/core/orchestrator.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py).

```
          +-------------------------------------------------------------+
          |             Orchestrator.tick(project_id, accounts)         |
          +-------------------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |  GIAI ĐOẠN 1: RECONCILE ACTIVE EXECUTIONS         |
               |  - Duyệt qua self.active_executions                |
               |  - Kiểm tra timeout -> terminate_tree()           |
               |  - Kiểm tra tiến trình hoàn tất:                  |
               |    * exit_code != 0: Classify failure             |
               |      - Cooldown quota nếu cần                     |
               |      - Retry nếu retryable & còn số lần thử       |
               |      - Ngược lại: FAILED                          |
               |    * exit_code == 0: Thẩm định artifacts          |
               |      - Đủ artifact: ACCEPTED                      |
               |  - Giải phóng leases (OwnershipManager)           |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |  GIAI ĐOẠN 2: SCHEDULE & DISPATCH                 |
               |  - Scheduler.schedule_next()                      |
               |  - Kiểm tra DAG sẵn sàng                          |
               |  - Kiểm tra tài khoản không dính cooldown         |
               |  - Dispatcher.dispatch() khởi chạy worker mới     |
               +---------------------------------------------------+
                                         |
                                         v
               +---------------------------------------------------+
               |  GIAI ĐOẠN 3: CHECK TERMINAL STATUS               |
               |  - Mọi task ACCEPTED -> Project COMPLETED         |
               |  - Có task FAILED & không còn task chạy -> FAILED |
               +---------------------------------------------------+
                                         |
                                         v
                             [Trả về kết quả nhịp Tick]
```

---

### 2.1. Cấu Trúc và Trách Nhiệm Của `Orchestrator`

Lớp `Orchestrator` được khởi tạo với sự tập hợp của toàn bộ các tầng Repositories, Workspace Manager, Runtime Adapter và Quota Tracker:

```python
# Trích xuất từ src/agy_mas/core/orchestrator.py
class Orchestrator:
    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
        execution_repo: ExecutionRepository,
        event_repo: EventRepository,
        artifact_repo: ArtifactRepository,
        resource_repo: ResourceRepository,
        workspace_mgr: WorkspaceManager,
        adapter: AgentRuntimeAdapter,
        quota_tracker: Optional[QuotaTracker] = None,
        max_concurrency: int = 4,
        default_policy: Optional[Dict[str, Any]] = None,
    ):
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.execution_repo = execution_repo
        self.event_repo = event_repo
        self.artifact_repo = artifact_repo
        self.resource_repo = resource_repo
        self.workspace_mgr = workspace_mgr
        self.adapter = adapter
        self.default_policy = default_policy or {}

        self.quota_tracker = quota_tracker or QuotaTracker(resource_repo)
        self.scheduler = Scheduler(task_repo, resource_repo, self.quota_tracker, max_concurrency)
        self.dispatcher = Dispatcher(task_repo, execution_repo, event_repo, workspace_mgr, adapter)

        # Bộ nhớ theo dõi tiến trình:
        # execution_id -> (task_id, ManagedProcess, TaskContract, account_id, started_timestamp)
        self.active_executions: Dict[str, Tuple[str, ManagedProcess, TaskContract, str, float]] = {}
```

---

### 2.2. Chu Trình Tick Loop (`.tick()`): 3 Giai Đoạn Vận Hành

Hàm [`.tick(project_id, available_accounts)`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py#L58) thực hiện một nhịp đánh giá duy nhất. Không giống các vòng lặp vô tận (infinite while loops) gây khó khăn cho việc viết unit test, thiết kế dạng **Tick-based State Machine** giúp hệ thống kiểm thử được từng bước chuyển trạng thái một cách hoàn hảo:

```python
def tick(self, project_id: str, available_accounts: List[str]) -> Dict[str, Any]:
    project = self.project_repo.get(project_id)
    if not project or project["status"] in ("COMPLETED", "FAILED", "CANCELLED", "PAUSED"):
        return {"status": project["status"] if project else "NOT_FOUND", "active": len(self.active_executions)}
    ...
```

---

### 2.3. Đối Soát Tiến Trình (Active Executions Reconciliation)

Tại mỗi nhịp tick, Orchestrator duyệt qua toàn bộ các tiến trình đang nằm trong `self.active_executions`:

```python
# Trích xuất từ src/agy_mas/core/orchestrator.py (Lines 64-83)
finished_execs = []
for exec_id, (tid, proc, contract, acc_id, start_ts) in list(self.active_executions.items()):
    elapsed = time.time() - start_ts
    
    # 1. Kiểm tra vượt ngưỡng thời gian (Timeout Guard)
    if proc.is_alive() and elapsed > contract.timeout_seconds:
        proc.terminate_tree(reason="TASK_TIMEOUT")
        self.execution_repo.mark_completed(
            exec_id, status="TIMEOUT", exit_code=-1,
            termination_reason="PROCESS_TIMEOUT",
            error_type="PROCESS_TIMEOUT",
            error_message=f"Exceeded timeout of {contract.timeout_seconds}s",
        )
        self.workspace_mgr.ownership_manager.release_all(exec_id)
        TaskStateMachine.transition(
            self.task_repo, tid, TaskState.TIMEOUT,
            event_repo=self.event_repo, execution_id=exec_id, reason="Timeout reached"
        )
        finished_execs.append(exec_id)
        continue
```

---

### 2.4. Phân Loại Thất Bại & Cooldown Hạn Ngạch

Khi tiến trình kết thúc (`not proc.is_alive()`), nếu `exit_code != 0`, Orchestrator ủy quyền cho Runtime Adapter phân loại lỗi theo bảng phân loại lỗi Section 10 Error Taxonomy:

```python
# Trích xuất từ src/agy_mas/core/orchestrator.py (Lines 101-142)
if exit_code != 0:
    cls_fail = self.adapter.classify_failure(exit_code, stdout_text, stderr_text, valid_events)
    self.execution_repo.mark_completed(
        exec_id,
        status="FAILED",
        exit_code=exit_code,
        error_type=cls_fail.error_type,
        error_message=cls_fail.reason,
    )
    self.workspace_mgr.ownership_manager.release_all(exec_id)

    # 1. Kích hoạt Cooldown nếu lỗi liên quan tới hạn ngạch
    if cls_fail.cooldown_required:
        model = contract.inputs.parameters.get("model", "gemini-3.8-flash")
        self.quota_tracker.record_quota_exhaustion(
            account_id=acc_id,
            model_key=model,
            retry_after_seconds=cls_fail.retry_after_seconds,
            reason=cls_fail.reason,
            source=cls_fail.evidence_source,
        )

    # 2. Đánh giá khả năng thử lại (Retry Evaluation)
    past_attempts = len(self.execution_repo.list_by_task(tid))
    if cls_fail.retryable and past_attempts <= contract.max_retries:
        TaskStateMachine.transition(
            self.task_repo, tid, TaskState.RETRY_WAIT,
            event_repo=self.event_repo, execution_id=exec_id,
            reason=f"Retryable failure ({cls_fail.error_type}); waiting to retry"
        )
        # Đưa ngay về READY để nhịp tick sau lập tức schedule sang account khác!
        TaskStateMachine.transition(
            self.task_repo, tid, TaskState.READY,
            event_repo=self.event_repo, execution_id=exec_id,
            reason="Resetting to READY after failure"
        )
    else:
        TaskStateMachine.transition(
            self.task_repo, tid, TaskState.FAILED,
            event_repo=self.event_repo, execution_id=exec_id,
            reason=f"Task failed: {cls_fail.reason}"
        )
```

---

### 2.5. Thẩm Định Nghiệm Thu Artifacts (Verification & Acceptance)

Nếu tiến trình kết thúc với `exit_code == 0`:
Hệ thống **không vội vàng đánh dấu hoàn thành**. Theo kiến trúc **ADR-016 & ADR-017**, Orchestrator yêu cầu WorkspaceManager kiểm tra sự hiện diện, kích thước tối thiểu và tính toán mã băm SHA-256 của các tệp sản phẩm bàn giao (Deliverables):

```python
# Trích xuất từ src/agy_mas/core/orchestrator.py (Lines 144-162)
self.workspace_mgr.register_task_artifacts(
    project_id=project_id,
    task_id=tid,
    execution_id=exec_id,
    expected_artifacts=[{"path": a.path, "artifact_type": a.artifact_type} for a in contract.outputs.expected_artifacts],
    process=proc,
)
self.execution_repo.mark_completed(
    exec_id, status="COMPLETED", exit_code=0, normalized_outcome="SUCCESS"
)
self.workspace_mgr.ownership_manager.release_all(exec_id)

TaskStateMachine.transition(
    self.task_repo, tid, TaskState.ACCEPTED,
    event_repo=self.event_repo, execution_id=exec_id, reason="Execution and artifacts verified"
)
```

---

### 2.6. Đánh Giá Trạng Thái Kết Thúc Dự Án

Cuối mỗi nhịp tick, Orchestrator rà soát tổng thể trạng thái của mọi task trong dự án:
- Nếu **toàn bộ task đều đạt `ACCEPTED`**: Dự án chuyển thành `COMPLETED`.
- Nếu **có task bị `FAILED`** và **không còn bất kỳ task nào** đang `RUNNING`, `CLAIMED`, `READY`, `PENDING` hay `RETRY_WAIT`: Dự án chuyển thành `FAILED`.

---

## 3. CHƯƠNG 2: BỘ LẬP LỊCH TẤT ĐỊNH & PHÂN PHỐI TÁC VỤ (SCHEDULER & DISPATCHER)

### 3.1. Bộ Lập Lịch Đồ Thị `Scheduler`

Nằm tại [`src/agy_mas/core/scheduler.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/scheduler.py), lớp [`Scheduler`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/scheduler.py#L20) có nhiệm vụ tìm kiếm các tác vụ đủ điều kiện chạy mà không gây nghẽn tài nguyên:

```python
@dataclass
class ScheduleDecision:
    task_id: str
    account_id: str
    model: str
    task_contract: TaskContract
```

#### Quy trình ra quyết định:
1. **Kiểm tra giới hạn đồng thời**: Nếu `running_count >= max_concurrency`, lập tức trả về rỗng `[]`.
2. **Xây dựng DAG và lọc Ready Tasks**: Sử dụng [`DependencyGraph`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/planning/dependency_graph.py#L11) để trích xuất các task có toàn bộ dependency đã đạt trạng thái `ACCEPTED`.
3. **Lựa chọn tài khoản khả dụng**:
   ```python
   # Trích xuất từ src/agy_mas/core/scheduler.py (Lines 84-88)
   account = self.quota_tracker.select_eligible_account(model, available_accounts)
   if not account:
       # Toàn bộ tài khoản ứng viên đều đang dính Cooldown đối với model này!
       continue
   ```
   Nếu tất cả tài khoản đều đang trong thời gian nghỉ Cooldown đối với model yêu cầu, Scheduler kiên nhẫn bỏ qua task đó trong nhịp này và đợi tài khoản hồi phục hoặc task khác sử dụng model khác.

---

### 3.2. Bộ Khởi Chạy `Dispatcher`

Nằm tại [`src/agy_mas/core/dispatcher.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/dispatcher.py), lớp [`Dispatcher`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/dispatcher.py#L18) đảm nhiệm việc hiện thực hóa quyết định `ScheduleDecision` thành một tiến trình OS sống:

```
+----------------------------------------------------------------------------------+
|                          Dispatcher.dispatch(decision)                           |
+----------------------------------------------------------------------------------+
                                          |
                                          v
      1. TaskStateMachine: PENDING/BLOCKED -> READY -> CLAIMED
                                          |
                                          v
      2. ExecutionRepository: Tạo bản ghi bất biến (exec_xxxx)
                                          |
                                          v
      3. OwnershipManager: Khóa đường dẫn ghi độc quyền (Lease write_paths)
                                          |
                                          v
      4. AGYAdapter: Xây dựng cấu trúc Invocation (Command line args & env)
                                          |
                                          v
      5. Atomic Credential Switch:
         ┌─────────────────────────────────────────────────────────────┐
         │ with CredentialSwitchLock():                                │
         │     switch_credential_to_account(decision.account_id)       │
         │     process = ManagedProcess(invocation)                    │
         │     process.start()                                         │
         │     time.sleep(0.4)  # Chờ agy đọc token vào RAM!           │
         └─────────────────────────────────────────────────────────────┘
                                          |
                                          v
      6. ExecutionRepository: Cập nhật PID tiến trình
                                          |
                                          v
      7. TaskStateMachine: CLAIMED -> RUNNING
```

---

## 4. CHƯƠNG 3: QUẢN LÝ HẠN NGẠCH & TỰ ĐỘNG CHUYỂN GIAO (QUOTATRACKER & RESOURCE MANAGEMENT)

### 4.1. Mô Hình Hạn Ngạch Phân Tầng Theo Cặp `(account_id, model_key)`

Các công cụ thông thường thường quản lý hạn ngạch ở cấp độ tài khoản toàn cục (Account Level). Tuy nhiên, trên Google Antigravity:
- Một tài khoản khi hết quota `gemini-3.8-flash` **vẫn có thể còn nguyên quota** cho `claude-sonnet-4-6` hoặc `gpt-oss-120b-medium`!
- Do đó, kiến trúc v1.1 của AGY-MAS thiết kế bảng [`account_model_resources`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/resource_repo.py#L30) với khóa chính phức hợp: `PRIMARY KEY (account_id, model_key)`.

Bảng lược đồ `account_model_resources`:

| Cột | Kiểu dữ liệu | Ý nghĩa |
| :--- | :--- | :--- |
| `account_id` | `TEXT` | Định danh tài khoản (profile name) |
| `model_key` | `TEXT` | Tên định danh mô hình (`gemini-3.8-flash`, ...) |
| `resource_state` | `TEXT` | Trạng thái: `AVAILABLE` hoặc `COOLDOWN` |
| `cooldown_until` | `TEXT (ISO8601)` | Mốc thời gian UTC được phép mở lại |
| `cooldown_reason`| `TEXT` | Nguyên nhân kích hoạt cooldown |
| `cooldown_source`| `TEXT` | Nguồn phát hiện: `structured` hoặc `pattern` |
| `last_error_code`| `TEXT` | Mã lỗi ghi nhận gần nhất (`QUOTA_EXHAUSTED`, ...) |

---

### 4.2. Cơ Chế Ghi Nhận Cooldown & Hết Hạn Lười (Lazy Expiration)

Tại [`src/agy_mas/resources/quota_tracker.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/resources/quota_tracker.py), hàm `record_quota_exhaustion` ghi nhận thời điểm mở lại:

```python
# Trích xuất từ src/agy_mas/resources/quota_tracker.py
def record_quota_exhaustion(
    self,
    account_id: str,
    model_key: str,
    retry_after_seconds: Optional[int] = None,
    reason: str = "Quota limit reached",
    source: str = "structured",
) -> str:
    # Mặc định thời gian chờ fallback là 18.000 giây (5 tiếng) nếu nhà cung cấp không báo retry-after
    cooldown_sec = retry_after_seconds or self.config.cooldown.fallback_seconds
    until = (
        datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=cooldown_sec)
    ).isoformat()

    self.resource_repo.set_account_model_cooldown(
        account_id=account_id,
        model_key=model_key,
        cooldown_until=until,
        cooldown_reason=reason,
        cooldown_source=source,
        retry_after_seconds=retry_after_seconds,
        last_error_code="QUOTA_EXHAUSTED",
    )
    return until
```

#### Triết lý Hết Hạn Lười (Lazy Expiration):
Thay vì phải duy trì một cron job hoặc thread chạy ngầm liên tục thăm dò cơ sở dữ liệu để mở khóa cooldown, hàm [`is_in_cooldown`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/storage/repositories/resource_repo.py#L75) kiểm tra thời gian thực tại thời điểm được gọi. Nếu `now >= until`, hàm tự động cập nhật `resource_state = 'AVAILABLE'` và giải phóng cooldown ngay lập tức!

---

### 4.3. Cơ Chế Tự Động Failover Tức Thì (QUOTA-01)

Sự phối hợp nhịp nhàng giữa Orchestrator, QuotaTracker và Scheduler tạo nên tính năng chuyển giao tác vụ tự động mượt mà:

```
[Thời điểm T0]: Task-1 khởi chạy trên Tài khoản "acc-1" (Model: gemini-3.8-flash)
                        │
                        ▼
[Thời điểm T1]: Tiến trình thoát với lỗi Quota ("resource_exhausted")
                        │
                        ▼
[Thời điểm T2]: Orchestrator.tick() bắt được sự kiện:
                1. QuotaTracker.record_quota_exhaustion("acc-1", "gemini-3.8-flash")
                   -> Đưa cặp ("acc-1", "gemini-3.8-flash") vào COOLDOWN.
                2. Task-1 chuyển trạng thái: RUNNING -> RETRY_WAIT -> READY.
                        │
                        ▼
[Thời điểm T3]: Cùng trong nhịp Tick đó, Scheduler.schedule_next() được gọi:
                1. Task-1 đang READY.
                2. QuotaTracker.select_eligible_account("gemini-3.8-flash", ["acc-1", "acc-2"])
                   - "acc-1" đang COOLDOWN -> BỎ QUA.
                   - "acc-2" khả dụng -> CHỌN "acc-2"!
                3. Dispatcher lập tức khởi chạy Task-1 trên "acc-2"!
                        │
                        ▼
[Kết quả]: Tác vụ hoàn thành thành công mà người dùng KHÔNG cần can thiệp!
```

---

### 4.4. Phân Định Taxonomy Lỗi Thực Thi (Section 10 Error Taxonomy)

Bộ phân loại lỗi [`classify_failure`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/agents/adapters/agy_adapter.py#L172) chia lỗi thành 5 nhóm rõ rệt:

| Error Type | Retryable? | Cooldown Required? | Cooldown Scope | Giải thích |
| :--- | :---: | :---: | :--- | :--- |
| **`QUOTA_EXHAUSTED`** | **Có** | **Có** | `(account, model)` | Cạn ngạch ngày/phút (429, resource_exhausted). Failover sang account khác. |
| **`RATE_LIMITED`** | **Có** | **Có** | `(account, model)` | Giới hạn tần suất gọi ngắn hạn. Chờ 60 giây và thử lại. |
| **`AUTHENTICATION_FAILED`**| Không | **Có** | `account` | Token hết hạn 7 ngày hoặc bị Google thu hồi. Cần login lại. |
| **`PERMISSION_SOFT_DENIED`**| Không | Không | - | CLI đòi quyền tương tác trong môi trường headless print mode. |
| **`FILE_BUSY`** | **Có** | Không | `path` | Xung đột file Windows (`WinError 32`). Áp dụng retry backoff jitter. |
| **`PROCESS_TIMEOUT`** | Không | Không | - | Tác vụ chạy vượt quá `timeout_seconds`. Bị Job Object kết liễu. |

---

## 5. CHƯƠNG 4: BỘ ĐIỀU KHIỂN ĐA TÀI KHOẢN `agy-controller`

Tệp [`agy_controller.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py) là công cụ độc lập mạnh mẽ, vừa cung cấp giao diện TUI tương tác, vừa quản lý đa tài khoản Google và đóng vai trò cầu nối hạ tầng cho `agy-mas`.

---

### 5.1. Cơ Chế Tương Tác Win32 Credential Manager (`advapi32.dll`)

Thay vì dựa vào các thư viện bên thứ ba dễ bị lỗi font chữ hoặc phụ thuộc môi trường, `agy_controller.py` giao tiếp trực tiếp với Windows API thông qua thư viện chuẩn `ctypes`:

```python
# Trích xuất từ agy_controller.py (Lines 222-249)
class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", wintypes.FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]

advapi32 = ctypes.windll.advapi32
CredRead = advapi32.CredReadW
CredWrite = advapi32.CredWriteW
CredDelete = advapi32.CredDeleteW
CredFree = advapi32.CredFree
```

Các hàm nguyên tử:
- `get_credential_raw()`: Đọc payload JSON của token đăng nhập.
- `set_credential_raw()`: Ghi đè token đăng nhập với cờ `CRED_PERSIST_LOCAL_MACHINE` (Persist = 2).
- `delete_credential_raw()`: Dọn dẹp token khi đăng xuất.

---

### 5.2. Giải Pháp Đột Phá: Đa Tiến Trình Song Song Trên Một Ô Nhớ Duy Nhất

Để giải quyết bài toán: **Windows Credential Manager chỉ có 1 ô nhớ duy nhất `gemini:antigravity`, làm sao chạy 5 worker song song trên 5 tài khoản khác nhau?**

Hệ thống triển khai kỹ thuật **Staggered Startup với RAM Token Ingestion**:
1. CLI `agy` khi khởi động sẽ gọi hàm Win32 API để đọc token từ `gemini:antigravity` và lưu bản sao token này vào biến trong bộ nhớ RAM của tiến trình đó.
2. Quá trình đọc từ OS store vào RAM này diễn ra rất nhanh (chưa tới 100ms).
3. Sau khi token đã nằm trong RAM của Worker 1, ta hoàn toàn có thể tráo đổi ô nhớ `gemini:antigravity` sang tài khoản của Worker 2!

Khóa đồng bộ liên tiến trình [`CredentialSwitchLock`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L77):
```python
# Trích xuất từ agy_controller.py (Lines 77-109)
class CredentialSwitchLock:
    """Inter-process lock to prevent race conditions during credential switching."""
    def __init__(self, lock_file: Path = AUTH_LOCK_FILE, timeout: float = 30.0):
        self.lock_file = lock_file
        self.timeout = timeout
        self.handle = None

    def acquire(self):
        ensure_profiles_dir()
        start = time.time()
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    self.handle = open(self.lock_file, "a+b")
                    msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    self.handle = open(self.lock_file, "a+b")
                    fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except (IOError, OSError, BlockingIOError):
                if time.time() - start > self.timeout:
                    raise TimeoutError("Hết thời gian chờ khóa đồng bộ Credential Manager.")
                time.sleep(0.05)
```

#### Quy trình khởi động so le trong [`cmd_run_many`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L1125):
```python
# Trích xuất từ agy_controller.py (Lines 1195-1214)
with CredentialSwitchLock():
    write_current_session(p_data.get("session", {}))
    set_active_profile_name(profile_path.stem)
    
    proc = subprocess.Popen(
        cmd_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        shell=(os.name == "nt")
    )
    # TẠM DỪNG 0.4s để agy kịp load token vào RAM trước khi cho worker tiếp theo tráo đổi!
    time.sleep(0.4)
```

---

### 5.3. Lá Chắn Kiến Trúc: Ngăn Chặn Poisoning Xác Thực Chéo

Một lỗi nguy hiểm rất dễ xảy ra: Người dùng đang chạy dự án MAS gồm 4 worker ngầm, nhưng lại mở một console khác gõ `agy-controller check <tài khoản>`. Lệnh `check` thông thường sẽ tráo đổi Credential Manager để gửi ping tới Google, vô tình **phá hoại phiên làm việc của các worker đang chạy song song**!

Để ngăn ngừa tuyệt đối thảm họa này, `agy_controller.py` trang bị hàm bảo vệ [`get_active_workers_info()`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L1598):

```python
# Trích xuất từ agy_controller.py (Lines 1636-1648)
def probe_single_account(profile_path: Path):
    active_workers = get_active_workers_info()
    if active_workers:
        print_warning("\n[TỪ CHỐI LIVE PROBE - PHÁT HIỆN WORKER ĐANG HOẠT ĐỘNG]")
        print(f"Hệ thống phát hiện có {len(active_workers)} tác vụ đang chạy song song:")
        for w in active_workers:
            print(f"  • Task '{w['task_id']}' (PID: {w['pid']}, Tài khoản: {w['account_id']})")
        print_error("Từ chối tráo đổi Credential Manager để bảo vệ các worker đang chạy không bị lỗi xác thực chéo.")
        print("Lưu ý: Để kiểm tra an toàn lúc này, hãy dùng bảng tĩnh: 'agy-controller check-all'\n")
        return
```

- Lệnh **`agy-controller check-all`**: Đọc trạng thái từ tệp tĩnh `.json` trong thư mục `~/.gemini/agy-profiles/`, **hoàn toàn không chạm vào Credential Manager**, an toàn 100% khi chạy đồng thời với MAS.
- Lệnh **`agy-controller check <tên>`**: Chỉ thực hiện Live Probe khi hệ thống hoàn toàn rảnh rỗi (Pre-flight check).

---

### 5.4. Giao Diện Tương Tác Động TUI (Interactive TUI)

Khi gõ `agy-controller` không tham số (hoặc `agy-controller tui`), chương trình khởi chạy giao diện tương tác TUI hoàn toàn bằng bàn phím qua cơ chế xử lý phím `msvcrt.getwch()` trên Windows:

```
┌─────────────────────────────────────────────────────────────┐
│             ANTIGRAVITY CONTROLLER - PROFILE TUI            │
├─────────────────────────────────────────────────────────────┤
│  [Refresh]   [Add]   [Edit]   [Search]   [Delete]   [Exit]  │
├─────┬──────────────────┬───────────────────┬────────┬───────┤
│ STT │ Tài khoản        │ Model             │ Effort │ Mode  │
├─────┼──────────────────┼───────────────────┼────────┼───────┤
│ > 1*│ dev_acc (user1)  │ gemini-3.8-flash  │ high   │ turbo │
│   2 │ prod_acc (user2) │ claude-sonnet-4-6 │ built-in normal │
│   3 │ test_acc (user3) │ gpt-oss-120b-med  │ built-in turbo │
└─────┴──────────────────┴───────────────────┴────────┴───────┘
  [TAB]: Chuyển vùng Focus | [ENTER]: Chọn / Chuyển tài khoản
```

Các tính năng nổi bật của TUI:
- **Điều hướng mượt mà**: Phím mũi tên lên/xuống/trái/phải, `TAB` để chuyển đổi giữa hàng nút bấm và danh sách tài khoản.
- **Tìm kiếm tức thì (`Search`)**: Gõ ký tự để lọc nhanh danh sách tài khoản theo tên hoặc địa chỉ email.
- **Chỉnh sửa trực tiếp (`Edit`)**: Cho phép thay đổi Model, Effort, và Turbo mode cho từng tài khoản mà không cần chỉnh sửa tệp JSON thủ công.

---

### 5.5. Cấu Hình Phân Cấp 3 Tầng (3-Tier Hierarchical Fallback)

Hệ thống áp dụng cơ chế xác định Model và Effort theo 3 cấp độ ưu tiên từ cao xuống thấp:

```
Cấp 3: Task Contract (--model, --effort trong task create)    [ƯU TIÊN CAO NHẤT]
       ▲
       │ (nếu task không chỉ định)
Cấp 2: Account Profile (Cấu hình riêng của từng tài khoản)
       ▲
       │ (nếu account để mặc định)
Cấp 1: Orchestrator Policy (--model, --effort trong agy-mas run)
```

Hàm chuẩn hóa độc lập [`normalize_model_and_effort`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L160) bảo đảm sự tách bạch tuyệt đối giữa **tên Model** và **mức độ suy luận Effort**, đồng thời tự động gán nhãn `built-in` cho Claude và GPT.

---

## 6. CHƯƠNG 5: GIAO DIỆN DÒNG LỆNH `agy-mas` CLI & HỆ THỐNG WRAPPERS

### 6.1. Cây Lệnh Phân Cấp (Subcommand Hierarchy)

Tệp [`src/agy_mas/cli/main.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/cli/main.py) định nghĩa hệ thống phân cấp câu lệnh của AGY-MAS:

```text
agy-mas
├── project
│   ├── create <name> <goal> [--id <id>] [--workspace <path>]
│   ├── list
│   └── inspect <id>
├── task
│   ├── create <project_id> <task_id> <title> [--desc] [--priority] [--depends-on] [--model] [--effort] [--mode]
│   └── list <project_id>
├── resource
│   └── status
├── plan <project_id> [--model <model>]
├── orchestrate
│   └── start <project_id> [--accounts <acc1,acc2>] [--concurrency <n>]
└── run <goal> [--name] [--id] [--workspace] [--accounts] [--concurrency] [--model] [--effort]
```

---

### 6.2. Luồng Tự Trị Một Lệnh Duy Nhất: `agy-mas run "<goal>"`

Lệnh `run` ([`cmd_run`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/cli/main.py#L201)) là tính năng tinh hoa nhất của hệ thống, đóng gói toàn bộ quy trình 3 bước phức tạp vào một lệnh ngắn gọn duy nhất:

```bash
agy-mas run "Xây dựng cổng thanh toán Stripe và webhook xử lý sự kiện" \
    --workspace "C:\projects\payment" \
    --accounts dev1,dev2,dev3 \
    --concurrency 3 \
    --model gemini-3.8-flash \
    --effort high
```

Quy trình tự động hóa:
1. **[1/3] Khởi tạo Dự án & Cơ sở dữ liệu**: Tạo bản ghi trong SQLite, kích hoạt WAL mode và liên kết thư mục làm việc.
2. **[2/3] Phân rã mục tiêu (Planner & Validator)**: Bộ lập kế hoạch tự động sinh các hợp đồng `TaskContract`, phân định vùng ghi độc lập và kiểm tra chu trình DAG bằng thuật toán Kahn.
3. **[3/3] Điều phối Đa Tác tử (Multi-Agent Orchestrator)**: Khởi chạy vòng lặp tick, phân bổ tài khoản luân phiên và tự động giám sát tiến trình đến khi hoàn thành toàn bộ sản phẩm.

---

### 6.3. Hệ Thống Wrappers Windows & Cài Đặt PATH Người Dùng

Để người dùng có thể thực thi lệnh từ bất kỳ thư mục nào trong CMD hoặc PowerShell mà không cần gõ tiền tố `python`, hệ thống cung cấp các wrapper:

- [`agy-controller.cmd`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-controller.cmd) & [`agy-controller.ps1`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-controller.ps1)
- [`agy-mas.cmd`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-mas.cmd) & [`agy-mas.ps1`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy-mas.ps1)

Khi chạy `install.cmd` hoặc `install.ps1`, hàm [`cmd_install`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/agy_controller.py#L1788) tự động:
1. Xác định thư mục bin người dùng (`%LOCALAPPDATA%\agy\bin` hoặc `.gemini\antigravity-cli\bin`).
2. Dọn dẹp các tệp wrapper cũ lỗi thời.
3. Tạo các tệp wrapper trỏ tới mã nguồn hiện tại kèm biến môi trường `PYTHONPATH=%~dp0src;%PYTHONPATH%`.

---

## 7. CHƯƠNG 6: CÁC CA BIÊN (EDGE CASES), BẪY KỸ THUẬT & GIẢI PHÁP GIA CỐ TRÊN WINDOWS

### 7.1. Chống Race Condition Khi Tráo Đổi Credential Giữa Nhiều Workers

- **Vấn đề**: Khi nhiều worker cùng bắt đầu một lúc, nếu cả hai cùng mở Win32 Credential Manager và cùng ghi dữ liệu, tài khoản của worker sau sẽ đè lên worker trước trước khi worker trước kịp khởi động.
- **Giải pháp**: Áp dụng triệt để mẫu khối ngữ cảnh `with CredentialSwitchLock():`. Khóa này sử dụng cơ chế khóa file nhị phân cấp hệ điều hành qua `msvcrt.locking(handle, msvcrt.LK_NBLCK, 1)`. Chỉ có duy nhất một tiến trình được phép tương tác với Credential Manager tại một thời điểm, kết hợp độ trễ 0.4s để bảo đảm tính ổn định.

---

### 7.2. Rào Cản Cờ `--effort` Giữa Các Dòng Mô Hình

- **Vấn đề**: Google Antigravity CLI chỉ hỗ trợ cờ `--effort` cho các model thuộc dòng Gemini (như `gemini-3.8-flash`). Nếu truyền `--effort` cho `claude-sonnet-4-6` hoặc `gpt-oss-120b-medium`, Antigravity CLI sẽ lập tức báo lỗi cú pháp: `unknown option --effort` và thoát với mã lỗi 1.
- **Giải pháp**: Cả `AGYAdapter.build_invocation()` và `cmd_run_many()` đều áp dụng bộ lọc bảo vệ nghiêm ngặt:
  ```python
  if effort and model and model.startswith("gemini") and effort in ("low", "medium", "high", "xhigh", "max"):
      cmd.extend(["--effort", effort])
  ```
  Nếu model không bắt đầu bằng `"gemini"`, cờ `--effort` sẽ tự động bị loại bỏ hoàn toàn khỏi danh sách đối số dòng lệnh.

---

### 7.3. Triệt Tiêu Tiến Trình Con Mồ Côi Bằng Windows Job Objects

- **Vấn đề**: Trong Windows, khi một tiến trình cha (Parent Process) bị hủy đột ngột, các tiến trình con (Child Processes) được tạo bởi `subprocess.Popen` không tự động bị hủy theo mà trở thành các tiến trình mồ côi (Orphan Processes), tiếp tục chiếm giữ CPU và khóa tệp tin.
- **Giải pháp**: Sử dụng **Windows Job Objects** thông qua `kernel32.dll`:
  1. Tạo Job Object bằng `CreateJobObjectW`.
  2. Bật cờ `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000`. Cờ này ra lệnh cho nhân Windows: **"Khi tiến trình quản lý đóng handle của Job Object này, hãy tự động tiêu diệt toàn bộ cây tiến trình nằm trong Job Object!"**
  3. Gán tiến trình worker vào Job Object ngay khi vừa được tạo bằng `AssignProcessToJobObject`.
  4. Nếu cần cưỡng chế dừng tiến trình, gọi `TerminateJobObject(handle, 1)` kết hợp `taskkill /F /T /PID <pid>`.

---

### 7.4. Đảm Bảo An Toàn Snapshot Deliverables (Tuân Thủ ADR-016)

- **Vấn đề**: Nếu kiểm tra mã băm SHA-256 hoặc sao lưu file kết quả khi tiến trình worker vẫn đang mở tệp để ghi, kết quả băm sẽ không chính xác hoặc phát sinh lỗi `WinError 32`.
- **Giải pháp**: Tuân thủ quyết định kiến trúc **ADR-016**: Hàm `register_task_artifacts()` chỉ được phép tính checksum SHA-256 sau khi kiểm tra chắc chắn tiến trình worker đã thoát hoàn toàn (`proc.is_alive() == False`) và toàn bộ stream stdout/stderr đã đóng.

---

### 7.5. Phòng Chống Lỗi Soft Denial (Tuân Thủ ADR-014)

- **Vấn đề**: Trong chế độ headless (`agy -p ...`), nếu agent yêu cầu quyền tương tác đọc/ghi file ngoài phạm vi cho phép, CLI có thể in ra thông báo `Permission Denied` nhưng vẫn trả về mã thoát `exit code 0`.
- **Giải pháp**: Tuân thủ quyết định kiến trúc **ADR-014**: Bộ thẩm định không bao giờ tin tưởng mù quáng vào `exit code == 0`. Bất kỳ dấu hiệu xuất hiện của chuỗi "soft-denial" hoặc "permission denied" trong luồng stdout/stderr đều bị xếp vào lỗi `PERMISSION_SOFT_DENIED` và từ chối nghiệm thu tác vụ!

---

## 8. CHƯƠNG 7: THỰC HÀNH & BÀI TẬP CHUYÊN SÂU (HANDS-ON LAB)

### Lab 1: Tương Tác Win32 Credential Manager và Atomic Locking Qua Python

**Mục tiêu**: Nắm vững cách Win32 API lưu trữ và trích xuất dữ liệu xác thực, đồng thời kiểm chứng tính an toàn của `CredentialSwitchLock`.

Tạo tệp kiểm thử `lab1_credential.py`:

```python
import os
import sys
import json
import time
from pathlib import Path

# Nạp mã nguồn agy-mas
sys.path.insert(0, str(Path(__file__).parent / "src"))
from agy_mas.accounts.credential_provider import CredentialSwitchLock
from agy_controller import get_credential_raw, set_credential_raw

def main():
    print("=== LAB 1: THỬ NGHIỆM WIN32 CREDENTIAL MANAGER & LOCK ===")
    
    # 1. Đọc credential hiện tại
    current = get_credential_raw()
    print(f"1. Trạng thái Credential hiện tại: {'Có dữ liệu ✓' if current else 'Trống'}")
    
    # 2. Thử nghiệm khóa đồng bộ liên tiến trình
    print("2. Đang kiểm tra CredentialSwitchLock...")
    with CredentialSwitchLock():
        print("   -> Đã giữ khóa thành công! Giả lập tráo đổi credential...")
        time.sleep(0.5)
        print("   -> Hoàn tất thao tác an toàn trong vùng khóa.")
    
    print("3. Đã giải phóng khóa. Kiểm tra an toàn tuyệt đối!\n")

if __name__ == "__main__":
    main()
```

---

### Lab 2: Thiết Lập Quota Tracker, Mô Phỏng Cạn Hạn Ngạch & Tự Động Failover

**Mục tiêu**: Kiểm chứng logic cách ly hạn ngạch theo cặp `(account, model)` và tính năng tự động chuyển giao tài khoản.

Tạo tệp kiểm thử `lab2_quota_failover.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories.resource_repo import ResourceRepository
from agy_mas.resources.quota_tracker import QuotaTracker

def main():
    print("=== LAB 2: MÔ PHỎNG QUOTA COOLDOWN VÀ FAILOVER ===")
    db = Database(":memory:")
    MigrationRunner(db).run_all()
    
    resource_repo = ResourceRepository(db)
    quota_tracker = QuotaTracker(resource_repo)
    
    accounts = ["account_A", "account_B", "account_C"]
    target_model = "gemini-3.8-flash"
    
    # 1. Ban đầu: Tài khoản nào đủ điều kiện?
    selected = quota_tracker.select_eligible_account(target_model, accounts)
    print(f"1. Tài khoản được chọn ban đầu: {selected} (Kỳ vọng: account_A)")
    
    # 2. Giả lập account_A bị cạn hạn ngạch
    print(f"2. Ghi nhận cạn quota trên account_A với model {target_model}...")
    until = quota_tracker.record_quota_exhaustion("account_A", target_model, retry_after_seconds=3600)
    print(f"   -> account_A rơi vào Cooldown đến: {until}")
    
    # 3. Lựa chọn lại tài khoản cho cùng model đó
    new_selected = quota_tracker.select_eligible_account(target_model, accounts)
    print(f"3. Tài khoản được tự động Failover: {new_selected} (Kỳ vọng: account_B)")
    
    # 4. Kiểm chứng tính độc lập: account_A có dùng được cho claude-sonnet-4-6 không?
    is_avail_claude = quota_tracker.is_available("account_A", "claude-sonnet-4-6")
    print(f"4. account_A với model claude-sonnet-4-6 có khả dụng không?: {is_avail_claude} (Kỳ vọng: True)")
    
    db.close()
    print("\n✓ Kiểm thử logic Quota & Failover hoàn toàn thành công!\n")

if __name__ == "__main__":
    main()
```

---

### Lab 3: Triển Khai Vòng Lặp Orchestration Hoàn Chỉnh Với Mock Adapter

**Mục tiêu**: Tái hiện toàn bộ chu trình xử lý của Orchestrator: Lập lịch DAG -> Khởi chạy Worker -> Giả lập hoàn thành -> Thẩm định và Kết thúc Dự án.

Tạo tệp kiểm thử `lab3_orchestrator_loop.py`:

```python
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from agy_mas.storage.database import Database
from agy_mas.storage.migrations.runner import MigrationRunner
from agy_mas.storage.repositories import (
    ProjectRepository, TaskRepository, ExecutionRepository,
    EventRepository, ArtifactRepository, ResourceRepository
)
from agy_mas.workspace.workspace_manager import WorkspaceManager
from agy_mas.resources.quota_tracker import QuotaTracker
from agy_mas.agents.base import AgentRuntimeAdapter, RuntimeCapabilities, Invocation, RuntimeEvent, FailureClassification
from agy_mas.core.orchestrator import Orchestrator

class FastMockAdapter(AgentRuntimeAdapter):
    def validate_runtime(self): return RuntimeCapabilities("mock", "1.0")
    def build_invocation(self, task_contract, execution_record, policy=None):
        return Invocation(command_args=[sys.executable, "-c", "import sys; print('Worker finished successfully'); sys.exit(0)"])
    def parse_line(self, line): return RuntimeEvent("OUTPUT", "2026-11-01T00:00:00Z", message=line)
    def classify_failure(self, exit_code, stdout, stderr, events=None):
        return FailureClassification("SUCCESS", False, False, "OK")

def main():
    print("=== LAB 3: CHU TRÌNH ĐIỀU PHỐI ORCHESTRATOR TICK LOOP ===")
    tmp = tempfile.mkdtemp()
    db = Database(":memory:")
    MigrationRunner(db).run_all()
    
    p_repo = ProjectRepository(db)
    t_repo = TaskRepository(db)
    e_repo = ExecutionRepository(db)
    ev_repo = EventRepository(db)
    a_repo = ArtifactRepository(db)
    r_repo = ResourceRepository(db)
    ws_mgr = WorkspaceManager(tmp, r_repo, a_repo)
    quota = QuotaTracker(r_repo)
    adapter = FastMockAdapter()
    
    orch = Orchestrator(p_repo, t_repo, e_repo, ev_repo, a_repo, r_repo, ws_mgr, adapter, quota, max_concurrency=2)
    
    # Tạo dự án và 2 task có quan hệ phụ thuộc: T1 -> T2
    p_repo.create("p_test", "Demo DAG", "Goal", tmp, status="RUNNING")
    t_repo.create("task_1", "p_test", "Task Khởi Tạo", "Viết schema")
    t_repo.create("task_2", "p_test", "Task Kế Thừa", "Viết API", depends_on=["task_1"])
    
    print("Khởi tạo DAG: task_1 -> task_2")
    
    # Nhịp Tick 1: task_1 được phân phối
    res1 = orch.tick("p_test", ["acc_1"])
    print(f"Nhịp Tick 1: Số tiến trình đang chạy = {res1['active_executions']} (Kỳ vọng: 1 - task_1)")
    
    # Đợi task_1 hoàn thành
    for _, proc, _, _, _ in list(orch.active_executions.values()):
        proc.wait(timeout_seconds=5)
        
    # Nhịp Tick 2: task_1 được nghiệm thu, task_2 đủ điều kiện và được phân phối
    res2 = orch.tick("p_test", ["acc_1"])
    print(f"Nhịp Tick 2: task_1 status = {t_repo.get('task_1')['status']}, task_2 khởi chạy!")
    
    # Đợi task_2 hoàn thành
    for _, proc, _, _, _ in list(orch.active_executions.values()):
        proc.wait(timeout_seconds=5)
        
    # Nhịp Tick 3: task_2 được nghiệm thu, Dự án COMPLETED!
    res3 = orch.tick("p_test", ["acc_1"])
    print(f"Nhịp Tick 3: Trạng thái Dự án = {res3['status']} (Kỳ vọng: COMPLETED)")
    
    db.close()
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n✓ Chu trình Orchestration đạt chuẩn tuyệt đối!\n")

if __name__ == "__main__":
    main()
```

---

### Lab 4: Khởi Chạy Song Song Đa Tác Tử Thực Chiến Với `agy-mas run`

**Mục tiêu**: Trải nghiệm lệnh tự trị hoàn toàn trên môi trường thực tế.

Thực hiện lệnh sau trong cửa sổ CMD/PowerShell:

```bash
# Khởi chạy một dự án thực tế với 2 tài khoản xoay vòng
agy-mas run "Viết bộ tiện ích string_utils.py gồm các hàm slugify, truncate và test tương ứng" \
    --name "Utils Project" \
    --accounts default \
    --concurrency 2 \
    --model gemini-3.8-flash \
    --effort medium
```

Theo dõi trên màn hình console:
- Giai đoạn `[1/3]`: Dự án được đăng ký vào SQLite WAL.
- Giai đoạn `[2/3]`: Kế hoạch được phân rã thành các hợp đồng tác vụ decoupled.
- Giai đoạn `[3/3]`: Orchestrator khởi chạy tick loop, giám sát kết quả và hoàn thành dự án.

---

## 9. TỔNG KẾT & BẢNG TRA CỨU NHANH (CHEAT SHEET)

### Bảng Tra Cứu Lệnh `agy-controller`

| Lệnh | Mô tả cú pháp | Ví dụ |
| :--- | :--- | :--- |
| **`tui`** | Mở giao diện bảng tương tác động | `agy-controller tui` |
| **`list` (`ls`)** | Liệt kê danh sách tài khoản, Model, Effort, Mode | `agy-controller list` |
| **`switch` (`use`)** | Chuyển tài khoản hiện hành theo STT hoặc tên | `agy-controller switch 2` |
| **`config` (`cfg`)** | Cấu hình Model / Effort / Mode cho tài khoản | `agy-controller config 1 --model claude-sonnet-4-6` |
| **`run`** | Chạy `agy` kèm cập nhật nhanh thông số | `agy-controller run --effort high -p "Refactor code"` |
| **`run-many`** | Chạy song song nhiều worker so le Staggered Startup | `agy-controller run-many -w 1 "Task A" -w 2 "Task B"` |
| **`check-all`** | Xem bảng tĩnh tình trạng token toàn bộ tài khoản | `agy-controller check-all` |
| **`check`** | Live Probe kiểm tra và làm mới token (Pre-flight only)| `agy-controller check 1` |
| **`login`** | Đăng nhập tài khoản Google mới và lưu profile | `agy-controller login dev_account` |
| **`install`** | Cài đặt các wrapper thống nhất vào PATH | `agy-controller install` |

---

### Bảng Tra Cứu Lệnh `agy-mas`

| Lệnh | Mô tả cú pháp | Ví dụ |
| :--- | :--- | :--- |
| **`run`** | Lệnh tự trị: Goal -> Plan -> Parallel Multi-Agent | `agy-mas run "Xây dựng REST API"` |
| **`project create`** | Đăng ký dự án thủ công | `agy-mas project create "API" "Xây dựng backend"` |
| **`task create`** | Tạo hợp đồng tác vụ thủ công kèm phụ thuộc | `agy-mas task create proj_1 t2 "API" --depends-on t1` |
| **`plan`** | Tự động sinh DAG tasks cho dự án đã có | `agy-mas plan proj_1` |
| **`orchestrate start`**| Kích hoạt vòng lặp Orchestrator tick loop | `agy-mas orchestrate start proj_1 --concurrency 3` |
| **`resource status`** | Kiểm tra danh sách các cặp đang bị Quota Cooldown | `agy-mas resource status` |

---

### Bảng Chuyển Dịch Máy Trạng Thái 12 Bước (Task State Machine Transitions)

| Trạng thái hiện tại | Các trạng thái kế tiếp hợp lệ | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- |
| **`PENDING`** | `READY`, `BLOCKED`, `CANCELLED` | Vừa tạo, kiểm tra phụ thuộc DAG |
| **`BLOCKED`** | `READY`, `CANCELLED` | Đang đợi các tác vụ cha hoàn tất |
| **`READY`** | `CLAIMED`, `CANCELLED` | Đủ điều kiện, chờ Scheduler cấp phát tài khoản |
| **`CLAIMED`** | `RUNNING`, `RETRY_WAIT`, `CANCELLED` | Đã giữ khóa vùng ghi, đang chuẩn bị nạp credential |
| **`RUNNING`** | `VERIFYING`, `RETRY_WAIT`, `FAILED`, `TIMEOUT`, `CANCELLED` | Tiến trình OS đang thực thi lệnh CLI |
| **`VERIFYING`** | `ACCEPTED`, `RETRY_WAIT`, `FAILED` | Tiến trình xong, đang thẩm định artifacts & output |
| **`RETRY_WAIT`** | `READY`, `FAILED`, `CANCELLED` | Thất bại tạm thời, chờ chuyển giao sang account khác |
| **`TIMEOUT`** | `RETRY_WAIT`, `FAILED` | Vượt ngưỡng thời gian, bị Job Object kết liễu |
| **`ACCEPTED`** | *(Terminal - Điểm cuối)* | Nghiệm thu thành công 100% |
| **`FAILED`** | *(Terminal - Điểm cuối)* | Thất bại vĩnh viễn (hết lượt thử lại) |
| **`CANCELLED`** | *(Terminal - Điểm cuối)* | Bị hủy bởi người dùng hoặc dự án dừng |

---

### Bộ 10 Câu Hỏi Trắc Nghiệm Kiến Trúc Chuyên Sâu (Kèm Lời Giải)

1. **Tại sao `Orchestrator` lại được thiết kế theo mô hình Tick Loop (`.tick()`) thay vì một vòng lặp `while True` nội bộ?**
   - *Trả lời*: Thiết kế Tick Loop giúp tách rời hoàn toàn thời gian thực khỏi logic điều phối, cho phép viết các bài Unit Test tất định (Deterministic Testing) kiểm thử từng bước chuyển trạng thái mà không cần `sleep()` giả tạo.
2. **Kỹ thuật nào cho phép `agy_controller.py` chạy 5 tiến trình `agy` trên 5 tài khoản Google khác nhau dù Windows Credential Manager chỉ có 1 ô nhớ `gemini:antigravity`?**
   - *Trả lời*: Kỹ thuật **Staggered Startup** kết hợp **`CredentialSwitchLock`**. Mỗi tiến trình được cấp quyền đọc token độc quyền vào RAM trong 0.4 giây đầu, sau đó ô nhớ được giải phóng để tráo đổi cho tiến trình tiếp theo.
3. **Tại sao cờ `--effort` lại bị loại bỏ khi chạy các mô hình Claude (`claude-sonnet-4-6`) hoặc GPT trên Antigravity CLI?**
   - *Trả lời*: Vì CLI Antigravity chỉ hỗ trợ đối số `--effort` đối với các mô hình Google Gemini. Truyền cờ này cho Claude hoặc GPT sẽ khiến CLI báo lỗi cú pháp và trả về exit code 1.
4. **Cơ chế nào bảo đảm khi một worker bị Timeout, toàn bộ các tiến trình con do nó sinh ra trên Windows đều bị tiêu diệt sạch sẽ?**
   - *Trả lời*: **Windows Job Objects** với cờ `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Khi handle của Job Object đóng, hệ điều hành tự động tiêu diệt toàn bộ cây tiến trình con được gán vào Job đó.
5. **Tại sao bảng hạn ngạch `account_model_resources` lại có khóa chính phức hợp gồm cả `account_id` và `model_key`?**
   - *Trả lời*: Vì hạn ngạch của các mô hình là độc lập. Một tài khoản hết hạn ngạch Gemini Flash vẫn có thể còn hạn ngạch Claude Sonnet. Khóa phức hợp giúp tối ưu hóa tối đa năng lực phục vụ của tài khoản.
6. **"Lazy Expiration" trong quản lý Cooldown mang lại lợi ích gì cho hệ thống?**
   - *Trả lời*: Giúp loại bỏ sự cần thiết của các luồng chạy ngầm (background polling threads) gây hao tổn CPU và lock database; thời gian hết hạn chỉ được đánh giá chính xác khi có yêu cầu kiểm tra tài nguyên.
7. **Lá chắn kiến trúc trong `probe_single_account` ngăn chặn điều gì?**
   - *Trả lời*: Ngăn chặn việc người dùng thực hiện Live Probe làm tráo đổi Credential Manager trong khi các tiến trình Multi-Agent worker đang chạy song song, bảo vệ hệ thống khỏi lỗi ô nhiễm xác thực chéo (Cross-Account Credential Poisoning).
8. **Theo ADR-014, tại sao một tiến trình có `exit code == 0` vẫn có thể bị coi là `FAILED`?**
   - *Trả lời*: Vì trong chế độ headless print mode, CLI có thể gặp lỗi từ chối quyền (Soft Denial) nhưng vẫn thoát với exit code 0. Hệ thống bắt buộc phải quét luồng stdout/stderr để phát hiện lỗi này.
9. **Theo ADR-016, tại sao việc tính mã băm SHA-256 của Deliverables phải đợi sau khi tiến trình worker thoát hoàn toàn?**
   - *Trả lời*: Để tránh xung đột khóa file độc quyền trên Windows (`WinError 32`) và bảo đảm dữ liệu tệp tin đã được flush hoàn toàn từ bộ đệm đĩa cứng.
10. **Khi nào một dự án trong Orchestrator chuyển sang trạng thái `FAILED`?**
    - *Trả lời*: Khi có ít nhất một tác vụ bị `FAILED` (hết lượt thử lại) và không còn bất kỳ tác vụ nào khác trong hệ thống đang ở trạng thái có thể tiếp tục (`RUNNING`, `CLAIMED`, `READY`, `PENDING`, `RETRY_WAIT`).
