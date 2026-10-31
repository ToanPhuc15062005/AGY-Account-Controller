#!/usr/bin/env python3
"""
agy-controller
Unified controller for Google Antigravity CLI (agy).
Manages multi-account authentication, profile configurations (Model, Effort, Turbo Mode),
and execution workflows for Windows (CMD & PowerShell).
"""

import sys
import os
import json
import argparse
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Enable ANSI color support on Windows console
if os.name == "nt":
    os.system("")

# ANSI Color codes
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

ANSI_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def visible_len(s: str) -> int:
    """Return visible string length excluding ANSI escape codes."""
    return len(ANSI_REGEX.sub('', str(s)))

def pad_cell(text: str, width: int, align: str = "left") -> str:
    vlen = visible_len(text)
    pad = max(0, width - vlen)
    if align == "right":
        return " " * pad + text
    elif align == "center":
        left = pad // 2
        right = pad - left
        return " " * left + text + " " * right
    else:
        return text + " " * pad

def print_success(msg):
    print(f"{Style.GREEN}✓{Style.RESET} {msg}")

def print_info(msg):
    print(f"{Style.CYAN}ℹ{Style.RESET} {msg}")

def print_warning(msg):
    print(f"{Style.YELLOW}⚠{Style.RESET} {msg}")

def print_error(msg):
    print(f"{Style.RED}✗{Style.RESET} {msg}", file=sys.stderr)

CREDENTIAL_TARGET = "gemini:antigravity"
CREDENTIAL_USER = "antigravity"

# Storage locations
PROFILES_DIR = Path.home() / ".gemini" / "agy-profiles"
CURRENT_PROFILE_FILE = PROFILES_DIR / ".current_profile"
SETTINGS_FILE = Path.home() / ".gemini" / "antigravity-cli" / "settings.json"

DEFAULT_MODEL = "Gemini 3.8 Flash (Medium)"
DEFAULT_EFFORT = "-"
DEFAULT_MODE = "normal"


# ---------------------------------------------------------------------------
# Windows Credential Manager Implementation (Win32 advapi32.dll)
# ---------------------------------------------------------------------------
if os.name == "nt":
    import ctypes
    from ctypes import wintypes

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", wintypes.FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.c_void_p),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    advapi32 = ctypes.windll.advapi32

    CredRead = advapi32.CredReadW
    CredRead.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
    CredRead.restype = wintypes.BOOL

    CredWrite = advapi32.CredWriteW
    CredWrite.argtypes = [ctypes.POINTER(CREDENTIAL), wintypes.DWORD]
    CredWrite.restype = wintypes.BOOL

    CredDelete = advapi32.CredDeleteW
    CredDelete.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
    CredDelete.restype = wintypes.BOOL

    CredFree = advapi32.CredFree
    CredFree.argtypes = [ctypes.c_void_p]

    def get_credential_raw(target: str = CREDENTIAL_TARGET) -> str | None:
        pcred = ctypes.POINTER(CREDENTIAL)()
        if CredRead(target, 1, 0, ctypes.byref(pcred)):
            try:
                cred = pcred.contents
                raw = bytes(cred.CredentialBlob[:cred.CredentialBlobSize])
                return raw.decode("utf-8")
            finally:
                CredFree(pcred)
        return None

    def set_credential_raw(target: str, user: str, payload_str: str) -> bool:
        data = payload_str.encode("utf-8")
        blob = (ctypes.c_byte * len(data)).from_buffer_copy(data)

        cred = CREDENTIAL()
        cred.Flags = 0
        cred.Type = 1  # CRED_TYPE_GENERIC
        cred.TargetName = target
        cred.Comment = None
        cred.CredentialBlobSize = len(data)
        cred.CredentialBlob = ctypes.cast(blob, ctypes.POINTER(ctypes.c_byte))
        cred.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE
        cred.AttributeCount = 0
        cred.Attributes = None
        cred.TargetAlias = None
        cred.UserName = user

        return bool(CredWrite(ctypes.byref(cred), 0))

    def delete_credential_raw(target: str = CREDENTIAL_TARGET) -> bool:
        return bool(CredDelete(target, 1, 0))

else:
    # Non-Windows fallback
    try:
        import keyring
        def get_credential_raw(target: str = CREDENTIAL_TARGET) -> str | None:
            return keyring.get_password(target, CREDENTIAL_USER)

        def set_credential_raw(target: str, user: str, payload_str: str) -> bool:
            keyring.set_password(target, user, payload_str)
            return True

        def delete_credential_raw(target: str = CREDENTIAL_TARGET) -> bool:
            try:
                keyring.delete_password(target, CREDENTIAL_USER)
                return True
            except Exception:
                return False
    except ImportError:
        def get_credential_raw(target: str = CREDENTIAL_TARGET) -> str | None:
            return None
        def set_credential_raw(target: str, user: str, payload_str: str) -> bool:
            return False
        def delete_credential_raw(target: str = CREDENTIAL_TARGET) -> bool:
            return False


