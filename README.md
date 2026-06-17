# Wi-Fi Controller

A sleek local web app to enable/disable your Wi-Fi adapter from the browser.

## Project Structure

```
wifi disabler/
├── server.py        ← Flask backend (runs netsh commands)
├── start.bat        ← One-click launcher (auto-elevates to Admin)
└── static/
    └── index.html   ← Frontend UI
```

## Quick Start

**Option A – Double-click launcher (easiest)**  
Double-click `start.bat`. It will:
1. Ask for Administrator permission (required for netsh)
2. Auto-install Flask if missing
3. Open your browser to `http://localhost:5000`

**Option B – Manual**
```powershell
# In an Administrator PowerShell:
pip install flask
python server.py
# Then open http://localhost:5000
```

## Requirements

- Python 3.7+
- Flask (`pip install flask`)
- **Must run as Administrator** (netsh requires it)

## What it does

| Action | Windows Command |
|--------|----------------|
| Disable Wi-Fi | `netsh interface set interface "Wi-Fi" disable` |
| Enable Wi-Fi  | `netsh interface set interface "Wi-Fi" enable`  |

The adapter name is auto-detected from your system.

## Security Note

The server only listens on `127.0.0.1` (localhost), so it's not accessible from other devices on your network.
