import time
import os
import sys

LOG_FILE = "stolen_logs.txt"
THRESHOLD_KB = 10
POLL_INTERVAL = 0.5


def get_file_size_kb(path):
    try:
        return os.path.getsize(path) / 1024.0
    except FileNotFoundError:
        return 0.0


def wipe_log(path):
    try:
        with open(path, "w") as f:
            f.truncate(0)
        print(f"[!] Sentinel: Wiped {path} — threat log eliminated.")
    except Exception as e:
        print(f"[-] Sentinel: Wipe failed — {e}")


def monitor():
    print("[*] Storage Sentinel Activated.")
    print(f"[*] Monitoring '{LOG_FILE}' — threshold: {THRESHOLD_KB}KB\n")
    while True:
        size_kb = get_file_size_kb(LOG_FILE)
        if size_kb >= THRESHOLD_KB:
            print(f"[!] Sentinel: {LOG_FILE} reached {size_kb:.1f}KB (threshold: {THRESHOLD_KB}KB)")
            wipe_log(LOG_FILE)
        else:
            print(f"[*] Sentinel: {LOG_FILE} — {size_kb:.1f}KB / {THRESHOLD_KB}KB")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    monitor()
