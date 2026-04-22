#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "access.log"


class ModelRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        # Silence default stderr logging; requests are logged in structured form.
        return

    def do_GET(self) -> None:
        self._log_request()
        super().do_GET()

    def do_HEAD(self) -> None:
        self._log_request()
        super().do_HEAD()

    def _log_request(self) -> None:
        forwarded_for = self.headers.get("X-Forwarded-For", "")
        real_ip = self.headers.get("X-Real-IP", "")
        entry = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "client_ip": self.client_address[0],
            "client_port": self.client_address[1],
            "method": self.command,
            "path": self.path,
            "user_agent": self.headers.get("User-Agent", ""),
            "referer": self.headers.get("Referer", ""),
            "x_forwarded_for": forwarded_for,
            "x_real_ip": real_ip,
        }
        line = json.dumps(entry, ensure_ascii=True)
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        print(line, flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the solar model with access logging.")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host, default: 0.0.0.0")
    parser.add_argument("--port", type=int, default=8000, help="Bind port, default: 8000")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ModelRequestHandler)
    print(f"Serving {ROOT} on http://{args.host}:{args.port}", flush=True)
    print(f"Access log: {LOG_FILE}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
