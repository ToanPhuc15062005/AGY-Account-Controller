#!/usr/bin/env python3
"""
agy-controller
Unified controller and interactive TUI for Google Antigravity CLI (agy).
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
import time
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
AUTH_LOCK_FILE = PROFILES_DIR / ".auth_switch.lock"

# Mutex / File lock for safe concurrent credential switching
class CredentialSwitchLock:
    """Inter-process lock to prevent race conditions during credential switching."""
    def __init__(self, lock_file: Path = AUTH_LOCK_FILE, timeout: float = 30.0):
        self.lock_file = lock_file
        self.timeout = timeout
        self.handle = None

    def acquire(self):
        ensure_profiles_dir()
        start = time.time()
        while True:
            try:
                # Exclusive file creation acts as a clean atomic lock on Windows & POSIX
                if os.name == "nt":
                    import msvcrt
                    self.handle = open(self.lock_file, "a+b")
                    msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    self.handle = open(self.lock_file, "a+b")
                    fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except (IOError, OSError, BlockingIOError):
                if self.handle:
                    try:
                        self.handle.close()
                    except Exception:
                        pass
                    self.handle = None
                if time.time() - start > self.timeout:
                    raise TimeoutError("Hết thời gian chờ khóa đồng bộ Credential Manager.")
                time.sleep(0.05)

    def release(self):
        if self.handle:
            try:
                if os.name == "nt":
                    import msvcrt
                    self.handle.seek(0)
                    msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.handle, fcntl.LOCK_UN)
            except Exception:
                pass
            finally:
                try:
                    self.handle.close()
                except Exception:
                    pass
                self.handle = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

DEFAULT_MODEL = "gemini-3.8-flash"
DEFAULT_EFFORT = "medium"
DEFAULT_MODE = "normal"

AVAILABLE_MODELS = [
    "gemini-3.8-flash",
    "claude-sonnet-4-6",
    "claude-opus-4-6-thinking",
    "gpt-oss-120b-medium"
]

AVAILABLE_EFFORTS = [
    "low",
    "medium",
    "high",
    "xhigh",
    "max"
]

AVAILABLE_MODES = [
    "normal",
    "turbo"
]

def normalize_model_and_effort(model_raw: str | None, effort_raw: str | None) -> tuple[str, str]:
    """Tách biệt hoàn toàn Model và Effort thành 2 tham số riêng rẽ."""
    model_str = (model_raw or DEFAULT_MODEL).strip()
    effort_str = (effort_raw or DEFAULT_EFFORT).strip()

    m_low = model_str.lower()
    if "gemini" in m_low and "3.8" in m_low:
        clean_model = "gemini-3.8-flash"
        if "low" in m_low: clean_effort = "low"
        elif "high" in m_low: clean_effort = "high"
        elif "medium" in m_low: clean_effort = "medium"
        else: clean_effort = effort_str if effort_str in AVAILABLE_EFFORTS else "medium"
    elif "sonnet" in m_low:
        clean_model = "claude-sonnet-4-6"
        clean_effort = effort_str if effort_str in AVAILABLE_EFFORTS else "medium"
    elif "opus" in m_low:
        clean_model = "claude-opus-4-6-thinking"
        clean_effort = effort_str if effort_str in AVAILABLE_EFFORTS else "medium"
    elif "gpt-oss" in m_low:
        clean_model = "gpt-oss-120b-medium"
        clean_effort = effort_str if effort_str in AVAILABLE_EFFORTS else "medium"
    else:
        clean_model = model_str if model_str in AVAILABLE_MODELS else DEFAULT_MODEL
        clean_effort = effort_str if effort_str in AVAILABLE_EFFORTS else "medium"

    return clean_model, clean_effort

TUI_BUTTONS = ["Refresh", "Add", "Edit", "Search", "Delete", "Exit"]


# ---------------------------------------------------------------------------
# Windows Keyboard Input Handling (msvcrt)
# ---------------------------------------------------------------------------
if os.name == "nt":
    import msvcrt

    def read_input_key():
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):
            ch2 = msvcrt.getwch()
            if ch2 == 'H': return 'UP'
            if ch2 == 'P': return 'DOWN'
            if ch2 == 'K': return 'LEFT'
            if ch2 == 'M': return 'RIGHT'
            return 'EXT_' + ch2
        if ch == '\r': return 'ENTER'
        if ch == '\x1b': return 'ESC'
        if ch == '\x08': return 'BACKSPACE'
        if ch == '\t': return 'TAB'
        return ch
else:
    def read_input_key():
        return sys.stdin.read(1)


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
# View Formats (Mẫu 1 & Mẫu 2 & Dynamic Table)
# ---------------------------------------------------------------------------
def format_account_details(profile_path: Path) -> list[str]:
    """Mẫu hiển thị 1: Chi tiết tài khoản."""
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
        session = data.get("session", {})
        meta = data.get("_meta", {})
        email = session.get("id_token_email", meta.get("email", "Unknown"))
        model, effort = normalize_model_and_effort(meta.get("model"), meta.get("effort"))
        mode = meta.get("mode", DEFAULT_MODE)
        token = session.get("token", {})
        expiry_str = token.get("expiry")
        has_refresh = bool(token.get("refresh_token"))
        _, expiry_status = parse_expiry(expiry_str)
        mode_display = "turbo (dangerously-skip-permissions)" if mode == "turbo" else "normal"

        return [
            f"Tên Profile    : {profile_path.stem}",
            f"\tGoogle Email   : {email}",
            f"\tModel          : {model}",
            f"\tEffort         : {effort}",
            f"\tMode           : {mode_display}",
            f"\tAccess Token   : {expiry_status}",
            f"\tRefresh Token  : {'Có sẵn ✓' if has_refresh else 'Thiếu ✗'}",
            f"\tLưu trữ        : {CREDENTIAL_TARGET}"
        ]
    except Exception as e:
        return [f"  Lỗi đọc profile: {e}"]

def format_search_box(query: str) -> list[str]:
    """Mẫu hiển thị 2: Dòng nhập tìm kiếm Gmail/Tên."""
    line = "─" * 61
    return [
        f"{line}",
        f"> {query}",
        f"{line}"
    ]

def build_table_lines(profiles: list[Path], active_profile_name: str | None, active_email: str | None, selected_idx: int | None = None, is_row_focused: bool = False) -> list[str]:
    """Tạo bảng động STT, Tài khoản, Model, Effort, Mode."""
    if not profiles:
        return ["  [Chưa có tài khoản nào phù hợp]"]

    headers = ["STT", "Tài khoản", "Model", "Effort", "Mode"]
    rows = []

    for i, p in enumerate(profiles, start=1):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            session = data.get("session", {})
            meta = data.get("_meta", {})
            email = session.get("id_token_email", meta.get("email", "Unknown"))
            model, effort = normalize_model_and_effort(meta.get("model"), meta.get("effort"))
            mode = meta.get("mode", DEFAULT_MODE)

            is_active = (p.stem == active_profile_name) or (email == active_email and not active_profile_name)
            is_cursor = (selected_idx is not None and (i - 1) == selected_idx)
            
            # Format STT with cursor indicator
            base_stt = f"{i}*" if is_active else str(i)
            if is_cursor and is_row_focused:
                stt_str = f"> {base_stt}"
            else:
                stt_str = f"  {base_stt}"

            if is_active:
                stt_display = f"{Style.GREEN}{Style.BOLD}{stt_str:>5}{Style.RESET}"
            else:
                stt_display = f"{stt_str:>5}"

            # Format Account
            acc_raw = f"{p.stem} ({email})"
            if is_cursor and is_row_focused:
                acc_display = f"{Style.CYAN}{Style.BOLD}{acc_raw}{Style.RESET}"
            elif is_active:
                acc_display = f"{Style.GREEN}{acc_raw}{Style.RESET}"
            else:
                acc_display = acc_raw

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
                "is_active": is_active,
                "is_cursor": is_cursor
            })
        except Exception as e:
            rows.append({
                "stt": str(i),
                "acc": f"{p.stem} [Lỗi: {e}]",
                "model": "Unknown",
                "effort": "Unknown",
                "mode": "Unknown",
                "is_active": False,
                "is_cursor": False
            })

    # Calculate dynamic column widths based on maximum visible length
    keys = ["stt", "acc", "model", "effort", "mode"]
    widths = []
    for h, k in zip(headers, keys):
        max_v = len(h)
        for r in rows:
            max_v = max(max_v, visible_len(r[k]))
        widths.append(max_v + 2)

    top_border = "┌" + "┬".join("─" * w for w in widths) + "┐"
    header_sep = "├" + "┼".join("─" * w for w in widths) + "┤"
    bottom_border = "└" + "┴".join("─" * w for w in widths) + "┘"

    header_cells = [pad_cell(f" {h} ", w, "center") for h, w in zip(headers, widths)]
    header_line = "│" + "│".join(header_cells) + "│"

    table_lines = [top_border, f"{Style.BOLD}{header_line}{Style.RESET}", header_sep]

    for r in rows:
        row_cells = [
            pad_cell(f" {r['stt']} ", widths[0], "center"),
            pad_cell(f" {r['acc']} ", widths[1], "left"),
            pad_cell(f" {r['model']} ", widths[2], "left"),
            pad_cell(f" {r['effort']} ", widths[3], "center"),
            pad_cell(f" {r['mode']} ", widths[4], "left"),
        ]
        line = "│" + "│".join(row_cells) + "│"
        if r["is_cursor"] and is_row_focused:
            line = f"{Style.BOLD}{line}{Style.RESET}"
        table_lines.append(line)

    table_lines.append(bottom_border)
    return table_lines


# ---------------------------------------------------------------------------
# Interactive TUI Engine
# ---------------------------------------------------------------------------
def run_interactive_tui():
    """Giao diện động tương tác toàn diện cho agy-controller."""
    state = "NAV"  # NAV, EDIT_ROW, EDIT_PROP, SEARCH, DELETE_ROW, DELETE_CONFIRM
    active_btn_idx = 0
    focus_area = "BUTTONS"  # "BUTTONS" or "TABLE"
    selected_row_idx = 0
    prop_idx = 0  # 0: Model, 1: Effort, 2: Mode
    search_query = ""
    status_message = ""

    # Temporary properties for EDIT_PROP
    edit_model = DEFAULT_MODEL
    edit_effort = DEFAULT_EFFORT
    edit_mode = DEFAULT_MODE
    edit_profile_path = None

    while True:
        all_profiles = get_sorted_profiles()
        current_session = get_current_session()
        active_email = current_session.get("id_token_email") if current_session else None
        active_profile_name = get_active_profile_name()

        # Filter profiles in SEARCH mode
        if state == "SEARCH" and search_query.strip():
            q = search_query.strip().lower()
            filtered_profiles = []
            for p in all_profiles:
                try:
                    d = json.loads(p.read_text(encoding="utf-8"))
                    em = d.get("session", {}).get("id_token_email", "")
                    if q in p.stem.lower() or q in em.lower():
                        filtered_profiles.append(p)
                except Exception:
                    pass
        else:
            filtered_profiles = all_profiles

        # Clamp row index
        if filtered_profiles:
            selected_row_idx = max(0, min(selected_row_idx, len(filtered_profiles) - 1))
        else:
            selected_row_idx = 0

        # Build Screen Buffer
        out = []
        out.append(f"\n{Style.BOLD}Antigravity Controller (agy-controller){Style.RESET}\n")

        # Buttons Bar: [ Refresh ]  [ Add ]  [ Edit ]  [ Search ]  [ Delete ]  [ Exit ]
        btn_strs = []
        for i, b_name in enumerate(TUI_BUTTONS):
            is_active_btn = (i == active_btn_idx)
            btn_label = f"{i+1}. {b_name}"
            if is_active_btn and (state == "NAV" and focus_area == "BUTTONS"):
                btn_strs.append(f"{Style.BOLD}\033[7m[ {btn_label} ]\033[0m")
            elif is_active_btn:
                btn_strs.append(f"{Style.CYAN}{Style.BOLD}[ {btn_label} ]{Style.RESET}")
            else:
                btn_strs.append(f"[ {btn_label} ]")
        out.append("  " + "   ".join(btn_strs) + "\n")

        # Search Box (Mẫu hiển thị 2)
        if state == "SEARCH":
            out.extend(["  " + l for l in format_search_box(search_query)])
            out.append("")

        # Dynamic Table
        is_row_focused = (focus_area == "TABLE") or (state in ("EDIT_ROW", "EDIT_PROP", "DELETE_ROW", "DELETE_CONFIRM"))
        table_lines = build_table_lines(
            filtered_profiles,
            active_profile_name,
            active_email,
            selected_idx=selected_row_idx if filtered_profiles else None,
            is_row_focused=is_row_focused
        )
        out.extend(table_lines)

        # Status Notification
        if status_message:
            out.append(f"\n  {Style.GREEN}{status_message}{Style.RESET}")

        # Context-dependent Footer & Editor
        if state == "NAV":
            if focus_area == "BUTTONS":
                out.append(f"\n  {Style.DIM}[◄ ►]: Chọn nút  |  [▼]: Xuống duyệt bảng  |  [Enter]: Kích hoạt nút  |  [1-6]: Phím tắt{Style.RESET}")
            else:
                out.append(f"\n  {Style.DIM}[▲ ▼]: Duyệt tài khoản  |  [Enter]: Kích hoạt tài khoản  |  [Esc]: Lên hàng nút{Style.RESET}")

        elif state == "EDIT_ROW":
            out.append(f"\n  {Style.CYAN}{Style.BOLD}Chế độ Edit:{Style.RESET} Dùng {Style.BOLD}[▲ ▼]{Style.RESET} chọn tài khoản cần sửa, nhấn {Style.BOLD}[Enter]{Style.RESET} để cấu hình, {Style.BOLD}[Esc]{Style.RESET} để quay lại.")

        elif state == "EDIT_PROP" and edit_profile_path and edit_profile_path.exists():
            out.append(f"\n{Style.BOLD}Chi tiết tài khoản đang chọn:{Style.RESET}")
            out.extend(format_account_details(edit_profile_path))
            out.append(f"\n  {Style.DIM}" + "─" * 61 + f"{Style.RESET}")
            out.append(f"  {Style.BOLD}Chọn thuộc tính cần cấu hình:{Style.RESET}")

            p_model = f"◄ {edit_model} ►" if prop_idx == 0 else f"  {edit_model}"
            p_effort = f"◄ {edit_effort} ►" if prop_idx == 1 else f"  {edit_effort}"
            p_mode = f"◄ {edit_mode} ►" if prop_idx == 2 else f"  {edit_mode}"

            m_ptr = f"{Style.GREEN}>{Style.RESET}" if prop_idx == 0 else " "
            e_ptr = f"{Style.GREEN}>{Style.RESET}" if prop_idx == 1 else " "
            o_ptr = f"{Style.GREEN}>{Style.RESET}" if prop_idx == 2 else " "

            out.append(f"  {m_ptr} Model  : {Style.BOLD if prop_idx == 0 else Style.RESET}{p_model}{Style.RESET}")
            out.append(f"  {e_ptr} Effort : {Style.BOLD if prop_idx == 1 else Style.RESET}{p_effort}{Style.RESET}")
            out.append(f"  {o_ptr} Mode   : {Style.BOLD if prop_idx == 2 else Style.RESET}{p_mode}{Style.RESET}")
            out.append(f"  {Style.DIM}" + "─" * 61 + f"{Style.RESET}")
            out.append(f"  {Style.DIM}[▲ ▼]: Chọn thuộc tính  |  [◄ ►]: Chọn tham số  |  [Enter]: Lưu cấu hình  |  [Esc]: Quay lại duyệt bảng{Style.RESET}")

        elif state == "SEARCH":
            out.append(f"\n  {Style.DIM}[Gõ phím]: Tìm theo Gmail hoặc Tên  |  [▲ ▼]: Duyệt kết quả  |  [Enter]: Kích hoạt  |  [Esc]: Thoát tìm kiếm{Style.RESET}")

        elif state == "DELETE_ROW":
            out.append(f"\n  {Style.RED}{Style.BOLD}Chế độ Delete:{Style.RESET} Dùng {Style.BOLD}[▲ ▼]{Style.RESET} chọn tài khoản cần xóa, nhấn {Style.BOLD}[Enter]{Style.RESET} để xóa, {Style.BOLD}[Esc]{Style.RESET} để quay lại.")

        elif state == "DELETE_CONFIRM" and filtered_profiles:
            del_target = filtered_profiles[selected_row_idx]
            out.append(f"\n  {Style.YELLOW}{Style.BOLD}⚠ XÁC NHẬN:{Style.RESET} Bạn có chắc chắn muốn xóa tài khoản '{Style.BOLD}{del_target.stem}{Style.RESET}' khỏi danh sách?")
            out.append(f"  Nhấn {Style.GREEN}{Style.BOLD}[Y]{Style.RESET} để xác nhận xóa  |  Nhấn {Style.RED}{Style.BOLD}[N]{Style.RESET} hoặc {Style.BOLD}[Esc]{Style.RESET} để hủy bỏ.")

        # Render screen at once
        sys.stdout.write("\033[H\033[J" + "\n".join(out) + "\n")
        sys.stdout.flush()

        # Read key input
        key = read_input_key()

        # -------------------------------------------------------------
        # Key Handling Logic
        # -------------------------------------------------------------
        if state == "NAV" and focus_area == "BUTTONS":
            # Quick Hotkeys for Buttons
            if key in ('1', 'r', 'R'):
                status_message = "✓ Đã làm mới danh sách tài khoản!"
                continue
            elif key in ('2', 'a', 'A'):
                script_path = Path(__file__).resolve()
                subprocess.Popen(f'start "Antigravity Login" cmd /k "python \"{script_path}\" login"', shell=True)
                status_message = "✓ Đã mở cửa sổ CMD mới để đăng nhập. Sau khi xong, nhấn Refresh [1] để cập nhật."
                continue
            elif key in ('3', 'e', 'E'):
                state = "EDIT_ROW"
                status_message = ""
                continue
            elif key in ('4', 's', 'S'):
                state = "SEARCH"
                search_query = ""
                status_message = ""
                continue
            elif key in ('5', 'd', 'D'):
                state = "DELETE_ROW"
                status_message = ""
                continue
            elif key in ('6', 'x', 'X', 'q', 'Q'):
                os.system('cls')
                sys.exit(0)

        if state == "NAV":
            if focus_area == "BUTTONS":
                if key == 'LEFT':
                    active_btn_idx = (active_btn_idx - 1) % len(TUI_BUTTONS)
                elif key == 'RIGHT':
                    active_btn_idx = (active_btn_idx + 1) % len(TUI_BUTTONS)
                elif key == 'DOWN':
                    if filtered_profiles:
                        focus_area = "TABLE"
                        selected_row_idx = 0
                elif key == 'ENTER':
                    btn_name = TUI_BUTTONS[active_btn_idx]
                    if btn_name == "Refresh":
                        status_message = "✓ Đã làm mới danh sách tài khoản!"
                    elif btn_name == "Add":
                        script_path = Path(__file__).resolve()
                        subprocess.Popen(f'start "Antigravity Login" cmd /k "python \"{script_path}\" login"', shell=True)
                        status_message = "✓ Đã mở cửa sổ CMD mới để đăng nhập. Sau khi xong, nhấn Refresh [1] để cập nhật."
                    elif btn_name == "Edit":
                        state = "EDIT_ROW"
                        status_message = ""
                    elif btn_name == "Search":
                        state = "SEARCH"
                        search_query = ""
                        status_message = ""
                    elif btn_name == "Delete":
                        state = "DELETE_ROW"
                        status_message = ""
                    elif btn_name == "Exit":
                        os.system('cls')
                        sys.exit(0)
                elif key == 'ESC':
                    os.system('cls')
                    sys.exit(0)
            elif focus_area == "TABLE":
                if key == 'UP':
                    if selected_row_idx > 0:
                        selected_row_idx -= 1
                    else:
                        focus_area = "BUTTONS"
                elif key == 'DOWN':
                    if selected_row_idx < len(filtered_profiles) - 1:
                        selected_row_idx += 1
                elif key == 'ENTER':
                    if filtered_profiles:
                        p_target = filtered_profiles[selected_row_idx]
                        data = json.loads(p_target.read_text(encoding="utf-8"))
                        write_current_session(data.get("session", {}))
                        set_active_profile_name(p_target.stem)
                        meta = data.get("_meta", {})
                        update_antigravity_settings(meta.get("model"))
                        status_message = f"✓ Đã kích hoạt tài khoản [{selected_row_idx + 1}] '{p_target.stem}'!"
                elif key == 'ESC':
                    focus_area = "BUTTONS"

        elif state == "EDIT_ROW":
            if key == 'UP':
                if selected_row_idx > 0:
                    selected_row_idx -= 1
            elif key == 'DOWN':
                if selected_row_idx < len(filtered_profiles) - 1:
                    selected_row_idx += 1
            elif key == 'ENTER':
                if filtered_profiles:
                    state = "EDIT_PROP"
                    edit_profile_path = filtered_profiles[selected_row_idx]
                    prop_idx = 0
                    try:
                        d = json.loads(edit_profile_path.read_text(encoding="utf-8"))
                        m = d.get("_meta", {})
                        edit_model, edit_effort = normalize_model_and_effort(m.get("model"), m.get("effort"))
                        edit_mode = m.get("mode", DEFAULT_MODE)
                    except Exception:
                        pass
                    status_message = ""
            elif key == 'ESC':
                state = "NAV"
                focus_area = "BUTTONS"
                status_message = ""

        elif state == "EDIT_PROP":
            if key == 'UP':
                prop_idx = (prop_idx - 1) % 3
            elif key == 'DOWN':
                prop_idx = (prop_idx + 1) % 3
            elif key == 'LEFT':
                if prop_idx == 0:
                    idx = AVAILABLE_MODELS.index(edit_model) if edit_model in AVAILABLE_MODELS else 0
                    edit_model = AVAILABLE_MODELS[(idx - 1) % len(AVAILABLE_MODELS)]
                elif prop_idx == 1:
                    idx = AVAILABLE_EFFORTS.index(edit_effort) if edit_effort in AVAILABLE_EFFORTS else 0
                    edit_effort = AVAILABLE_EFFORTS[(idx - 1) % len(AVAILABLE_EFFORTS)]
                elif prop_idx == 2:
                    idx = AVAILABLE_MODES.index(edit_mode) if edit_mode in AVAILABLE_MODES else 0
                    edit_mode = AVAILABLE_MODES[(idx - 1) % len(AVAILABLE_MODES)]
            elif key == 'RIGHT':
                if prop_idx == 0:
                    idx = AVAILABLE_MODELS.index(edit_model) if edit_model in AVAILABLE_MODELS else 0
                    edit_model = AVAILABLE_MODELS[(idx + 1) % len(AVAILABLE_MODELS)]
                elif prop_idx == 1:
                    idx = AVAILABLE_EFFORTS.index(edit_effort) if edit_effort in AVAILABLE_EFFORTS else 0
                    edit_effort = AVAILABLE_EFFORTS[(idx + 1) % len(AVAILABLE_EFFORTS)]
                elif prop_idx == 2:
                    idx = AVAILABLE_MODES.index(edit_mode) if edit_mode in AVAILABLE_MODES else 0
                    edit_mode = AVAILABLE_MODES[(idx + 1) % len(AVAILABLE_MODES)]
            elif key == 'ENTER':
                try:
                    data = json.loads(edit_profile_path.read_text(encoding="utf-8"))
                    meta = data.setdefault("_meta", {})
                    meta["model"] = edit_model
                    meta["effort"] = edit_effort
                    meta["mode"] = edit_mode
                    edit_profile_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                    if get_active_profile_name() == edit_profile_path.stem:
                        update_antigravity_settings(edit_model)
                    status_message = f"✓ Đã lưu cấu hình mới cho '{edit_profile_path.stem}'!"
                except Exception as e:
                    status_message = f"✗ Lỗi lưu cấu hình: {e}"
            elif key == 'ESC':
                state = "EDIT_ROW"
                status_message = ""

        elif state == "SEARCH":
            if key == 'ESC':
                search_query = ""
                state = "NAV"
                focus_area = "BUTTONS"
                status_message = ""
            elif key == 'BACKSPACE':
                search_query = search_query[:-1]
                selected_row_idx = 0
            elif key == 'UP':
                if selected_row_idx > 0:
                    selected_row_idx -= 1
            elif key == 'DOWN':
                if selected_row_idx < len(filtered_profiles) - 1:
                    selected_row_idx += 1
            elif key == 'ENTER':
                if filtered_profiles:
                    p_target = filtered_profiles[selected_row_idx]
                    data = json.loads(p_target.read_text(encoding="utf-8"))
                    write_current_session(data.get("session", {}))
                    set_active_profile_name(p_target.stem)
                    meta = data.get("_meta", {})
                    update_antigravity_settings(meta.get("model"))
                    status_message = f"✓ Đã kích hoạt tài khoản '{p_target.stem}'!"
                    search_query = ""
                    state = "NAV"
            elif len(key) == 1 and ord(key) >= 32:
                search_query += key
                selected_row_idx = 0

        elif state == "DELETE_ROW":
            if key == 'UP':
                if selected_row_idx > 0:
                    selected_row_idx -= 1
            elif key == 'DOWN':
                if selected_row_idx < len(filtered_profiles) - 1:
                    selected_row_idx += 1
            elif key == 'ENTER':
                if filtered_profiles:
                    state = "DELETE_CONFIRM"
                    status_message = ""
            elif key == 'ESC':
                state = "NAV"
                focus_area = "BUTTONS"
                status_message = ""

        elif state == "DELETE_CONFIRM":
            if key in ('y', 'Y'):
                if filtered_profiles:
                    del_p = filtered_profiles[selected_row_idx]
                    p_name = del_p.stem
                    del_p.unlink()
                    if get_active_profile_name() == p_name:
                        if CURRENT_PROFILE_FILE.exists():
                            CURRENT_PROFILE_FILE.unlink()
                    status_message = f"✓ Đã xóa tài khoản '{p_name}' thành công!"
                    state = "NAV"
                    focus_area = "BUTTONS"
            elif key in ('n', 'N', 'ESC'):
                state = "DELETE_ROW"
                status_message = "Đã hủy thao tác xóa."


# ---------------------------------------------------------------------------
# CLI Subcommands (Non-interactive)
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

    model, effort = normalize_model_and_effort(meta.get("model"), meta.get("effort"))
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

    table_lines = build_table_lines(profiles, active_profile_name, active_email)
    print(f"\n{Style.BOLD}Danh sách tài khoản Antigravity:{Style.RESET}\n")
    for line in table_lines:
        print(line)

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

    with CredentialSwitchLock():
        success = write_current_session(session)
        if not success:
            print_error("Không thể ghi thông tin vào Windows Credential Manager.")
            sys.exit(1)

        set_active_profile_name(profile_name)
    email = session.get("id_token_email", meta.get("email", "Unknown"))
    model, effort = normalize_model_and_effort(meta.get("model"), meta.get("effort"))
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
    Uses CredentialSwitchLock to serialize authentication and delay until agy reads credentials.
    """
    target = None
    if hasattr(args, "extra_args") and args.extra_args:
        first = args.extra_args[0]
        if not first.startswith("-"):
            p_test, _ = resolve_profile(first)
            if p_test:
                target = args.extra_args.pop(0)

    # Determine profile path
    if target:
        profile_path, stt = resolve_profile(target)
    else:
        active_name = get_active_profile_name()
        if not active_name:
            profiles = get_sorted_profiles()
            if profiles:
                profile_path = profiles[0]
            else:
                print_error("Chưa có tài khoản nào được lưu. Hãy đăng nhập với 'agy-controller login' trước.")
                sys.exit(1)
        else:
            profile_path = PROFILES_DIR / f"{active_name}.json"
            if not profile_path.exists():
                print_error(f"Không tìm thấy file profile của tài khoản '{active_name}'.")
                sys.exit(1)

    # Load profile data
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception as e:
        print_error(f"Lỗi đọc file profile: {e}")
        sys.exit(1)

    meta = data.setdefault("_meta", {})
    changed = False

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

    model, effort = normalize_model_and_effort(meta.get("model"), meta.get("effort"))
    mode = meta.get("mode", DEFAULT_MODE)

    # Sync model to settings.json
    update_antigravity_settings(model)

    # Build command line
    agy_binary = shutil.which("agy") or "agy"
    cmd_args = [agy_binary]

    if model:
        cmd_args.extend(["--model", model])
    if effort:
        cmd_args.extend(["--effort", effort])
    if mode.lower() == "turbo":
        cmd_args.append("--dangerously-skip-permissions")

    if hasattr(args, "extra_args") and args.extra_args:
        cmd_args.extend(args.extra_args)

    mode_note = f"{Style.YELLOW}{Style.BOLD}turbo{Style.RESET} (bỏ qua xác nhận quyền)" if mode.lower() == "turbo" else "normal"
    print_info(f"Chạy agy: Tài khoản={Style.CYAN}{profile_path.stem}{Style.RESET} | Model={model} | Effort={effort} | Mode={mode_note}")
    print(f"{Style.DIM}Lệnh thực thi: {' '.join(cmd_args)}{Style.RESET}\n")

    # Safe execution with inter-process lock & startup delay
    try:
        with CredentialSwitchLock():
            session = data.get("session", {})
            write_current_session(session)
            set_active_profile_name(profile_path.stem)
            
            # Khởi chạy tiến trình agy
            proc = subprocess.Popen(cmd_args, shell=(os.name == "nt"))
            # Delay an toàn 0.4s để agy khởi động và nạp token từ Credential Manager vào RAM
            time.sleep(0.4)
            
        # Ra khỏi block 'with', lock được giải phóng ngay lập tức cho các lệnh gọi khác!
        return_code = proc.wait()
        sys.exit(return_code)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print_error(f"Không thể khởi chạy agy: {e}")
        sys.exit(1)


