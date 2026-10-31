"""Execution repository for recording immutable agent execution attempts."""

import datetime
import json
from typing import Optional, List, Dict, Any
from ..database import Database


class ExecutionRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(
        self,
        execution_id: str,
        task_id: str,
        runtime_type: str,
        agent_id: Optional[str] = None,
        account_id: Optional[str] = None,
        model: Optional[str] = None,
        status: str = "PENDING",
        lease_version: int = 1,
        metadata: Optional[Dict[str, Any]] = None,
        runtime_name: Optional[str] = None,
        runtime_version: Optional[str] = None,
        agent_print_timeout_seconds: Optional[int] = None,
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        metadata_json = json.dumps(metadata or {})

        with self.db.transaction() as conn:
            # Determine next attempt number atomically
            row = conn.execute(
                "SELECT COALESCE(MAX(attempt), 0) + 1 AS next_attempt FROM executions WHERE task_id = ?;",
                (task_id,),
            ).fetchone()
            attempt = row["next_attempt"] if row else 1

            conn.execute(
                """
                INSERT INTO executions (
                    execution_id, task_id, attempt, agent_id, runtime_type,
                    account_id, model, status, lease_version, started_at,
                    metadata_json, runtime_name, runtime_version, agent_print_timeout_seconds
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    execution_id, task_id, attempt, agent_id, runtime_type,
                    account_id, model, status, lease_version, now,
                    metadata_json, runtime_name, runtime_version, agent_print_timeout_seconds
                ),
            )

        return self.get(execution_id)  # type: ignore

    def get(self, execution_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM executions WHERE execution_id = ?;", (execution_id,))
        if not row:
            return None
        d = dict(row)
        d["metadata"] = json.loads(d.get("metadata_json") or "{}")
        return d

    def get_latest_for_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM executions WHERE task_id = ? ORDER BY attempt DESC LIMIT 1;",
            (task_id,),
        )
        if not row:
            return None
        d = dict(row)
        d["metadata"] = json.loads(d.get("metadata_json") or "{}")
        return d

    def list_by_task(self, task_id: str) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM executions WHERE task_id = ? ORDER BY attempt ASC;",
            (task_id,),
        )
        res = []
        for r in rows:
            d = dict(r)
            d["metadata"] = json.loads(d.get("metadata_json") or "{}")
            res.append(d)
        return res

    def mark_process_started(
        self,
        execution_id: str,
        pid: int,
        command_fingerprint: Optional[str] = None,
        process_creation_time: Optional[str] = None,
    ) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE executions
                SET status = 'RUNNING',
                    process_id = ?,
                    pid = ?,
                    process_started_at = ?,
                    process_creation_time = ?,
                    command_fingerprint = ?
                WHERE execution_id = ?;
                """,
                (pid, pid, now, process_creation_time or now, command_fingerprint, execution_id),
            )
            return cur.rowcount > 0

    def mark_completed(
        self,
        execution_id: str,
        status: str,
        exit_code: Optional[int] = None,
        normalized_outcome: Optional[str] = None,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None,
        termination_reason: Optional[str] = None,
        metadata_update: Optional[Dict[str, Any]] = None,
    ) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        existing = self.get(execution_id)
        if not existing:
            return False

        meta = existing.get("metadata", {})
        if metadata_update:
            meta.update(metadata_update)

        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE executions
                SET status = ?,
                    finished_at = ?,
                    exit_code = ?,
                    normalized_outcome = ?,
                    error_type = ?,
                    error_message = ?,
                    termination_reason = ?,
                    metadata_json = ?
                WHERE execution_id = ?;
                """,
                (
                    status,
                    now,
                    exit_code,
                    normalized_outcome,
                    error_type,
                    error_message,
                    termination_reason,
                    json.dumps(meta),
                    execution_id,
                ),
            )
            return cur.rowcount > 0
