# QuotaTracker

> God node · 24 connections · `src/agy_mas/resources/quota_tracker.py`

**Community:** [ResourceRepository](ResourceRepository.md)

## Connections by Relation

### calls
- init_mas() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`

### contains
- quota_tracker.py `EXTRACTED`

### imports
- [main.py](main.py.md) `EXTRACTED`
- [orchestrator.py](orchestrator.py.md) `EXTRACTED`
- scheduler.py `EXTRACTED`
- resources/__init__.py `EXTRACTED`

### method
- .is_available() `EXTRACTED`
- .select_eligible_account() `EXTRACTED`
- .__init__() `EXTRACTED`
- .record_quota_exhaustion() `EXTRACTED`
- .clear_cooldown() `EXTRACTED`

### rationale_for
- Manages resource cooldown states scoped to (account_id, model_key). `EXTRACTED`

### references
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [ResourceRepository](ResourceRepository.md) `INFERRED`
- TestArchitectureV11Acceptance `INFERRED`
- Orchestrator `INFERRED`
- [TestAGYAdapterAndQuota](TestAGYAdapterAndQuota.md) `INFERRED`
- Scheduler `INFERRED`
- TestOrchestrator `INFERRED`
- QuotaConfig `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*