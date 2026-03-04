#!/usr/bin/env python3
"""
Lightweight web wrapper for the ACN demo.
- Serves static UI from Demo/web
- Streams live demo output via SSE at /api/run
- Exposes chain data as JSON at /api/chain

Run:
    python3 Demo/web_server.py
Then open http://localhost:8000
"""
import json
import os
import subprocess
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DEMO_ROOT = ROOT  # contains run_demo.py
WEB_ROOT = ROOT / "web"
PORT = int(os.environ.get("PORT", "8000"))

# Ensure imports from Demo/ work
sys.path.insert(0, str(DEMO_ROOT))


class ACNHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # quieter server logs
        pass

    def translate_path(self, path):
        # Serve static files from WEB_ROOT
        path = path.split("?", 1)[0].split("#", 1)[0]
        if path == "/":
            path = "/index.html"
        candidate = WEB_ROOT / path.lstrip("/")
        return str(candidate)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/run":
            return self.handle_run()
        if parsed.path == "/api/chain":
            return self.handle_chain()
        return super().do_GET()

    def handle_run(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        cmd = ["python3", "run_demo.py", "--no-color"]
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        proc = subprocess.Popen(
            cmd,
            cwd=str(DEMO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
        )
        try:
            for line in proc.stdout:  # type: ignore
                line = line.rstrip("\n")
                payload = f"data: {line}\n\n"
                self.wfile.write(payload.encode("utf-8"))
                self.wfile.flush()
        except BrokenPipeError:
            proc.kill()
            return
        finally:
            proc.wait()
        # Signal completion
        self.wfile.write(b"event: end\ndata: done\n\n")
        self.wfile.flush()

    def handle_chain(self):
        try:
            from acn.blockchain import Blockchain
            chain = Blockchain().get_chain()
            payload = [
                {
                    "block_num": b.block_num,
                    "block_hash": b.block_hash,
                    "prev_hash": b.prev_hash,
                    "timestamp": b.timestamp,
                    "record_type": b.record_type,
                    "summary": b.summary(),
                    "data": b.data,
                }
                for b in chain
            ]
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:  # pragma: no cover
            msg = {"error": str(exc)}
            body = json.dumps(msg).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


def main():
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), ACNHandler)
    print(f"ACN web server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
