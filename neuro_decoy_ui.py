#!/usr/bin/env python3
"""
Neuro-Decoy: Deception Framework
Cyber Defense Command Center UI  v2.1.0
"""

import customtkinter as ctk
import subprocess
import threading
import os
import signal
import sys
import time
from datetime import datetime

# ── Color Palette ──────────────────────────────────────────────────────────
BG_PRIMARY = "#0B0E14"
BG_CARD   = "#141820"
BG_TERM   = "#0A0C10"
CYAN      = "#00E5FF"
RED       = "#FF3366"
GREEN     = "#00FF41"
YELLOW    = "#FFD600"
WHITE     = "#E8EAF0"
GRAY      = "#3A3F4A"
DIM       = "#1E2230"

# ── Fonts ──────────────────────────────────────────────────────────────────
FONT_H1       = ("Segoe UI", 22, "bold")
FONT_H2       = ("Segoe UI", 11)
FONT_MONO     = ("JetBrains Mono", 11)
FONT_MONO_SM  = ("JetBrains Mono", 10)
FONT_BADGE    = ("Segoe UI", 26, "bold")
FONT_COUNTER  = ("Segoe UI", 24, "bold")

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DECOY_PY  = os.path.join(BASE_DIR, "decoy.py")
SENT_PY   = os.path.join(BASE_DIR, "sentinel.py")

try:
    from config import LOG_FILE
except ImportError:
    LOG_FILE = os.path.join(BASE_DIR, "stolen_logs.txt")

_PYTHON = sys.executable if sys.executable else "python3"
_UNBUF_ENV = {**os.environ, "PYTHONUNBUFFERED": "1"}


# ══════════════════════════════════════════════════════════════════════════
#  Glassmorphism Card Base
# ══════════════════════════════════════════════════════════════════════════
class GlassCard(ctk.CTkFrame):
    def __init__(self, master, **kw):
        super().__init__(master, fg_color=BG_CARD, corner_radius=12,
                         border_width=1, border_color=DIM, **kw)


# ══════════════════════════════════════════════════════════════════════════
#  Live Execution Terminal
# ══════════════════════════════════════════════════════════════════════════
class LiveTerminal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_TERM, corner_radius=8,
                         border_width=1, border_color=DIM)

        lbl = ctk.CTkLabel(self, text="⚡ LIVE EXECUTION TERMINAL",
                           font=FONT_MONO, text_color=CYAN, anchor="w")
        lbl.pack(fill="x", padx=14, pady=(8, 0))

        self.txt = ctk.CTkTextbox(self, fg_color="#080A0E", text_color=GREEN,
                                  font=FONT_MONO_SM, corner_radius=6,
                                  border_width=0, height=180)
        self.txt.pack(fill="both", expand=True, padx=8, pady=(4, 8))
        self.txt.configure(state="disabled")

        self._append("root@neuro-decoy:~$ System ready.\n")

    def _append(self, text, color=None):
        self.txt.configure(state="normal")
        self.txt.insert("end", text)
        self.txt.see("end")
        self.txt.configure(state="disabled")

    def write(self, tag, msg, color=GREEN):
        ts = datetime.now().strftime("%H:%M:%S")
        self._append(f"[{ts}] ")
        self.txt.configure(state="normal")
        self.txt.insert("end", f"[{tag}] ", "tag_cyan")
        self.txt.insert("end", f"{msg}\n")
        self.txt.tag_config("tag_cyan", foreground=CYAN)
        self.txt.see("end")
        self.txt.configure(state="disabled")


