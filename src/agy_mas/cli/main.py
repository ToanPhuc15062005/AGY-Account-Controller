"""CLI entrypoint for AGY-MAS (Multi-Agent System)."""

import argparse
import sys
import json
import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Ensure line-buffering on stdout/stderr to prevent log starvation in background pipes
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass
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
from ..planning.planner import Planner
import uuid


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
        task_spec = {}
        params = {}
        if getattr(args, "model", None):
            params["model"] = args.model
        if getattr(args, "effort", None):
            params["effort"] = args.effort
        if getattr(args, "mode", None):
            params["mode"] = args.mode
        if params:
            task_spec["inputs"] = {"parameters": params}

        t = task_repo.create(
            task_id=args.id,
            project_id=args.project_id,
            title=args.title,
            description=args.desc or args.title,
            priority=args.priority,
            depends_on=deps,
            task_spec=task_spec if task_spec else None,
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

    elif args.task_action == "logs":
        exec_repo = ctx["execution_repo"]
        execs = exec_repo.list_by_task(args.task_id)
        log_path = None
        latest = {}
        if execs:
            latest = execs[-1]
            meta = json.loads(latest.get("metadata_json") or "{}")
            log_path = meta.get("log_path")

        if not log_path or not Path(log_path).exists():
            log_dir = Path.home() / ".gemini" / "antigravity-cli" / "logs" / args.project_id
            candidates = sorted(log_dir.glob(f"{args.task_id}_*.log")) if log_dir.exists() else []
            if candidates:
                log_path = str(candidates[-1])
            else:
                print(f"No log file found on disk for task '{args.task_id}'.")
                return

        exec_id = latest.get("execution_id", "N/A")
        pid_info = latest.get("pid", "N/A")
        print(f"=== Logs for Task '{args.task_id}' (Execution: {exec_id}, PID: {pid_info}) ===")
        print(f"Log File: {log_path}\n" + "-" * 75)
        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                tail_lines = lines[-args.tail:] if (args.tail and args.tail > 0) else lines
                for l in tail_lines:
                    print(l, end="", flush=True)
        except Exception as e:
            print(f"Error reading log file: {e}")


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

    policy = {
        "default_model": getattr(args, "model", None),
        "default_effort": getattr(args, "effort", None),
    }

    def cli_event_listener(event_type: str, data: Dict[str, Any]):
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        if event_type == "TASK_DISPATCHED":
            tid = data.get("task_id")
            acc = data.get("account_id")
            model = data.get("model")
            pid = data.get("pid")
            title = data.get("title", "")
            print(f"[{now_str}] [DISPATCH]  Task '{tid}' -> Account: {acc} | Model: {model} | PID: {pid} | Title: {title}", flush=True)
        elif event_type == "TASK_VERIFYING":
            tid = data.get("task_id")
            code = data.get("exit_code")
            el = data.get("elapsed_seconds")
            print(f"[{now_str}] [VERIFYING] Task '{tid}' process exited (Exit: {code}, elapsed: {el}s) -> verifying artifacts...", flush=True)
        elif event_type == "TASK_ACCEPTED":
            tid = data.get("task_id")
            el = data.get("elapsed_seconds")
            arts = data.get("artifacts", [])
            art_str = f" ({len(arts)} artifact(s): {', '.join(arts[:2])})" if arts else ""
            print(f"[{now_str}] [ACCEPTED]  Task '{tid}' verified successfully in {el}s{art_str}", flush=True)
        elif event_type == "TASK_FAILED":
            tid = data.get("task_id")
            err = data.get("error_type")
            reason = data.get("reason")
            retry = " (will retry)" if data.get("retryable") else " (terminal failure)"
            print(f"[{now_str}] [FAILED]    Task '{tid}' failed: [{err}] {reason}{retry}", flush=True)
        elif event_type == "TASK_TIMEOUT":
            tid = data.get("task_id")
            el = data.get("elapsed_seconds")
            print(f"[{now_str}] [TIMEOUT]   Task '{tid}' timed out after {el}s", flush=True)
        elif event_type == "HEARTBEAT":
            workers = data.get("workers", [])
            w_info = " | ".join(f"{w['task_id']} ({w['account_id']}, {w['elapsed_seconds']}s)" for w in workers)
            print(f"[{now_str}] [HEARTBEAT] Active: {data.get('active_count')} worker(s) -> {w_info}", flush=True)
        elif event_type == "QUOTA_COOLDOWN":
            acc = data.get("account_id")
            model = data.get("model")
            dur = data.get("retry_after_seconds")
            print(f"[{now_str}] [COOLDOWN]  Account '{acc}' model '{model}' entered cooldown for {dur}s", flush=True)

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
        default_policy=policy,
        on_event=cli_event_listener,
    )

    accounts = [a.strip() for a in args.accounts.split(",") if a.strip()] if args.accounts else ["default"]
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now_str}] [START] Starting orchestration for project '{p['name']}' ({args.project_id})...", flush=True)
    print(f"[{now_str}] [CONFIG] Candidate accounts: {', '.join(accounts)} | Max concurrency: {args.concurrency}", flush=True)
    project_repo.update_status(args.project_id, "RUNNING")

    # Run tick loop with clean KeyboardInterrupt handling
    try:
        import time
        while True:
            status = orchestrator.tick(args.project_id, available_accounts=accounts)
            if status["status"] in ("COMPLETED", "FAILED", "CANCELLED"):
                now_str = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"[{now_str}] [FINISHED] Orchestration reached terminal status: {status['status']}", flush=True)
                break
            time.sleep(1.0)
    except KeyboardInterrupt:
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n[{now_str}] [INTERRUPTED] Orchestration loop paused by user.", flush=True)


