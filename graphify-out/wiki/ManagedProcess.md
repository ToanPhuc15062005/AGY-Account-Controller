# ManagedProcess

> 22 nodes · cohesion 0.14

## Key Concepts

- **ManagedProcess** (30 connections) — `src/agy_mas/agents/process_manager.py`
- **.dispatch()** (15 connections) — `src/agy_mas/core/dispatcher.py`
- **.terminate_tree()** (7 connections) — `src/agy_mas/agents/process_manager.py`
- **3.3. Thu thập Stream bất đồng bộ Non-blocking & Bộ ngắt tiến trình 2 lớp** (5 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **3. Phân hệ Agent Runtime & Process Supervision (`agents/`)** (5 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **.start()** (5 connections) — `src/agy_mas/agents/process_manager.py`
- **.test_managed_process_execution()** (5 connections) — `tests/unit/test_agy_adapter.py`
- **.close_log()** (4 connections) — `src/agy_mas/agents/process_manager.py`
- **3.2. Giám sát tiến trình cấp thấp & Windows Job Objects (`process_manager.py`)** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **JOBOBJECT_EXTENDED_LIMIT_INFORMATION** (3 connections) — `src/agy_mas/agents/process_manager.py`
- **.wait()** (3 connections) — `src/agy_mas/agents/process_manager.py`
- **.mark_process_started()** (3 connections) — `src/agy_mas/storage/repositories/execution_repo.py`
- **Cơ chế thiết lập Win32 Job Object:** (2 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **Cơ chế tiêu diệt tiến trình 2 lớp (Two-Layer Defense Termination):** (2 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **.is_alive()** (2 connections) — `src/agy_mas/agents/process_manager.py`
- **._read_stderr()** (2 connections) — `src/agy_mas/agents/process_manager.py`
- **._read_stdout()** (2 connections) — `src/agy_mas/agents/process_manager.py`
- **Safely flushes and closes task execution log file.** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Terminates process and all child descendants, ensuring process tree is dead.** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Manages an active agent subprocess, capturing streams and supervising process…** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Starts the subprocess and attaches Windows Job Object if supported.** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Any** (1 connections)

## Relationships

- [main.py](main.py.md) (5 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (4 shared connections)
- [Invocation](Invocation.md) (4 shared connections)
- [ResourceRepository](ResourceRepository.md) (4 shared connections)
- [AGYAdapter](AGYAdapter.md) (3 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (2 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (2 shared connections)
- [ExecutionRepository](ExecutionRepository.md) (2 shared connections)
- [TaskContract](TaskContract.md) (2 shared connections)
- [OwnershipManager](OwnershipManager.md) (2 shared connections)
- [Orchestrator](Orchestrator.md) (2 shared connections)
- [GIÁO TRÌNH KIẾN TRÚC & PHÁT TRIỂN AGY-MAS](GIÁO_TRÌNH_KIẾN_TRÚC_&_PHÁT_TRIỂN_AGY-MAS.md) (1 shared connections)

## Source Files

- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/agents/process_manager.py`
- `src/agy_mas/core/dispatcher.py`
- `src/agy_mas/storage/repositories/execution_repo.py`
- `tests/unit/test_agy_adapter.py`

## Audit Trail

- EXTRACTED: 42 (59%)
- INFERRED: 29 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*