"""Approval repository for human-in-the-loop and permission approvals."""

import datetime
import json
import uuid
from typing import Optional, List, Dict, Any
from ..database import Database


class ApprovalRepository:
    def __init__(self, db: Database):
        self.db = db

    def request_approval(
        self,
        project_id: str,
        requested_action: str,
        resource_scope: str,
        reason: str,
        task_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        approval_type: str = "ACTION",
        requested_payload: Optional[Dict[str, Any]] = None,
        policy_version: Optional[str] = None,
        approval_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        aid = approval_id or f"appr_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        req_json = json.dumps(requested_payload or {})

        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO approvals (
                    approval_id, project_id, task_id, execution_id, requested_action,
                    resource_scope, reason, approval_type, status, requested_payload_json,
                    policy_version, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?, ?);
                """,
                (aid, project_id, task_id, execution_id, requested_action, resource_scope, reason, approval_type, req_json, policy_version, now),
            )

        return self.get(aid)  # type: ignore

    def get(self, approval_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM approvals WHERE approval_id = ?;", (approval_id,))
        if not row:
            return None
        d = dict(row)
        d["requested_payload"] = json.loads(d.get("requested_payload_json") or "{}")
        d["decision_payload"] = json.loads(d.get("decision_payload_json") or "{}") if d.get("decision_payload_json") else None
        return d

    def list_pending(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if project_id:
            rows = self.db.fetchall(
                "SELECT * FROM approvals WHERE status = 'PENDING' AND project_id = ? ORDER BY created_at ASC;",
                (project_id,),
            )
        else:
            rows = self.db.fetchall("SELECT * FROM approvals WHERE status = 'PENDING' ORDER BY created_at ASC;")

        res = []
        for r in rows:
            d = dict(r)
            d["requested_payload"] = json.loads(d.get("requested_payload_json") or "{}")
            d["decision_payload"] = json.loads(d.get("decision_payload_json") or "{}") if d.get("decision_payload_json") else None
            res.append(d)
        return res

    def decide(
        self,
        approval_id: str,
        decision: str,  # "APPROVED" or "REJECTED"
        decided_by: str,
        decision_payload: Optional[Dict[str, Any]] = None,
    ) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        dec_json = json.dumps(decision_payload or {})
        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE approvals
                SET status = ?,
                    decided_by = ?,
                    decision_payload_json = ?,
                    decided_at = ?
                WHERE approval_id = ? AND status = 'PENDING';
                """,
                (decision, decided_by, dec_json, now, approval_id),
            )
            return cur.rowcount > 0
