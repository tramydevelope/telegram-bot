# 💰 Telegram Bot Kiếm Tiền

Bot Telegram toàn diện với xác minh thiết bị, quản lý mời giới thiệu, rút tiền và phát hiện gian lận.

## ⚡ Tính Năng Chính

- ✅ **Xác minh thiết bị** qua Mini App (IP, GPU, CPU, RAM, Fingerprint)
- 👥 **Hệ thống mời giới thiệu** — nhận thưởng khi bạn bè hoàn thành xác minh
- 💰 **Rút tiền** với kiểm tra gian lận tự động
- 🚨 **Phát hiện trùng lặp** (IP, thiết bị) — cảnh báo admin
- 🤖 **Hỗ trợ bot con** — cấp quyền admin cho từng bot
- 📊 **Thống kê chi tiết** — theo dõi từng tài khoản, lịch sử duyệt tiền
- 🎙️ **Broadcast** — gửi tin nhắn tới toàn bộ thành viên

## 📋 Yêu Cầu Hệ Thống

- Python 3.10+
- Node.js 18+
- pnpm
- Tài khoản Telegram Bot (từ @BotFather)

## 🚀 Cài Đặt Nhanh (Replit)

### 1. Tạo Replit
- Vào https://replit.com → New Repl → chọn **Node.js**
- Clone hoặc upload repo

### 2. Cấu Hình Biến Môi Trường
Nhấp **Secrets** và thêm:
```
BOT_TOKEN=<token từ @BotFather>
SESSION_SECRET=<chuỗi ngẫu nhiên>
```

### 3. Cài Thư Viện
```bash
pip install python-telegram-bot==22.8 pandas aiohttp
pnpm install
```

### 4. Tạo File Cấu Hình
```bash
echo '{"groups": [-1001234567890], "users": []}' > admins.json
echo '{"reward_invite": 500, "min_withdraw": 10000}' > config.json
```

### 5. Khởi Động
- Workflow 1: `python bot_manager.py` (Bot Telegram)
- Workflow 2: `pnpm dev` (API Server Mini App)

## 📖 Lệnh Chính

### Người Dùng
- `/start` — Menu chính
- `/profile` — Xem hồ sơ & số dư
- `/invite` — Lấy link mời bạn
- `/withdraw` — Rút tiền

### Admin
- `/cai_dat` — Xem toàn bộ cấu hình
- `/set_ref <số>` — Đặt thưởng mỗi lần mời
- `/set_min <số>` — Đặt mức rút tối thiểu
- `/add_channel @kenh Tên` — Thêm kênh bắt buộc
- `/check_device` — Kiểm tra trùng thiết bị
- `/tat_ca` — Xem toàn bộ người dùng
- `/them_bot <TOKEN>` — Cấp bot con mới

## 🔐 Cấu Trúc Dữ Liệu

- `danh_sach_thanh_vien.csv` — Dữ liệu user
- `verified_users.json` — Xác minh thiết bị
- `admins.json` — Danh sách admin
- `config.json` — Cấu hình hệ thống
- `withdraw_log.json` — Lịch sử rút tiền
- `subbots.json` — Danh sách bot con

## 📱 Mini App

Xác minh tự động được hosting trên Replit:
```
https://<domain>/api/miniapp?bid=<bot_id>
```

## 🚨 Phát Hiện Gian Lận

- Kiểm tra IP trùng lặp
- Kiểm tra Fingerprint (GPU + CPU + RAM + canvas)
- Ngưỡng cảnh báo: >3 tài khoản trùng → "GIAN LẬN HÀNG LOẠT"
- Admin duyệt thủ công (Approve/Reject)

## 🤖 Hỗ Trợ Bot Con

```bash
# Cấp bot con
/them_bot <BOT_TOKEN>

# Cấp admin cho bot con
/cap_admin_con <bot_id> <user_id>
/cap_admin_con <bot_id> group <group_id>

# Xem danh sách
/ds_bot
```

## ⚙️ Cấu Hình VPS (Systemd)

Tạo `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 bot_manager.py
EnvironmentFile=/path/to/bot/.env
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## 📞 Liên Hệ & Hỗ Trợ

Nếu cần hỗ trợ, cung cấp:
1. Log lỗi từ console
2. Phiên bản Python/Node.js
3. Mô tả chi tiết vấn đề

---

**⚠️ Lưu ý:** Luôn bảo vệ `BOT_TOKEN` và file dữ liệu nhạy cảm. Sử dụng `.env` và `.gitignore`!