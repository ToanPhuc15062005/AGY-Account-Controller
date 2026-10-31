# Antigravity Controller (`agy-controller`)

Trình điều khiển và **giao diện động tương tác (TUI)** duy nhất cho Antigravity CLI (`agy`) trên Windows (CMD & PowerShell). Quản lý phiên đa tài khoản, cấu hình độc lập **Model**, **Effort**, **Turbo Mode** (`--dangerously-skip-permissions`), và khởi chạy tự động.

---

## ⚙️ Model & Effort tách biệt hoàn toàn

* **Model độc lập**: `gemini-3.8-flash`, `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `gpt-oss-120b-medium`.
* **Effort độc lập**: `low`, `medium`, `high`, `xhigh`, `max` (mặc định: `medium`).
* **Mode**: `normal` (hỏi quyền khi chạy công cụ) hoặc `turbo` (tự động bật `--dangerously-skip-permissions`).

Lệnh thực thi khi chạy được cấu trúc chính xác:
```cmd
agy --model gemini-3.8-flash --effort medium [--dangerously-skip-permissions]
```

---

## 🎮 Giao diện động tương tác (TUI)

Chỉ cần gõ:
```cmd
agy-controller
```
Hệ thống sẽ mở giao diện điều khiển tương tác trực quan ngay trong terminal.

### 1. Thanh nút điều khiển
```text
  [ 1. Refresh ]   [ 2. Add ]   [ 3. Edit ]   [ 4. Search ]   [ 5. Delete ]   [ 6. Exit ]
```
* **Phím điều hướng**: Dùng phím mũi tên **`Trái / Phải`** để chọn nút, nhấn **`Enter`** để kích hoạt. Hoặc bấm phím tắt số **`1` - `6`** / **`R, A, E, S, D, X`**.
* **Phím `Xuống`**: Di chuyển xuống duyệt trực tiếp bảng danh sách tài khoản.

---

### 2. Chi tiết các nút chức năng

#### 🔄 Nút `Refresh` (Phím `1` hoặc `R`)
Làm mới dữ liệu từ thư mục profile và Windows Credential Manager ngay lập tức.

#### ➕ Nút `Add` (Phím `2` hoặc `A`)
Tự động mở một **cửa sổ Command Prompt mới** chạy lệnh đăng nhập Google OAuth mà không làm gián đoạn hay mất phiên làm việc của giao diện hiện tại. Sau khi đăng nhập xong ở cửa sổ mới, quay lại giao diện và chọn `Refresh`.

#### ✏️ Nút `Edit` (Phím `3` hoặc `E`)
1. Dùng phím **`Lên / Xuống`** để duyệt giữa các tài khoản. Nhấn **`Esc`** để quay lại thanh nút.
2. Nhấn **`Enter`** để chọn tài khoản cấu hình:
   * Hiển thị bảng chi tiết tài khoản theo **Mẫu hiển thị 1**:
     ```text
     Tên Profile    : default
     	Google Email   : phucnguyentenda@gmail.com
     	Model          : gemini-3.8-flash
     	Effort         : medium
     	Mode           : turbo (dangerously-skip-permissions)
     	Access Token   : Hợp lệ (0h 58m còn lại)
     	Refresh Token  : Có sẵn ✓
     	Lưu trữ        : gemini:antigravity
     ```
   * Dùng **`Lên / Xuống`** để chọn thuộc tính cần sửa: **`Model`**, **`Effort`**, **`Mode`**.
   * Dùng **`Trái / Phải`** để đổi tham số của thuộc tính (Ví dụ Model: `gemini-3.8-flash` ◄► `claude-sonnet-4-6`, Effort: `low` ◄► `medium` ◄► `high`).
   * Nhấn **`Enter`** để lưu thay đổi.
   * Nhấn **`Esc`** để quay lại duyệt danh sách tài khoản.

#### 🔍 Nút `Search` (Phím `4` hoặc `S`)
Mở ô tìm kiếm theo **Mẫu hiển thị 2** ngay phía trên bảng:
```text
─────────────────────────────────────────────────────────────
> [nhập từ khóa tìm kiếm...]
─────────────────────────────────────────────────────────────
```
* Tự động lọc bảng danh sách tài khoản theo thời gian thực theo Gmail hoặc Tên profile.
* Dùng **`Lên / Xuống`** để duyệt kết quả, nhấn **`Enter`** để kích hoạt tài khoản.
* Nhấn **`Esc`** để thoát chế độ tìm kiếm và quay về giao diện chính.

#### 🗑️ Nút `Delete` (Phím `5` hoặc `D`)
1. Dùng **`Lên / Xuống`** để duyệt chọn tài khoản cần xóa.
2. Nhấn **`Enter`** để chọn.
3. Xuất hiện hộp thoại xác nhận lần cuối:
   * Nhấn **`Y`**: Xác nhận xóa tài khoản khỏi danh sách.
   * Nhấn **`N`** hoặc **`Esc`**: Hủy bỏ và quay lại.

#### 🚪 Nút `Exit` (Phím `6` hoặc `X` / `Q`)
Thoát chương trình và xóa màn hình console (`cls`).

---

## ⚡ Các lệnh CLI (Chạy trực tiếp không cần mở TUI)

| Lệnh CLI | Chức năng |
|---|---|
| `agy-controller list` | In bảng danh sách tài khoản ra console |
| `agy-controller <STT>` *(VD: `agy-controller 2`)* | Chuyển tài khoản cực nhanh theo số STT |
| `agy-controller switch <STT/Tên>` | Chuyển tài khoản đang kích hoạt |
| `agy-controller run [STT] [cấu hình] [args]` | Chạy `agy`, tự động lưu cấu hình nếu đổi `--mode`, `--model`, `--effort` (bảo vệ chống xung đột đồng thời) |
| `agy-controller run-many ...` | Chạy song song nhiều worker/tài khoản với Staggered Startup (0.4s) |
| `agy-controller config <STT> [cấu hình]` | Cập nhật cấu hình riêng cho tài khoản qua dòng lệnh |
| `agy-controller login [tên]` | Đăng nhập tài khoản Google mới và lưu profile |
| `agy-controller logout` | Đăng xuất an toàn khỏi Credential Manager |
| `agy-controller delete <STT/tên>` | Xóa profile |
| `agy-controller install` | Cập nhật / cài đặt wrapper vào PATH |
| `agy-controller uninstall` | Gỡ bỏ wrapper khỏi PATH |
