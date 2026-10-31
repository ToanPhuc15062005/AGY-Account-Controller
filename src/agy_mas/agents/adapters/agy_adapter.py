"""AGY Runtime Adapter supporting headless print-mode, stream-json parsing, and error taxonomy."""

import json
import re
import shutil
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..base import (
    AgentRuntimeAdapter,
    RuntimeCapabilities,
    Invocation,
    RuntimeEvent,
    FailureClassification,
)


class AGYAdapter(AgentRuntimeAdapter):
    """Adapter for Google Antigravity CLI (agy)."""

    def __init__(self, agy_cmd_path: Optional[str] = None):
        self.agy_cmd_path = agy_cmd_path or shutil.which("agy") or shutil.which("agy.cmd") or "agy"

    def validate_runtime(self) -> RuntimeCapabilities:
        """Probes agy executable and determines version and capabilities."""
        version = "unknown"
        try:
            res = subprocess.run(
                [self.agy_cmd_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            out = res.stdout.strip() or res.stderr.strip()
            if out:
                version = out.splitlines()[0]
        except Exception:
            pass

        return RuntimeCapabilities(
            runtime_name="agy",
            version=version,
            supports_print_mode=True,
            supports_stream_json=True,
            supports_scoped_permissions=True,
            supported_models=[
                "gemini-3.8-flash",
                "claude-sonnet-4-6",
                "claude-opus-4-6-thinking",
                "gpt-oss-120b-medium",
            ],
        )

    def build_invocation(
        self,
        task_contract: Dict[str, Any],
        execution_record: Dict[str, Any],
        policy: Optional[Dict[str, Any]] = None,
    ) -> Invocation:
        policy = policy or {}
        cmd = [self.agy_cmd_path]

        # ADR-009: AGY orchestration uses headless print mode for unattended execution
        cmd.append("-p")

        # Output format
        output_format = policy.get("output_format", "stream-json")
        cmd.extend(["--output-format", output_format])

        # Load account profile metadata if available
        account_id = execution_record.get("account_id")
        profile_meta = {}
        if account_id:
            profile_path = Path.home() / ".gemini" / "agy-profiles" / f"{account_id}.json"
            if profile_path.exists():
                try:
                    profile_meta = json.loads(profile_path.read_text(encoding="utf-8")).get("_meta", {})
                except Exception:
                    pass

        params = task_contract.get("inputs", {}).get("parameters", {})

        # Model selection (Contract Param -> Exec Record -> Profile Meta -> Policy Default -> "gemini-3.8-flash")
        model = params.get("model") or execution_record.get("model") or profile_meta.get("model") or policy.get("default_model") or "gemini-3.8-flash"
        if model:
            cmd.extend(["--model", model])

        # Effort selection (Contract Param -> Profile Meta -> Policy Default)
        effort = params.get("effort") or profile_meta.get("effort") or policy.get("default_effort")
        if effort:
            cmd.extend(["--effort", effort])

        # ADR-013: Scoped permissions by default; unrestricted bypass is opt-in (Turbo Mode)
        perm_profile = task_contract.get("permission_profile", {})
        if perm_profile.get("dangerously_skip_permissions", False) or profile_meta.get("mode") == "turbo" or params.get("mode") == "turbo":
            cmd.append("--dangerously-skip-permissions")

        # Assemble prompt payload
        title = task_contract.get("title", "")
        desc = task_contract.get("description", "")
        outs = task_contract.get("outputs", {})
        expected_arts = outs.get("expected_artifacts", [])
        expected_str = ", ".join(f"`{a.get('path')}`" for a in expected_arts) if expected_arts else "None specified"

        prompt_body = (
            f"TASK: {title}\n"
            f"OBJECTIVE: {desc}\n"
            f"EXPECTED ARTIFACTS: {expected_str}\n"
            "REQUIREMENTS: Execute strictly within requested scopes and verify outputs.\n"
        )
        cmd.append(prompt_body)

        timeout = task_contract.get("timeout_seconds", 900)

        return Invocation(
            command_args=cmd,
            cwd=policy.get("workspace_root"),
            timeout_seconds=timeout,
            metadata={
                "task_id": task_contract.get("task_id"),
                "execution_id": execution_record.get("execution_id"),
                "model": model,
            },
        )

    def parse_line(self, line: str) -> Optional[RuntimeEvent]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        stripped = line.strip()
        if not stripped:
            return None

        # Structured-first parsing (stream-json)
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                data = json.loads(stripped)
                event_type = data.get("type", "STRUCTURED_OUTPUT")
                msg = data.get("message") or data.get("content") or str(data)
                return RuntimeEvent(
                    event_type=event_type,
                    timestamp=now,
                    raw_data=data,
                    message=msg,
                    structured_payload=data,
                )
            except Exception:
                pass

        # Text stream fallback
        if "permission denied" in stripped.lower() or "soft-denial" in stripped.lower():
            return RuntimeEvent(
                event_type="PERMISSION_SOFT_DENIED",
                timestamp=now,
                message=stripped,
                error_type="PERMISSION_SOFT_DENIED",
            )
        elif "quota" in stripped.lower() or "resource_exhausted" in stripped.lower():
            return RuntimeEvent(
                event_type="QUOTA_EXHAUSTED",
                timestamp=now,
                message=stripped,
                error_type="QUOTA_EXHAUSTED",
            )

        return RuntimeEvent(
            event_type="RUNTIME_OUTPUT",
            timestamp=now,
            message=stripped,
        )

    def classify_failure(
        self,
        exit_code: int,
        stdout_tail: str,
        stderr_tail: str,
        events: Optional[List[RuntimeEvent]] = None,
    ) -> FailureClassification:
        combined_text = (stdout_tail + "\n" + stderr_tail).lower()

        # 1. Check structured events first (ADR-010)
        if events:
            for ev in reversed(events):
                if ev.error_type == "QUOTA_EXHAUSTED" or ev.event_type == "QUOTA_EXHAUSTED":
                    return FailureClassification(
                        error_type="QUOTA_EXHAUSTED",
                        retryable=True,
                        cooldown_required=True,
                        reason="Structured quota exhaustion detected",
                        cooldown_seconds=18000,
                        evidence_source="structured",
                    )
                if ev.error_type == "PERMISSION_SOFT_DENIED" or ev.event_type == "PERMISSION_SOFT_DENIED":
                    return FailureClassification(
                        error_type="PERMISSION_SOFT_DENIED",
                        retryable=False,
                        cooldown_required=False,
                        reason="Permission soft denial encountered in headless execution",
                        evidence_source="structured",
                    )

        # 2. Text pattern fallback
        if "quota exceeded" in combined_text or "resource_exhausted" in combined_text or "429" in combined_text:
            return FailureClassification(
                error_type="QUOTA_EXHAUSTED",
                retryable=True,
                cooldown_required=True,
                reason="Quota exhaustion pattern detected in output",
                cooldown_seconds=18000,
                evidence_source="pattern",
            )

        if "rate limit" in combined_text or "too many requests" in combined_text:
            return FailureClassification(
                error_type="RATE_LIMITED",
                retryable=True,
                cooldown_required=True,
                reason="Rate limit encountered",
                retry_after_seconds=60,
                evidence_source="pattern",
            )

        if "auth" in combined_text and ("unauthorized" in combined_text or "credential" in combined_text or "invalid_token" in combined_text):
            return FailureClassification(
                error_type="AUTHENTICATION_FAILED",
                retryable=False,
                cooldown_required=True,
                reason="Authentication failure",
                evidence_source="pattern",
            )

        if "permission denied" in combined_text or "access denied" in combined_text:
            return FailureClassification(
                error_type="PERMISSION_SOFT_DENIED",
                retryable=False,
                cooldown_required=False,
                reason="Permission denied pattern matched",
                evidence_source="pattern",
            )

        if "winerror 32" in combined_text or "winerror 33" in combined_text or "file is being used" in combined_text:
            return FailureClassification(
                error_type="FILE_BUSY",
                retryable=True,
                cooldown_required=False,
                reason="Windows file sharing contention",
                evidence_source="pattern",
            )

        return FailureClassification(
            error_type="UNKNOWN_RUNTIME_FAILURE",
            retryable=False,
            cooldown_required=False,
            reason=f"Exited with code {exit_code}",
            evidence_source="exit_code",
        )
