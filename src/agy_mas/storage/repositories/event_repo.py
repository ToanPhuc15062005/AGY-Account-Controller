"""Event repository for append-only project event log."""

import datetime
import json
import uuid
from typing import Optional, List, Dict, Any
from ..database import Database


class EventRepository:
    def __init__(self, db: Database):
        self.db = db

    def append(
        self,
        project_id: str,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        event_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        eid = event_id or f"evt_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        payload_json = json.dumps(payload or {})

        with self.db.transaction() as conn:
            # Atomic sequence increment per project
            row = conn.execute(
                "SELECT COALESCE(MAX(sequence), 0) + 1 AS next_seq FROM events WHERE project_id = ?;",
                (project_id,),
            ).fetchone()
            seq = row["next_seq"] if row else 1

            conn.execute(
                """
                INSERT INTO events (event_id, project_id, task_id, execution_id, event_type, sequence, timestamp, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (eid, project_id, task_id, execution_id, event_type, seq, now, payload_json),
            )

        return {
            "event_id": eid,
            "project_id": project_id,
            "task_id": task_id,
            "execution_id": execution_id,
            "event_type": event_type,
            "sequence": seq,
            "timestamp": now,
            "payload": payload or {},
        }

    def list_by_project(self, project_id: str, after_sequence: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """
            SELECT * FROM events
            WHERE project_id = ? AND sequence > ?
            ORDER BY sequence ASC
            LIMIT ?;
            """,
            (project_id, after_sequence, limit),
        )
        res = []
        for r in rows:
            d = dict(r)
            d["payload"] = json.loads(d.get("payload_json") or "{}")
            res.append(d)
        return res
