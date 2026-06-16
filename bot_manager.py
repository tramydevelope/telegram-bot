#!/usr/bin/env python3
import os, json, subprocess, time, signal, sys, threading
from datetime import datetime

SUBBOTS_FILE = 'subbots.json'
CHECK_INTERVAL = 10

def ts():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def load_subbots() -> list:
    try:
        if os.path.exists(SUBBOTS_FILE):
            return json.load(open(SUBBOTS_FILE, encoding='utf-8'))
    except Exception as e:
        print(f"[{ts()}] [MANAGER] Lỗi đọc subbots.json: {e}", flush=True)
    return []

running: dict = {}
stop_flag = False

def start_instance(bot_id: str, token: str, data_dir: str, username: str = "?"):
    os.makedirs(data_dir, exist_ok=True)
    env = os.environ.copy()
    env['BOT_TOKEN'] = token
    env['BOT_DATA_DIR'] = data_dir
    proc = subprocess.Popen(
        ['python', 'bot.py'],
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    running[bot_id] = {
        "proc": proc,
        "token": token,
        "data_dir": data_dir,
        "username": username,
    }
    label = "MAIN" if bot_id == "MAIN" else f"SUB @{username}"
    print(f"[{ts()}] [{label}] Khởi động — PID {proc.pid}", flush=True)
    return proc

def watchdog_loop():
    while not stop_flag:
        time.sleep(CHECK_INTERVAL)
        for bot_id, info in list(running.items()):
            ret = info["proc"].poll()
            if ret is not None:
                label = "MAIN" if bot_id == "MAIN" else f"SUB @{info['username']}"
                print(f"[{ts()}] [{label}] Crashed! Đang khởi động lại...", flush=True)
                new_proc = start_instance(bot_id, info["token"], info["data_dir"], info["username"])
                running[bot_id]["proc"] = new_proc

def shutdown(sig, frame):
    global stop_flag
    print(f"\n[{ts()}] [MANAGER] Nhận tín hiệu dừng. Đang tắt tất cả bots...", flush=True)
    stop_flag = True
    for bot_id, info in list(running.items()):
        try:
            info["proc"].terminate()
            info["proc"].wait(timeout=5)
        except Exception:
            pass
    sys.exit(0)

def main():
    print(f"[{ts()}] ╔══════════════════════════════════")
    print(f"[{ts()}] ║  BOT MANAGER — KHỞI ĐỘNG")
    print(f"[{ts()}] ╚══════════════════════════════════")

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    main_token = os.environ.get('BOT_TOKEN', '')
    if not main_token:
        print(f"[{ts()}] [MANAGER] LỖI: BOT_TOKEN chưa được cấu hình!", flush=True)
        sys.exit(1)

    start_instance("MAIN", main_token, ".")
    subbots = load_subbots()
    for s in subbots:
        time.sleep(3)
        start_instance(s['id'], s['token'], s.get('data_dir', f"bots/{s['id']}"), s.get('username', '?'))

    total = 1 + len(subbots)
    print(f"[{ts()}] [MANAGER] Đang chạy: 1 main + {len(subbots)} sub-bot(s) = {total} bots", flush=True)

    threading.Thread(target=watchdog_loop, daemon=True, name="watchdog").start()
    while True:
        try:
            time.sleep(30)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(f"[{ts()}] [MANAGER] Lỗi: {e}", flush=True)

if __name__ == '__main__':
    main()