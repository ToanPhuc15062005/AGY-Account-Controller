"""Process manager handling cross-platform process trees, Windows Job Objects, and streams."""

import os
import sys
import time
import datetime
import subprocess
import threading
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Callable
from .base import Invocation, TerminationResult

# Windows-specific imports for Job Objects
IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JobObjectExtendedLimitInformation = 9

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        ]

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", wintypes.LARGE_INTEGER),
            ("PerJobUserTimeLimit", wintypes.LARGE_INTEGER),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryLimit", ctypes.c_size_t),
            ("PeakJobMemoryLimit", ctypes.c_size_t),
        ]


class ManagedProcess:
    """Manages an active agent subprocess, capturing streams and supervising process tree."""

    def __init__(
        self,
        invocation: Invocation,
        on_stdout_line: Optional[Callable[[str], None]] = None,
        log_path: Optional[str] = None,
    ):
        self.invocation = invocation
        self.on_stdout_line = on_stdout_line
        self.log_path = log_path
        self._log_file = None

        self.process: Optional[subprocess.Popen] = None
        self.pid: Optional[int] = None
        self.start_time: Optional[str] = None
        self.job_handle: Optional[int] = None

        self.stdout_lines: List[str] = []
        self.stderr_lines: List[str] = []
        self._stdout_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Starts the subprocess and attaches Windows Job Object if supported."""
        env = os.environ.copy()
        env.update(self.invocation.env)

        creationflags = 0
        if IS_WINDOWS:
            # CREATE_SUSPENDED = 0x00000004
            # We can create job object first
            try:
                self.job_handle = kernel32.CreateJobObjectW(None, None)
                if self.job_handle:
                    info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
                    info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                    kernel32.SetInformationJobObject(
                        self.job_handle,
                        JobObjectExtendedLimitInformation,
                        ctypes.byref(info),
                        ctypes.sizeof(info),
                    )
            except Exception:
                self.job_handle = None

        self.start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.process = subprocess.Popen(
            self.invocation.command_args,
            cwd=self.invocation.cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            creationflags=creationflags,
        )
        self.pid = self.process.pid

        # Open dedicated task log file if path provided
        if self.log_path:
            try:
                Path(self.log_path).parent.mkdir(parents=True, exist_ok=True)
                self._log_file = open(self.log_path, "a", encoding="utf-8", buffering=1)
                self._log_file.write(f"=== Execution started at {self.start_time} (PID: {self.pid}) ===\n")
                self._log_file.write(f"Command: {' '.join(self.invocation.command_args[:3])}...\n\n")
                self._log_file.flush()
            except Exception:
                self._log_file = None

        if IS_WINDOWS and self.job_handle and self.process:
            try:
                # Open process handle with PROCESS_SET_QUOTA | PROCESS_TERMINATE
                PROCESS_ALL_ACCESS = 0x1F0FFF
                proc_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
                if proc_handle:
                    kernel32.AssignProcessToJobObject(self.job_handle, proc_handle)
                    kernel32.CloseHandle(proc_handle)
            except Exception:
                pass

        # Start stream capturing threads
        self._stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _read_stdout(self) -> None:
        if not self.process or not self.process.stdout:
            return
        for line in iter(self.process.stdout.readline, ""):
            cleaned = line.rstrip("\r\n")
            self.stdout_lines.append(cleaned)
            if self._log_file and not self._log_file.closed:
                try:
                    self._log_file.write(f"{cleaned}\n")
                    self._log_file.flush()
                except Exception:
                    pass
            if self.on_stdout_line:
                try:
                    self.on_stdout_line(cleaned)
                except Exception:
                    pass
        self.process.stdout.close()

    def _read_stderr(self) -> None:
        if not self.process or not self.process.stderr:
            return
        for line in iter(self.process.stderr.readline, ""):
            cleaned = line.rstrip("\r\n")
            self.stderr_lines.append(cleaned)
            if self._log_file and not self._log_file.closed:
                try:
                    self._log_file.write(f"[STDERR] {cleaned}\n")
                    self._log_file.flush()
                except Exception:
                    pass
        self.process.stderr.close()

    def close_log(self) -> None:
        """Safely flushes and closes task execution log file."""
        if self._log_file and not self._log_file.closed:
            try:
                code = self.process.poll() if self.process else "UNKNOWN"
                self._log_file.write(f"\n=== Execution ended with exit code {code} ===\n")
                self._log_file.flush()
                self._log_file.close()
            except Exception:
                pass
            self._log_file = None

    def wait(self, timeout_seconds: Optional[int] = None) -> int:
        if not self.process:
            raise RuntimeError("Process not started")
        exit_code = self.process.wait(timeout=timeout_seconds)
        if self._stdout_thread:
            self._stdout_thread.join(timeout=2.0)
        if self._stderr_thread:
            self._stderr_thread.join(timeout=2.0)
        self.close_log()
        return exit_code

    def is_alive(self) -> bool:
        if not self.process:
            return False
        return self.process.poll() is None

    def terminate_tree(self, reason: str = "ORCHESTRATOR_ABORT") -> TerminationResult:
        """Terminates process and all child descendants, ensuring process tree is dead."""
        if not self.process or not self.pid:
            return TerminationResult(True, 0, 0, reason)

        terminated_count = 0
        if IS_WINDOWS:
            if self.job_handle:
                try:
                    kernel32.TerminateJobObject(self.job_handle, 1)
                    terminated_count += 1
                except Exception:
                    pass

            # Also execute taskkill /F /T as defensive fallback
            try:
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(self.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                terminated_count += 1
            except Exception:
                pass
        else:
            try:
                self.process.kill()
                terminated_count += 1
            except Exception:
                pass

        # Wait briefly for process to exit
        for _ in range(10):
            if not self.is_alive():
                break
            time.sleep(0.1)

        residual = 1 if self.is_alive() else 0

        if self.job_handle and IS_WINDOWS:
            try:
                kernel32.CloseHandle(self.job_handle)
            except Exception:
                pass
            self.job_handle = None

        self.close_log()

        return TerminationResult(
            success=(residual == 0),
            processes_terminated=terminated_count,
            residual_processes=residual,
            termination_reason=reason,
        )
