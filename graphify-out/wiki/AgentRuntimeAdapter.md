# AgentRuntimeAdapter

> 8 nodes · cohesion 0.25

## Key Concepts

- **AgentRuntimeAdapter** (17 connections) — `src/agy_mas/agents/base.py`
- **.build_invocation()** (5 connections) — `src/agy_mas/agents/base.py`
- **.parse_line()** (4 connections) — `src/agy_mas/agents/base.py`
- **ABC** (2 connections)
- **Any** (1 connections)
- **Abstract contract isolating provider-specific CLI behavior behind adapters.** (1 connections) — `src/agy_mas/agents/base.py`
- **Constructs safe CLI invocation arguments according to task contract and policy.** (1 connections) — `src/agy_mas/agents/base.py`
- **Parses a single stdout/stderr line into a typed RuntimeEvent.** (1 connections) — `src/agy_mas/agents/base.py`

## Relationships

- [orchestrator.py](orchestrator.py.md) (5 shared connections)
- [main.py](main.py.md) (3 shared connections)
- [MockAdapter](MockAdapter.md) (3 shared connections)
- [RuntimeCapabilities](RuntimeCapabilities.md) (2 shared connections)
- [Invocation](Invocation.md) (2 shared connections)
- [EventRepository](EventRepository.md) (1 shared connections)
- [ResourceRepository](ResourceRepository.md) (1 shared connections)
- [AGYAdapter](AGYAdapter.md) (1 shared connections)

## Source Files

- `src/agy_mas/agents/base.py`

## Audit Trail

- EXTRACTED: 22 (88%)
- INFERRED: 3 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*