# Verifier

> 7 nodes · cohesion 0.38

## Key Concepts

- **Verifier** (26 connections) — `src/agy_mas/verification/verifier.py`
- **.verify_task()** (10 connections) — `src/agy_mas/verification/verifier.py`
- **Lab 3: Thiết lập Pipeline Xác minh cho Tác vụ Sinh Code** (4 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **5.3. Verification Engine: Thực thi ADR-014 và ADR-017** (3 connections) — `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- **.allows_write()** (3 connections) — `src/agy_mas/planning/plan_schema.py`
- **.check_paths()** (3 connections) — `src/agy_mas/verification/scope_checker.py`
- **Orchestrates comprehensive task verification according to ADR-014 and ADR-017.** (1 connections) — `src/agy_mas/verification/verifier.py`

## Relationships

- [PathPolicy](PathPolicy.md) (11 shared connections)
- [TaskContract](TaskContract.md) (8 shared connections)
- [ReviewEngine](ReviewEngine.md) (4 shared connections)
- [Module 03: Agents Runtime, Workspace Management & Process Isolation trên Windows](Module_03-_Agents_Runtime,_Workspace_Management_&_Process_Isolation_trên_Windows.md) (2 shared connections)
- [ResourceRepository](ResourceRepository.md) (2 shared connections)
- [Database](Database.md) (2 shared connections)
- [OwnershipManager](OwnershipManager.md) (2 shared connections)
- [.resolve_safe_path](resolve_safe_path.md) (2 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (1 shared connections)

## Source Files

- `docs/study_guide/03_agents_workspace_and_process_isolation.md`
- `src/agy_mas/planning/plan_schema.py`
- `src/agy_mas/verification/scope_checker.py`
- `src/agy_mas/verification/verifier.py`

## Audit Trail

- EXTRACTED: 17 (40%)
- INFERRED: 25 (60%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*