# Graph Report - multi-agy-tool  (2026-11-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 616 nodes · 1749 edges · 34 communities (10 shown, 24 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 292 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7312f5ca`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- TaskContract
- agy_controller.py
- orchestrator.py
- PathPolicy
- ResourceRepository
- config.py
- MigrationRunner
- process_manager.py
- Database
- MockAdapter
- TaskRepository
- TestStorageLayer
- .snapshot_file
- ExecutionRepository
- AGYAdapter
- Invocation
- AgentRuntimeAdapter
- EventRepository
- .setUp
- ArtifactRepository
- TestAGYAdapterAndQuota
- RuntimeCapabilities
- DummyProcess

## God Nodes (most connected - your core abstractions)
1. `Database` - 55 edges
2. `ResourceRepository` - 41 edges
3. `TaskRepository` - 39 edges
4. `TaskContract` - 32 edges
5. `MigrationRunner` - 26 edges
6. `WorkspaceManager` - 25 edges
7. `ExecutionRepository` - 24 edges
8. `TestWorkspaceCoordination` - 24 edges
9. `QuotaTracker` - 24 edges
10. `EventRepository` - 23 edges

## Surprising Connections (you probably didn't know these)
- `TestArchitectureV11Acceptance` --uses--> `WindowsFileRetryManager`  [INFERRED]
  tests/integration/test_e2e_acceptance.py → src/agy_mas/workspace/file_lock_manager.py
- `TestWorkspaceCoordination` --uses--> `WindowsFileRetryManager`  [INFERRED]
  tests/unit/test_workspace.py → src/agy_mas/workspace/file_lock_manager.py
- `TestWorkspaceCoordination` --uses--> `SnapshotManager`  [INFERRED]
  tests/unit/test_workspace.py → src/agy_mas/workspace/snapshot_manager.py
- `TestWorkspaceCoordination` --uses--> `OwnershipConflictError`  [INFERRED]
  tests/unit/test_workspace.py → src/agy_mas/workspace/ownership_manager.py
- `TestPlanner` --uses--> `PlanValidator`  [INFERRED]
  tests/unit/test_planner.py → src/agy_mas/planning/plan_validator.py

## Import Cycles
- None detected.

## Communities (34 total, 24 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.06
Nodes (11): cmd_orchestrate(), cmd_project(), cmd_resource(), cmd_run(), cmd_task(), main(), windows_file_retry(), decorator() (+3 more)

### Community 1 - "TaskContract"
Cohesion: 0.06
Nodes (15): cmd_plan(), CycleDetectedError, DependencyGraph, AcceptanceCriterion, ExpectedArtifact, InputScope, OutputScope, PermissionProfile (+7 more)

### Community 2 - "agy_controller.py"
Cohesion: 0.07
Nodes (47): build_table_lines(), check_account_status(), cmd_check(), cmd_check_all(), cmd_config(), cmd_current(), cmd_delete(), cmd_install() (+39 more)

### Community 3 - "orchestrator.py"
Cohesion: 0.06
Nodes (11): CredentialSwitchLock, Dispatcher, Orchestrator, ScheduleDecision, Scheduler, InvalidStateTransitionError, TaskState, TaskStateMachine (+3 more)

### Community 4 - "PathPolicy"
Cohesion: 0.10
Nodes (7): AcceptanceChecker, ArtifactChecker, ScopeChecker, VerificationReport, Verifier, PathPolicy, PathPolicyError

### Community 5 - "ResourceRepository"
Cohesion: 0.10
Nodes (5): QuotaTracker, ResourceRepository, OwnershipManager, WorkspaceManager, TestWorkspaceCoordination

### Community 6 - "config.py"
Cohesion: 0.08
Nodes (12): get_active_workers_info(), FailoverConfig, MASConfig, QuotaConfig, QuotaCooldownConfig, QuotaDetectionConfig, RuntimeConfig, StorageConfig (+4 more)

### Community 7 - "MigrationRunner"
Cohesion: 0.15
Nodes (3): MigrationRunner, ProjectRepository, TestPlanner

### Community 8 - "process_manager.py"
Cohesion: 0.14
Nodes (5): TerminationResult, IO_COUNTERS, JOBOBJECT_BASIC_LIMIT_INFORMATION, JOBOBJECT_EXTENDED_LIMIT_INFORMATION, ManagedProcess

### Community 10 - "MockAdapter"
Cohesion: 0.25
Nodes (3): FailureClassification, RuntimeEvent, MockAdapter

## Knowledge Gaps
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Database` connect `Database` to `main.py`, `TaskContract`, `agy_controller.py`, `orchestrator.py`, `ResourceRepository`, `config.py`, `MigrationRunner`, `TaskRepository`, `TestStorageLayer`, `ExecutionRepository`, `.transaction`, `EventRepository`, `.setUp`, `.fetchone`, `ArtifactRepository`, `TestAGYAdapterAndQuota`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Database` (e.g. with `check_account_status()` and `get_active_workers_info()`) actually correct?**
  _`Database` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06210670314637483 - nodes in this community are weakly interconnected._
- **Why does `ResourceRepository` connect `ResourceRepository` to `main.py`, `orchestrator.py`, `MigrationRunner`, `Database`, `.transaction`, `EventRepository`, `.setUp`, `.fetchone`, `TestAGYAdapterAndQuota`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `ResourceRepository` (e.g. with `Scheduler` and `QuotaTracker`) actually correct?**
  _`ResourceRepository` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `TaskContract` be split into smaller, more focused modules?**
  _Cohesion score 0.05847781369379959 - nodes in this community are weakly interconnected._
- **Why does `TestWorkspaceCoordination` connect `ResourceRepository` to `main.py`, `PathPolicy`, `config.py`, `MigrationRunner`, `Database`, `TaskRepository`, `.snapshot_file`, `ExecutionRepository`, `ArtifactRepository`, `DummyProcess`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._