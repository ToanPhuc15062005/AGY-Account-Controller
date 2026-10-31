# Antigravity Controller (`agy-controller`)

Trình điều khiển thống nhất duy nhất cho Antigravity CLI (`agy`) trên Windows (CMD & PowerShell). Quản lý phiên đa tài khoản, cấu hình Model, Effort, Turbo Mode (`--dangerously-skip-permissions`), và khởi chạy tự động.

---

## 🚀 Các lệnh chính của `agy-controller`

| Lệnh | Chức năng |
|---|---|
| `agy-controller` | Xem nhanh thông tin phiên hiện tại và bảng danh sách tài khoản |
| `agy-controller list` | Xem bảng động: STT, Tài khoản, Model, Effort, Mode |
| `agy-controller switch <STT/Tên>` | Chuyển tài khoản (VD: `agy-controller switch 2` hoặc gõ tắt: `agy-controller 2`) |
| `agy-controller run [STT] [flags]` | Chạy `agy`, tự động lưu cấu hình nếu có tham số `--mode`, `--model`, `--effort` |
| `agy-controller config <STT> [flags]` | Cập nhật cấu hình Model, Effort, Mode cho tài khoản |
| `agy-controller login [tên]` | Đăng nhập tài khoản Google mới và lưu thành profile |
| `agy-controller logout` | Đăng xuất an toàn khỏi Credential Manager |
| `agy-controller save [tên]` | Lưu phiên đăng nhập hiện tại thành profile |
| `agy-controller current` | Xem chi tiết thông tin token và tài khoản đang kích hoạt |
| `agy-controller delete <STT/tên>` | Xóa profile tài khoản |
| `agy-controller rename <cũ> <mới>` | Đổi tên profile tài khoản |
| `agy-controller install` | Cài đặt wrapper `agy-controller` vào hệ thống (PATH) |
| `agy-controller uninstall` | Gỡ bỏ wrapper khỏi PATH |

---

## 📊 Bảng danh sách động

Khi gọi `agy-controller` hoặc `agy-controller list`:

```text
Danh sách tài khoản Antigravity:

┌─────┬────────────────────────────────────────────────┬───────────────────────────┬────────┬───────────────────┐
│ STT │                   Tài khoản                    │           Model           │ Effort │       Mode        │
├─────┼────────────────────────────────────────────────┼───────────────────────────┼────────┼───────────────────┤
│   1 │ default (phucnguyentenda@gmail.com)            │ Gemini 3.8 Flash (Medium) │   -    │ normal            │
│  2* │ n23dccn115 (n23dccn115@student.ptithcm.edu.vn) │ Gemini 3.8 Flash (Medium) │   -    │ turbo (skip-perm) │
│   3 │ phucnguyentenda (phucnguyentenda@gmail.com)    │ Gemini 3.8 Flash (Medium) │   -    │ normal            │
└─────┴────────────────────────────────────────────────┴───────────────────────────┴────────┴───────────────────┘

  * : Tài khoản đang kích hoạt (Active)
```

---

## ⚡ Thao tác nhanh hàng ngày

### 1. Chuyển tài khoản siêu tốc:
```cmd
agy-controller 1
agy-controller 2
```
*(Gõ trực tiếp số STT, `agy-controller` tự động hiểu là lệnh switch).*

### 2. Vừa cấu hình vừa chạy:
```cmd
agy-controller run --mode turbo
```
*(Tự động lưu mode `turbo` cho tài khoản này và khởi chạy `agy` với cờ `--dangerously-skip-permissions`).*

Chạy với tài khoản khác:
```cmd
agy-controller run 1 --mode normal
```

Truyền cờ và prompt cho `agy`:
```cmd
agy-controller run -p "xin chào"
```

### 3. Đăng nhập tài khoản mới:
```cmd
agy-controller login work
```
