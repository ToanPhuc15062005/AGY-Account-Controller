# QuotaTracker

> God node · 31 connections · `src/agy_mas/resources/quota_tracker.py`

**Community:** [ResourceRepository](ResourceRepository.md)

## Connections by Relation

### calls
- init_mas() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`

### contains
- quota_tracker.py `EXTRACTED`

### imports
- orchestrator.py `EXTRACTED`
- [main.py](main.py.md) `EXTRACTED`
- scheduler.py `EXTRACTED`
- resources/__init__.py `EXTRACTED`

### method
- .record_quota_exhaustion() `EXTRACTED`
- .is_available() `EXTRACTED`
- .select_eligible_account() `EXTRACTED`
- .__init__() `EXTRACTED`
- .clear_cooldown() `EXTRACTED`

### rationale_for
- Manages resource cooldown states scoped to (account_id, model_key). `EXTRACTED`

### references
- [6.1. Classes & Modules](6.1._Classes_&_Modules.md) `INFERRED`
- Tổng Kết & Bảng Tra Cứu Nhanh `INFERRED`
- 🚀 Tính năng cốt lõi của Multi-Agent System (`agy-mas`) `INFERRED`
- .__init__() `EXTRACTED`
- 4.4. Chuyên Đề 04 — Orchestrator, Quota & CLI `INFERRED`
- .__init__() `EXTRACTED`
- 1. GIỚI THIỆU & BỐI CẢNH BÀI TOÁN `INFERRED`

### uses
- [ResourceRepository](ResourceRepository.md) `INFERRED`
- [Orchestrator](Orchestrator.md) `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- Scheduler `INFERRED`
- TestPairProgramming `INFERRED`
- TestAGYAdapterAndQuota `INFERRED`
- TestOrchestrator `INFERRED`
- QuotaConfig `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*