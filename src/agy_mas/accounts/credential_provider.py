"""Thread and process-safe credential switching lock for concurrent AGY execution."""

import os
import sys
import time
from pathlib import Path
from contextlib import contextmanager
from typing import Optional

IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    import msvcrt
else:
    import fcntl


class CredentialSwitchLock:
    """Acquires an atomic cross-process file lock while switching credentials in OS store."""

    def __init__(self, lock_path: Optional[str] = None):
        if not lock_path:
            lock_dir = Path.home() / ".gemini" / "antigravity-cli"
            lock_dir.mkdir(parents=True, exist_ok=True)
            self.lock_file = lock_dir / "credential_switch.lock"
        else:
            self.lock_file = Path(lock_path)
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self._fd = None

    def acquire(self, timeout_sec: float = 30.0) -> bool:
        start = time.time()
        self._fd = open(self.lock_file, "a+")
        while time.time() - start < timeout_sec:
            try:
                if IS_WINDOWS:
                    msvcrt.locking(self._fd.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self._fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except (OSError, IOError):
                time.sleep(0.05)
        return False

    def release(self) -> None:
        if self._fd:
            try:
                if IS_WINDOWS:
                    self._fd.seek(0)
                    msvcrt.locking(self._fd.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(self._fd.fileno(), fcntl.LOCK_UN)
            except (OSError, IOError):
                pass
            finally:
                self._fd.close()
                self._fd = None

    def __enter__(self):
        if not self.acquire():
            raise TimeoutError("Timed out acquiring CredentialSwitchLock")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
