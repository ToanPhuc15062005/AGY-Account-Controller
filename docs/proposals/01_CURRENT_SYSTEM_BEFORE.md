# ARCHITECTURE BASELINE (BEFORE: HIỆN TRẠNG HỆ THỐNG)

> **Mục đích tài liệu:** Mô tả chính xác các cấu trúc, luồng điều phối và mã nguồn hiện tại của hệ thống `agy-mas` trước khi tích hợp cơ chế Pair-Programming (Coder $\longleftrightarrow$ Reviewer).  
> **Phạm vi:** Chỉ tập trung vào các thành phần liên quan đến: Hợp đồng tác vụ, Quản lý trạng thái, Khâu thẩm định (Verification) và Cơ chế thử lại (Retry).

---

## 1. Cấu trúc Hợp đồng Tác vụ Hiện tại (`plan_schema.py`)

Trong [`src/agy_mas/planning/plan_schema.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/planning/plan_schema.py), một tác vụ chỉ được gắn với **một vai trò đơn lẻ (Single Worker)**:

```python
@dataclass
class TaskContract:
    task_id: str
    project_id: str
    title: str
    description: str
    domain: str = "software"
    role: str = "developer"             # Chỉ hỗ trợ 1 role duy nhất đảm nhiệm
    priority: int = 50
    inputs: InputScope = field(default_factory=InputScope)
    outputs: OutputScope = field(default_factory=OutputScope)
    acceptance_criteria: List[AcceptanceCriterion] = field(default_factory=list)
    permission_profile: PermissionProfile = field(default_factory=PermissionProfile)
    timeout_seconds: int = 900
    max_retries: int = 2
    depends_on: List[str] = field(default_factory=list)
```

### Hạn chế hiện tại:
* Không có thuộc tính cấu hình chế độ thẩm định đôi (Pair-Review).
* Không có vai trò giám sát / kiểm thử viên (`reviewer_role`).
* Không có cơ chế lưu vết nhận xét góp ý (`critique_feedback`).

---

## 2. Vòng đời Tác vụ & Khâu Thẩm định Hiện tại (`orchestrator.py`)

Trong [`src/agy_mas/core/orchestrator.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py), khi tiến trình con kết thúc với mã thoát `0`, Orchestrator thực hiện thẩm định thụ động:

```python
if not proc.is_alive():
    exit_code = proc.process.poll() if proc.process else -1

    # Chuyển trạng thái sang VERIFYING
    TaskStateMachine.transition(
        self.task_repo, tid, TaskState.VERIFYING,
        event_repo=self.event_repo, execution_id=exec_id
    )

    if exit_code != 0:
        # Xử lý thất bại...
        pass
    else:
        # Exit code 0: Thẩm định thụ động và chấp thuận ngay lập tức
        self.workspace_mgr.register_task_artifacts(
            project_id=project_id,
            task_id=tid,
            execution_id=exec_id,
            expected_artifacts=[{"path": a.path, "artifact_type": a.artifact_type} 
                                for a in contract.outputs.expected_artifacts],
            process=proc,
        )
        self.execution_repo.mark_completed(
            exec_id, status="COMPLETED", exit_code=0, normalized_outcome="SUCCESS"
        )
        self.workspace_mgr.ownership_manager.release_all(exec_id)

        # Chuyển thẳng sang ACCEPTED mà không có bước Review chất lượng
        TaskStateMachine.transition(
            self.task_repo, tid, TaskState.ACCEPTED,
            event_repo=self.event_repo, execution_id=exec_id,
            reason="Execution and artifacts verified"
        )
```

### Luồng thực thi hiện tại:
$$\text{RUNNING (Worker đơn lẻ)} \xrightarrow{\text{exit code 0}} \text{VERIFYING (Kiểm tra file tồn tại)} \xrightarrow{\text{Thành công}} \text{ACCEPTED}$$

### Hạn chế hiện tại:
* **Chấp thuận mù quáng (Blind Acceptance):** Chỉ cần tiến trình thoát mã `0` và tạo ra file (kể cả file rỗng hoặc code sai logic), hệ thống lập tức đóng dấu `ACCEPTED`.
* Hoàn toàn thiếu vắng bước kiểm tra chéo (Cross-validation) từ một Agent thứ hai.

---

## 3. Cơ chế Khởi tạo Prompt và Thử lại Hiện tại (`agy_adapter.py`)

Trong [`src/agy_mas/agents/adapters/agy_adapter.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/agents/adapters/agy_adapter.py), hàm `build_invocation()` lắp ráp Prompt theo khuôn mẫu cố định:

```python
prompt_body = (
    f"TASK: {title}\n"
    f"OBJECTIVE: {desc}\n"
    f"EXPECTED ARTIFACTS: {expected_str}\n"
    "REQUIREMENTS: Execute strictly within requested scopes and verify outputs.\n"
)
cmd.extend(["-p", prompt_body])
```

### Hạn chế khi Thử lại (Retry Flaw):
* Khi một task thất bại ở lần 1 (ví dụ dính lỗi chia cho 0, syntax error hoặc test fail):
* Ở lần thử 2 (`attempt #2`), hệ thống **gửi lại đúng 100% nội dung Prompt ban đầu**.
* Worker ở lần 2 hoàn toàn không biết lần 1 mình đã viết gì, sai ở dòng nào, thiếu cái gì. Nó lặp lại toàn bộ quá trình mò mẫm từ đầu (Zero-feedback retry).

---

## 4. Mô hình Lưu trữ Database Hiện tại (`schema.sql`)

Bảng `tasks` và `executions` hiện tại chỉ ghi nhận số liệu thực thi độc lập:

```sql
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    domain TEXT NOT NULL,
    role TEXT NOT NULL,
    priority INTEGER NOT NULL,
    status TEXT NOT NULL,
    task_spec_json TEXT NOT NULL,
    dependencies_json TEXT NOT NULL
);

CREATE TABLE executions (
    execution_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    runtime_type TEXT NOT NULL,
    account_id TEXT,
    model TEXT,
    status TEXT NOT NULL,
    exit_code INTEGER,
    started_at TEXT NOT NULL,
    completed_at TEXT
);
```

### Hạn chế:
* Không có trường thể hiện số vòng phản biện (Round index).
* Không có bảng ghi nhận biên bản đánh giá chất lượng (Critique Reports).
