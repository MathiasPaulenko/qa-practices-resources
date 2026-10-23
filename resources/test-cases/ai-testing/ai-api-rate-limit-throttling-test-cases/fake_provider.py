"""Fake AI provider with RPM + TPM rate limiting, stdlib only.

Implements the surfaces the test-cases exercise:
- Per-key + per-model request buckets (RPM) and token buckets (TPM, daily quota).
- OpenAI-style x-ratelimit-* headers on every response.
- Retry-After on 429 (seconds or HTTP-date, configurable).
- 529 overload simulation via the X-Force-Status request header.
- Fixed window resets so quota-reset behaviour is testable in milliseconds.
"""

import json
import threading
import time
from collections import deque
from email.utils import formatdate
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class ProviderConfig:
    """Rate-limit policy for the fake provider.

    window is in seconds and may be fractional so tests can observe resets
    without waiting a real minute.
    """

    def __init__(self, window: float = 60.0):
        self.window = window
        # per-key tier: rpm / tpm / daily token cap
        self.key_tiers = {
            "free-key": {"rpm": 5, "tpm": 200, "daily": 1000},
            "pro-key": {"rpm": 50, "tpm": 5000, "daily": 100000},
        }
        # optional per-model RPM override (model -> rpm)
        self.model_rpm = {"big-model": 2, "small-model": 50}
        # return Retry-After as HTTP-date instead of seconds
        self.retry_after_http_date = False


class _Bucket:
    __slots__ = ("stamps", "tokens", "daily", "win_start")

    def __init__(self):
        self.stamps = deque()
        self.tokens = 0
        self.daily = 0
        self.win_start = time.monotonic()


class FakeProvider:
    def __init__(self, config: ProviderConfig | None = None):
        self.config = config or ProviderConfig()
        self._buckets: dict[tuple[str, str], _Bucket] = {}
        self._lock = threading.Lock()
        self._server: ThreadingHTTPServer | None = None
        self.port: int = 0

    # -- lifecycle --------------------------------------------------------

    def start(self) -> "FakeProvider":
        provider = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # keep tests quiet
                pass

            def _json(self, status, payload, headers=None):
                body = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                for k, v in (headers or {}).items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                if self.path != "/v1/chat/completions":
                    self._json(404, {"error": {"message": "not found"}})
                    return
                if self.headers.get("X-Force-Status") == "529":
                    self._json(529, {"error": {"type": "overloaded", "message": "provider overloaded"}})
                    return
                auth = self.headers.get("Authorization", "")
                key = auth.removeprefix("Bearer ").strip()
                cfg = provider.config
                tier = cfg.key_tiers.get(key)
                if tier is None:
                    self._json(401, {"error": {"message": "invalid api key"}})
                    return
                length = int(self.headers.get("Content-Length", 0))
                try:
                    body = json.loads(self.rfile.read(length) or b"{}")
                except json.JSONDecodeError:
                    self._json(400, {"error": {"message": "malformed json"}})
                    return
                model = body.get("model", "small-model")
                max_tokens = int(body.get("max_tokens", 1))

                status, headers, payload = provider._check(key, model, max_tokens, tier)
                self._json(status, payload, headers)

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self._server.server_address[1]
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        return self

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/v1/chat/completions"

    # -- rate-limit core --------------------------------------------------

    def _check(self, key: str, model: str, max_tokens: int, tier: dict):
        cfg = self.config
        now = time.monotonic()
        with self._lock:
            bucket = self._buckets.setdefault((key, model), _Bucket())
            if now - bucket.win_start >= cfg.window:
                bucket.stamps.clear()
                bucket.tokens = 0
                bucket.win_start = now

            rpm = min(tier["rpm"], cfg.model_rpm.get(model, tier["rpm"]))
            reset_in = max(0.0, cfg.window - (now - bucket.win_start))
            headers = self._rl_headers(rpm - len(bucket.stamps), rpm, reset_in, tier["tpm"], tier["tpm"] - bucket.tokens)

            def retry_after():
                if cfg.retry_after_http_date:
                    return formatdate(time.time() + reset_in, usegmt=True)
                return str(int(reset_in) + 1)

            if len(bucket.stamps) >= rpm:
                headers["Retry-After"] = retry_after()
                return 429, headers, {"error": {"type": "rate_limit", "message": f"RPM limit {rpm} exceeded"}}

            if bucket.tokens + max_tokens > tier["tpm"]:
                headers["Retry-After"] = retry_after()
                return 429, headers, {"error": {"type": "tokens", "message": "token budget (TPM) exceeded"}}

            if bucket.daily + max_tokens > tier["daily"]:
                return 403, headers, {"error": {"type": "insufficient_quota", "message": "daily quota exhausted"}}

            bucket.stamps.append(now)
            bucket.tokens += max_tokens
            bucket.daily += max_tokens
            headers = self._rl_headers(rpm - len(bucket.stamps), rpm, reset_in, tier["tpm"], tier["tpm"] - bucket.tokens)
            return 200, headers, {
                "id": "cmpl-fake-1",
                "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
                "usage": {"total_tokens": max_tokens},
            }

    @staticmethod
    def _rl_headers(req_remaining: int, req_limit: int, reset_in: float, tok_limit: int, tok_remaining: int) -> dict:
        return {
            "x-ratelimit-limit-requests": str(req_limit),
            "x-ratelimit-remaining-requests": str(max(0, req_remaining)),
            "x-ratelimit-reset-requests": f"{reset_in:.2f}s",
            "x-ratelimit-limit-tokens": str(tok_limit),
            "x-ratelimit-remaining-tokens": str(max(0, tok_remaining)),
        }
