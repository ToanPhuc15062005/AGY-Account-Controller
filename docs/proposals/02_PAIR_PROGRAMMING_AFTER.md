# ARCHITECTURE PROPOSAL (AFTER: KIẾN TRÚC PAIR-PROGRAMMING)

> **Mục đích tài liệu:** Đặc tả chi tiết các thay đổi cấu trúc, luồng dữ liệu và mã nguồn chuẩn bị triển khai để tích hợp cơ chế **Lập trình Cặp (Pair-Programming: Coder $\longleftrightarrow$ Reviewer)** vào hệ thống `agy-mas`.  
> **Phạm vi:** Chỉ tập trung đối chiếu các điểm thay đổi so với bản BEFORE (Hợp đồng tác vụ, Quản lý trạng thái, Khâu thẩm định chủ động và Vòng lặp phản hồi Feedback Loop).

---

## 1. Cấu trúc Hợp đồng Tác vụ Mở rộng (`plan_schema.py`)

Bổ sung các trường cấu hình Pair-Review và cấu trúc dữ liệu Biên bản Đánh giá:

```python
from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

class ReviewVerdict(str, Enum):
    APPROVED = "APPROVED"                   # Đạt chuẩn -> Nghiệm thu task
    CHANGES_REQUESTED = "CHANGES_REQUESTED" # Chưa đạt -> Yêu cầu Coder sửa

@dataclass
class ReviewReport:
    """Biên bản đánh giá chất lượng code do Reviewer Agent tạo ra."""
    verdict: ReviewVerdict
    score: int                              # Thang điểm 0 - 100 (Ví dụ >= 80 là Approved)
    critique_summary: str                   # Tóm tắt lý do từ chối / chấp thuận
    actionable_feedback: List[str]          # Danh sách chỉ thị sửa đổi chi tiết từng file, dòng
    test_output_summary: Optional[str] = None # Log lỗi kiểm thử (nếu có)

@dataclass
class TaskContract:
    task_id: str
    project_id: str
    title: str
    description: str
    domain: str = "software"
    role: str = "developer"                 # Coder (Primary Worker)
    priority: int = 50
    inputs: InputScope = field(default_factory=InputScope)
    outputs: OutputScope = field(default_factory=OutputScope)
    acceptance_criteria: List[AcceptanceCriterion] = field(default_factory=list)
    permission_profile: PermissionProfile = field(default_factory=PermissionProfile)
    timeout_seconds: int = 900
    max_retries: int = 2
    depends_on: List[str] = field(default_factory=list)

    # === [MỚI BỔ SUNG CHO PAIR-PROGRAMMING] ===
    enable_pair_review: bool = True         # Bật/tắt chế độ thẩm định đôi
    reviewer_role: str = "qa_reviewer"      # Vai trò thẩm định
    reviewer_model: Optional[str] = None    # Model dùng cho Reviewer (ví dụ: claude-sonnet-4-6)
    max_pair_rounds: int = 3                # Tối đa 3 vòng đối thoại Coder <-> Reviewer
    pair_round: int = 0                     # Vòng hiện tại
    last_review_report: Optional[Dict[str, Any]] = None # Biên bản góp ý gần nhất
```

---

## 2. Nâng cấp Vòng đời Tác vụ: Khâu Thẩm định Chủ động (`orchestrator.py`)

