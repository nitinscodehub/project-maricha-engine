# Keylogger & Neuro-Decoy Deception Framework

A dual-purpose cybersecurity project featuring a user-mode keylogger and an advanced deception framework that floods keylog files with realistic decoy data to confuse attackers.


<img width="935" height="709" alt="image" src="https://github.com/user-attachments/assets/52130ca6-5e62-4bf9-97b4-4bf238d5cec8" />

---

## Files

| File | Purpose |
|---|---|
| `keylogger.py` | Basic keylogger – logs keystrokes to `stolen_logs.txt` using `pynput.keyboard.Listener`. Press ESC to stop. |
| `decoy.py` | Deception engine – runs alongside the keylogger. After 1.5s of idle typing, it injects realistic fake passwords, emails, and Linux commands directly into the log file, formatted identically to real keystrokes (including simulated typos). |
| `sentinel.py` | Storage sentinel – monitors `stolen_logs.txt` and auto-wipes it when the file exceeds 10KB, starving the malware of data. |
| `neuro_decoy_ui.py` | Desktop command center (CustomTkinter GUI) with toggle buttons, live stats, progress bar, and a real-time terminal for both daemons. |

---

## Quick Start

### 1. Create a virtual environment (Kali Linux)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install pynput customtkinter
```

### 3. Run the basic keylogger

```bash
python3 keylogger.py
```

### 4. Run the deception engine (replaces the basic keylogger)

```bash
python3 decoy.py
```

### 5. Run the storage sentinel (separate terminal)

```bash
python3 sentinel.py
```

### 6. Launch the GUI dashboard

```bash
python3 neuro_decoy_ui.py
```

The GUI lets you toggle both modules on/off and monitor payloads injected, file size, and wipe events in real time.

---

## Architecture

```
User keystrokes
      │
      ▼
┌─────────────┐     ┌──────────────────┐
│ decoy.py    │────▶│ stolen_logs.txt  │
│ (listener)  │     │ (log file)       │
└─────────────┘     └────────┬─────────┘
      │                      │
      │  idle > 1.5s         │  size ≥ 10KB
      ▼                      ▼
┌──────────────────┐  ┌─────────────┐
│ DecoyGenerator   │  │ sentinel.py │
│ (fake passwords, │  │ (auto-wipe) │
│  emails, cmds)   │  └─────────────┘
└──────────────────┘
```

- `decoy.py` listens for real keystrokes and logs them
- When you stop typing for 1.5s, it appends realistic decoy lines (with ~8% typo rate) that look indistinguishable from real keystrokes
- `sentinel.py` polls the log file every 0.5s and wipes it at 10KB

---

## DecoyGenerator (standalone)

The `DecoyGenerator` class inside `decoy.py` can also be used independently:

```python
from decoy import DecoyGenerator

dg = DecoyGenerator()
print(dg.get_random_decoy())  # random password / email / command
```

---

## Disclaimer

This project is for **educational and authorized testing purposes only**. Do not use on systems you do not own or have explicit permission to test.
