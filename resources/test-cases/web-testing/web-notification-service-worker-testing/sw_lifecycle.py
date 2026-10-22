"""Service worker lifecycle + web push pipeline simulator.

Pure-stdlib model of the parts of a service worker that break in
production: registration scope, install precaching, cache purging on
activate, the waiting/skipWaiting update dance, push payload validation,
410-expired subscriptions and opt-out cleanup.

Companion to https://qapractices.com/test-cases/web-notification-service-worker-testing/
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

MAX_PUSH_PAYLOAD_BYTES = 4096


class InsecureContextError(Exception):
    """navigator.serviceWorker is undefined outside secure contexts."""


class CacheStorage:
    def __init__(self) -> None:
        self._stores: dict[str, list[str]] = {}

    def open(self, name: str) -> list[str]:
        return self._stores.setdefault(name, [])

    def keys(self) -> list[str]:
        return list(self._stores)

    def delete(self, name: str) -> bool:
        return self._stores.pop(name, None) is not None


@dataclass
class Subscription:
    endpoint: str
    p256dh: str
    auth: str


class PushService:
    """Stands in for FCM/Mozilla push: tracks live endpoints, TTL and sends."""

    def __init__(self) -> None:
        self.live_endpoints: set[str] = set()
        self.delivered: list[dict] = []

    def subscribe(self, endpoint: str) -> Subscription:
        self.live_endpoints.add(endpoint)
        return Subscription(endpoint=endpoint, p256dh="k" * 87, auth="a" * 22)

    def send(self, endpoint: str, payload: bytes, ttl: int = 3600) -> int:
        """Returns 201 created, 413 too large, or 410 if the endpoint is dead."""
        if endpoint not in self.live_endpoints:
            return 410
        if len(payload) > MAX_PUSH_PAYLOAD_BYTES:
            return 413
        self.delivered.append({"endpoint": endpoint, "payload": payload, "ttl": ttl})
        return 201

    def expire(self, endpoint: str) -> None:
        self.live_endpoints.discard(endpoint)


class ServiceWorker:
    """Lifecycle model: registered -> installing -> waiting|activated.

    `version` identifies the deployed build; `cache_name` follows it so
    activation can purge stale stores.
    """

    def __init__(self, cache_name: str, shell_assets: list[str],
                 scope: str = "/", version: int = 1,
                 skip_waiting: bool = False) -> None:
        self.version = version
        self.cache_name = cache_name
        self.shell_assets = shell_assets
        self.scope = scope
        self.skip_waiting = skip_waiting
        self.state = "parsed"  # parsed -> installing -> waiting -> activated -> redundant
        self.analytics: list[str] = []
        self.rendered: list[dict] = []

    # -- lifecycle -----------------------------------------------------

    def install(self, caches: CacheStorage) -> None:
        self.state = "installing"
        store = caches.open(self.cache_name)
        store.extend(self.shell_assets)
        if self.skip_waiting:
            self.activate(caches)
        else:
            self.state = "installed"

    def activate(self, caches: CacheStorage) -> None:
        # Equivalent of caches.keys().filter(not current).map(delete)
        for name in list(caches.keys()):
            if name != self.cache_name:
                caches.delete(name)
        self.state = "activated"


class PushHandler:
    """What a correct `push` event listener must do — and where it breaks."""

    def __init__(self, worker: ServiceWorker) -> None:
        self.worker = worker

    @staticmethod
    def parse(payload: bytes) -> dict:
        """Malformed payloads must fall back, not kill the worker."""
        try:
            data = json.loads(payload.decode("utf-8")) if payload else {}
            return data if isinstance(data, dict) else {}
        except (ValueError, UnicodeDecodeError):
            return {}

    def handle_push(self, payload: bytes, *, wait_until: bool) -> dict | None:
        """Returns the rendered notification, or None if the SW died early.

        Without waitUntil the browser may terminate the worker before
        showNotification resolves — that path returns None here.
        """
        data = self.parse(payload)
        notification = {
            "title": data.get("title", "New update"),
            "body": data.get("body", ""),
            "url": data.get("url", "/"),
            "actions": data.get("actions", []),
        }
        if not wait_until:
            return None
        self.worker.rendered.append(notification)
        return notification

    def handle_click(self, notification: dict, action: str | None,
                     open_tabs: list[str]) -> dict:
        """notificationclick: focus an existing client on the URL or open one."""
        url = notification.get("url", "/")
        if action == "dismiss":
            return {"result": "closed"}
        if url in open_tabs:
            return {"result": "focused", "url": url}
        return {"result": "opened", "url": url}

    def handle_close(self, notification: dict) -> None:
        self.worker.analytics.append("notificationclose")


class Application:
    """Glues the registration, subscription and update flow together."""

    def __init__(self, *, secure_context: bool = True) -> None:
        self.secure_context = secure_context
        self.caches = CacheStorage()
        self.push = PushService()
        self.push_handler: PushHandler | None = None
        self.active: ServiceWorker | None = None
        self.waiting: ServiceWorker | None = None
        self.subscription: Subscription | None = None

    def register(self, worker: ServiceWorker) -> ServiceWorker:
        if not self.secure_context:
            raise InsecureContextError(
                "service workers require a secure context (HTTPS or localhost)"
            )
        worker.install(self.caches)
        if worker.state == "installed":
            self.waiting = worker
        else:
            self.active = worker
        self.push_handler = PushHandler(worker)
        return worker

    def apply_update(self) -> str:
        """waiting -> activated; the previously active SW becomes redundant."""
        if not self.waiting:
            return "no-update"
        self.waiting.activate(self.caches)
        if self.active:
            self.active.state = "redundant"
        self.active = self.waiting
        self.waiting = None
        self.push_handler = PushHandler(self.active)
        return "activated"

    def is_update_stuck(self) -> bool:
        return self.waiting is not None and not self.waiting.skip_waiting

    def send_push(self, payload: bytes, ttl: int = 3600) -> int:
        """Sends to the stored subscription; on 410 the dead endpoint is
        deleted and the client resubscribes on next load."""
        if not self.subscription:
            raise RuntimeError("no active subscription")
        status = self.push.send(self.subscription.endpoint, payload, ttl)
        if status == 410:
            self.subscription = None
        return status

    def resubscribe(self, endpoint: str) -> Subscription:
        self.subscription = self.push.subscribe(endpoint)
        return self.subscription

    def opt_out(self) -> None:
        """Full cleanup: unregister, purge caches, drop the subscription."""
        if self.active:
            self.active.state = "redundant"
            self.active = None
        for name in list(self.caches.keys()):
            self.caches.delete(name)
        self.subscription = None
