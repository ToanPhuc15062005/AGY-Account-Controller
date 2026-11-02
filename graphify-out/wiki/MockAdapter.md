# MockAdapter

> 12 nodes · cohesion 0.18

## Key Concepts

- **MockAdapter** (16 connections) — `tests/unit/test_orchestrator.py`
- **FailureClassification** (13 connections) — `src/agy_mas/agents/base.py`
- **.classify_failure()** (5 connections) — `src/agy_mas/agents/base.py`
- **.classify_failure()** (2 connections) — `tests/integration/test_e2e_acceptance.py`
- **.build_invocation()** (2 connections) — `tests/unit/test_orchestrator.py`
- **.classify_failure()** (2 connections) — `tests/unit/test_orchestrator.py`
- **.parse_line()** (2 connections) — `tests/unit/test_orchestrator.py`
- **.validate_runtime()** (2 connections) — `tests/unit/test_orchestrator.py`
- **.classify_failure()** (2 connections) — `tests/unit/test_pair_programming.py`
- **Maps process exit and runtime output into the typed error taxonomy.** (1 connections) — `src/agy_mas/agents/base.py`
- **.__init__()** (1 connections) — `tests/unit/test_orchestrator.py`
- **Mock adapter producing predetermined exit codes and messages.** (1 connections) — `tests/unit/test_orchestrator.py`

## Relationships

- [AGYAdapter](AGYAdapter.md) (6 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (5 shared connections)
- [Orchestrator](Orchestrator.md) (4 shared connections)
- [RuntimeCapabilities](RuntimeCapabilities.md) (4 shared connections)
- [Invocation](Invocation.md) (4 shared connections)
- [main.py](main.py.md) (1 shared connections)
- [3. CÁC DESIGN PATTERNS CỐT LÕI](3._CÁC_DESIGN_PATTERNS_CỐT_LÕI.md) (1 shared connections)

## Source Files

- `src/agy_mas/agents/base.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_orchestrator.py`
- `tests/unit/test_pair_programming.py`

## Audit Trail

- EXTRACTED: 27 (73%)
- INFERRED: 10 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*