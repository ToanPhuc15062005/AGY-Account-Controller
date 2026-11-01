# process_manager.py

> 19 nodes · cohesion 0.14

## Key Concepts

- **process_manager.py** (21 connections) — `src/agy_mas/agents/process_manager.py`
- **ManagedProcess** (19 connections) — `src/agy_mas/agents/process_manager.py`
- **TerminationResult** (5 connections) — `src/agy_mas/agents/base.py`
- **.start()** (5 connections) — `src/agy_mas/agents/process_manager.py`
- **.test_managed_process_execution()** (5 connections) — `tests/unit/test_agy_adapter.py`
- **.terminate_tree()** (4 connections) — `src/agy_mas/agents/process_manager.py`
- **ctypes** (2 connections)
- **JOBOBJECT_EXTENDED_LIMIT_INFORMATION** (2 connections) — `src/agy_mas/agents/process_manager.py`
- **.is_alive()** (2 connections) — `src/agy_mas/agents/process_manager.py`
- **.wait()** (2 connections) — `src/agy_mas/agents/process_manager.py`
- **threading** (2 connections)
- **IO_COUNTERS** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **JOBOBJECT_BASIC_LIMIT_INFORMATION** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **._read_stderr()** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **._read_stdout()** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Process manager handling cross-platform process trees, Windows Job Objects, and…** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Terminates process and all child descendants, ensuring process tree is dead.** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Manages an active agent subprocess, capturing streams and supervising process…** (1 connections) — `src/agy_mas/agents/process_manager.py`
- **Starts the subprocess and attaches Windows Job Object if supported.** (1 connections) — `src/agy_mas/agents/process_manager.py`

## Relationships

- [orchestrator.py](orchestrator.py.md) (10 shared connections)
- [main.py](main.py.md) (9 shared connections)
- [Invocation](Invocation.md) (4 shared connections)
- [RuntimeCapabilities](RuntimeCapabilities.md) (3 shared connections)
- [TestAGYAdapterAndQuota](TestAGYAdapterAndQuota.md) (2 shared connections)
- [agy_controller.py](agy_controller.py.md) (1 shared connections)

## Source Files

- `src/agy_mas/agents/base.py`
- `src/agy_mas/agents/process_manager.py`
- `tests/unit/test_agy_adapter.py`

## Audit Trail

- EXTRACTED: 46 (87%)
- INFERRED: 7 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*