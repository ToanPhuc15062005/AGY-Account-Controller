"""Database connection and transaction manager for AGY-MAS SQLite persistence."""

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional, Any, List, Dict


class Database:
    """Manages SQLite database connections and transactions with robust pragmas."""

    def __init__(self, db_path: str = ":memory:", busy_timeout_ms: int = 5000, wal_mode: bool = True):
        self.db_path = db_path
        self.busy_timeout_ms = busy_timeout_ms
        self.wal_mode = wal_mode and (db_path != ":memory:")
        self._local = threading.local()

        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize connection once to ensure DB file is created and PRAGMAs applied
        with self.connect() as conn:
            pass

    def _create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.busy_timeout_ms / 1000.0,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute(f"PRAGMA busy_timeout = {self.busy_timeout_ms};")
        if self.wal_mode:
            conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    @contextmanager
    def connect(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager yielding a thread-local SQLite connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = self._create_connection()

        yield self._local.conn

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for atomic transaction block."""
        with self.connect() as conn:
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def execute(self, query: str, params: Any = ()) -> sqlite3.Cursor:
        """Executes a query directly within an auto-commit or existing transaction."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetchone(self, query: str, params: Any = ()) -> Optional[sqlite3.Row]:
        """Executes query and returns one row or None."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetchall(self, query: str, params: Any = ()) -> List[sqlite3.Row]:
        """Executes query and returns all matching rows."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def close(self) -> None:
        """Closes thread-local connection if open."""
        if hasattr(self._local, "conn") and self._local.conn is not None:
            self._local.conn.close()
            self._local.conn = None