def cmd_run_many(args):
    """Run agy on multiple accounts concurrently with staggered startup delay.
    Supports either:
      1) --prompt "<shared_prompt>" with multiple accounts (--accounts 1,2,3)
      2) --worker <account> "<prompt>" (repeated multiple times)
    """
    agy_binary = shutil.which("agy") or "agy"
    tasks = []  # list of (account_target, prompt_text)

    # Mode 1: Repeated --worker target prompt
    if args.worker:
        for item in args.worker:
            # item is a tuple/list [target, prompt]
            tasks.append((item[0], item[1]))

    # Mode 2: --accounts 1,2,3 --prompt "some text"
    elif args.accounts and args.prompt:
        targets = [t.strip() for t in args.accounts.split(",") if t.strip()]
        for target in targets:
            tasks.append((target, args.prompt))

    elif args.accounts and hasattr(args, "extra_args") and args.extra_args:
        prompt_text = " ".join(args.extra_args)
        targets = [t.strip() for t in args.accounts.split(",") if t.strip()]
        for target in targets:
            tasks.append((target, prompt_text))

    if not tasks:
        print_error("Không có nhiệm vụ nào được chỉ định.")
        print("\nCách dùng:")
        print("  1. Dùng chung 1 prompt cho nhiều tài khoản:")
        print("     agy-controller run-many --accounts 1,2,3 --prompt \"Giải thích Transformer\"")
        print("  2. Chỉ định từng worker và nhiệm vụ riêng:")
        print("     agy-controller run-many -w 1 \"Tạo FastAPI router\" -w 2 \"Viết giao diện UI\"")
        sys.exit(1)

    print_info(f"Bắt đầu khởi chạy song song {len(tasks)} tiến trình agy với Staggered Startup...")

    processes = []
    for idx, (target, prompt_text) in enumerate(tasks, start=1):
        profile_path, stt = resolve_profile(target)
        if not profile_path or not profile_path.exists():
            print_error(f"[{idx}/{len(tasks)}] Không tìm thấy tài khoản '{target}', bỏ qua.")
            continue

        try:
            p_data = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception as e:
            print_error(f"[{idx}/{len(tasks)}] Lỗi đọc profile '{profile_path.stem}': {e}")
            continue

        p_meta = p_data.get("_meta", {})
        m, ef = normalize_model_and_effort(p_meta.get("model"), p_meta.get("effort"))
        mo = p_meta.get("mode", DEFAULT_MODE)

        # Build command line for this worker
        # By default run non-interactively with --print to capture stream cleanly
        cmd_args = [agy_binary]
        if m:
            cmd_args.extend(["--model", m])
        if ef:
            cmd_args.extend(["--effort", ef])
        if mo.lower() == "turbo":
            cmd_args.append("--dangerously-skip-permissions")

        # Non-interactive print prompt
        cmd_args.extend(["-p", prompt_text])

        # Safely acquire lock, swap credential, start process, then delay 0.4s to let it read key
        with CredentialSwitchLock():
            write_current_session(p_data.get("session", {}))
            set_active_profile_name(profile_path.stem)
            print(f"  {Style.GREEN}▶{Style.RESET} Khởi chạy [{stt}] {Style.CYAN}{profile_path.stem}{Style.RESET} (Model: {m}, Effort: {ef})...")
            
            # Start process
            proc = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                shell=(os.name == "nt")
            )
            # Give agy ~0.4s to load Windows Credential into RAM before allowing next switch
            time.sleep(0.4)

        processes.append((profile_path.stem, proc))

    print_success(f"Tất cả {len(processes)} tiến trình agy đã khởi động và đang chạy song song 100%!\n")

    # Read output asynchronously with profile prefix
    import threading

    def stream_output(name: str, p: subprocess.Popen):
        prefix = f"[{Style.CYAN}{name}{Style.RESET}] "
        if p.stdout:
            for line in iter(p.stdout.readline, ""):
                if line:
                    sys.stdout.write(f"{prefix}{line}")
                    sys.stdout.flush()
            p.stdout.close()

    threads = []
    for name, p in processes:
        t = threading.Thread(target=stream_output, args=(name, p))
        t.daemon = True
        t.start()
        threads.append((t, p))

    for t, p in threads:
        p.wait()
        t.join()

    print()
    print_success("Tất cả các worker đã hoàn thành nhiệm vụ.")


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
    res_m, res_e = normalize_model_and_effort(meta.get("model"), meta.get("effort"))
    print(f"  Model  : {res_m}")
    print(f"  Effort : {res_e}")
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

    print_info("Chuẩn bị phiên đăng nhập mới...")
    delete_credential_raw(CREDENTIAL_TARGET)
    if CURRENT_PROFILE_FILE.exists():
        CURRENT_PROFILE_FILE.unlink()

    agy_cmd = shutil.which("agy") or "agy"
    print_info(f"Khởi chạy '{agy_cmd}' để xác thực Google...")
    print(f"{Style.DIM}>>> Hãy hoàn tất đăng nhập trong trình duyệt, sau đó quay lại terminal này <<<{Style.RESET}\n")

    try:
        subprocess.run([agy_cmd], shell=(os.name == "nt"))
    except KeyboardInterrupt:
        print("\nĐã hủy đăng nhập.")
    except Exception as e:
        print_error(f"Không thể khởi chạy agy: {e}")

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

        for lf in legacy_files:
            old_f = bin_dir / lf
            if old_f.exists():
                old_f.unlink()

        (bin_dir / "agy-controller.cmd").write_text(f'@echo off\npython "{script_path}" %*\n', encoding="utf-8")
        (bin_dir / "agy-controller.ps1").write_text(f'& python "{script_path}" @args\n', encoding="utf-8")

    print_success("Đã cài đặt thống nhất lệnh 'agy-controller' vào các thư mục PATH:")
    for d in unique_dirs:
        print(f"  Thư mục: {d}")
    print(f"\nLệnh khả dụng duy nhất: {Style.BOLD}{Style.CYAN}agy-controller{Style.RESET}")
    print(f"Bạn có thể gõ {Style.CYAN}agy-controller{Style.RESET} ở bất kỳ đâu trong CMD hoặc PowerShell để mở giao diện điều khiển!\n")

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

    # tui
    p_tui = subparsers.add_parser("tui", help="Khởi chạy giao diện tương tác động TUI")
    p_tui.set_defaults(func=lambda args: run_interactive_tui())

    # list
    p_list = subparsers.add_parser("list", aliases=["ls"], help="Xem bảng động danh sách tài khoản, Model, Effort, Mode")
    p_list.set_defaults(func=cmd_list)

    # switch
    p_switch = subparsers.add_parser("switch", aliases=["use"], help="Chuyển tài khoản (theo STT, tên hoặc email)")
    p_switch.add_argument("name", help="Số STT (1, 2, ...), tên profile hoặc email")
    p_switch.set_defaults(func=cmd_switch)

    # run
    p_run = subparsers.add_parser("run", help="Chạy agy (có thể kèm STT, đổi Model, Effort, Mode và tự động lưu)")
    p_run.add_argument("--model", help="Cập nhật Model (VD: 'gemini-3.8-flash', 'claude-sonnet-4-6')")
    p_run.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="Cập nhật Effort")
    p_run.add_argument("--mode", choices=["normal", "turbo"], help="Cập nhật Mode: normal hoặc turbo (--dangerously-skip-permissions)")
    p_run.set_defaults(func=cmd_run)

    # run-many
    p_run_many = subparsers.add_parser("run-many", help="Chạy song song nhiều worker/tài khoản với Staggered Startup")
    p_run_many.add_argument("-w", "--worker", nargs=2, action="append", metavar=("ACCOUNT", "PROMPT"), help="Chỉ định worker và prompt riêng (có thể lặp lại: -w 1 'prompt1' -w 2 'prompt2')")
    p_run_many.add_argument("-a", "--accounts", help="Danh sách STT hoặc tên tài khoản phân tách bằng dấu phẩy (VD: 1,2,3)")
    p_run_many.add_argument("-p", "--prompt", help="Prompt dùng chung cho các tài khoản chỉ định bởi --accounts")
    p_run_many.set_defaults(func=cmd_run_many)

    # config
    p_cfg = subparsers.add_parser("config", aliases=["cfg", "set"], help="Cấu hình Model, Effort, Mode cho tài khoản")
    p_cfg.add_argument("target", help="Số STT hoặc tên profile")
    p_cfg.add_argument("--model", help="Tên Model (VD: 'gemini-3.8-flash', 'claude-sonnet-4-6')")
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
        # Default behavior: launch interactive dynamic TUI!
        run_interactive_tui()
        return

    args.func(args)

if __name__ == "__main__":
    main()
