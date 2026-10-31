"""Configuration module for AGY-MAS (Multi-Agent System).

Defines configuration data structures and defaults aligned with
Architecture Specification v1.1.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any
import json
import os


@dataclass
class RuntimeConfig:
    default_runtime: str = "agy"
    print_mode: bool = True
    output_format: str = "stream-json"
    print_timeout_seconds: int = 900
    permission_mode: str = "scoped"  # "scoped" or "bypass"
    dangerously_skip_permissions: bool = False
    capture_stdout: bool = True
    capture_stderr: bool = True


@dataclass
class QuotaDetectionConfig:
    structured_errors_first: bool = True
    text_pattern_fallback: bool = True


@dataclass
class QuotaCooldownConfig:
    fallback_seconds: int = 18000  # 5 hours
    fallback_is_estimate: bool = True
    scope: str = "account_model"  # (account_id, model_key)


@dataclass
class FailoverConfig:
    enabled: bool = True
    require_same_model: bool = True
    max_attempts: int = 2


@dataclass
class QuotaConfig:
    detection: QuotaDetectionConfig = field(default_factory=QuotaDetectionConfig)
    cooldown: QuotaCooldownConfig = field(default_factory=QuotaCooldownConfig)
    failover: FailoverConfig = field(default_factory=FailoverConfig)


@dataclass
class WindowsFileRetryConfig:
    initial_delay_ms: int = 100
    max_delay_ms: int = 1500
    max_attempts: int = 5
    jitter_ratio: float = 0.2


@dataclass
class WorkspaceConfig:
    windows_file_retry: WindowsFileRetryConfig = field(default_factory=WindowsFileRetryConfig)
    snapshot_only_after_process_exit: bool = True


@dataclass
class StorageConfig:
    db_path: str = str(Path.home() / ".gemini" / "antigravity-cli" / "agy_mas.db")
    busy_timeout_ms: int = 5000
    wal_mode: bool = True


@dataclass
class MASConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    quota: QuotaConfig = field(default_factory=QuotaConfig)
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "MASConfig":
        """Loads configuration from a JSON/YAML file or returns default."""
        if not config_path:
            env_path = os.environ.get("AGY_MAS_CONFIG")
            if env_path and os.path.exists(env_path):
                config_path = env_path

        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls.from_dict(data)

        return cls()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MASConfig":
        rc = data.get("runtime", {})
        qc = data.get("quota", {})
        wc = data.get("workspace", {})
        sc = data.get("storage", {})

        return cls(
            runtime=RuntimeConfig(
                default_runtime=rc.get("default_runtime", rc.get("default", "agy")),
                print_mode=rc.get("print_mode", True),
                output_format=rc.get("output_format", "stream-json"),
                print_timeout_seconds=rc.get("print_timeout_seconds", 900),
                permission_mode=rc.get("permission_mode", "scoped"),
                dangerously_skip_permissions=rc.get("dangerously_skip_permissions", False),
                capture_stdout=rc.get("capture_stdout", True),
                capture_stderr=rc.get("capture_stderr", True),
            ),
            quota=QuotaConfig(
                detection=QuotaDetectionConfig(
                    structured_errors_first=qc.get("detection", {}).get("structured_errors_first", True),
                    text_pattern_fallback=qc.get("detection", {}).get("text_pattern_fallback", True),
                ),
                cooldown=QuotaCooldownConfig(
                    fallback_seconds=qc.get("cooldown", {}).get("fallback_seconds", 18000),
                    fallback_is_estimate=qc.get("cooldown", {}).get("fallback_is_estimate", True),
                    scope=qc.get("cooldown", {}).get("scope", "account_model"),
                ),
                failover=FailoverConfig(
                    enabled=qc.get("failover", {}).get("enabled", True),
                    require_same_model=qc.get("failover", {}).get("require_same_model", True),
                    max_attempts=qc.get("failover", {}).get("max_attempts", 2),
                ),
            ),
            workspace=WorkspaceConfig(
                windows_file_retry=WindowsFileRetryConfig(
                    initial_delay_ms=wc.get("windows_file_retry", {}).get("initial_delay_ms", 100),
                    max_delay_ms=wc.get("windows_file_retry", {}).get("max_delay_ms", 1500),
                    max_attempts=wc.get("windows_file_retry", {}).get("max_attempts", 5),
                    jitter_ratio=wc.get("windows_file_retry", {}).get("jitter_ratio", 0.2),
                ),
                snapshot_only_after_process_exit=wc.get("snapshot_only_after_process_exit", True),
            ),
            storage=StorageConfig(
                db_path=sc.get("db_path", str(Path.home() / ".gemini" / "antigravity-cli" / "agy_mas.db")),
                busy_timeout_ms=sc.get("busy_timeout_ms", 5000),
                wal_mode=sc.get("wal_mode", True),
            ),
        )
