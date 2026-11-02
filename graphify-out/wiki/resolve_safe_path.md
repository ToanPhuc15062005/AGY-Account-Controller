# .resolve_safe_path

> 11 nodes · cohesion 0.20

## Key Concepts

- **.resolve_safe_path()** (9 connections) — `src/agy_mas/workspace/path_policy.py`
- **PathPolicyError** (8 connections) — `src/agy_mas/workspace/path_policy.py`
- **.get_relative_path()** (5 connections) — `src/agy_mas/workspace/path_policy.py`
- **.evaluate()** (4 connections) — `src/agy_mas/verification/acceptance_checker.py`
- **.check_artifacts()** (4 connections) — `src/agy_mas/verification/artifact_checker.py`
- **Path** (3 connections)
- **.__init__()** (2 connections) — `src/agy_mas/workspace/path_policy.py`
- **ValueError** (1 connections)
- **Resolves path and verifies it resides inside the workspace root without…** (1 connections) — `src/agy_mas/workspace/path_policy.py`
- **Returns clean forward-slash relative path within workspace.** (1 connections) — `src/agy_mas/workspace/path_policy.py`
- **Raised when an unsafe path attempts to escape the workspace root.** (1 connections) — `src/agy_mas/workspace/path_policy.py`

## Relationships

- [PathPolicy](PathPolicy.md) (6 shared connections)
- [TaskContract](TaskContract.md) (3 shared connections)
- [.snapshot_file](snapshot_file.md) (3 shared connections)
- [Verifier](Verifier.md) (2 shared connections)
- [WindowsFileRetryManager](WindowsFileRetryManager.md) (2 shared connections)
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) (1 shared connections)

## Source Files

- `src/agy_mas/verification/acceptance_checker.py`
- `src/agy_mas/verification/artifact_checker.py`
- `src/agy_mas/workspace/path_policy.py`

## Audit Trail

- EXTRACTED: 18 (64%)
- INFERRED: 10 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*