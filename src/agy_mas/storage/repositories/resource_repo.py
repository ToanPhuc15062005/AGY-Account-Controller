"""Resource repository for locks, file ownerships, and account-model quotas."""

import datetime
from typing import Optional, List, Dict, Any
from ..database import Database


class ResourceRepository:
    def __init__(self, db: Database):
        self.db = db

    # -------------------------------------------------------------
    # Account Model Resources (v1.1)
    # -------------------------------------------------------------
    def set_account_model_cooldown(
        self,
        account_id: str,
        model_key: str,
        cooldown_until: str,
        cooldown_reason: str,
        cooldown_source: str = "structured",
        retry_after_seconds: Optional[int] = None,
        last_error_code: Optional[str] = None,
        confidence: float = 1.0,
    ) -> None:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO account_model_resources (
                    account_id, model_key, resource_state, cooldown_until,
                    cooldown_reason, cooldown_source, retry_after_seconds,
                    last_quota_observed_at, last_error_code, confidence, updated_at
                ) VALUES (?, ?, 'COOLDOWN', ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(account_id, model_key) DO UPDATE SET
                    resource_state = 'COOLDOWN',
                    cooldown_until = excluded.cooldown_until,
                    cooldown_reason = excluded.cooldown_reason,
                    cooldown_source = excluded.cooldown_source,
                    retry_after_seconds = excluded.retry_after_seconds,
                    last_quota_observed_at = excluded.last_quota_observed_at,
                    last_error_code = excluded.last_error_code,
                    confidence = excluded.confidence,
                    updated_at = excluded.updated_at;
                """,
                (
                    account_id, model_key, cooldown_until, cooldown_reason,
                    cooldown_source, retry_after_seconds, now, last_error_code,
                    confidence, now
                ),
            )

    def clear_account_model_cooldown(self, account_id: str, model_key: str) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE account_model_resources
                SET resource_state = 'AVAILABLE',
                    cooldown_until = NULL,
                    updated_at = ?
                WHERE account_id = ? AND model_key = ?;
                """,
                (now, account_id, model_key),
            )
            return cur.rowcount > 0

    def get_account_model_resource(self, account_id: str, model_key: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM account_model_resources WHERE account_id = ? AND model_key = ?;",
            (account_id, model_key),
        )
        return dict(row) if row else None

    def is_in_cooldown(self, account_id: str, model_key: str) -> bool:
        res = self.get_account_model_resource(account_id, model_key)
        if not res or res.get("resource_state") != "COOLDOWN":
            return False

        cooldown_until = res.get("cooldown_until")
        if not cooldown_until:
            return False

        try:
            until_dt = datetime.datetime.fromisoformat(cooldown_until)
            now_dt = datetime.datetime.now(datetime.timezone.utc)
            if now_dt < until_dt:
                return True
            else:
                # Expired cooldown; reset state lazily
                self.clear_account_model_cooldown(account_id, model_key)
                return False
        except Exception:
            return False

    def list_account_model_resources(self) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM account_model_resources ORDER BY account_id, model_key;")
        return [dict(r) for r in rows]

    # -------------------------------------------------------------
    # Resource Locks
    # -------------------------------------------------------------
    def acquire_lock(
        self,
        lock_id: str,
        resource_type: str,
        resource_key: str,
        owner_execution_id: str,
        expires_at: str,
        lease_version: int = 1,
    ) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            # Check if active unexpired lock exists
            existing = conn.execute(
                "SELECT * FROM resource_locks WHERE resource_type = ? AND resource_key = ?;",
                (resource_type, resource_key),
            ).fetchone()

            if existing:
                # If expired, replace it
                if existing["expires_at"] < now:
                    conn.execute(
                        """
                        UPDATE resource_locks
                        SET lock_id = ?, owner_execution_id = ?, lease_version = ?,
                            acquired_at = ?, expires_at = ?
                        WHERE resource_type = ? AND resource_key = ?;
                        """,
                        (lock_id, owner_execution_id, lease_version, now, expires_at, resource_type, resource_key),
                    )
                    return True
                return False

            conn.execute(
                """
                INSERT INTO resource_locks (lock_id, resource_type, resource_key, owner_execution_id, lease_version, acquired_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (lock_id, resource_type, resource_key, owner_execution_id, lease_version, now, expires_at),
            )
            return True

    def release_lock(self, lock_id: str, owner_execution_id: Optional[str] = None) -> bool:
        with self.db.transaction() as conn:
            if owner_execution_id:
                cur = conn.execute(
                    "DELETE FROM resource_locks WHERE lock_id = ? AND owner_execution_id = ?;",
                    (lock_id, owner_execution_id),
                )
            else:
                cur = conn.execute("DELETE FROM resource_locks WHERE lock_id = ?;", (lock_id,))
            return cur.rowcount > 0

    def get_lock(self, resource_type: str, resource_key: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM resource_locks WHERE resource_type = ? AND resource_key = ?;",
            (resource_type, resource_key),
        )
        return dict(row) if row else None

    # -------------------------------------------------------------
    # File Ownerships
    # -------------------------------------------------------------
    def claim_file_ownership(
        self,
        ownership_id: str,
        project_id: str,
        path_pattern: str,
        access_mode: str,
        owner_execution_id: str,
        expires_at: str,
        lease_version: int = 1,
    ) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO file_ownerships (
                    ownership_id, project_id, path_pattern, access_mode,
                    owner_execution_id, lease_version, acquired_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (ownership_id, project_id, path_pattern, access_mode, owner_execution_id, lease_version, now, expires_at),
            )
            return True

    def release_file_ownership(self, ownership_id: str) -> bool:
        with self.db.transaction() as conn:
            cur = conn.execute("DELETE FROM file_ownerships WHERE ownership_id = ?;", (ownership_id,))
            return cur.rowcount > 0

    def release_all_for_execution(self, owner_execution_id: str) -> None:
        with self.db.transaction() as conn:
            conn.execute("DELETE FROM resource_locks WHERE owner_execution_id = ?;", (owner_execution_id,))
            conn.execute("DELETE FROM file_ownerships WHERE owner_execution_id = ?;", (owner_execution_id,))
