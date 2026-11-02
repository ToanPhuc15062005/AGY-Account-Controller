# PathPolicy

> 25 nodes · cohesion 0.16

## Key Concepts

- **PathPolicy** (31 connections) — `src/agy_mas/workspace/path_policy.py`
- **🚀 Tính năng cốt lõi của Multi-Agent System (`agy-mas`)** (20 connections) — `README.md`
- **verifier.py** (19 connections) — `src/agy_mas/verification/verifier.py`
- **ArtifactChecker** (14 connections) — `src/agy_mas/verification/artifact_checker.py`
- **AcceptanceChecker** (13 connections) — `src/agy_mas/verification/acceptance_checker.py`
- **ScopeChecker** (12 connections) — `src/agy_mas/verification/scope_checker.py`
- **path_policy.py** (12 connections) — `src/agy_mas/workspace/path_policy.py`
- **artifact_checker.py** (10 connections) — `src/agy_mas/verification/artifact_checker.py`
- **acceptance_checker.py** (9 connections) — `src/agy_mas/verification/acceptance_checker.py`
- **verification/__init__.py** (9 connections) — `src/agy_mas/verification/__init__.py`
- **dataclasses** (5 connections)
- **1. `ArtifactChecker` ([artifact_checker.py](file:///C:/Users/TOAN%20PHUC/Desktop/project/multi-agy-tool/src/agy_mas/verification/artifact_checker.py))** (4 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **.__init__()** (4 connections) — `src/agy_mas/verification/verifier.py`
- **VerificationReport** (3 connections) — `src/agy_mas/verification/verifier.py`
- **.__init__()** (2 connections) — `src/agy_mas/verification/acceptance_checker.py`
- **.__init__()** (2 connections) — `src/agy_mas/verification/artifact_checker.py`
- **.__init__()** (2 connections) — `src/agy_mas/verification/scope_checker.py`
- **Acceptance criteria checker evaluating contract verification rules.** (1 connections) — `src/agy_mas/verification/acceptance_checker.py`
- **Evaluates criteria like EXIT_CODE_ZERO, NO_SOFT_DENIAL, and ARTIFACT_EXISTS.** (1 connections) — `src/agy_mas/verification/acceptance_checker.py`
- **Artifact verification checking file existence, minimum size, and checksums.** (1 connections) — `src/agy_mas/verification/artifact_checker.py`
- **Verifies that deliverables meet declared artifact specifications.** (1 connections) — `src/agy_mas/verification/artifact_checker.py`
- **Verifies that touched paths adhere to task write scopes.** (1 connections) — `src/agy_mas/verification/scope_checker.py`
- **Verification engine enforcing that process success alone cannot accept a task.** (1 connections) — `src/agy_mas/verification/verifier.py`
- **Workspace path security and normalization policy.** (1 connections) — `src/agy_mas/workspace/path_policy.py`
- **Enforces that all file operations are strictly confined within the workspace…** (1 connections) — `src/agy_mas/workspace/path_policy.py`

## Relationships

- [TaskContract](TaskContract.md) (20 shared connections)
- [main.py](main.py.md) (12 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (12 shared connections)
- [Verifier](Verifier.md) (11 shared connections)
- [ResourceRepository](ResourceRepository.md) (8 shared connections)
- [.resolve_safe_path](resolve_safe_path.md) (6 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (3 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (2 shared connections)
- [OwnershipManager](OwnershipManager.md) (2 shared connections)
- [config.py](config.py.md) (1 shared connections)
- [Antigravity Controller & Multi-Agent System (`agy-mas`)](Antigravity_Controller_&_Multi-Agent_System_`agy-mas`.md) (1 shared connections)
- [Orchestrator](Orchestrator.md) (1 shared connections)

## Source Files

- `README.md`
- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/verification/__init__.py`
- `src/agy_mas/verification/acceptance_checker.py`
- `src/agy_mas/verification/artifact_checker.py`
- `src/agy_mas/verification/scope_checker.py`
- `src/agy_mas/verification/verifier.py`
- `src/agy_mas/workspace/path_policy.py`

## Audit Trail

- EXTRACTED: 86 (65%)
- INFERRED: 46 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*