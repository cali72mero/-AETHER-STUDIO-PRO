import os
import sys
import time
import json
import socket
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

_splash_server = None
_splash_thread = None
_splash_status = {
    "ready": False,
    "step": 1,
    "total_steps": 3,
    "message": "⚡ Aether Studio Pro startet... Bitte kurz warten!"
}

SPLASH_HTML = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aether Diffusion Studio Pro – Startet...</title>
    <style>
        :root {
            --bg: #0b0f19;
            --card: rgba(18, 24, 38, 0.85);
            --border: rgba(99, 102, 241, 0.3);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.5);
            --cyan: #06b6d4;
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.15), transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.12), transparent 40%);
            color: var(--text);
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .splash-card {
            background: var(--card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 40px;
            max-width: 540px;
            width: 100%;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 40px var(--primary-glow);
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid var(--primary);
            color: #a5b4fc;
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 20px;
        }
        h1 {
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 32px;
        }
        .spinner-container {
            position: relative;
            width: 90px;
            height: 90px;
            margin: 0 auto 28px;
        }
        .spinner-ring {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px solid rgba(99, 102, 241, 0.15);
            border-top-color: var(--primary);
            border-right-color: var(--cyan);
            animation: spin 1.2s cubic-bezier(0.5, 0.1, 0.4, 0.9) infinite;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
        }
        .spinner-inner {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.8rem;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes pulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.9; }
            50% { transform: translate(-50%, -50%) scale(1.15); opacity: 1; }
        }
        .status-box {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
        }
        .status-message {
            font-size: 1.05rem;
            font-weight: 600;
            color: #38bdf8;
            margin-bottom: 8px;
            min-height: 24px;
            transition: all 0.3s;
        }
        .progress-track {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 999px;
            overflow: hidden;
            position: relative;
        }
        .progress-fill {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 30%;
            background: linear-gradient(90deg, var(--primary), var(--cyan));
            border-radius: 999px;
            animation: progressMove 2.5s ease-in-out infinite;
        }
        @keyframes progressMove {
            0% { left: -30%; width: 30%; }
            50% { width: 50%; }
            100% { left: 100%; width: 30%; }
        }
        .info-hint {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
        }
        .highlight {
            color: #a5b4fc;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="splash-card">
        <div class="badge">🚀 Startet automatisch</div>
        <h1>Aether Diffusion Studio Pro</h1>
        <p class="subtitle">v2.7.2 • Ultra-Schneller Start & Low-VRAM Engine</p>

        <div class="spinner-container">
            <div class="spinner-ring"></div>
            <div class="spinner-inner">🌌</div>
        </div>

        <div class="status-box">
            <div id="status-message" class="status-message">⚡ Studio wird initialisiert...</div>
            <div class="progress-track">
                <div class="progress-fill"></div>
            </div>
        </div>

        <p class="info-hint">
            Bitte kurz warten – die Seite <span class="highlight">wechselt automatisch</span> direkt ins Studio, sobald die KI-Modelle einsatzbereit sind. Du musst das Terminal nicht mehr beobachten!
        </p>
    </div>

    <script>
        let isRedirecting = false;
        async function checkStatus() {
            if (isRedirecting) return;
            try {
                let res = await fetch('/api/splash_status?t=' + Date.now());
                if (res.ok) {
                    let data = await res.json();
                    if (data.message) {
                        document.getElementById('status-message').innerText = data.message;
                    }
                    if (data.ready) {
                        isRedirecting = true;
                        document.getElementById('status-message').innerText = "✅ Bereit! Studio lädt...";
                        setTimeout(() => location.reload(), 400);
                        return;
                    }
                }
            } catch (err) {
                // Splash server might have shut down to let Gradio take over port 7865!
                setTimeout(async () => {
                    try {
                        let testRes = await fetch('/?t=' + Date.now());
                        if (testRes.status === 200) {
                            isRedirecting = true;
                            location.reload();
                        }
                    } catch (e) {}
                }, 1000);
            }
        }
        setInterval(checkStatus, 700);
    </script>
</body>
</html>
"""


class SplashHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence HTTP access logs
        return

    def do_GET(self):
        global _splash_status
        if self.path.startswith('/api/splash_status'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps(_splash_status).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.end_headers()
            self.wfile.write(SPLASH_HTML.encode('utf-8'))


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def start_splash_server(port=7865, open_browser_flag=True):
    """
    Starts the instant splash server on the specified port.
    Opens the browser immediately so the user sees feedback instantly.
    """
    global _splash_server, _splash_thread

    # Check if port is already bound
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', port))
        sock.close()
    except OSError:
        # Port already occupied (e.g. previous server running), skip splash
        print(f"[Splash] Port {port} already occupied. Skipping splash screen.")
        return False

    try:
        _splash_server = ReusableHTTPServer(('0.0.0.0', port), SplashHTTPHandler)
        _splash_thread = threading.Thread(target=_splash_server.serve_forever, daemon=True)
        _splash_thread.start()
        print(f"[Splash] Instant Loading Screen active on http://127.0.0.1:{port}")

        if open_browser_flag:
            def _open():
                time.sleep(0.1)
                try:
                    webbrowser.open(f"http://127.0.0.1:{port}")
                except Exception:
                    pass
            threading.Thread(target=_open, daemon=True).start()

        return True
    except Exception as e:
        print(f"[Splash] Could not start splash server: {e}")
        return False


def update_splash_status(message, step=None, total_steps=None):
    """Updates the status displayed on the splash screen."""
    global _splash_status
    _splash_status["message"] = message
    if step is not None:
        _splash_status["step"] = step
    if total_steps is not None:
        _splash_status["total_steps"] = total_steps


def stop_splash_server():
    """Stops the splash server so Gradio can cleanly bind to the port."""
    global _splash_server, _splash_thread
    if _splash_server is not None:
        _splash_status["ready"] = True
        try:
            _splash_server.shutdown()
            _splash_server.server_close()
        except Exception:
            pass
        _splash_server = None
        _splash_thread = None
        time.sleep(0.15)