# ══════════════════════════════════════════════════════════════════════════
#  Module 1 – Core Deception Engine
# ══════════════════════════════════════════════════════════════════════════
class DecoyPanel(GlassCard):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        # Header row
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(14, 0))
        ctk.CTkLabel(hdr, text="⚡", font=FONT_BADGE,
                     text_color=CYAN).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(hdr, text="CORE DECEPTION\nENGINE",
                     font=FONT_H2, text_color=WHITE, justify="left").pack(side="left")
        ctk.CTkLabel(hdr, text="MODULE 01", font=("Segoe UI", 8),
                     text_color=GRAY).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=DIM).pack(fill="x", padx=16, pady=(10, 10))

        # Toggle
        tf = ctk.CTkFrame(self, fg_color="transparent")
        tf.pack(fill="x", padx=16, pady=4)
        self.toggle = ctk.CTkSwitch(tf, text="", switch_width=50, switch_height=24,
                                    progress_color=CYAN, command=self._on_toggle)
        self.toggle.pack(side="left")
        self.toggle_lbl = ctk.CTkLabel(tf, text="ENGAGE DECEPTION",
                                       font=FONT_MONO, text_color=GRAY)
        self.toggle_lbl.pack(side="left", padx=(10, 0))

        # Status
        sf = ctk.CTkFrame(self, fg_color="transparent")
        sf.pack(fill="x", padx=16, pady=(8, 2))
        ctk.CTkLabel(sf, text="STATUS:", font=FONT_MONO_SM,
                     text_color=GRAY).pack(side="left")
        self.dot = ctk.CTkLabel(sf, text="●", font=FONT_MONO, text_color=GRAY)
        self.dot.pack(side="left", padx=(6, 0))
        self.stat = ctk.CTkLabel(sf, text="DISENGAGED", font=FONT_MONO_SM,
                                 text_color=GRAY)
        self.stat.pack(side="left", padx=(4, 0))

        # Stats
        bt = ctk.CTkFrame(self, fg_color="transparent")
        bt.pack(fill="x", padx=16, pady=(10, 14))
        # payloads
        p1 = ctk.CTkFrame(bt, fg_color="transparent")
        p1.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(p1, text="PAYLOADS INJECTED", font=FONT_MONO_SM,
                     text_color=GRAY, anchor="w").pack(fill="x")
        self.cnt = ctk.CTkLabel(p1, text="0", font=FONT_COUNTER,
                                text_color=CYAN, anchor="w")
        self.cnt.pack(fill="x")
        # last burst
        p2 = ctk.CTkFrame(bt, fg_color="transparent")
        p2.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(p2, text="LAST BURST", font=FONT_MONO_SM,
                     text_color=GRAY, anchor="w").pack(fill="x")
        self.burst = ctk.CTkLabel(p2, text="--", font=FONT_MONO,
                                  text_color=WHITE, anchor="w")
        self.burst.pack(fill="x")

    def _on_toggle(self):
        on = self.toggle.get()
        if on:
            self.toggle_lbl.configure(text_color=CYAN)
            self.dot.configure(text_color=GREEN)
            self.stat.configure(text="ACTIVE — IDLE TRACKING")
            self.app.start_decoy()
        else:
            self.toggle_lbl.configure(text_color=GRAY)
            self.dot.configure(text_color=GRAY)
            self.stat.configure(text="DISENGAGED")
            self.app.stop_decoy()

    def push_stats(self, count, last_burst):
        self.cnt.configure(text=str(count))
        self.burst.configure(text=last_burst)


