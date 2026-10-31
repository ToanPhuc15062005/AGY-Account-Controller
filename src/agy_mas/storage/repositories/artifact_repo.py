"""Artifact repository for tracking deliverables, logs, and output products."""

import datetime
import json
import uuid
from typing import Optional, List, Dict, Any
from ..database import Database


class ArtifactRepository:
    def __init__(self, db: Database):
        self.db = db

    def register(
        self,
        project_id: str,
        task_id: str,
        execution_id: str,
        path: str,
        artifact_type: str,
        checksum: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        artifact_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        aid = artifact_id or f"art_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        metadata_json = json.dumps(metadata or {})

        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO artifacts (
                    artifact_id, project_id, task_id, execution_id, path,
                    artifact_type, checksum, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (aid, project_id, task_id, execution_id, path, artifact_type, checksum, metadata_json, now),
            )

        return self.get(aid)  # type: ignore

    def get(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM artifacts WHERE artifact_id = ?;", (artifact_id,))
        if not row:
            return None
        d = dict(row)
        d["metadata"] = json.loads(d.get("metadata_json") or "{}")
        return d

    def list_by_task(self, task_id: str) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM artifacts WHERE task_id = ? ORDER BY created_at ASC;", (task_id,))
        res = []
        for r in rows:
            d = dict(r)
            d["metadata"] = json.loads(d.get("metadata_json") or "{}")
            res.append(d)
        return res

    def list_by_execution(self, execution_id: str) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM artifacts WHERE execution_id = ? ORDER BY created_at ASC;", (execution_id,))
        res = []
        for r in rows:
            d = dict(r)
            d["metadata"] = json.loads(d.get("metadata_json") or "{}")
            res.append(d)
        return res
