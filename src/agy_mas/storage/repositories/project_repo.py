"""Project repository for persisting multi-agent projects."""

import datetime
import json
from typing import Optional, List, Dict, Any
from ..database import Database


class ProjectRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(
        self,
        project_id: str,
        name: str,
        goal: str,
        workspace_root: str,
        status: str = "CREATED",
        policy: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        policy_json = json.dumps(policy or {})

        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO projects (project_id, name, goal, workspace_root, status, policy_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (project_id, name, goal, workspace_root, status, policy_json, now, now),
            )

        return self.get(project_id)  # type: ignore

    def get(self, project_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM projects WHERE project_id = ?;", (project_id,))
        if not row:
            return None
        d = dict(row)
        d["policy"] = json.loads(d.get("policy_json") or "{}")
        return d

    def list_all(self) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM projects ORDER BY created_at DESC;")
        res = []
        for r in rows:
            d = dict(r)
            d["policy"] = json.loads(d.get("policy_json") or "{}")
            res.append(d)
        return res

    def update_status(self, project_id: str, status: str) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            cur = conn.execute(
                "UPDATE projects SET status = ?, updated_at = ? WHERE project_id = ?;",
                (status, now, project_id),
            )
            return cur.rowcount > 0
