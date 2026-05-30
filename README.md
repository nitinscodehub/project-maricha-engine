# PROJECT MARICHA 🛡️

**Deception-Based Keystroke Defense Framework** *Machine-Assisted Random Injection & Covert Heuristic Alteration*

---

## Overview

PROJECT MARICHA ek **real-time keystroke deception system** hai jo:
- Real keyboard input log karta hai (`stolen_logs.txt`)
- **Fake decoy data** (passwords, emails, shell commands) automatically inject karta hai jab aap idle ho
- **Typo simulation** karta hai — human typing errors jaise dikhta hai
- **Auto-wipe** karta hai log file jab threshold (10KB) cross ho

Iska matlab: agar koi keylogger steal kare, to usse **useless fake data** milega aur asli keystrokes wipe ho jaayengi.

---

## 📦 Installation

```bash
# 1. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Dependencies
pip install pynput customtkinter

# 3. Run
python maricha_ui.py
```

Ya ek command mein:

```bash
./run.sh
```

---

## 🚀 How to Use

### Option 1: GUI Mode (Recommended)

```bash
./run.sh
```

GUI open hoga:
1. **Decoy Engine** toggle ON karein → keylogger + fake decoy injection start
2. **Storage Sentinel** toggle ON karein → auto-wipe monitoring start  
3. **Live Terminal** mein saara output real-time dikhega

![GUI Layout](https://via.placeholder.com/600x300/0B0E14/00E5FF?text=Project+Maricha+UI+Preview)

### Option 2: CLI Mode (Headless)

```bash
# Sirf decoy engine (keylogger + injection)
venv/bin/python decoy.py

# Sirf sentinel (monitor + auto-wipe)
venv/bin/python sentinel.py
```

### Option 3: Sirf Basic Keylogger

```bash
venv/bin/python keylogger.py
```

---

## ⚙️ Configuration

Sab kuch customize kar sakte hain `config.py` mein:

```python
DECOY_IDLE_SECONDS = 1.5        # Kitni der idle hona chahiye injection se pehle
DECOY_BREAK_SECONDS = 1.0       # Typing resume hone par injection ruk jayega
DECOY_TYPO_CHANCE = 0.08        # 8% chance har character ka typo ho
DECOY_POLL_INTERVAL = 0.5       # Idle check frequency (seconds)
SENTINEL_THRESHOLD_KB = 10      # Kitna size hone par auto-wipe kare
SENTINEL_POLL_INTERVAL = 1.0    # File monitor frequency
```

Decoy word lists, commands, domains bhi yahi customize kar sakte hain.

---

## 📂 File Structure

| File | Role |
|---|---|
| `decoy.py` | Core engine — keylogger + decoy injection |
| `sentinel.py` | Storage sentinel — auto-wipe monitor |
| `maricha_ui.py` | GUI command center |
| `keylogger.py` | Standalone basic keylogger |
| `config.py` | Central settings |
| `run.sh` | One-click launcher |
| `stolen_logs.txt` | Log file (auto-generated) |

---

## 🧪 Testing

```bash
# Decoy engine test
timeout 10 venv/bin/python decoy.py
cat stolen_logs.txt

# Sentinel test
echo "AAAA... (10KB+ data)" > stolen_logs.txt
timeout 5 venv/bin/python sentinel.py
```

---

## 🐞 Known Behavior

- **ESC key** press karein to keylogger stop hota hai (basic mode)
- **Ctrl+C** / SIGTERM se saare components gracefully shutdown hote hain
- Decoy injection **typing ke beech** nahi hota — sirf idle time pe
- Sentinel **sirf tab print** karta hai jab file size change ho ya threshold cross ho

---

## 📄 License & Patent

Patent disclosure document: `PROJECT_MARICHA.pdf`  
System: **Project MARICHA v2.1.0 | Cyber Deception Framework** Author & Lead Researcher: **Nitin Dhurve**
