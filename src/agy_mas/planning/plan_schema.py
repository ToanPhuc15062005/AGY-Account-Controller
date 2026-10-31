"""Task contract schema and plan data structures according to MAS Specification v1.1."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import fnmatch


@dataclass
class InputScope:
    paths: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    context_keys: List[str] = field(default_factory=list)


@dataclass
class ExpectedArtifact:
    path: str
    artifact_type: str = "FILE"  # FILE, TEST_REPORT, LOG, CODE
    min_size_bytes: int = 1
    required: bool = True


@dataclass
class OutputScope:
    expected_artifacts: List[ExpectedArtifact] = field(default_factory=list)
    target_paths: List[str] = field(default_factory=list)


@dataclass
class AcceptanceCriterion:
    criterion_type: str  # ARTIFACT_EXISTS, EXIT_CODE_ZERO, TEST_PASSED, NO_SOFT_DENIAL
    description: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PermissionProfile:
    read_paths: List[str] = field(default_factory=list)
    write_paths: List[str] = field(default_factory=list)
    allow_network: bool = False
    dangerously_skip_permissions: bool = False

    def allows_write(self, target_path: str) -> bool:
        if self.dangerously_skip_permissions:
            return True
        norm = target_path.replace("\\", "/").lstrip("/")
        for wp in self.write_paths:
            wp_norm = wp.replace("\\", "/").lstrip("/")
            if fnmatch.fnmatch(norm, wp_norm) or norm.startswith(wp_norm.rstrip("*").rstrip("/")):
                return True
        return False


@dataclass
class TaskContract:
    task_id: str
    project_id: str
    title: str
    description: str
    domain: str = "software"
    role: str = "developer"
    priority: int = 50
    inputs: InputScope = field(default_factory=InputScope)
    outputs: OutputScope = field(default_factory=OutputScope)
    acceptance_criteria: List[AcceptanceCriterion] = field(default_factory=list)
    permission_profile: PermissionProfile = field(default_factory=PermissionProfile)
    max_retries: int = 2
    retry_delay_seconds: int = 10
    timeout_seconds: int = 900
    depends_on: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "domain": self.domain,
            "role": self.role,
            "priority": self.priority,
            "inputs": {
                "paths": self.inputs.paths,
                "parameters": self.inputs.parameters,
                "context_keys": self.inputs.context_keys,
            },
            "outputs": {
                "expected_artifacts": [
                    {
                        "path": a.path,
                        "artifact_type": a.artifact_type,
                        "min_size_bytes": a.min_size_bytes,
                        "required": a.required,
                    }
                    for a in self.outputs.expected_artifacts
                ],
                "target_paths": self.outputs.target_paths,
            },
            "acceptance_criteria": [
                {
                    "criterion_type": c.criterion_type,
                    "description": c.description,
                    "params": c.params,
                }
                for c in self.acceptance_criteria
            ],
            "permission_profile": {
                "read_paths": self.permission_profile.read_paths,
                "write_paths": self.permission_profile.write_paths,
                "allow_network": self.permission_profile.allow_network,
                "dangerously_skip_permissions": self.permission_profile.dangerously_skip_permissions,
            },
            "max_retries": self.max_retries,
            "retry_delay_seconds": self.retry_delay_seconds,
            "timeout_seconds": self.timeout_seconds,
            "depends_on": self.depends_on,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskContract":
        in_data = data.get("inputs", {})
        out_data = data.get("outputs", {})
        perm_data = data.get("permission_profile", {})
        crit_data = data.get("acceptance_criteria", [])

        expected_arts = [
            ExpectedArtifact(
                path=a.get("path", ""),
                artifact_type=a.get("artifact_type", "FILE"),
                min_size_bytes=a.get("min_size_bytes", 1),
                required=a.get("required", True),
            )
            for a in out_data.get("expected_artifacts", [])
        ]

        criteria = [
            AcceptanceCriterion(
                criterion_type=c.get("criterion_type", "EXIT_CODE_ZERO"),
                description=c.get("description", ""),
                params=c.get("params", {}),
            )
            for c in crit_data
        ]

        return cls(
            task_id=data["task_id"],
            project_id=data["project_id"],
            title=data["title"],
            description=data.get("description", ""),
            domain=data.get("domain", "software"),
            role=data.get("role", "developer"),
            priority=data.get("priority", 50),
            inputs=InputScope(
                paths=in_data.get("paths", []),
                parameters=in_data.get("parameters", {}),
                context_keys=in_data.get("context_keys", []),
            ),
            outputs=OutputScope(
                expected_artifacts=expected_arts,
                target_paths=out_data.get("target_paths", []),
            ),
            acceptance_criteria=criteria,
            permission_profile=PermissionProfile(
                read_paths=perm_data.get("read_paths", []),
                write_paths=perm_data.get("write_paths", []),
                allow_network=perm_data.get("allow_network", False),
                dangerously_skip_permissions=perm_data.get("dangerously_skip_permissions", False),
            ),
            max_retries=data.get("max_retries", 2),
            retry_delay_seconds=data.get("retry_delay_seconds", 10),
            timeout_seconds=data.get("timeout_seconds", 900),
            depends_on=data.get("depends_on", []),
        )