# ══════════════════════════════════════════════════════════════════════════
#  Module 2 – Storage Sentinel
# ══════════════════════════════════════════════════════════════════════════
class SentinelPanel(GlassCard):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(14, 0))
        ctk.CTkLabel(hdr, text="🛡", font=FONT_BADGE,
                     text_color=CYAN).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(hdr, text="STORAGE\nSENTINEL",
                     font=FONT_H2, text_color=WHITE, justify="left").pack(side="left")
        ctk.CTkLabel(hdr, text="MODULE 02", font=("Segoe UI", 8),
                     text_color=GRAY).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=DIM).pack(fill="x", padx=16, pady=(10, 10))

        # Toggle
        tf = ctk.CTkFrame(self, fg_color="transparent")
        tf.pack(fill="x", padx=16, pady=4)
        self.toggle = ctk.CTkSwitch(tf, text="", switch_width=50, switch_height=24,
                                    progress_color=CYAN, command=self._on_toggle)
        self.toggle.pack(side="left")
        self.toggle_lbl = ctk.CTkLabel(tf, text="ENABLE SENTINEL",
                                       font=FONT_MONO, text_color=GRAY)
        self.toggle_lbl.pack(side="left", padx=(10, 0))

        # Progress bar
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="x", padx=16, pady=(12, 0))
        self.pbar = ctk.CTkProgressBar(self, orientation="horizontal",
                                       progress_color=CYAN, height=8,
                                       corner_radius=4, border_width=0)
        self.pbar.pack(fill="x", padx=16)
        self.pbar.set(0.0)

        sizef = ctk.CTkFrame(self, fg_color="transparent")
        sizef.pack(fill="x", padx=16, pady=(2, 0))
        self.sz_lbl = ctk.CTkLabel(sizef, text="0.0 KB / 10.0 KB",
                                   font=FONT_MONO_SM, text_color=GRAY, anchor="w")
        self.sz_lbl.pack(side="left")
        ctk.CTkLabel(sizef, text="THRESHOLD: 10 KB",
                     font=FONT_MONO_SM, text_color=GRAY, anchor="e").pack(side="right")

        # Stats
        bt = ctk.CTkFrame(self, fg_color="transparent")
        bt.pack(fill="x", padx=16, pady=(6, 14))
        p1 = ctk.CTkFrame(bt, fg_color="transparent")
        p1.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(p1, text="THREAT LOGS WIPED", font=FONT_MONO_SM,
                     text_color=GRAY, anchor="w").pack(fill="x")
        self.wiped = ctk.CTkLabel(p1, text="0", font=FONT_COUNTER,
                                  text_color=RED, anchor="w")
        self.wiped.pack(fill="x")
        p2 = ctk.CTkFrame(bt, fg_color="transparent")
        p2.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(p2, text="CURRENT SIZE", font=FONT_MONO_SM,
                     text_color=GRAY, anchor="w").pack(fill="x")
        self.cur_sz = ctk.CTkLabel(p2, text="0.0 KB", font=FONT_MONO,
                                   text_color=WHITE, anchor="w")
        self.cur_sz.pack(fill="x")

    def _on_toggle(self):
        on = self.toggle.get()
        if on:
            self.toggle_lbl.configure(text_color=CYAN)
            self.app.start_sentinel()
        else:
            self.toggle_lbl.configure(text_color=GRAY)
            self.app.stop_sentinel()

    def push_progress(self, size_kb, threshold=10.0):
        pct = min(size_kb / threshold, 1.0)
        self.pbar.set(pct)
        self.sz_lbl.configure(text=f"{size_kb:.1f} KB / {threshold:.1f} KB")
        self.cur_sz.configure(text=f"{size_kb:.1f} KB")
        if pct >= 0.9:
            self.pbar.configure(progress_color=RED)
        elif pct >= 0.7:
            self.pbar.configure(progress_color=YELLOW)
        else:
            self.pbar.configure(progress_color=CYAN)

    def push_wiped(self, n):
        self.wiped.configure(text=str(n))