# ---------------------------------------------------------------------------
# Core Helpers
# ---------------------------------------------------------------------------
def ensure_profiles_dir():
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

def get_current_session() -> dict | None:
    raw = get_credential_raw(CREDENTIAL_TARGET)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None

def write_current_session(session_data: dict) -> bool:
    payload = json.dumps(session_data, indent=2)
    return set_credential_raw(CREDENTIAL_TARGET, CREDENTIAL_USER, payload)

def parse_expiry(expiry_str: str | None) -> tuple[datetime | None, str]:
    if not expiry_str:
        return None, "Không xác định"
    try:
        dt = datetime.fromisoformat(expiry_str)
        now = datetime.now(timezone.utc)
        diff = (dt.astimezone(timezone.utc) - now).total_seconds()
        if diff < 0:
            status = f"{Style.RED}Hết hạn ({abs(int(diff // 60))}m trước){Style.RESET}"
        else:
            hours = int(diff // 3600)
            minutes = int((diff % 3600) // 60)
            status = f"{Style.GREEN}Hợp lệ ({hours}h {minutes}m còn lại){Style.RESET}"
        return dt, status
    except Exception:
        return None, expiry_str

def get_active_profile_name() -> str | None:
    if CURRENT_PROFILE_FILE.exists():
        try:
            return CURRENT_PROFILE_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return None

def set_active_profile_name(name: str):
    ensure_profiles_dir()
    CURRENT_PROFILE_FILE.write_text(name, encoding="utf-8")

def update_antigravity_settings(model: str | None):
    """Sync model choice to Antigravity settings.json so agy uses it directly."""
    if not model or not SETTINGS_FILE.exists():
        return
    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        data["model"] = model
        SETTINGS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass

def get_sorted_profiles() -> list[Path]:
    ensure_profiles_dir()
    return sorted(PROFILES_DIR.glob("*.json"), key=lambda x: x.stem.lower())

def resolve_profile(target_str: str) -> tuple[Path | None, int | None]:
    """Resolve a profile by STT index (1, 2, ...), profile name, or email."""
    profiles = get_sorted_profiles()
    if not profiles:
        return None, None

    # 1. By numeric STT
    if target_str.isdigit():
        idx = int(target_str)
        if 1 <= idx <= len(profiles):
            return profiles[idx - 1], idx

    # 2. By exact profile stem
    for i, p in enumerate(profiles, start=1):
        if p.stem.lower() == target_str.lower():
            return p, i

    # 3. By partial or email match
    matches = []
    for i, p in enumerate(profiles, start=1):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            email = d.get("session", {}).get("id_token_email", "")
            meta_email = d.get("_meta", {}).get("email", "")
            if target_str.lower() in p.stem.lower() or target_str.lower() in email.lower() or target_str.lower() in meta_email.lower():
                matches.append((p, i))
        except Exception:
            continue

    if len(matches) == 1:
        return matches[0]

    return None, None


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------
def cmd_current(args):
    """Show the currently active Antigravity account."""
    session = get_current_session()
    if not session:
        print_warning("Không tìm thấy phiên Antigravity nào đang hoạt động trong Credential Manager.")
        print(f"Gợi ý: Dùng {Style.BOLD}agy-controller login{Style.RESET} để đăng nhập.")
        return

    email = session.get("id_token_email", "Unknown")
    auth_method = session.get("auth_method", "Unknown")
    token = session.get("token", {})
    expiry_str = token.get("expiry")
    has_refresh = bool(token.get("refresh_token"))
    _, expiry_status = parse_expiry(expiry_str)

    active_name = get_active_profile_name()
    meta = {}
    if active_name:
        p_path = PROFILES_DIR / f"{active_name}.json"
        if p_path.exists():
            try:
                meta = json.loads(p_path.read_text(encoding="utf-8")).get("_meta", {})
            except Exception:
                pass

    model = meta.get("model", DEFAULT_MODEL)
    effort = meta.get("effort", DEFAULT_EFFORT)
    mode = meta.get("mode", DEFAULT_MODE)
    mode_display = f"{Style.YELLOW}{Style.BOLD}turbo (dangerously-skip-permissions){Style.RESET}" if mode == "turbo" else "normal"

    print(f"\n{Style.BOLD}Phiên Antigravity hiện tại:{Style.RESET}")
    print(f"  Tên Profile    : {Style.CYAN}{active_name or '(Chưa gán profile)'}{Style.RESET}")
    print(f"  Google Email   : {Style.GREEN}{email}{Style.RESET}")
    print(f"  Model          : {Style.CYAN}{model}{Style.RESET}")
    print(f"  Effort         : {effort}")
    print(f"  Mode           : {mode_display}")
    print(f"  Access Token   : {expiry_status}")
    print(f"  Refresh Token  : {'Có sẵn ✓' if has_refresh else 'Thiếu ✗'}")
    print(f"  Lưu trữ        : {CREDENTIAL_TARGET}\n")


def cmd_list(args):
    """List all saved profiles in a dynamic table."""
    profiles = get_sorted_profiles()

    if not profiles:
        print_info("Chưa có tài khoản nào được lưu.")
        print(f"Lưu tài khoản hiện tại với: {Style.BOLD}agy-controller save <tên_profile>{Style.RESET}")
        return

    current_session = get_current_session()
    active_email = current_session.get("id_token_email") if current_session else None
    active_profile_name = get_active_profile_name()

    headers = ["STT", "Tài khoản", "Model", "Effort", "Mode"]
    rows = []

    for i, p in enumerate(profiles, start=1):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            session = data.get("session", {})
            meta = data.get("_meta", {})
            email = session.get("id_token_email", meta.get("email", "Unknown"))
            model = meta.get("model", DEFAULT_MODEL)
            effort = meta.get("effort", DEFAULT_EFFORT)
            mode = meta.get("mode", DEFAULT_MODE)

            is_active = (p.stem == active_profile_name) or (email == active_email and not active_profile_name)
            
            # Format STT
            stt_str = f"{i}*" if is_active else str(i)
            stt_display = f"{Style.GREEN}{Style.BOLD}{stt_str:>3}{Style.RESET}" if is_active else f"{stt_str:>3}"

            # Format Account
            acc_raw = f"{p.stem} ({email})"
            acc_display = f"{Style.CYAN}{Style.BOLD}{acc_raw}{Style.RESET}" if is_active else acc_raw

            # Format Model
            model_display = f"{Style.WHITE}{model}{Style.RESET}"

            # Format Effort
            effort_display = f"{Style.CYAN}{effort}{Style.RESET}"

            # Format Mode
            if mode.lower() == "turbo":
                mode_display = f"{Style.YELLOW}{Style.BOLD}turbo{Style.RESET} {Style.DIM}(skip-perm){Style.RESET}"
            else:
                mode_display = f"{Style.DIM}normal{Style.RESET}"

            rows.append({
                "stt": stt_display,
                "acc": acc_display,
                "model": model_display,
                "effort": effort_display,
                "mode": mode_display,
                "is_active": is_active
            })
        except Exception as e:
            rows.append({
                "stt": str(i),
                "acc": f"{p.stem} [Lỗi: {e}]",
                "model": "Unknown",
                "effort": "Unknown",
                "mode": "Unknown",
                "is_active": False
            })

    # Calculate dynamic column widths based on maximum visible length
    keys = ["stt", "acc", "model", "effort", "mode"]
    widths = []
    for h, k in zip(headers, keys):
        max_v = len(h)
        for r in rows:
            max_v = max(max_v, visible_len(r[k]))
        widths.append(max_v + 2)

    # Box Drawing Borders
    top_border = "┌" + "┬".join("─" * w for w in widths) + "┐"
    header_sep = "├" + "┼".join("─" * w for w in widths) + "┤"
    bottom_border = "└" + "┴".join("─" * w for w in widths) + "┘"

    header_cells = [pad_cell(f" {h} ", w, "center") for h, w in zip(headers, widths)]
    header_line = "│" + "│".join(header_cells) + "│"

    print(f"\n{Style.BOLD}Danh sách tài khoản Antigravity:{Style.RESET}\n")
    print(top_border)
    print(f"{Style.BOLD}{header_line}{Style.RESET}")
    print(header_sep)

    for r in rows:
        row_cells = [
            pad_cell(f" {r['stt']} ", widths[0], "center"),
            pad_cell(f" {r['acc']} ", widths[1], "left"),
            pad_cell(f" {r['model']} ", widths[2], "left"),
            pad_cell(f" {r['effort']} ", widths[3], "center"),
            pad_cell(f" {r['mode']} ", widths[4], "left"),
        ]
        print("│" + "│".join(row_cells) + "│")

    print(bottom_border)
    print(f"\n  {Style.GREEN}*{Style.RESET} : Tài khoản đang kích hoạt (Active)")
    print(f"  {Style.CYAN}Chuyển nhanh theo STT{Style.RESET} : {Style.BOLD}agy-controller switch <STT>{Style.RESET}  (VD: {Style.CYAN}agy-controller switch 2{Style.RESET})")
    print(f"  {Style.CYAN}Chạy và đổi cấu hình{Style.RESET} : {Style.BOLD}agy-controller run [STT] [--mode normal|turbo] [--model ...]{Style.RESET}")
    print(f"  {Style.CYAN}Chỉnh sửa cấu hình{Style.RESET}   : {Style.BOLD}agy-controller config <STT> [--mode normal|turbo] [--model ...]{Style.RESET}\n")


def cmd_switch(args):
    """Switch to a saved profile by STT, profile name, or email."""
    profile_path, stt = resolve_profile(args.name)

    if not profile_path or not profile_path.exists():
        profiles = get_sorted_profiles()
        print_error(f"Không tìm thấy tài khoản '{args.name}'.")
        print(f"Tài khoản có sẵn: {Style.BOLD}{', '.join(f'{i}:{p.stem}' for i, p in enumerate(profiles, 1)) or 'Chưa có'}{Style.RESET}")
        print(f"Gợi ý: Dùng số STT: {Style.BOLD}agy-controller switch 1{Style.RESET}")
        sys.exit(1)

    profile_name = profile_path.stem

    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
        session = data.get("session", {})
        meta = data.get("_meta", {})
    except Exception as e:
        print_error(f"Lỗi đọc dữ liệu profile: {e}")
        sys.exit(1)

    if not session:
        print_error("Dữ liệu session trong profile rỗng.")
        sys.exit(1)

    success = write_current_session(session)
    if not success:
        print_error("Không thể ghi thông tin vào Windows Credential Manager.")
        sys.exit(1)

    set_active_profile_name(profile_name)
    email = session.get("id_token_email", meta.get("email", "Unknown"))
    model = meta.get("model", DEFAULT_MODEL)
    effort = meta.get("effort", DEFAULT_EFFORT)
    mode = meta.get("mode", DEFAULT_MODE)

    # Sync model to settings.json
    update_antigravity_settings(model)

    print_success(f"Đã chuyển sang [{stt}] '{Style.CYAN}{profile_name}{Style.RESET}' ({Style.BOLD}{email}{Style.RESET})")
    print(f"  Model  : {Style.CYAN}{model}{Style.RESET}")
    print(f"  Effort : {effort}")
    if mode == "turbo":
        print(f"  Mode   : {Style.YELLOW}{Style.BOLD}turbo{Style.RESET} (--dangerously-skip-permissions)")
    else:
        print(f"  Mode   : normal")
    print()


def cmd_run(args):
    """Run agy with the active or specified profile's configured model, effort, and mode.
    If --model, --effort, or --mode are provided, saves them to the profile first.
    """
    target = None
    if hasattr(args, "extra_args") and args.extra_args:
        first = args.extra_args[0]
        if not first.startswith("-"):
            p_test, _ = resolve_profile(first)
            if p_test:
                target = args.extra_args.pop(0)

    # 1. Determine profile path
    if target:
        profile_path, stt = resolve_profile(target)
        # Switch to this profile if not already active
        if get_active_profile_name() != profile_path.stem:
            try:
                data = json.loads(profile_path.read_text(encoding="utf-8"))
                session = data.get("session", {})
                write_current_session(session)
                set_active_profile_name(profile_path.stem)
                print_info(f"Đã chuyển sang [{stt}] '{profile_path.stem}'")
            except Exception as e:
                print_error(f"Lỗi khi chuyển tài khoản: {e}")
                sys.exit(1)
    else:
        active_name = get_active_profile_name()
        if not active_name:
            profiles = get_sorted_profiles()
            if profiles:
                profile_path = profiles[0]
                set_active_profile_name(profile_path.stem)
                data = json.loads(profile_path.read_text(encoding="utf-8"))
                write_current_session(data.get("session", {}))
                print_info(f"Tự động chọn tài khoản đầu tiên: '{profile_path.stem}'")
            else:
                print_error("Chưa có tài khoản nào được lưu. Hãy đăng nhập với 'agy-controller login' trước.")
                sys.exit(1)
        else:
            profile_path = PROFILES_DIR / f"{active_name}.json"
            if not profile_path.exists():
                print_error(f"Không tìm thấy file profile của tài khoản '{active_name}'.")
                sys.exit(1)

    # 2. Load profile data
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception as e:
        print_error(f"Lỗi đọc file profile: {e}")
        sys.exit(1)

    meta = data.setdefault("_meta", {})
    changed = False

    # 3. Update & Save configuration if any config flags provided
    if getattr(args, "model", None):
        meta["model"] = args.model
        changed = True

    if getattr(args, "effort", None):
        meta["effort"] = args.effort.lower()
        changed = True

    if getattr(args, "mode", None):
        meta["mode"] = args.mode.lower()
        changed = True

    if changed:
        profile_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print_success(f"Đã lưu cấu hình mới cho '{profile_path.stem}': Model={meta.get('model', DEFAULT_MODEL)} | Effort={meta.get('effort', DEFAULT_EFFORT)} | Mode={meta.get('mode', DEFAULT_MODE)}")

    model = meta.get("model", DEFAULT_MODEL)
    effort = meta.get("effort", DEFAULT_EFFORT)
    mode = meta.get("mode", DEFAULT_MODE)

    # Sync model to settings.json
    update_antigravity_settings(model)

    # 4. Build command line
    agy_binary = shutil.which("agy") or "agy"
    cmd_args = [agy_binary]

    if model:
        cmd_args.extend(["--model", model])
    if effort and effort.lower() not in ("-", "default", "none"):
        # agy rejects --effort on models with fixed effort in name like Gemini 3.8 Flash (Medium)
        if not any(f"({e.lower()})" in model.lower() for e in ["low", "medium", "high", "xhigh", "max"]):
            cmd_args.extend(["--effort", effort])
    if mode.lower() == "turbo":
        cmd_args.append("--dangerously-skip-permissions")

    # Pass through any extra arguments
    if hasattr(args, "extra_args") and args.extra_args:
        cmd_args.extend(args.extra_args)

    mode_note = f"{Style.YELLOW}{Style.BOLD}turbo{Style.RESET} (bỏ qua xác nhận quyền)" if mode.lower() == "turbo" else "normal"
    print_info(f"Chạy agy: Tài khoản={Style.CYAN}{profile_path.stem}{Style.RESET} | Model={model} | Effort={effort} | Mode={mode_note}")
    print(f"{Style.DIM}Lệnh thực thi: {' '.join(cmd_args)}{Style.RESET}\n")

    try:
        subprocess.run(cmd_args, shell=(os.name == "nt"))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print_error(f"Không thể khởi chạy agy: {e}")


def cmd_config(args):
    """Configure model, effort, or mode for a profile."""
    profile_path, stt = resolve_profile(args.target)
    if not profile_path or not profile_path.exists():
        print_error(f"Không tìm thấy tài khoản '{args.target}'. Dùng 'agy-controller list' để xem STT/Tên.")
        sys.exit(1)

    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception as e:
        print_error(f"Lỗi đọc file profile: {e}")
        sys.exit(1)

    meta = data.setdefault("_meta", {})
    changed = False

    if args.model:
        meta["model"] = args.model
        changed = True
        if get_active_profile_name() == profile_path.stem:
            update_antigravity_settings(args.model)

    if args.effort:
        valid_efforts = ["low", "medium", "high", "xhigh", "max"]
        if args.effort.lower() not in valid_efforts:
            print_error(f"Effort không hợp lệ. Chọn một trong: {', '.join(valid_efforts)}")
            sys.exit(1)
        meta["effort"] = args.effort.lower()
        changed = True

    if args.mode:
        valid_modes = ["normal", "turbo"]
        if args.mode.lower() not in valid_modes:
            print_error(f"Mode không hợp lệ. Chọn một trong: normal, turbo")
            sys.exit(1)
        meta["mode"] = args.mode.lower()
        changed = True

    if not changed:
        print_info("Không có thay đổi nào được chỉ định.")
        print("Tùy chọn: --model <model>  |  --effort <effort>  |  --mode normal|turbo")
        return

    profile_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print_success(f"Đã cập nhật cấu hình cho [{stt}] '{Style.CYAN}{profile_path.stem}{Style.RESET}':")
    print(f"  Model  : {meta.get('model', DEFAULT_MODEL)}")
    print(f"  Effort : {meta.get('effort', DEFAULT_EFFORT)}")
    print(f"  Mode   : {meta.get('mode', DEFAULT_MODE)}")


def cmd_save(args):
    """Save the current session as a named profile."""
    session = get_current_session()
    if not session:
        print_error("Không có phiên Antigravity nào đang hoạt động để lưu. Vui lòng đăng nhập với 'agy' trước.")
        sys.exit(1)

    email = session.get("id_token_email")
    if not email:
        print_error("Dữ liệu session thiếu 'id_token_email'.")
        sys.exit(1)

    profile_name = args.name
    if not profile_name:
        profile_name = email.split("@")[0].lower().replace(".", "_")

    ensure_profiles_dir()
    profile_path = PROFILES_DIR / f"{profile_name}.json"

    if profile_path.exists() and not args.force:
        print_warning(f"Profile '{profile_name}' đã tồn tại.")
        print(f"Dùng {Style.BOLD}--force{Style.RESET} hoặc {Style.BOLD}-f{Style.RESET} để ghi đè.")
        sys.exit(1)

    existing_meta = {}
    if profile_path.exists():
        try:
            existing_meta = json.loads(profile_path.read_text(encoding="utf-8")).get("_meta", {})
        except Exception:
            pass

    save_data = {
        "_meta": {
            "profile_name": profile_name,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "email": email,
            "model": getattr(args, "model", None) or existing_meta.get("model", DEFAULT_MODEL),
            "effort": getattr(args, "effort", None) or existing_meta.get("effort", DEFAULT_EFFORT),
            "mode": getattr(args, "mode", None) or existing_meta.get("mode", DEFAULT_MODE),
        },
        "session": session
    }

    profile_path.write_text(json.dumps(save_data, indent=2), encoding="utf-8")
    set_active_profile_name(profile_name)
    update_antigravity_settings(save_data["_meta"]["model"])

    print_success(f"Đã lưu session cho {Style.BOLD}{email}{Style.RESET} thành profile '{Style.CYAN}{profile_name}{Style.RESET}'")
    print(f"  Model : {save_data['_meta']['model']} | Effort: {save_data['_meta']['effort']} | Mode: {save_data['_meta']['mode']}")
    print(f"  File  : {profile_path}")


def cmd_login(args):
    """Log into a Google account via agy and save it as a profile."""
    old_session = get_current_session()
    old_email = old_session.get("id_token_email") if old_session else None

    # Auto-preserve old session if not yet saved
    if old_session and old_email:
        ensure_profiles_dir()
        is_saved = any(
            json.loads(p.read_text(encoding="utf-8")).get("session", {}).get("id_token_email") == old_email
            for p in PROFILES_DIR.glob("*.json")
            if p.is_file()
        )
        if not is_saved:
            default_old_name = old_email.split("@")[0].lower().replace(".", "_")
            print_info(f"Tự động sao lưu tài khoản hiện tại '{old_email}' thành profile '{default_old_name}'...")
            save_data = {
                "_meta": {
                    "profile_name": default_old_name,
                    "saved_at": datetime.now(timezone.utc).isoformat(),
                    "email": old_email,
                },
                "session": old_session
            }
            (PROFILES_DIR / f"{default_old_name}.json").write_text(json.dumps(save_data, indent=2), encoding="utf-8")
            print_success(f"Tài khoản cũ đã được lưu an toàn thành '{default_old_name}'.")

    # Clear credential
    print_info("Chuẩn bị phiên đăng nhập mới...")
    delete_credential_raw(CREDENTIAL_TARGET)
    if CURRENT_PROFILE_FILE.exists():
        CURRENT_PROFILE_FILE.unlink()

    # Launch agy
    agy_cmd = shutil.which("agy") or "agy"
    print_info(f"Khởi chạy '{agy_cmd}' để xác thực Google...")
    print(f"{Style.DIM}>>> Hãy hoàn tất đăng nhập trong trình duyệt, sau đó quay lại terminal này <<<{Style.RESET}\n")

    try:
        subprocess.run([agy_cmd], shell=(os.name == "nt"))
    except KeyboardInterrupt:
        print("\nĐã hủy đăng nhập.")
    except Exception as e:
        print_error(f"Không thể khởi chạy agy: {e}")

    # Check new credential
    new_session = get_current_session()
    if not new_session:
        print_warning("Không phát hiện phiên đăng nhập mới nào.")
        if old_session:
            print_info("Đang phục hồi lại phiên trước đó...")
            write_current_session(old_session)
        return

    new_email = new_session.get("id_token_email", "Unknown")
    print_success(f"\nĐăng nhập thành công với: {Style.BOLD}{new_email}{Style.RESET}")

    profile_name = args.name
    if not profile_name:
        profile_name = new_email.split("@")[0].lower().replace(".", "_")

    ensure_profiles_dir()
    profile_path = PROFILES_DIR / f"{profile_name}.json"
    save_data = {
        "_meta": {
            "profile_name": profile_name,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "email": new_email,
        },
        "session": new_session
    }
    profile_path.write_text(json.dumps(save_data, indent=2), encoding="utf-8")
    set_active_profile_name(profile_name)

    print_success(f"Đã lưu tài khoản mới thành profile '{Style.CYAN}{profile_name}{Style.RESET}'")
    print(f"Chuyển qua lại dễ dàng với: {Style.BOLD}agy-controller switch {profile_name}{Style.RESET}\n")


def cmd_logout(args):
    """Log out of Antigravity by clearing active credentials."""
    current = get_current_session()
    if not current:
        print_info("Không có phiên Antigravity nào đang hoạt động.")
        return

    email = current.get("id_token_email", "Unknown")

    ensure_profiles_dir()
    saved_profiles = []
    for p in PROFILES_DIR.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if d.get("session", {}).get("id_token_email") == email:
                saved_profiles.append(p.stem)
        except Exception:
            pass

    if not saved_profiles and not args.force:
        print_warning(f"Tài khoản '{email}' CHƯA được lưu vào bất kỳ profile nào!")
        confirm = input("Bạn có chắc chắn muốn đăng xuất không? (y/N): ").strip().lower()
        if confirm != "y":
            print_info("Đã hủy đăng xuất. Hãy chạy 'agy-controller save <tên>' trước.")
            return

    success = delete_credential_raw(CREDENTIAL_TARGET)
    if success:
        if CURRENT_PROFILE_FILE.exists():
            CURRENT_PROFILE_FILE.unlink()
        print_success(f"Đã đăng xuất. Xóa phiên của '{email}' khỏi Credential Manager.")
        if saved_profiles:
            print(f"  Lưu ý: Profile '{', '.join(saved_profiles)}' vẫn được lưu trữ an toàn. Dùng 'agy-controller switch {saved_profiles[0]}' để kích hoạt lại bất kỳ lúc nào.")
        else:
            print(f"  Chạy {Style.BOLD}agy{Style.RESET} hoặc {Style.BOLD}agy-controller login{Style.RESET} để đăng nhập lại.")
    else:
        print_error("Không thể xóa thông tin đăng nhập khỏi Credential Manager.")


def cmd_delete(args):
    """Delete a saved profile."""
    profile_path, stt = resolve_profile(args.name)
    if not profile_path or not profile_path.exists():
        print_error(f"Profile '{args.name}' không tồn tại.")
        sys.exit(1)

    name = profile_path.stem
    profile_path.unlink()
    if get_active_profile_name() == name:
        if CURRENT_PROFILE_FILE.exists():
            CURRENT_PROFILE_FILE.unlink()

    print_success(f"Đã xóa profile '{name}'.")


def cmd_rename(args):
    """Rename a profile."""
    profile_path, stt = resolve_profile(args.old_name)
    if not profile_path or not profile_path.exists():
        print_error(f"Profile '{args.old_name}' không tồn tại.")
        sys.exit(1)

    dst = PROFILES_DIR / f"{args.new_name}.json"
    if dst.exists() and not args.force:
        print_error(f"Profile '{args.new_name}' đã tồn tại. Dùng --force để ghi đè.")
        sys.exit(1)

    data = json.loads(profile_path.read_text(encoding="utf-8"))
    data.setdefault("_meta", {})["profile_name"] = args.new_name
    dst.write_text(json.dumps(data, indent=2), encoding="utf-8")
    profile_path.unlink()

    if get_active_profile_name() == profile_path.stem:
        set_active_profile_name(args.new_name)

    print_success(f"Đã đổi tên profile '{profile_path.stem}' thành '{args.new_name}'")


# ---------------------------------------------------------------------------
# Installer & System Integration
# ---------------------------------------------------------------------------
def get_best_bin_dir() -> Path:
    """Find the best directory that is already in user PATH (where agy.exe lives)."""
    agy_path = shutil.which("agy")
    if agy_path:
        return Path(agy_path).parent

    local_agy = Path.home() / "AppData" / "Local" / "agy" / "bin"
    if local_agy.exists():
        return local_agy

    gemini_bin = Path.home() / ".gemini" / "antigravity-cli" / "bin"
    gemini_bin.mkdir(parents=True, exist_ok=True)
    return gemini_bin

def cmd_install(args):
    """Install unified agy-controller into user's PATH directory and clean up legacy wrappers."""
    bin_dirs = [get_best_bin_dir(), Path.home() / ".gemini" / "antigravity-cli" / "bin"]
    unique_dirs = []
    for d in bin_dirs:
        if d not in unique_dirs:
            unique_dirs.append(d)

    script_path = Path(__file__).resolve()

    # Legacy files to clean up
    legacy_files = ["agy-acc.cmd", "agy-acc.ps1", "agy-switch.cmd", "agy-switch.ps1", "agy-run.cmd", "agy-run.ps1"]

    for bin_dir in unique_dirs:
        bin_dir.mkdir(parents=True, exist_ok=True)

        # 1. Clean legacy wrappers
        for lf in legacy_files:
            old_f = bin_dir / lf
            if old_f.exists():
                old_f.unlink()

        # 2. Install unified command: agy-controller
        (bin_dir / "agy-controller.cmd").write_text(f'@echo off\npython "{script_path}" %*\n', encoding="utf-8")
        (bin_dir / "agy-controller.ps1").write_text(f'& python "{script_path}" @args\n', encoding="utf-8")

    print_success("Đã cài đặt thống nhất lệnh 'agy-controller' vào các thư mục PATH:")
    for d in unique_dirs:
        print(f"  Thư mục: {d}")
    print(f"\nLệnh khả dụng duy nhất: {Style.BOLD}{Style.CYAN}agy-controller{Style.RESET}")
    print(f"Bạn có thể gõ {Style.CYAN}agy-controller list{Style.RESET} hoặc {Style.CYAN}agy-controller run{Style.RESET} ở bất kỳ đâu trong CMD hoặc PowerShell!\n")

def cmd_uninstall(args):
    """Remove CLI wrappers from user's agy bin folder."""
    bin_dirs = [get_best_bin_dir(), Path.home() / ".gemini" / "antigravity-cli" / "bin"]
    files = [
        "agy-controller.cmd", "agy-controller.ps1",
        "agy-acc.cmd", "agy-acc.ps1",
        "agy-switch.cmd", "agy-switch.ps1",
        "agy-run.cmd", "agy-run.ps1"
    ]
    removed = 0
    for b in set(bin_dirs):
        for f in files:
            target = b / f
            if target.exists():
                target.unlink()
                removed += 1
    print_success(f"Đã gỡ bỏ {removed} file wrapper khỏi hệ thống.")


# ---------------------------------------------------------------------------
# Argument Parser
# ---------------------------------------------------------------------------
def main():
    # If first argument is just a number (e.g.: agy-controller 1), treat as `switch 1`
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        sys.argv.insert(1, "switch")

    parser = argparse.ArgumentParser(
        prog="agy-controller",
        description=f"{Style.BOLD}Antigravity Controller (agy-controller){Style.RESET}\nTrình điều khiển và quản lý phiên làm việc duy nhất cho Antigravity CLI.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Các lệnh có sẵn")

    # list
    p_list = subparsers.add_parser("list", aliases=["ls"], help="Xem bảng động danh sách tài khoản, Model, Effort, Mode")
    p_list.set_defaults(func=cmd_list)

    # switch
    p_switch = subparsers.add_parser("switch", aliases=["use"], help="Chuyển tài khoản (theo STT, tên hoặc email)")
    p_switch.add_argument("name", help="Số STT (1, 2, ...), tên profile hoặc email")
    p_switch.set_defaults(func=cmd_switch)

    # run
    p_run = subparsers.add_parser("run", help="Chạy agy (có thể kèm STT, đổi Model, Effort, Mode và tự động lưu)")
    p_run.add_argument("--model", help="Cập nhật Model (VD: 'Gemini 3.8 Flash (High)')")
    p_run.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="Cập nhật Effort")
    p_run.add_argument("--mode", choices=["normal", "turbo"], help="Cập nhật Mode: normal hoặc turbo (--dangerously-skip-permissions)")
    p_run.set_defaults(func=cmd_run)

    # config
    p_cfg = subparsers.add_parser("config", aliases=["cfg", "set"], help="Cấu hình Model, Effort, Mode cho tài khoản")
    p_cfg.add_argument("target", help="Số STT hoặc tên profile")
    p_cfg.add_argument("--model", help="Tên Model")
    p_cfg.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="Mức Effort")
    p_cfg.add_argument("--mode", choices=["normal", "turbo"], help="Mode: normal hoặc turbo")
    p_cfg.set_defaults(func=cmd_config)

    # login
    p_login = subparsers.add_parser("login", help="Đăng nhập tài khoản Google mới và lưu profile")
    p_login.add_argument("name", nargs="?", help="Tên profile muốn đặt cho tài khoản mới")
    p_login.set_defaults(func=cmd_login)

    # logout
    p_logout = subparsers.add_parser("logout", help="Đăng xuất khỏi tài khoản hiện tại")
    p_logout.add_argument("-f", "--force", action="store_true", help="Bắt buộc đăng xuất dù chưa lưu profile")
    p_logout.set_defaults(func=cmd_logout)

    # save
    p_save = subparsers.add_parser("save", aliases=["add"], help="Lưu phiên đăng nhập hiện tại thành profile")
    p_save.add_argument("name", nargs="?", help="Tên profile (mặc định lấy theo email)")
    p_save.add_argument("--model", help="Model mặc định")
    p_save.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="Effort mặc định")
    p_save.add_argument("--mode", choices=["normal", "turbo"], help="Mode: normal hoặc turbo")
    p_save.add_argument("-f", "--force", action="store_true", help="Ghi đè nếu profile đã tồn tại")
    p_save.set_defaults(func=cmd_save)

    # current / whoami
    p_curr = subparsers.add_parser("current", aliases=["whoami", "status"], help="Xem chi tiết tài khoản hiện tại")
    p_curr.set_defaults(func=cmd_current)

    # delete
    p_del = subparsers.add_parser("delete", aliases=["rm"], help="Xóa profile")
    p_del.add_argument("name", help="Số STT hoặc tên profile cần xóa")
    p_del.set_defaults(func=cmd_delete)

    # rename
    p_ren = subparsers.add_parser("rename", aliases=["mv"], help="Đổi tên profile")
    p_ren.add_argument("old_name", help="Tên profile hiện tại hoặc STT")
    p_ren.add_argument("new_name", help="Tên profile mới")
    p_ren.add_argument("-f", "--force", action="store_true", help="Ghi đè nếu tên mới đã tồn tại")
    p_ren.set_defaults(func=cmd_rename)

    # install
    p_inst = subparsers.add_parser("install", help="Cài đặt lệnh thống nhất agy-controller vào PATH")
    p_inst.set_defaults(func=cmd_install)

    # uninstall
    p_uninst = subparsers.add_parser("uninstall", help="Gỡ cài đặt agy-controller khỏi PATH")
    p_uninst.set_defaults(func=cmd_uninstall)

    args, extra_args = parser.parse_known_args()
    args.extra_args = extra_args

    if not args.command:
        # Default behavior: show current info and list table
        cmd_current(args)
        cmd_list(args)
        return

    args.func(args)

if __name__ == "__main__":
    main()
