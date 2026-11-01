"""Task repository for persisting tasks and DAG dependencies."""

import datetime
import json
from typing import Optional, List, Dict, Any
from ..database import Database


class TaskRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(
        self,
        task_id: str,
        project_id: str,
        title: str,
        description: str,
        domain: Optional[str] = None,
        role: Optional[str] = None,
        priority: int = 50,
        status: str = "PENDING",
        task_spec: Optional[Dict[str, Any]] = None,
        depends_on: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        task_json = json.dumps(task_spec or {})

        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO tasks (
                    task_id, project_id, title, description, domain, role,
                    priority, status, task_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (task_id, project_id, title, description, domain, role, priority, status, task_json, now, now),
            )

            if depends_on:
                for dep_id in set(depends_on):
                    if dep_id != task_id:
                        conn.execute(
                            "INSERT OR IGNORE INTO task_dependencies (task_id, depends_on_task_id) VALUES (?, ?);",
                            (task_id, dep_id),
                        )

        return self.get(task_id)  # type: ignore

    def get(self, task_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM tasks WHERE task_id = ?;", (task_id,))
        if not row:
            return None
        d = dict(row)
        d["task_spec"] = json.loads(d.get("task_json") or "{}")
        d["dependencies"] = self.get_dependencies(task_id)
        if d.get("last_critique_json"):
            try:
                d["last_critique"] = json.loads(d["last_critique_json"])
            except Exception:
                d["last_critique"] = None
        else:
            d["last_critique"] = None
        return d

    def list_by_project(self, project_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            rows = self.db.fetchall(
                "SELECT * FROM tasks WHERE project_id = ? AND status = ? ORDER BY priority DESC, created_at ASC;",
                (project_id, status),
            )
        else:
            rows = self.db.fetchall(
                "SELECT * FROM tasks WHERE project_id = ? ORDER BY priority DESC, created_at ASC;",
                (project_id,),
            )

        res = []
        for r in rows:
            d = dict(r)
            d["task_spec"] = json.loads(d.get("task_json") or "{}")
            d["dependencies"] = self.get_dependencies(d["task_id"])
            if d.get("last_critique_json"):
                try:
                    d["last_critique"] = json.loads(d["last_critique_json"])
                except Exception:
                    d["last_critique"] = None
            else:
                d["last_critique"] = None
            res.append(d)
        return res

    def update_critique(self, task_id: str, critique_dict: Dict[str, Any], pair_round: int) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        critique_json = json.dumps(critique_dict)
        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE tasks
                SET pair_round = ?, last_critique_json = ?, updated_at = ?
                WHERE task_id = ?;
                """,
                (pair_round, critique_json, now, task_id),
            )
            return cur.rowcount > 0

    def update_status(self, task_id: str, status: str) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            cur = conn.execute(
                "UPDATE tasks SET status = ?, updated_at = ? WHERE task_id = ?;",
                (status, now, task_id),
            )
            return cur.rowcount > 0

    def add_dependency(self, task_id: str, depends_on_task_id: str) -> bool:
        if task_id == depends_on_task_id:
            raise ValueError(f"Self-dependency is invalid: {task_id}")
        with self.db.transaction() as conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO task_dependencies (task_id, depends_on_task_id) VALUES (?, ?);",
                (task_id, depends_on_task_id),
            )
            return cur.rowcount > 0

    def get_dependencies(self, task_id: str) -> List[str]:
        rows = self.db.fetchall(
            "SELECT depends_on_task_id FROM task_dependencies WHERE task_id = ? ORDER BY depends_on_task_id;",
            (task_id,),
        )
        return [r["depends_on_task_id"] for r in rows]

    def get_dependents(self, task_id: str) -> List[str]:
        rows = self.db.fetchall(
            "SELECT task_id FROM task_dependencies WHERE depends_on_task_id = ? ORDER BY task_id;",
            (task_id,),
        )
        return [r["task_id"] for r in rows]

    def get_dependency_map(self, project_id: str) -> Dict[str, List[str]]:
        rows = self.db.fetchall(
            """
            SELECT td.task_id, td.depends_on_task_id
            FROM task_dependencies td
            JOIN tasks t ON td.task_id = t.task_id
            WHERE t.project_id = ?;
            """,
            (project_id,),
        )
        dep_map: Dict[str, List[str]] = {}
        for r in rows:
            dep_map.setdefault(r["task_id"], []).append(r["depends_on_task_id"])
        return dep_map