# ══════════════════════════════════════════════════════════════════════════
#  Main Application
# ══════════════════════════════════════════════════════════════════════════
class NeuroDecoyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Neuro-Decoy: Deception Framework  v2.1.0")
        self.geometry("960x700")
        self.configure(fg_color=BG_PRIMARY)
        self.resizable(False, False)

        # ── internal state ──
        self.decoy_proc: subprocess.Popen | None = None
        self.sent_proc: subprocess.Popen | None = None
        self.decoy_on = False
        self.sent_on = False
        self.payload_cnt = 0
        self.wiped_cnt = 0
        self.last_burst = "--"
        self._dying = False

        # ── build UI ──
        self._build_header()
        self._build_dashboard()
        self._build_terminal()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # periodic file-size poll
        self.after(1000, self._poll_log)

    # ── layout helpers ─────────────────────────────────────────────────────

    def _build_header(self):
        h = ctk.CTkFrame(self, fg_color="transparent")
        h.pack(fill="x", padx=24, pady=(18, 0))
        ctk.CTkLabel(h, text="⚡ NEURO-DECOY",
                     font=FONT_H1, text_color=CYAN).pack(side="left")
        ctk.CTkLabel(h, text="DECEPTION FRAMEWORK",
                     font=FONT_MONO, text_color=GRAY).pack(side="left", padx=(10, 0))
        ctk.CTkLabel(h, text="v2.1.0  |  CYBER DEFENSE SYSTEMS",
                     font=FONT_MONO_SM, text_color=GRAY).pack(side="right")
        ctk.CTkFrame(self, height=1, fg_color=DIM).pack(fill="x", padx=24, pady=(12, 0))

    def _build_dashboard(self):
        d = ctk.CTkFrame(self, fg_color="transparent")
        d.pack(fill="both", expand=True, padx=24, pady=(16, 0))
        d.grid_columnconfigure(0, weight=1, uniform="c")
        d.grid_columnconfigure(1, weight=1, uniform="c")
        d.grid_rowconfigure(0, weight=1)

        self.p_decoy = DecoyPanel(d, self)
        self.p_decoy.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.p_sent = SentinelPanel(d, self)
        self.p_sent.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    def _build_terminal(self):
        self.term = LiveTerminal(self)
        self.term.pack(fill="both", expand=False, padx=24, pady=(12, 14))

    # ── process control – decoy ───────────────────────────────────────────

    def start_decoy(self):
        if self.decoy_on:
            return
        try:
            self.decoy_proc = subprocess.Popen(
                [_PYTHON, DECOY_PY],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, cwd=BASE_DIR, env=_UNBUF_ENV)
            self.decoy_on = True
            self.term.write("DECOY", "Engine engaged — injecting decoys on idle ...", CYAN)
            threading.Thread(target=self._pipe_decoy, daemon=True).start()
        except Exception as e:
            self.term.write("ERROR", f"decoy launch failed: {e}", RED)

    def stop_decoy(self):
        self.decoy_on = False
        if self.decoy_proc:
            self.decoy_proc.terminate()
            try:
                self.decoy_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.decoy_proc.kill()
            self.decoy_proc = None
        self.term.write("DECOY", "Engine disengaged.", YELLOW)

    def _pipe_decoy(self):
        try:
            for line in iter(self.decoy_proc.stdout.readline, ""):
                if not line or self._dying:
                    break
                ln = line.rstrip()
                if ln:
                    self.after(0, self._on_decoy_line, ln)
        except Exception:
            pass

    def _on_decoy_line(self, ln):
        self.term.write("DECOY", ln, GREEN)
        if "injected" in ln.lower() or "burst" in ln.lower():
            self.payload_cnt += 1
            self.last_burst = datetime.now().strftime("%H:%M:%S")
            self.p_decoy.push_stats(self.payload_cnt, self.last_burst)

    # ── process control – sentinel ────────────────────────────────────────

    def start_sentinel(self):
        if self.sent_on:
            return
        try:
            self.sent_proc = subprocess.Popen(
                [_PYTHON, SENT_PY],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, cwd=BASE_DIR, env=_UNBUF_ENV)
            self.sent_on = True
            self.term.write("SENTINEL", "Oversight engaged — monitoring log file ...", CYAN)
            threading.Thread(target=self._pipe_sent, daemon=True).start()
        except Exception as e:
            self.term.write("ERROR", f"sentinel launch failed: {e}", RED)

    def stop_sentinel(self):
        self.sent_on = False
        if self.sent_proc:
            self.sent_proc.terminate()
            try:
                self.sent_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.sent_proc.kill()
            self.sent_proc = None
        self.term.write("SENTINEL", "Oversight disengaged.", YELLOW)

    def _pipe_sent(self):
        try:
            for line in iter(self.sent_proc.stdout.readline, ""):
                if not line or self._dying:
                    break
                ln = line.rstrip()
                if ln:
                    self.after(0, self._on_sent_line, ln)
        except Exception:
            pass

    def _on_sent_line(self, ln):
        self.term.write("SENTINEL", ln, GREEN)
        if "wiped" in ln.lower() or "eliminated" in ln.lower():
            self.wiped_cnt += 1
            self.p_sent.push_wiped(self.wiped_cnt)

    # ── periodic file-size polling ────────────────────────────────────────

    def _poll_log(self):
        if self._dying:
            return
        try:
            kb = os.path.getsize(LOG_FILE) / 1024.0 if os.path.exists(LOG_FILE) else 0.0
        except OSError:
            kb = 0.0
        self.p_sent.push_progress(kb)
        self.after(1000, self._poll_log)

    # ── cleanup ───────────────────────────────────────────────────────────

    def _on_close(self):
        self._dying = True
        self.stop_decoy()
        self.stop_sentinel()
        self.destroy()


# ══════════════════════════════════════════════════════════════════════════
#  Entry Point
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    NeuroDecoyApp().mainloop()