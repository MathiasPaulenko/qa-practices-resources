"""MQTT protocol semantics model for the checklist on qapractices.com.

Pure stdlib — models the behaviors the checklist verifies:
wildcard matching, QoS downgrade, retained store, session persistence,
LWT triggering and clientID takeover. No broker needed.
"""

MAX_TOPIC_BYTES = 65_535
VALID_QOS = (0, 1, 2)


def validate_filter(sub_filter: str) -> bool:
    """Validate a subscription filter per spec: wildcards occupy a whole
    level and '#' must be the last level."""
    if not sub_filter or len(sub_filter.encode("utf-8")) > MAX_TOPIC_BYTES:
        raise ValueError("filter empty or exceeds 65535 UTF-8 bytes")
    levels = sub_filter.split("/")
    for i, level in enumerate(levels):
        if "#" in level:
            if level != "#":
                raise ValueError("'#' must occupy a whole level")
            if i != len(levels) - 1:
                raise ValueError("'#' must be the last level")
        if "+" in level and level != "+":
            raise ValueError("'+' must occupy a whole level")
    return True


def topic_match(sub_filter: str, topic: str) -> bool:
    """MQTT wildcard matching: '+' matches exactly one level, '#' matches
    all remaining levels. Wildcard filters never match '$'-prefixed topics."""
    if not sub_filter or not topic:
        return False
    f_levels = sub_filter.split("/")
    t_levels = topic.split("/")
    if topic.startswith("$") and f_levels[0] in ("+", "#"):
        return False
    for i, f in enumerate(f_levels):
        if f == "#":
            return i == len(f_levels) - 1
        if i >= len(t_levels):
            return False
        if f != "+" and f != t_levels[i]:
            return False
    return len(f_levels) == len(t_levels)


def effective_qos(publish_qos: int, subscribe_qos: int) -> int:
    """Delivered QoS is the minimum of publish and subscription QoS —
    the downgrade the checklist verifies."""
    for q in (publish_qos, subscribe_qos):
        if q not in VALID_QOS:
            raise ValueError(f"invalid QoS: {q}")
    return min(publish_qos, subscribe_qos)


class RetainedStore:
    """Broker retained-message store: last retained publish wins,
    empty payload with retain=true deletes the entry."""

    def __init__(self) -> None:
        self._store: dict[str, bytes] = {}

    def publish(self, topic: str, payload: bytes, retain: bool = False) -> None:
        if not retain:
            return
        if payload in (b"", ""):
            self._store.pop(topic, None)
        else:
            self._store[topic] = payload

    def for_new_subscriber(self, sub_filter: str) -> dict[str, bytes]:
        return {t: p for t, p in self._store.items() if topic_match(sub_filter, t)}


class Session:
    """Client session: persistent sessions keep subscriptions and
    unacknowledged QoS 1/2 messages across disconnects."""

    def __init__(self, persistent: bool = True, expiry_seconds: int | None = None) -> None:
        self.persistent = persistent
        self.expiry_seconds = expiry_seconds
        self.subscriptions: list[str] = []
        self.pending: list[dict] = []

    def queue(self, topic: str, payload: bytes, qos: int) -> None:
        if qos >= 1 and self.persistent:
            self.pending.append({"topic": topic, "payload": payload, "qos": qos})

    def reconnect(self) -> list[dict]:
        """On reconnect a persistent session returns pending messages;
        a clean session discards everything."""
        if not self.persistent:
            self.pending.clear()
            self.subscriptions.clear()
            return []
        return list(self.pending)


class WillMessage:
    """Last Will and Testament registered in the CONNECT packet."""

    def __init__(self, topic: str, payload: bytes, qos: int = 0, retain: bool = False) -> None:
        self.topic = topic
        self.payload = payload
        self.qos = qos
        self.retain = retain


def on_disconnect(will: WillMessage | None, graceful: bool) -> WillMessage | None:
    """The broker publishes the will only on ungraceful disconnects —
    never after a proper DISCONNECT packet."""
    if will is None or graceful:
        return None
    return will


class Broker:
    """Minimal broker connection table for clientID takeover checks."""

    def __init__(self) -> None:
        self.clients: dict[str, object] = {}

    def connect(self, client_id: str, connection: object) -> object | None:
        """A second CONNECT with the same clientID must close the
        existing connection (takeover semantics)."""
        previous = self.clients.get(client_id)
        self.clients[client_id] = connection
        return previous
