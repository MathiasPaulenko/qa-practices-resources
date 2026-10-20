"""CORS preflight evaluation — models the checks a browser runs before a cross-origin request.

Standard library only. Use ``evaluate_preflight`` to decide whether a browser
would let the real request through given the server's CORS response headers.
"""

from dataclasses import dataclass, field
from urllib.parse import urlparse

SIMPLE_METHODS = {"GET", "HEAD", "POST"}
SAFELISTED_HEADERS = {
    "accept",
    "accept-language",
    "content-language",
    "content-type",
    "range",
}
SAFELISTED_CONTENT_TYPES = {
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
}
# Headers every fetch adds — they must not force a preflight on their own.
# content-type is handled separately: only safelisted values stay simple.
ALWAYS_ALLOWED_REQUEST_HEADERS = {
    "accept",
    "accept-language",
    "content-language",
    "range",
    "origin",
    "referer",
    "sec-fetch-dest",
    "sec-fetch-mode",
    "sec-fetch-site",
    "user-agent",
}


@dataclass
class CorsConfig:
    """Server-side CORS policy as observed in a preflight response."""

    allowed_origins: list[str] = field(default_factory=list)
    allow_any_origin: bool = False
    allowed_methods: list[str] = field(default_factory=list)
    allowed_headers: list[str] = field(default_factory=list)
    allow_credentials: bool = False
    max_age: int | None = None


def is_simple_request(method: str, headers: dict[str, str]) -> bool:
    """Return True when the request needs no preflight per the Fetch spec."""
    if method.upper() not in SIMPLE_METHODS:
        return False
    lowered = {k.lower(): v for k, v in headers.items()}
    for name, value in lowered.items():
        if name in ALWAYS_ALLOWED_REQUEST_HEADERS:
            continue
        if name not in SAFELISTED_HEADERS:
            return False
        if name == "content-type" and value.lower() not in SAFELISTED_CONTENT_TYPES:
            return False
    return True


def origin_matches(origin: str, allowed: str) -> bool:
    """Exact origin tuple match (scheme, host, port) — subdomains don't count."""
    req, ok = urlparse(origin), urlparse(allowed)
    if not req.scheme or not req.netloc:
        return False
    return (req.scheme, req.hostname, req.port or _default_port(req.scheme)) == (
        ok.scheme,
        ok.hostname,
        ok.port or _default_port(ok.scheme),
    )


def _default_port(scheme: str) -> int | None:
    return {"https": 443, "http": 80}.get(scheme)


def credentials_wildcard_violation(allow_origin: str, allow_credentials: bool) -> bool:
    """True when `*` is combined with credentials — the Fetch spec forbids it."""
    return allow_origin.strip() == "*" and allow_credentials


def evaluate_preflight(
    config: CorsConfig,
    origin: str,
    method: str,
    request_headers: list[str] | None = None,
    with_credentials: bool = False,
) -> dict:
    """Evaluate a preflight the way a browser would.

    Returns {"allowed": bool, "reason": str, "cache_seconds": int|None}.
    """
    request_headers = [h.lower() for h in (request_headers or [])]
    if origin == "null" or not origin.strip():
        return {"allowed": False, "reason": "null or empty origin must not be allowed", "cache_seconds": config.max_age}

    reflected = config.allow_any_origin or any(
        origin_matches(origin, allowed) for allowed in config.allowed_origins
    )
    if not reflected:
        return {"allowed": False, "reason": f"origin {origin} not in allow-list", "cache_seconds": config.max_age}

    echo_origin = "*" if config.allow_any_origin else origin
    if credentials_wildcard_violation(echo_origin, config.allow_credentials):
        return {"allowed": False, "reason": "wildcard origin cannot be used with credentials", "cache_seconds": config.max_age}

    if with_credentials and not config.allow_credentials:
        return {"allowed": False, "reason": "credentialed request without Access-Control-Allow-Credentials", "cache_seconds": config.max_age}

    allowed_methods = {m.upper() for m in config.allowed_methods}
    if method.upper() not in allowed_methods:
        return {"allowed": False, "reason": f"method {method.upper()} not in Allow-Methods", "cache_seconds": config.max_age}

    allowed_headers = {h.lower() for h in config.allowed_headers}
    missing = [h for h in request_headers if h not in ALWAYS_ALLOWED_REQUEST_HEADERS and h not in allowed_headers]
    if missing:
        return {"allowed": False, "reason": f"headers not in Allow-Headers: {', '.join(missing)}", "cache_seconds": config.max_age}

    return {"allowed": True, "reason": "preflight approved", "cache_seconds": config.max_age}
