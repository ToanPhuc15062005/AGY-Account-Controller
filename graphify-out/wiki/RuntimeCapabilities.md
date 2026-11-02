# RuntimeCapabilities

> 12 nodes · cohesion 0.18

## Key Concepts

- **RuntimeCapabilities** (13 connections) — `src/agy_mas/agents/base.py`
- **ConfigurableTestAdapter** (12 connections) — `tests/integration/test_e2e_acceptance.py`
- **.validate_runtime()** (3 connections) — `src/agy_mas/agents/adapters/agy_adapter.py`
- **.validate_runtime()** (3 connections) — `src/agy_mas/agents/base.py`
- **.build_invocation()** (2 connections) — `tests/integration/test_e2e_acceptance.py`
- **.parse_line()** (2 connections) — `tests/integration/test_e2e_acceptance.py`
- **.validate_runtime()** (2 connections) — `tests/integration/test_e2e_acceptance.py`
- **.validate_runtime()** (2 connections) — `tests/unit/test_pair_programming.py`
- **Probes agy executable and determines version and capabilities.** (1 connections) — `src/agy_mas/agents/adapters/agy_adapter.py`
- **Validates runtime CLI availability, version, and supported flags.** (1 connections) — `src/agy_mas/agents/base.py`
- **.__init__()** (1 connections) — `tests/integration/test_e2e_acceptance.py`
- **Adapter with controllable execution outcomes for acceptance testing.** (1 connections) — `tests/integration/test_e2e_acceptance.py`

## Relationships

- [AGYAdapter](AGYAdapter.md) (5 shared connections)
- [AgentRuntimeAdapter](AgentRuntimeAdapter.md) (5 shared connections)
- [MockAdapter](MockAdapter.md) (4 shared connections)
- [Invocation](Invocation.md) (4 shared connections)
- [main.py](main.py.md) (1 shared connections)

## Source Files

- `src/agy_mas/agents/adapters/agy_adapter.py`
- `src/agy_mas/agents/base.py`
- `tests/integration/test_e2e_acceptance.py`
- `tests/unit/test_pair_programming.py`

## Audit Trail

- EXTRACTED: 23 (74%)
- INFERRED: 8 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*