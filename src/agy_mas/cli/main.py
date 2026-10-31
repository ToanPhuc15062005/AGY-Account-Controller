"""CLI entrypoint for AGY-MAS (Multi-Agent System)."""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional
from ..config import MASConfig
from ..storage.database import Database
from ..storage.migrations.runner import MigrationRunner
from ..storage.repositories import (
    ProjectRepository,
    TaskRepository,
    ExecutionRepository,
    EventRepository,
    ArtifactRepository,
    ResourceRepository,
)
from ..workspace.workspace_manager import WorkspaceManager
from ..resources.quota_tracker import QuotaTracker
from ..agents.adapters.agy_adapter import AGYAdapter
from ..core.orchestrator import Orchestrator


def init_mas(config: Optional[MASConfig] = None):
    cfg = config or MASConfig.load()
    db = Database(cfg.storage.db_path, cfg.storage.busy_timeout_ms, cfg.storage.wal_mode)
    MigrationRunner(db).run_all()

    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    execution_repo = ExecutionRepository(db)
    event_repo = EventRepository(db)
    artifact_repo = ArtifactRepository(db)
    resource_repo = ResourceRepository(db)
    quota_tracker = QuotaTracker(resource_repo, cfg.quota)
    adapter = AGYAdapter()

    return {
        "config": cfg,
        "db": db,
        "project_repo": project_repo,
        "task_repo": task_repo,
        "execution_repo": execution_repo,
        "event_repo": event_repo,
        "artifact_repo": artifact_repo,
        "resource_repo": resource_repo,
        "quota_tracker": quota_tracker,
        "adapter": adapter,
    }


def cmd_project(args, ctx):
    project_repo = ctx["project_repo"]
    if args.project_action == "create":
        pid = args.id or f"proj_{Path(args.name).stem.lower()[:8]}"
        ws = str(Path(args.workspace or ".").resolve())
        p = project_repo.create(pid, args.name, args.goal, ws, status="CREATED")
        print(f"[OK] Project created: {p['project_id']} ({p['name']}) -> {ws}")

    elif args.project_action == "list":
        projects = project_repo.list_all()
        if not projects:
            print("No projects registered.")
            return
        print(f"{'PROJECT ID':<16} {'STATUS':<12} {'NAME':<24} {'WORKSPACE'}")
        print("-" * 80)
        for p in projects:
            print(f"{p['project_id']:<16} {p['status']:<12} {p['name']:<24} {p['workspace_root']}")

    elif args.project_action == "inspect":
        p = project_repo.get(args.id)
        if not p:
            print(f"Error: Project '{args.id}' not found.")
            return
        print(json.dumps(p, indent=2))


def cmd_task(args, ctx):
    task_repo = ctx["task_repo"]
    if args.task_action == "create":
        deps = [d.strip() for d in args.depends_on.split(",") if d.strip()] if args.depends_on else []
        t = task_repo.create(
            task_id=args.id,
            project_id=args.project_id,
            title=args.title,
            description=args.desc or args.title,
            priority=args.priority,
            depends_on=deps,
        )
        print(f"[OK] Task created: {t['task_id']} in {t['project_id']} (deps: {t['dependencies']})")

    elif args.task_action == "list":
        tasks = task_repo.list_by_project(args.project_id)
        if not tasks:
            print(f"No tasks found for project {args.project_id}.")
            return
        print(f"{'TASK ID':<16} {'STATUS':<12} {'PRIORITY':<8} {'DEPS':<16} {'TITLE'}")
        print("-" * 80)
        for t in tasks:
            deps_str = ",".join(t.get("dependencies", [])) or "-"
            print(f"{t['task_id']:<16} {t['status']:<12} {t['priority']:<8} {deps_str:<16} {t['title']}")


def cmd_resource(args, ctx):
    resource_repo = ctx["resource_repo"]
    resources = resource_repo.list_account_model_resources()
    if not resources:
        print("No active account-model resource cooldowns or metrics.")
        return
    print(f"{'ACCOUNT':<16} {'MODEL':<24} {'STATE':<12} {'COOLDOWN UNTIL':<28} {'REASON'}")
    print("-" * 90)
    for r in resources:
        until = r.get("cooldown_until") or "-"
        reason = r.get("cooldown_reason") or "-"
        print(f"{r['account_id']:<16} {r['model_key']:<24} {r['resource_state']:<12} {until:<28} {reason}")


