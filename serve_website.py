"""
DataPulse-AI: Local Web Server for Project Showcase & Portfolio Website.
Serves the 'website/' directory with zero external dependencies using Python's built-in http.server.
"""

import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

# Directory to serve
WEBSITE_DIR = Path(__file__).resolve().parent / "website"

DEFAULT_PORT = 8000


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEBSITE_DIR), **kwargs)

    def log_message(self, format, *args):
        # Clean terminal logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def find_free_port(start_port=8000, max_attempts=20):
    """Finds an available TCP port starting from start_port."""
    import socket
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    return start_port


def start_server():
    if not WEBSITE_DIR.exists():
        print(f"[ERROR] Website directory not found: {WEBSITE_DIR}")
        sys.exit(1)

    port = find_free_port(DEFAULT_PORT)
    url = f"http://localhost:{port}"

    print("=" * 65)
    print("🔬 DataPulse-AI: Academic Showcase & Portfolio Website Server")
    print("=" * 65)
    print(f"📁 Serving Directory: {WEBSITE_DIR}")
    print(f"🌐 Local Website URL: {url}")
    print("=" * 65)
    print("💡 Press Ctrl+C to terminate the server.\n")

    # Automatically launch user browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), CustomHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server gracefully stopped.")
        sys.exit(0)


if __name__ == "__main__":
    start_server()
