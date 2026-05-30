#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$DIR/venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "[-] Virtual environment not found. Creating..."
    python3 -m venv "$DIR/venv"
    "$DIR/venv/bin/pip" install --quiet pynput customtkinter
fi

echo "[*] Starting Neuro-Decoy Command Center..."
exec "$VENV_PYTHON" "$DIR/neuro_decoy_ui.py"
