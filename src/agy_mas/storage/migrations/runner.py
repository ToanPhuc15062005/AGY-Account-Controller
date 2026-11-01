"""SQLite migration runner for AGY-MAS, applying schema v1.0 and v1.1 additions."""

import datetime
from typing import List, Set
from ..database import Database


class MigrationRunner:
    """Manages idempotent schema setup and progressive migrations for AGY-MAS."""

    def __init__(self, db: Database):
        self.db = db

    def run_all(self) -> List[str]:
        """Runs all pending migrations in order and returns applied migration names."""
        applied: List[str] = []
        with self.db.transaction() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TEXT NOT NULL
                );
            """)

            existing_versions = {
                row["version"] for row in conn.execute("SELECT version FROM schema_migrations;").fetchall()
            }

            if 1 not in existing_versions:
                self._apply_v1_0_baseline(conn)
                conn.execute(
                    "INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?);",
                    (1, "001_baseline_v1.0", datetime.datetime.now(datetime.timezone.utc).isoformat())
                )
                applied.append("001_baseline_v1.0")

            if 2 not in existing_versions:
                self._apply_v1_1_additions(conn)
                conn.execute(
                    "INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?);",
                    (2, "002_additions_v1.1", datetime.datetime.now(datetime.timezone.utc).isoformat())
                )
                applied.append("002_additions_v1.1")

            if 3 not in existing_versions:
                self._apply_v1_2_pair_programming(conn)
                conn.execute(
                    "INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?);",
                    (3, "003_pair_programming_v1.2", datetime.datetime.now(datetime.timezone.utc).isoformat())
                )
                applied.append("003_pair_programming_v1.2")

        return applied

    def _apply_v1_0_baseline(self, conn) -> None:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                goal TEXT NOT NULL,
                workspace_root TEXT NOT NULL,
                status TEXT NOT NULL,
                policy_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                domain TEXT,
                role TEXT,
                priority INTEGER NOT NULL DEFAULT 50,
                status TEXT NOT NULL,
                task_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );

            CREATE TABLE IF NOT EXISTS task_dependencies (
                task_id TEXT NOT NULL,
                depends_on_task_id TEXT NOT NULL,
                PRIMARY KEY (task_id, depends_on_task_id),
                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (depends_on_task_id) REFERENCES tasks(task_id),
                CHECK (task_id <> depends_on_task_id)
            );

            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                runtime_type TEXT NOT NULL,
                display_name TEXT NOT NULL,
                capabilities_json TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS executions (
                execution_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                attempt INTEGER NOT NULL,
                agent_id TEXT,
                runtime_type TEXT NOT NULL,
                account_id TEXT,
                model TEXT,
                status TEXT NOT NULL,
                process_id INTEGER,
                process_started_at TEXT,
                command_fingerprint TEXT,
                started_at TEXT,
                finished_at TEXT,
                exit_code INTEGER,
                lease_version INTEGER NOT NULL DEFAULT 1,
                error_type TEXT,
                error_message TEXT,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
                UNIQUE (task_id, attempt)
            );

            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                execution_id TEXT NOT NULL,
                path TEXT NOT NULL,
                artifact_type TEXT NOT NULL,
                checksum TEXT,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id),
                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
            );

            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                task_id TEXT,
                execution_id TEXT,
                event_type TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id),
                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
                UNIQUE (project_id, sequence)
            );

            CREATE TABLE IF NOT EXISTS resource_locks (
                lock_id TEXT PRIMARY KEY,
                resource_type TEXT NOT NULL,
                resource_key TEXT NOT NULL,
                owner_execution_id TEXT NOT NULL,
                lease_version INTEGER NOT NULL,
                acquired_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (owner_execution_id) REFERENCES executions(execution_id),
                UNIQUE (resource_type, resource_key)
            );

            CREATE TABLE IF NOT EXISTS file_ownerships (
                ownership_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                path_pattern TEXT NOT NULL,
                access_mode TEXT NOT NULL,
                owner_execution_id TEXT NOT NULL,
                lease_version INTEGER NOT NULL,
                acquired_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id),
                FOREIGN KEY (owner_execution_id) REFERENCES executions(execution_id)
            );

            CREATE TABLE IF NOT EXISTS account_resources (
                account_id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                status TEXT NOT NULL,
                capacity INTEGER NOT NULL DEFAULT 1,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS approvals (
                approval_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                task_id TEXT,
                execution_id TEXT,
                requested_action TEXT,
                resource_scope TEXT,
                reason TEXT,
                approval_type TEXT NOT NULL DEFAULT 'ACTION',
                status TEXT NOT NULL,
                requested_payload_json TEXT NOT NULL DEFAULT '{}',
                decision_payload_json TEXT,
                policy_version TEXT,
                decided_by TEXT,
                created_at TEXT NOT NULL,
                decided_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(project_id),
                FOREIGN KEY (task_id) REFERENCES tasks(task_id)
            );

            CREATE INDEX IF NOT EXISTS idx_tasks_project_status
                ON tasks(project_id, status);

            CREATE INDEX IF NOT EXISTS idx_executions_task_attempt
                ON executions(task_id, attempt);

            CREATE INDEX IF NOT EXISTS idx_events_project_sequence
                ON events(project_id, sequence);

            CREATE INDEX IF NOT EXISTS idx_locks_expiry
                ON resource_locks(expires_at);
        """)

    def _apply_v1_1_additions(self, conn) -> None:
        # Table 8.1 account_model_resources
        conn.execute("""
            CREATE TABLE IF NOT EXISTS account_model_resources (
                account_id TEXT NOT NULL,
                model_key TEXT NOT NULL,
                resource_state TEXT NOT NULL DEFAULT 'UNKNOWN',
                cooldown_until TEXT,
                cooldown_reason TEXT,
                cooldown_source TEXT,
                retry_after_seconds INTEGER,
                last_quota_observed_at TEXT,
                last_error_code TEXT,
                confidence REAL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (account_id, model_key)
            );
        """)

        # Section 8.2 Execution runtime metadata - check PRAGMA table_info before adding
        columns_info = conn.execute("PRAGMA table_info(executions);").fetchall()
        existing_cols: Set[str] = {row["name"] for row in columns_info}

        cols_to_add = [
            ("runtime_name", "TEXT"),
            ("runtime_version", "TEXT"),
            ("pid", "INTEGER"),
            ("process_creation_time", "TEXT"),
            ("agent_print_timeout_seconds", "INTEGER"),
            ("termination_reason", "TEXT"),
            ("normalized_outcome", "TEXT"),
            ("parser_version", "TEXT"),
        ]

        for col_name, col_type in cols_to_add:
            if col_name not in existing_cols:
                conn.execute(f"ALTER TABLE executions ADD COLUMN {col_name} {col_type};")

    def _apply_v1_2_pair_programming(self, conn) -> None:
        # Check and add columns to tasks table
        task_cols_info = conn.execute("PRAGMA table_info(tasks);").fetchall()
        existing_task_cols: Set[str] = {row["name"] for row in task_cols_info}

        if "pair_round" not in existing_task_cols:
            conn.execute("ALTER TABLE tasks ADD COLUMN pair_round INTEGER DEFAULT 0;")
        if "last_critique_json" not in existing_task_cols:
            conn.execute("ALTER TABLE tasks ADD COLUMN last_critique_json TEXT;")

        # Check and add execution_role to executions table
        exec_cols_info = conn.execute("PRAGMA table_info(executions);").fetchall()
        existing_exec_cols: Set[str] = {row["name"] for row in exec_cols_info}

        if "execution_role" not in existing_exec_cols:
            conn.execute("ALTER TABLE executions ADD COLUMN execution_role TEXT DEFAULT 'PRIMARY';")

        # Create task_reviews table
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS task_reviews (
                review_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                execution_id TEXT NOT NULL,
                round_number INTEGER NOT NULL,
                verdict TEXT NOT NULL,
                score INTEGER NOT NULL,
                critique_json TEXT NOT NULL,
                test_output TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
            );

            CREATE INDEX IF NOT EXISTS idx_reviews_task
                ON task_reviews(task_id, round_number);
        """)
