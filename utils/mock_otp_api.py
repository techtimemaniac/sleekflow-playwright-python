"""Local test-only REST endpoint for deterministic OTP data."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse


class _OtpHandler(BaseHTTPRequestHandler):
    """Serve a fixed OTP without contacting a real email or auth provider."""

    def do_GET(self):
        """Return the dummy OTP for an email query parameter."""
        query = parse_qs(urlparse(self.path).query)
        if self.path.startswith("/api/test/otp") and query.get("email"):
            payload = {"email": query["email"][0], "otp": "123456", "source": "test"}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404, "OTP endpoint requires an email query parameter")

    def log_message(self, *_args):
        """Keep the test endpoint quiet."""


class MockOtpApi:
    """Manage a local HTTP server exposing the dummy OTP endpoint."""

    def __init__(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _OtpHandler)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        """Return the base URL of the local endpoint."""
        return f"http://127.0.0.1:{self.server.server_port}"

    def start(self) -> None:
        """Start the local endpoint."""
        self.thread.start()

    def stop(self) -> None:
        """Stop the local endpoint."""
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