def cmd_orchestrate(args, ctx):
    project_repo = ctx["project_repo"]
    p = project_repo.get(args.project_id)
    if not p:
        print(f"Error: Project '{args.project_id}' not found.")
        return

    workspace_mgr = WorkspaceManager(
        workspace_root=p["workspace_root"],
        resource_repo=ctx["resource_repo"],
        artifact_repo=ctx["artifact_repo"],
        config=ctx["config"].workspace,
    )

    orchestrator = Orchestrator(
        project_repo=ctx["project_repo"],
        task_repo=ctx["task_repo"],
        execution_repo=ctx["execution_repo"],
        event_repo=ctx["event_repo"],
        artifact_repo=ctx["artifact_repo"],
        resource_repo=ctx["resource_repo"],
        workspace_mgr=workspace_mgr,
        adapter=ctx["adapter"],
        quota_tracker=ctx["quota_tracker"],
        max_concurrency=args.concurrency,
    )

    accounts = [a.strip() for a in args.accounts.split(",") if a.strip()] if args.accounts else ["default"]
    print(f"Starting orchestration for project '{p['name']}' ({args.project_id})...")
    project_repo.update_status(args.project_id, "RUNNING")

    # Run tick loop
    while True:
        status = orchestrator.tick(args.project_id, available_accounts=accounts)
        if status["status"] in ("COMPLETED", "FAILED", "CANCELLED"):
            print(f"[FINISHED] Orchestration reached terminal status: {status['status']}")
            break
        import time
        time.sleep(1.0)


def main():
    parser = argparse.ArgumentParser(prog="agy-mas", description="Multi-Agent System for AGY")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Project subparser
    proj_p = subparsers.add_parser("project", help="Manage projects")
    proj_sp = proj_p.add_subparsers(dest="project_action", required=True)

    create_p = proj_sp.add_parser("create", help="Create project")
    create_p.add_argument("name", help="Project name")
    create_p.add_argument("goal", help="Project goal description")
    create_p.add_argument("--id", help="Explicit project ID")
    create_p.add_argument("--workspace", help="Workspace root path")

    list_p = proj_sp.add_parser("list", help="List projects")
    insp_p = proj_sp.add_parser("inspect", help="Inspect project")
    insp_p.add_argument("id", help="Project ID")

    # Task subparser
    task_p = subparsers.add_parser("task", help="Manage tasks")
    task_sp = task_p.add_subparsers(dest="task_action", required=True)

    t_create = task_sp.add_parser("create", help="Create task")
    t_create.add_argument("project_id", help="Project ID")
    t_create.add_argument("id", help="Task ID")
    t_create.add_argument("title", help="Task title")
    t_create.add_argument("--desc", help="Task description")
    t_create.add_argument("--priority", type=int, default=50)
    t_create.add_argument("--depends-on", help="Comma-separated prerequisite task IDs")

    t_list = task_sp.add_parser("list", help="List tasks")
    t_list.add_argument("project_id", help="Project ID")

    # Resource subparser
    res_p = subparsers.add_parser("resource", help="Inspect resource states")
    res_sp = res_p.add_subparsers(dest="resource_action", required=True)
    res_sp.add_parser("status", help="List account-model cooldowns")

    # Orchestrate subparser
    orch_p = subparsers.add_parser("orchestrate", help="Run orchestrator")
    orch_sp = orch_p.add_subparsers(dest="orchestrate_action", required=True)
    o_start = orch_sp.add_parser("start", help="Start orchestration loop")
    o_start.add_argument("project_id", help="Project ID")
    o_start.add_argument("--accounts", help="Comma-separated candidate accounts")
    o_start.add_argument("--concurrency", type=int, default=4)

    args = parser.parse_args()
    ctx = init_mas()

    if args.subcommand == "project":
        cmd_project(args, ctx)
    elif args.subcommand == "task":
        cmd_task(args, ctx)
    elif args.subcommand == "resource":
        cmd_resource(args, ctx)
    elif args.subcommand == "orchestrate":
        cmd_orchestrate(args, ctx)


if __name__ == "__main__":
    main()
