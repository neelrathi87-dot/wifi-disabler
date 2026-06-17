"""
Desactivateur - Serveur backend
Necessite : pip install flask
"""

import sys
import ctypes
import subprocess
import re
from flask import Flask, jsonify, send_from_directory

# ─── Auto-elevation ──────────────────────────────────────────────────────────
# If not running as admin, re-launch self with a UAC prompt automatically.

def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

if __name__ == "__main__" and not _is_admin():
    print("Pas administrateur - demande d'elevation...")
    # ShellExecuteW with "runas" triggers the UAC dialog
    ret = ctypes.windll.shell32.ShellExecuteW(
        None,           # hwnd
        "runas",        # verb - triggers UAC
        sys.executable, # python.exe
        f'"{__file__}"',# this script
        None,           # working dir
        1               # SW_NORMAL - show window
    )
    # ret > 32 means success (UAC accepted and new process launched)
    sys.exit(0)

# ─── Flask app ───────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder="static")

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"]        = "no-cache"
    response.headers["Expires"]       = "0"
    return response

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _detect_interface():
    """Detecte le nom de l'adaptateur Wi-Fi via netsh."""
    try:
        out = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True, text=True, timeout=5
        ).stdout
        for line in out.splitlines():
            if re.search(r"wi.?fi|wireless|wlan", line, re.IGNORECASE):
                parts = line.split()
                name  = " ".join(parts[3:])
                if name:
                    return name
    except Exception:
        pass
    return "Wi-Fi"


def _run(action: str):
    """Execute netsh pour activer/desactiver l'adaptateur."""
    iface  = _detect_interface()
    result = subprocess.run(
        ["netsh", "interface", "set", "interface", iface, action],
        capture_output=True, text=True, timeout=10
    )
    ok  = result.returncode == 0
    msg = result.stdout.strip() or result.stderr.strip()
    return ok, msg or ("Desactive." if action == "disable" else "Active.")


def _is_enabled():
    """Retourne True si l'adaptateur Wi-Fi est active."""
    try:
        iface = _detect_interface()
        out   = subprocess.run(
            ["netsh", "interface", "show", "interface", iface],
            capture_output=True, text=True, timeout=5
        ).stdout
        return "enabled" in out.lower()
    except Exception:
        return None


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/status")
def api_status():
    return jsonify({"enabled": _is_enabled(), "admin": _is_admin()})


@app.route("/api/disable", methods=["POST"])
def api_disable():
    ok, msg = _run("disable")
    return jsonify({
        "success": ok,
        "message": msg if ok else (msg or "Echec - droits administrateur requis.")
    }), (200 if ok else 500)


@app.route("/api/enable", methods=["POST"])
def api_enable():
    ok, msg = _run("enable")
    return jsonify({
        "success": ok,
        "message": msg if ok else (msg or "Echec - droits administrateur requis.")
    }), (200 if ok else 500)


# ─── Lancement ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    admin_status = "ADMIN OK" if _is_admin() else "NON-ADMIN (erreur)"
    print("=" * 50)
    print(f"  Desactivateur  -  http://localhost:5000")
    print(f"  Statut : {admin_status}")
    print("=" * 50)
    app.run(host="127.0.0.1", port=5000, debug=False)
