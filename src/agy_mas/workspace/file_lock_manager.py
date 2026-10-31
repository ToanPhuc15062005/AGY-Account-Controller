"""Windows file lock manager with bounded retry and backoff for WinError 32/33."""

import time
import random
import sys
import functools
from typing import Callable, TypeVar, Any, Optional
from ..config import WindowsFileRetryConfig

T = TypeVar("T")


class FileSharingContentionError(IOError):
    """Raised when file access retries are exhausted due to concurrent Windows file locks."""
    pass


def is_windows_sharing_violation(exc: Exception) -> bool:
    """Checks if exception is WinError 32 (sharing violation) or 33 (lock violation)."""
    if isinstance(exc, PermissionError):
        # On Windows, PermissionError often wraps WinError 32
        winerror = getattr(exc, "winerror", None)
        if winerror in (32, 33):
            return True
        # Text fallback if winerror attribute is absent
        msg = str(exc).lower()
        if "used by another process" in msg or "winerror 32" in msg or "winerror 33" in msg:
            return True
    return False


class WindowsFileRetryManager:
    """Executes file operations with exponential backoff and jitter for Windows concurrency."""

    def __init__(self, config: Optional[WindowsFileRetryConfig] = None):
        self.config = config or WindowsFileRetryConfig()

    def execute_with_retry(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        attempts = 0
        delay_ms = self.config.initial_delay_ms

        while True:
            attempts += 1
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempts >= self.config.max_attempts or not is_windows_sharing_violation(e):
                    if is_windows_sharing_violation(e):
                        raise FileSharingContentionError(
                            f"File sharing violation persisted after {attempts} attempts: {e}"
                        ) from e
                    raise

                # Calculate backoff with jitter
                jitter = (random.random() * 2 - 1) * self.config.jitter_ratio
                actual_delay_ms = min(self.config.max_delay_ms, delay_ms * (1 + jitter))
                time.sleep(actual_delay_ms / 1000.0)
                delay_ms = min(self.config.max_delay_ms, delay_ms * 2)


def windows_file_retry(config: Optional[WindowsFileRetryConfig] = None):
    """Decorator for automatic Windows file contention retry."""
    retry_mgr = WindowsFileRetryManager(config)

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return retry_mgr.execute_with_retry(fn, *args, **kwargs)
        return wrapper
    return decorator