def cmd_plan(args, ctx):
    project_repo = ctx["project_repo"]
    p = project_repo.get(args.project_id)
    if not p:
        print(f"Error: Project '{args.project_id}' not found.")
        return
    planner = Planner(ctx["task_repo"])
    print(f"Planning subtasks for goal: '{p['goal']}'...")
    contracts = planner.plan_project(
        project_id=args.project_id,
        goal=p["goal"],
        workspace_root=p["workspace_root"],
        model=args.model or "gemini-3.8-flash",
    )
    print(f"[OK] Generated {len(contracts)} validated subtasks:")
    for c in contracts:
        deps = ",".join(c.depends_on) or "None (runs immediately)"
        print(f"  - [{c.task_id}] {c.title}")
        print(f"    Writes: {c.permission_profile.write_paths} | Dependencies: {deps}")


def cmd_run(args, ctx):
    project_repo = ctx["project_repo"]
    pid = args.id or f"proj_{uuid.uuid4().hex[:6]}"
    name = args.name or args.goal[:30]
    ws = str(Path(args.workspace or ".").resolve())
    project_repo.create(pid, name, args.goal, ws, status="PLANNING")
    print(f"[1/3] Project initialized: {pid} ('{name}')")

    planner = Planner(ctx["task_repo"])
    print(f"[2/3] Decomposing goal into parallel subtasks with zero collisions...")
    contracts = planner.plan_project(
        project_id=pid,
        goal=args.goal,
        workspace_root=ws,
        model=args.model or "gemini-3.8-flash",
    )
    print(f"      Generated {len(contracts)} decoupled subtasks:")
    for c in contracts:
        deps = ",".join(c.depends_on) or "independent (parallel)"
        print(f"      * [{c.task_id}] {c.title} (deps: {deps})")

    print(f"[3/3] Launching Multi-Agent Orchestrator...")
    args.project_id = pid
    cmd_orchestrate(args, ctx)


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
    t_create.add_argument("--model", help="Override Model for this specific task (e.g. claude-sonnet-4-6)")
    t_create.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="Override Effort level for this task")
    t_create.add_argument("--mode", choices=["normal", "turbo"], help="Mode for this task (normal hoặc turbo)")

    t_list = task_sp.add_parser("list", help="List tasks")
    t_list.add_argument("project_id", help="Project ID")

    t_logs = task_sp.add_parser("logs", help="View execution logs for a task")
    t_logs.add_argument("project_id", help="Project ID")
    t_logs.add_argument("task_id", help="Task ID")
    t_logs.add_argument("--tail", type=int, default=50, help="Number of lines to show from end (default: 50)")

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

    # Plan subparser
    plan_p = subparsers.add_parser("plan", help="Auto-decompose project goal into validated subtasks")
    plan_p.add_argument("project_id", help="Project ID to plan")
    plan_p.add_argument("--model", help="Planner model (default: gemini-3.8-flash)")

    # Run subparser (Single-command autonomous execution)
    run_p = subparsers.add_parser("run", help="Single-command: Goal -> Auto-Plan -> Parallel Multi-Agent execution")
    run_p.add_argument("goal", help="Project goal description")
    run_p.add_argument("--name", help="Project name")
    run_p.add_argument("--id", help="Explicit project ID")
    run_p.add_argument("--workspace", help="Workspace root path")
    run_p.add_argument("--accounts", help="Comma-separated candidate accounts (e.g. default,acc1,acc2)")
    run_p.add_argument("--concurrency", type=int, default=4, help="Maximum concurrent agents")
    run_p.add_argument("--model", help="Model to use for planning & orchestrating (default: gemini-3.8-flash)")
    run_p.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="Default effort level for agents (default: medium)")

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

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
    elif args.subcommand == "plan":
        cmd_plan(args, ctx)
    elif args.subcommand == "run":
        cmd_run(args, ctx)


if __name__ == "__main__":
    main()
