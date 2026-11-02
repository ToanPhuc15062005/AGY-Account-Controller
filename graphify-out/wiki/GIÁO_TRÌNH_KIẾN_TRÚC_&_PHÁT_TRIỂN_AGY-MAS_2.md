# GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS

> 44 nodes · cohesion 0.05

## Key Concepts

- **GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS** (12 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **7. CHƯƠNG 6: CÁC CA BIÊN (EDGE CASES), BẪY KỸ THUẬT & GIẢI PHÁP GIA CỐ TRÊN WINDOWS** (6 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **.is_in_cooldown()** (6 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **4. CHƯƠNG 3: QUẢN LÝ HẠN NGẠCH & TỰ ĐỘNG CHUYỂN GIAO (QUOTATRACKER & RESOURCE MANAGEMENT)** (5 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **8. CHƯƠNG 7: THỰC HÀNH & BÀI TẬP CHUYÊN SÂU (HANDS-ON LAB)** (5 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **9. TỔNG KẾT & BẢNG TRA CỨU NHANH (CHEAT SHEET)** (5 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **1. TỔNG QUAN KIẾN TRÚC & TRIẾT LÝ ĐIỀU PHỐI** (4 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **6. CHƯƠNG 5: GIAO DIỆN DÒNG LỆNH `agy-mas` CLI & HỆ THỐNG WRAPPERS** (4 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **.is_available()** (4 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.select_eligible_account()** (4 connections) — `src/agy_mas/resources/quota_tracker.py`
- **.get_account_model_resource()** (4 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **10. ĐÁP ÁN GỢI Ý & HƯỚNG DẪN TỰ ĐÁNH GIÁ** (3 connections) — `docs/study_guide/00_master_study_guide.md`
- **3.1. Bộ Lập Lịch Đồ Thị `Scheduler`** (3 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **3.2. Bộ Khởi Chạy `Dispatcher`** (3 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **3. CHƯƠNG 2: BỘ LẬP LỊCH TẤT ĐỊNH & PHÂN PHỐI TÁC VỤ (SCHEDULER & DISPATCHER)** (3 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **Bộ 10 Câu Hỏi Trắc Nghiệm Kiến Trúc Chuyên Sâu (Kèm Lời Giải)** (3 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **Đáp Án Câu Hỏi Ôn Tập (Chọn Lọc)** (2 connections) — `docs/study_guide/00_master_study_guide.md`
- **1.1. Vị Trí Của Orchestrator, Quota Tracker và CLI Trong Hệ Thống Multi-Agent** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **4.2. Cơ Chế Ghi Nhận Cooldown & Hết Hạn Lười (Lazy Expiration)** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **6.2. Luồng Tự Trị Một Lệnh Duy Nhất: `agy-mas run "<goal>"`** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **6.3. Hệ Thống Wrappers Windows & Cài Đặt PATH Người Dùng** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **7.4. Đảm Bảo An Toàn Snapshot Deliverables (Tuân Thủ ADR-016)** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **Quy trình ra quyết định:** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **Triết lý Hết Hạn Lười (Lazy Expiration):** (2 connections) — `docs/study_guide/04_orchestrator_quota_and_cli.md`
- **Rubric Tự Đánh Giá** (1 connections) — `docs/study_guide/00_master_study_guide.md`
- *... and 19 more nodes in this community*

## Relationships

- [ResourceRepository](ResourceRepository.md) (9 shared connections)
- [TaskContract](TaskContract.md) (3 shared connections)
- [agy_controller.py](agy_controller.py.md) (3 shared connections)
- [Orchestrator](Orchestrator.md) (2 shared connections)
- [MASTER STUDY GUIDE — AGY-MAS ARCHITECTURE & DEVELOPMENT](MASTER_STUDY_GUIDE_—_AGY-MAS_ARCHITECTURE_&_DEVELOPMENT.md) (1 shared connections)
- [main.py](main.py.md) (1 shared connections)
- [.snapshot_file](snapshot_file.md) (1 shared connections)
- [Invocation](Invocation.md) (1 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (1 shared connections)
- [2. CHƯƠNG 1: VÒNG LẶP ĐIỀU PHỐI TRUNG TÂM (CENTRAL ORCHESTRATOR)](2._CHƯƠNG_1-_VÒNG_LẶP_ĐIỀU_PHỐI_TRUNG_TÂM_CENTRAL_ORCHESTRATOR.md) (1 shared connections)
- [.fetchone](fetchone.md) (1 shared connections)

## Source Files

- `docs/study_guide/00_master_study_guide.md`
- `docs/study_guide/04_orchestrator_quota_and_cli.md`
- `src/agy_mas/resources/quota_tracker.py`
- `src/agy_mas/storage/repositories/resource_repo.py`

## Audit Trail

- EXTRACTED: 52 (78%)
- INFERRED: 15 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*