# TaskRepository

> God node · 39 connections · `src/agy_mas/storage/repositories/task_repo.py`

**Community:** [TaskRepository](TaskRepository.md)

## Connections by Relation

### calls
- init_mas() `EXTRACTED`
- .setUp() `INFERRED`
- .setUp() `EXTRACTED`
- .setUp() `INFERRED`
- .setUp() `INFERRED`
- .setUp() `INFERRED`
- .setUp() `EXTRACTED`
- .setUp() `EXTRACTED`

### contains
- task_repo.py `EXTRACTED`

### imports
- [main.py](main.py.md) `EXTRACTED`
- [orchestrator.py](orchestrator.py.md) `EXTRACTED`
- dispatcher.py `EXTRACTED`
- planner.py `EXTRACTED`
- repositories/__init__.py `EXTRACTED`
- scheduler.py `EXTRACTED`
- recovery_manager.py `EXTRACTED`
- state_machine.py `EXTRACTED`

### method
- .get() `EXTRACTED`
- .list_by_project() `EXTRACTED`
- .create() `EXTRACTED`
- .get_dependencies() `EXTRACTED`
- .update_status() `EXTRACTED`
- .__init__() `EXTRACTED`
- .get_dependents() `EXTRACTED`
- .get_dependency_map() `EXTRACTED`
- .add_dependency() `EXTRACTED`

### references
- .transition() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`
- .__init__() `EXTRACTED`

### uses
- [Database](Database.md) `INFERRED`
- [TestWorkspaceCoordination](TestWorkspaceCoordination.md) `INFERRED`
- TestTaskEngine `INFERRED`
- Planner `INFERRED`
- TaskStateMachine `INFERRED`
- Scheduler `INFERRED`
- TestPlanner `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*