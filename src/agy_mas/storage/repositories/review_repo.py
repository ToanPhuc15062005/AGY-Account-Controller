"""Review repository for persisting task critique reports and pair-programming rounds."""

import datetime
import json
import uuid
from typing import Optional, List, Dict, Any
from ..database import Database


class ReviewRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(
        self,
        task_id: str,
        execution_id: str,
        round_number: int,
        verdict: str,
        score: int,
        critique: Dict[str, Any],
        test_output: Optional[str] = None,
        review_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        rid = review_id or f"rev_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        critique_json = json.dumps(critique)

        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO task_reviews (
                    review_id, task_id, execution_id, round_number,
                    verdict, score, critique_json, test_output, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (rid, task_id, execution_id, round_number, verdict, score, critique_json, test_output, now),
            )

        return self.get(rid)  # type: ignore

    def get(self, review_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM task_reviews WHERE review_id = ?;", (review_id,))
        if not row:
            return None
        d = dict(row)
        d["critique"] = json.loads(d.get("critique_json") or "{}")
        return d

    def list_by_task(self, task_id: str) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM task_reviews WHERE task_id = ? ORDER BY round_number ASC, created_at ASC;",
            (task_id,),
        )
        res = []
        for r in rows:
            d = dict(r)
            d["critique"] = json.loads(d.get("critique_json") or "{}")
            res.append(d)
        return res

    def get_latest_for_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM task_reviews WHERE task_id = ? ORDER BY round_number DESC, created_at DESC LIMIT 1;",
            (task_id,),
        )
        if not row:
            return None
        d = dict(row)
        d["critique"] = json.loads(d.get("critique_json") or "{}")
        return d
