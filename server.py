#!/usr/bin/env python3
"""Local HTTPS API server."""
from __future__ import annotations

import json
import ssl
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


class ApiHandler(BaseHTTPRequestHandler):
    server_version = "LocalHttpsApi/1.0"

    def _send_json(self, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json({"status": "ok"})
            return
        self._send_json({"error": "not_found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/echo":
            self._send_json({"error": "not_found"}, status=HTTPStatus.NOT_FOUND)
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b""
        try:
            payload = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            self._send_json({"error": "invalid_json"}, status=HTTPStatus.BAD_REQUEST)
            return
        self._send_json({"received": payload})


def run(host: str = "0.0.0.0", port: int = 8443) -> None:
    httpd = HTTPServer((host, port), ApiHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f"Serving HTTPS on https://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
