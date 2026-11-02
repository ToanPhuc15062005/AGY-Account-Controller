# .snapshot_file

> 15 nodes · cohesion 0.14

## Key Concepts

- **.snapshot_file()** (9 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **.register_task_artifacts()** (9 connections) — `src/agy_mas/workspace/workspace_manager.py`
- **4. Phân hệ Quản trị Workspace & Windows Hardening (`workspace/`)** (6 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **3.4. Facade Pattern — `WorkspaceManager`** (4 connections) — `docs/study_guide/01_architecture_and_design_patterns.md`
- **4.1. Chính sách An toàn Đường dẫn (`path_policy.py`)** (4 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **4.3. Quản trị Quyền Ghi theo Lease Mẫu Đường dẫn (`ownership_manager.py`)** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **4.5. Facade Điều phối Workspace (`workspace_manager.py`)** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Vì sao quy tắc này sống còn?** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **4.4. Snapshot Deliverables & Quyết định Kiến trúc ADR-016 (`snapshot_manager.py`)** (2 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Quy tắc kiểm tra xung đột:** (1 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Any** (1 connections)
- **Calculates file checksum and metadata after verifying process is terminated.** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **_read_and_hash()** (1 connections) — `src/agy_mas/workspace/snapshot_manager.py`
- **Any** (1 connections)
- **Snapshots deliverables and commits them to the artifact repository.** (1 connections) — `src/agy_mas/workspace/workspace_manager.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (3 shared connections)
- [.resolve_safe_path](resolve_safe_path.md) (3 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (3 shared connections)
- [OwnershipManager](OwnershipManager.md) (2 shared connections)
- [3. CÁC DESIGN PATTERNS CỐT LÕI](3._CÁC_DESIGN_PATTERNS_CỐT_LÕI.md) (1 shared connections)
- [PathPolicy](PathPolicy.md) (1 shared connections)
- [FileSharingContentionError](FileSharingContentionError.md) (1 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (1 shared connections)
- [TaskContract](TaskContract.md) (1 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (1 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (1 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (1 shared connections)

## Source Files

- `docs/study_guide/01_architecture_and_design_patterns.md`
- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/workspace/snapshot_manager.py`
- `src/agy_mas/workspace/workspace_manager.py`

## Audit Trail

- EXTRACTED: 16 (47%)
- INFERRED: 18 (53%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*