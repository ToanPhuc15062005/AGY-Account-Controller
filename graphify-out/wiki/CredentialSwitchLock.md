# CredentialSwitchLock

> 7 nodes · cohesion 0.38

## Key Concepts

- **CredentialSwitchLock** (11 connections) — `src/agy_mas/accounts/credential_provider.py`
- **.acquire()** (2 connections) — `src/agy_mas/accounts/credential_provider.py`
- **.__enter__()** (2 connections) — `src/agy_mas/accounts/credential_provider.py`
- **.__exit__()** (2 connections) — `src/agy_mas/accounts/credential_provider.py`
- **.release()** (2 connections) — `src/agy_mas/accounts/credential_provider.py`
- **.__init__()** (1 connections) — `src/agy_mas/accounts/credential_provider.py`
- **Acquires an atomic cross-process file lock while switching credentials in OS…** (1 connections) — `src/agy_mas/accounts/credential_provider.py`

## Relationships

- [agy_controller.py](agy_controller.py.md) (2 shared connections)
- [ManagedProcess](ManagedProcess.md) (1 shared connections)
- [main.py](main.py.md) (1 shared connections)
- [ResourceRepository](ResourceRepository.md) (1 shared connections)

## Source Files

- `src/agy_mas/accounts/credential_provider.py`

## Audit Trail

- EXTRACTED: 12 (92%)
- INFERRED: 1 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*