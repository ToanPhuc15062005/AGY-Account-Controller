# ResourceRepository

> God node · 41 connections · `src/agy_mas/storage/repositories/resource_repo.py`

**Community:** [Community 11](Community_11.md)

## Connections by Relation

### calls
- init_mas() `EXTRACTED`
- .setUp() `INFERRED`
- .setUp() `EXTRACTED`
- .setUp() `INFERRED`
- .setUp() `INFERRED`
- .setUp() `INFERRED`
- .setUp() `EXTRACTED`

### contains
- resource_repo.py `EXTRACTED`

### imports
- main.py `EXTRACTED`
- orchestrator.py `EXTRACTED`
- workspace_manager.py `EXTRACTED`
- repositories/__init__.py `EXTRACTED`
- scheduler.py `EXTRACTED`
- recovery_manager.py `EXTRACTED`
- quota_tracker.py `EXTRACTED`
- ownership_manager.py `EXTRACTED`

### method
- .release_all_for_execution() `EXTRACTED`
- .clear_account_model_cooldown() `EXTRACTED`
- .get_account_model_resource() `EXTRACTED`
- .is_in_cooldown() `EXTRACTED`
- .set_account_model_cooldown() `EXTRACTED`
- .get_lock() `EXTRACTED`
- .claim_file_ownership() `EXTRACTED`
- .list_account_model_resources() `EXTRACTED`
- .acquire_lock() `EXTRACTED`
- .release_lock() `EXTRACTED`
- .release_file_ownership() `EXTRACTED`
- .__init__() `EXTRACTED`

### references
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [Database](Database.md) `INFERRED`
- [WorkspaceManager](WorkspaceManager.md) `INFERRED`
- [QuotaTracker](QuotaTracker.md) `INFERRED`
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) `INFERRED`
- TestAGYAdapterAndQuota `INFERRED`
- Scheduler `INFERRED`
- OwnershipManager `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*