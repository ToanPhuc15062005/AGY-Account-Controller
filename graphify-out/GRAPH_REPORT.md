# Graph Report - multi-agy-tool  (2026-11-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 614 nodes · 1746 edges · 33 communities (9 shown, 24 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 304 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8950f44f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 11
- Community 12
- Community 13
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 24

## God Nodes (most connected - your core abstractions)
1. `Database` - 55 edges
2. `ResourceRepository` - 41 edges
3. `TaskRepository` - 40 edges
4. `TaskContract` - 32 edges
5. `WorkspaceManager` - 26 edges
6. `MigrationRunner` - 26 edges
7. `ExecutionRepository` - 25 edges
8. `EventRepository` - 24 edges
9. `TestWorkspaceCoordination` - 24 edges
10. `QuotaTracker` - 24 edges

## Surprising Connections (you probably didn't know these)
- `TestTaskEngine` --uses--> `InvalidStateTransitionError`  [INFERRED]
  tests/unit/test_task_engine.py → src/agy_mas/core/state_machine.py
- `TestTaskEngine` --uses--> `TaskState`  [INFERRED]
  tests/unit/test_task_engine.py → src/agy_mas/core/state_machine.py
- `TestTaskEngine` --uses--> `TaskStateMachine`  [INFERRED]
  tests/unit/test_task_engine.py → src/agy_mas/core/state_machine.py
- `TestArchitectureV11Acceptance` --uses--> `RecoveryManager`  [INFERRED]
  tests/integration/test_e2e_acceptance.py → src/agy_mas/recovery/recovery_manager.py
- `TestVerificationAndRecovery` --uses--> `RecoveryManager`  [INFERRED]
  tests/unit/test_verification_recovery.py → src/agy_mas/recovery/recovery_manager.py

## Import Cycles
- None detected.

## Communities (33 total, 24 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (13): AgentRuntimeAdapter, Dispatcher, Orchestrator, ScheduleDecision, Scheduler, InvalidStateTransitionError, TaskState, TaskStateMachine (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (14): CycleDetectedError, DependencyGraph, AcceptanceCriterion, ExpectedArtifact, InputScope, OutputScope, PermissionProfile, TaskContract (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (47): build_table_lines(), check_account_status(), cmd_check(), cmd_check_all(), cmd_config(), cmd_current(), cmd_delete(), cmd_install() (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (17): cmd_orchestrate(), cmd_plan(), cmd_project(), cmd_resource(), cmd_run(), cmd_task(), init_mas(), main() (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (7): AcceptanceChecker, ArtifactChecker, ScopeChecker, VerificationReport, Verifier, PathPolicy, PathPolicyError

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (4): windows_file_retry(), decorator(), WindowsFileRetryManager, SnapshotManager

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (5): TerminationResult, IO_COUNTERS, JOBOBJECT_BASIC_LIMIT_INFORMATION, JOBOBJECT_EXTENDED_LIMIT_INFORMATION, ManagedProcess

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (3): AGYAdapter, RuntimeEvent, TestAGYAdapterAndQuota

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (4): WorkspaceConfig, ArtifactRepository, ResourceRepository, WorkspaceManager

## Knowledge Gaps
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Database` connect `Community 21` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 6`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 14`, `Community 15`, `Community 16`, `Community 18`, `Community 19`, `Community 22`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Database` (e.g. with `check_account_status()` and `get_active_workers_info()`) actually correct?**
  _`Database` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.057203956161454156 - nodes in this community are weakly interconnected._
- **Why does `ResourceRepository` connect `Community 11` to `Community 0`, `Community 3`, `Community 4`, `Community 6`, `Community 8`, `Community 9`, `Community 10`, `Community 14`, `Community 16`, `Community 21`, `Community 22`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `ResourceRepository` (e.g. with `Scheduler` and `QuotaTracker`) actually correct?**
  _`ResourceRepository` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05906553041434029 - nodes in this community are weakly interconnected._
- **Why does `TestWorkspaceCoordination` connect `Community 16` to `Community 0`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 11`, `Community 13`, `Community 17`, `Community 19`, `Community 21`, `Community 22`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._