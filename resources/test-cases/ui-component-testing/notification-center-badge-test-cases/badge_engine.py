"""Stdlib model of the notification badge counter used in the article.

Two pieces:

- ``NotificationServer`` — source of truth. Holds notification items keyed by
  id with read state and optional expiry; every write is idempotent on the
  message id.
- ``BadgeTab`` — one open tab's view of the counter. Tabs never keep their own
  math: they refetch the server after each applied change and broadcast it to
  peer tabs through a shared ``BroadcastChannel`` stand-in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count


@dataclass
class Notification:
    id: str
    read: bool = False
    expires_at: float | None = None


class NotificationServer:
    def __init__(self, now: float = 0.0) -> None:
        self._now = now
        self.items: dict[str, Notification] = {}
        self.audit: list[dict] = []

    def tick(self, seconds: float) -> None:
        self._now += seconds
        self._expire()

    def _expire(self) -> None:
        for nid, item in list(self.items.items()):
            if item.expires_at is not None and item.expires_at <= self._now:
                self.audit.append(
                    self._entry("expire", nid, before=None, after=None)
                )
                del self.items[nid]

    def _entry(self, action: str, nid: str, before: int | None, after: int | None):
        return {
            "action": action,
            "notification_id": nid,
            "count_before": before,
            "count_after": after,
            "ts": self._now,
        }

    def push(self, nid: str, *, expires_in: float | None = None) -> bool:
        """Deliver a notification. Dedup by id — a re-delivered push is a no-op."""
        if nid in self.items:
            return False
        self.items[nid] = Notification(
            id=nid,
            expires_at=None if expires_in is None else self._now + expires_in,
        )
        self.audit.append(self._entry("push", nid, None, self.unread_count()))
        return True

    def mark_read(self, nid: str) -> bool:
        item = self.items.get(nid)
        if item is None or item.read:
            return False
        before = self.unread_count()
        item.read = True
        self.audit.append(self._entry("read", nid, before, self.unread_count()))
        return True

    def mark_all_read(self) -> int:
        before = self.unread_count()
        for item in self.items.values():
            item.read = True
        self.audit.append(self._entry("clear_all", "*", before, 0))
        return before

    def delete(self, nid: str) -> bool:
        if nid not in self.items:
            return False
        before = self.unread_count()
        del self.items[nid]
        self.audit.append(self._entry("delete", nid, before, self.unread_count()))
        return True

    def unread_count(self) -> int:
        return sum(1 for i in self.items.values() if not i.read)


@dataclass
class BroadcastChannel:
    """Shared channel connecting tabs in the same 'browser'."""

    tabs: list["BadgeTab"] = field(default_factory=list)

    def post(self, sender: "BadgeTab", message: str) -> None:
        for tab in self.tabs:
            if tab is not sender:
                tab._on_broadcast(message)


class BadgeTab:
    """One tab's badge view. Always resolves state from the server."""

    def __init__(self, server: NotificationServer, channel: BroadcastChannel) -> None:
        self.server = server
        self.channel = channel
        self.online = True
        self._count: int | None = None  # None = not hydrated yet
        self.seen_messages: set[str] = set()
        channel.tabs.append(self)

    # -- hydration ------------------------------------------------------

    def open(self) -> None:
        self._count = self.server.unread_count()

    @property
    def display(self) -> str | None:
        """What the badge renders. None = hidden (no badge element)."""
        if self._count is None or self._count == 0:
            return None
        return "99+" if self._count > 99 else str(self._count)

    # -- inbound events -------------------------------------------------

    def push(self, message_id: str) -> None:
        """Apply a pushed notification. Offline tabs buffer nothing —
        the badge stays stale (and honest) until resync."""
        if not self.online:
            return
        if message_id in self.seen_messages:
            return  # dedup: same push delivered twice
        self.seen_messages.add(message_id)
        self.server.push(message_id)
        self._resync()
        self.channel.post(self, "refresh")

    def mark_read(self, nid: str) -> None:
        if not self.online:
            return
        if self.server.mark_read(nid):
            self._resync()
            self.channel.post(self, "refresh")

    def mark_all_read(self) -> None:
        if not self.online:
            return
        self.server.mark_all_read()
        self._resync()
        self.channel.post(self, "refresh")

    def reconnect(self) -> None:
        self.online = True
        self._resync()

    def disconnect(self) -> None:
        self.online = False

    # -- internals ------------------------------------------------------

    def _resync(self) -> None:
        if self.online:
            self._count = self.server.unread_count()

    def _on_broadcast(self, message: str) -> None:
        if message == "refresh":
            self._resync()


def make_bell(server: NotificationServer, channel: BroadcastChannel) -> BadgeTab:
    tab = BadgeTab(server, channel)
    tab.open()
    return tab


_seq = count(1)


def push_many(server: NotificationServer, n: int, prefix: str = "n") -> None:
    for _ in range(n):
        server.push(f"{prefix}-{next(_seq)}")
