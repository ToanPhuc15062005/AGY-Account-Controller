# OwnershipManager

> 16 nodes · cohesion 0.12

## Key Concepts

- **OwnershipManager** (22 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Luồng tương tác 6 bước chuẩn hóa** (8 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **2. Kiến trúc Tổng thể: Agents - Workspace - Verification Pipeline** (6 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Mục tiêu học tập (Learning Objectives)** (6 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **OwnershipConflictError** (6 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.claim_ownership()** (4 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.claim_file_ownership()** (3 connections) — `src/agy_mas/storage/repositories/resource_repo.py`
- **1. Tổng quan & Mục tiêu đào tạo (Overview & Objectives)** (2 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **.check_write_permitted()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **.__init__()** (2 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Sơ đồ tương tác kiến trúc hệ thống** (1 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **PermissionError** (1 connections)
- **Raised when an execution attempts to claim or write to a path owned by another…** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Manages path pattern leases and verifies file modification privileges.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Claims a path pattern lease for an execution attempt.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`
- **Checks if the given execution owns a valid, unexpired write lease for the path.** (1 connections) — `src/agy_mas/workspace/ownership_manager.py`

## Relationships

- [ResourceRepository](ResourceRepository.md) (8 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (6 shared connections)
- [main.py](main.py.md) (4 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (2 shared connections)
- [TaskContract](TaskContract.md) (2 shared connections)
- [Verifier](Verifier.md) (2 shared connections)
- [ManagedProcess](ManagedProcess.md) (2 shared connections)
- [PathPolicy](PathPolicy.md) (2 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (2 shared connections)
- [.snapshot_file](snapshot_file.md) (2 shared connections)
- [AGYAdapter](AGYAdapter.md) (1 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (1 shared connections)

## Source Files

- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/storage/repositories/resource_repo.py`
- `src/agy_mas/workspace/ownership_manager.py`

## Audit Trail

- EXTRACTED: 24 (46%)
- INFERRED: 28 (54%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*