Tại trạng thái [`TaskState.VERIFYING`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/state_machine.py#L37), thay vì chấp thuận thụ động, Orchestrator chuyển sang thực thi **Reviewer Subprocess**:

```python
# === [LUỒNG THẨM ĐỊNH MỚI] ===
if not proc.is_alive():
    exit_code = proc.process.poll() if proc.process else -1
    proc.close_log()

    # 1. Chuyển sang VERIFYING
    TaskStateMachine.transition(
        self.task_repo, tid, TaskState.VERIFYING,
        event_repo=self.event_repo, execution_id=exec_id
    )
    self._emit("TASK_VERIFYING", {"task_id": tid, "execution_id": exec_id})

    if exit_code != 0:
        # Xử lý crash/lỗi runtime như cũ...
        pass
    else:
        # Nếu task không bật Pair-Review -> Chấp thuận ngay như bản cũ
        if not contract.enable_pair_review:
            self._finalize_acceptance(project_id, tid, exec_id, contract, proc)
            finished_execs.append(exec_id)
            continue

        # NẾU BẬT PAIR-REVIEW: Kích hoạt Reviewer Agent với cơ chế Fault-Tolerance
        self._emit("PAIR_REVIEW_STARTED", {"task_id": tid, "round": contract.pair_round + 1})
        
        try:
            review_report = self.review_engine.execute_review(
                project_id=project_id,
                task_contract=contract,
                coder_execution_id=exec_id,
                workspace_root=self.workspace_mgr.workspace_root,
                timeout_seconds=180,  # Bọc timeout 3 phút cho Reviewer
            )
        except Exception as review_err:
            # Fallback nếu Reviewer crash/timeout: Ghi nhận lỗi và dọn dẹp an toàn
            self._emit("PAIR_REVIEW_ERROR", {"task_id": tid, "error": str(review_err)})
            self.execution_repo.mark_completed(
                exec_id, status="COMPLETED", exit_code=0, normalized_outcome="REVIEW_ERROR"
            )
            self.workspace_mgr.ownership_manager.release_all(exec_id)
            TaskStateMachine.transition(
                self.task_repo, tid, TaskState.RETRY_WAIT,
                event_repo=self.event_repo, execution_id=exec_id,
                reason=f"Reviewer execution failed: {review_err}"
            )
            finished_execs.append(exec_id)
            continue

        if review_report.verdict == ReviewVerdict.APPROVED:
            # Reviewer phê duyệt -> Giải phóng lock và Chấp thuận nghiệm thu
            self._finalize_acceptance(project_id, tid, exec_id, contract, proc)
            self._emit("PAIR_REVIEW_APPROVED", {
                "task_id": tid, "score": review_report.score
            })
        else:
            # Reviewer từ chối (CHANGES_REQUESTED)
            contract.pair_round += 1
            # Đóng dấu hoàn tất execution của Coder đợt này (tránh treo status RUNNING và completed_at = NULL)
            self.execution_repo.mark_completed(
                exec_id, status="COMPLETED", exit_code=0, normalized_outcome="CHANGES_REQUESTED"
            )
            # BẮT BUỘC: Giải phóng toàn bộ Write Leases của Coder lần này để tránh xung đột Lock ở lần sau
            self.workspace_mgr.ownership_manager.release_all(exec_id)

            if contract.pair_round < contract.max_pair_rounds:
                # Lưu biên bản góp ý vào DB
                self.task_repo.update_critique(tid, review_report.to_dict(), contract.pair_round)
                self._emit("PAIR_REVIEW_REJECTED", {
                    "task_id": tid,
                    "round": contract.pair_round,
                    "feedback": review_report.actionable_feedback
                })

                # Chuyển sang RETRY_WAIT (lưu vết Audit Trail). 
                # Scheduler ở tick kế tiếp sẽ thăng hạng sang READY sau khi áp dụng backoff dọn dẹp I/O
                TaskStateMachine.transition(
                    self.task_repo, tid, TaskState.RETRY_WAIT,
                    event_repo=self.event_repo, execution_id=exec_id,
                    reason=f"Reviewer requested changes (Round {contract.pair_round})"
                )
            else:
                # Quá số vòng quy định (Circuit Breaker)
                self._emit("PAIR_REVIEW_EXHAUSTED", {"task_id": tid, "rounds": contract.pair_round})
                TaskStateMachine.transition(
                    self.task_repo, tid, TaskState.FAILED,
                    event_repo=self.event_repo, execution_id=exec_id,
                    reason="Max pair-programming rounds reached without approval"
                )

        # BẮT BUỘC: Thu hồi tiến trình đã kết thúc ra khỏi active_executions (tránh lặp tick)
        finished_execs.append(exec_id)
```

### Luồng thực thi mới:
$$\text{RUNNING (Coder)} \xrightarrow{\text{code = 0}} \text{VERIFYING (Reviewer Agent)} \begin{cases} \xrightarrow{\text{APPROVED}} \text{ACCEPTED} \\ \xrightarrow{\text{REJECTED}} \text{RETRY\_WAIT} \rightarrow \text{READY (Coder sửa)} \end{cases}$$

---

## 3. Bơm Phản hồi (Feedback Injection) vào Prompt (`agy_adapter.py`)

Hàm `build_invocation()` được nâng cấp để tạo 2 loại Prompt chuyên biệt:

### A. Đối với Coder khi chạy lại từ Vòng 2 trở đi (`pair_round > 0`):
Hệ thống tự động tiêm toàn bộ nhận xét của Reviewer vào Prompt để Coder sửa đúng chỗ:

```python
last_critique = task_contract.get("last_review_report")
if last_critique:
    critique_items = "\n".join([f"  - {fb}" for fb in last_critique.get("actionable_feedback", [])])
    prompt_body += (
        f"\n\n=======================================================\n"
        f"🚨 [FEEDBACK FROM CODE REVIEWER - ROUND #{task_contract.get('pair_round')}]:\n"
        f"Summary: {last_critique.get('critique_summary')}\n"
        f"Specific Defect List:\n{critique_items}\n\n"
        f"INSTRUCTION: Preserve all working logic. Fix ONLY the defects listed above.\n"
        f"=======================================================\n"
    )
```

### B. Đối với Reviewer Agent:
Prompt được tạo theo khuôn mẫu thanh tra:
* **Inputs:** `git diff` của các file vừa sửa, danh sách `expected_artifacts`, lệnh chạy kiểm thử (`pytest`).
* **Output Format:** Ép buộc xuất JSON định dạng `ReviewReport`.

---

## 4. Mở rộng Cơ sở Dữ liệu (`schema.sql` Evolution)

Bổ sung bảng lưu vết `task_reviews` và mở rộng bảng `executions`:

```sql
-- Thêm cột vào bảng tasks
ALTER TABLE tasks ADD COLUMN pair_round INTEGER DEFAULT 0;
ALTER TABLE tasks ADD COLUMN last_critique_json TEXT;

-- Thêm cột vào bảng executions để phân biệt vai trò thực thi
ALTER TABLE executions ADD COLUMN execution_role TEXT DEFAULT 'PRIMARY'; -- 'PRIMARY' (Coder) hoặc 'REVIEWER'

-- Bảng mới lưu vết chi tiết từng vòng phản biện
CREATE TABLE IF NOT EXISTS task_reviews (
    review_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    round_number INTEGER NOT NULL,
    verdict TEXT NOT NULL,                  -- 'APPROVED', 'CHANGES_REQUESTED'
    score INTEGER NOT NULL,
    critique_json TEXT NOT NULL,            -- Danh sách nhận xét sửa đổi
    test_output TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id),
    FOREIGN KEY(execution_id) REFERENCES executions(execution_id)
);

CREATE INDEX IF NOT EXISTS idx_reviews_task ON task_reviews(task_id, round_number);
```

---

## 5. Bảng Đối chiếu Trực tiếp: BEFORE vs AFTER

| Thành phần | Hiện trạng (BEFORE) | Đề xuất mới (AFTER) |
| :--- | :--- | :--- |
| **Quy trình thẩm định** | Thụ động: Chỉ kiểm tra `exit_code == 0` và file tồn tại. | Chủ động: Chạy Reviewer Agent kiểm tra logic, linter và unit test. |
| **Cơ chế Retry** | Thử lại mù (Blind Retry): Gửi lại 100% prompt cũ, không có feedback. | Thử lại có định hướng (Feedback-driven): Bơm toàn bộ biên bản lỗi của Reviewer vào Prompt. |
| **Hợp đồng tác vụ** | Đơn lẻ: Chỉ 1 Worker gánh vác toàn bộ việc. | Lập trình cặp: Tách bạch rõ vai trò Coder (viết) và Reviewer (soi lỗi). |
| **Bảo vệ chống lặp** | Chỉ dựa vào `max_retries` thô sơ. | Giới hạn `max_pair_rounds = 3` với Circuit Breaker rõ ràng. |
| **Khả năng quan sát** | Chỉ biết task PASS hay FAIL chung chung. | Theo dõi được chi tiết từng vòng Review, lý do từ chối và điểm số chất lượng. |

---

## 6. Lưu ý Triển khai Thực tế (Implementation & Runtime Safeguards)

Khi chuyển giao bản thiết kế này vào mã nguồn thực tế của [`src/agy_mas/core/orchestrator.py`](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/core/orchestrator.py), bắt buộc phải tuân thủ nghiêm ngặt **3 nguyên tắc dọn dẹp trạng thái**:

1. **Thu hồi tiến trình vào `finished_execs`:**
   - Dòng `finished_execs.append(exec_id)` phải luôn được gọi ở cuối mọi nhánh kết thúc của lượt chạy (bao gồm cả khi `APPROVED`, `CHANGES_REQUESTED`, hoặc khi Reviewer ném ngoại lệ trong khối `except`).
   - *Nguy cơ nếu thiếu:* Tiến trình `proc` không được gỡ khỏi từ điển `self.active_executions`, dẫn đến việc Orchestrator tiếp tục quét lại tiến trình đã chết ở vòng lặp tick tiếp theo, gây lỗi lặp tick vô tận.

2. **Đóng dấu hoàn tất bản ghi `executions` khi bị Reject hoặc Error:**
   - Khi Coder hoàn thành đợt code nhưng bị Reviewer từ chối (`CHANGES_REQUESTED`) hoặc Reviewer bị lỗi (`REVIEW_ERROR`), bắt buộc phải gọi:
     ```python
     self.execution_repo.mark_completed(
         exec_id, status="COMPLETED", exit_code=0, normalized_outcome="CHANGES_REQUESTED"
     )
     ```
   - *Nguy cơ nếu thiếu:* Bản ghi trong bảng `executions` sẽ bị treo vĩnh viễn ở trạng thái `RUNNING` với trường `completed_at = NULL`, làm sai lệch hoàn toàn báo cáo đo lường thời gian thực thi (metrics) của hệ thống.

3. **Cơ chế Thăng hạng Trạng thái Tách rời (Decoupled Scheduler Tick Promotion):**
   - Tuyệt đối không gọi 2 lệnh chuyển trạng thái tức thì `VERIFYING -> RETRY_WAIT` và `RETRY_WAIT -> READY` trong cùng một dòng lệnh đồng bộ.
   - Khi Reviewer từ chối, task dừng lại ở `TaskState.RETRY_WAIT`.
   - Vòng lặp `tick()` tiếp theo của Orchestrator (sau khoảng thời gian backoff dọn dẹp đệm I/O của Windows) mới chịu trách nhiệm thăng hạng task từ `RETRY_WAIT` sang `READY` để bảo đảm tính tôn nghiêm và dấu vết kiểm toán (Audit Trail) của Máy trạng thái.

