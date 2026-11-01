# MockAdapter

> 11 nodes · cohesion 0.25

## Key Concepts

- **MockAdapter** (14 connections) — `tests/unit/test_orchestrator.py`
- **RuntimeEvent** (13 connections) — `src/agy_mas/agents/base.py`
- **FailureClassification** (9 connections) — `src/agy_mas/agents/base.py`
- **.classify_failure()** (5 connections) — `src/agy_mas/agents/base.py`
- **.classify_failure()** (3 connections) — `src/agy_mas/agents/adapters/agy_adapter.py`
- **.classify_failure()** (2 connections) — `tests/integration/test_e2e_acceptance.py`
- **.classify_failure()** (2 connections) — `tests/unit/test_orchestrator.py`
- **.parse_line()** (2 connections) — `tests/unit/test_orchestrator.py`
- **Maps process exit and runtime output into the typed error taxonomy.** (1 connections) — `src/agy_mas/agents/base.py`
- **.__init__()** (1 connections) — `tests/unit/test_orchestrator.py`
- **Mock adapter producing predetermined exit codes and messages.** (1 connections) — `tests/unit/test_orchestrator.py`

## Relationships

- [Invocation](Invocation.md) (6 shared connections)
- [main.py](main.py.md) (5 shared connections)
- [RuntimeCapabilities](RuntimeCapabilities.md) (4 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (3 shared connections)
- [orchestrator.py](orchestrator.py.md) (3 shared connections)
- [AGYAdapter](AGYAdapter.md) (2 shared connections)
- [TestAGYAdapterAndQuota](TestAGYAdapterAndQuota.md) (2 shared connections)

## Source Files

- `src/agy_mas/agents/adapters/agy_adapter.py`
- `src/agy_mas/agents/base.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_orchestrator.py`

## Audit Trail

- EXTRACTED: 31 (79%)
- INFERRED: 8 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*