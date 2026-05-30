import time
import os
import signal

try:
    from config import LOG_FILE, SENTINEL_THRESHOLD_KB, SENTINEL_POLL_INTERVAL
except ImportError:
    BASE = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE, "stolen_logs.txt")
    SENTINEL_THRESHOLD_KB = 10
    SENTINEL_POLL_INTERVAL = 1.0

RUNNING = True


def handler(signum, frame):
    global RUNNING
    RUNNING = False
    print("[*] Sentinel shutting down gracefully.", flush=True)


def get_file_size_kb(path):
    try:
        return os.path.getsize(path) / 1024.0
    except FileNotFoundError:
        return 0.0


def wipe_log(path):
    try:
        open(path, "w").close()
        print(f"[!] Sentinel: Wiped {path} — threat log eliminated.", flush=True)
        return True
    except Exception as e:
        print(f"[-] Sentinel: Wipe failed — {e}", flush=True)
        return False


def monitor():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    print("[*] Storage Sentinel Activated.", flush=True)
    print(f"[*] Monitoring '{LOG_FILE}' — threshold: {SENTINEL_THRESHOLD_KB}KB\n", flush=True)

    last_size = -1.0

    while RUNNING:
        size_kb = get_file_size_kb(LOG_FILE)

        if size_kb != last_size or size_kb >= SENTINEL_THRESHOLD_KB:
            if size_kb >= SENTINEL_THRESHOLD_KB:
                print(f"[!] Sentinel: {LOG_FILE} reached {size_kb:.1f}KB (threshold: {SENTINEL_THRESHOLD_KB}KB)", flush=True)
                wipe_log(LOG_FILE)
                last_size = 0.0
            else:
                print(f"[*] Sentinel: {os.path.basename(LOG_FILE)} — {size_kb:.1f}KB / {SENTINEL_THRESHOLD_KB}KB", flush=True)
                last_size = size_kb

        time.sleep(SENTINEL_POLL_INTERVAL)


if __name__ == "__main__":
    monitor()
