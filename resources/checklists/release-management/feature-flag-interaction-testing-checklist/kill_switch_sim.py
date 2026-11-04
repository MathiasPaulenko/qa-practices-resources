"""Kill switch simulation — shows why recovery needs testing, not just activation.

Simulates services holding cached flag values: killing the flag must propagate
to every service, and recovery must restore the exact pre-kill state.
"""
import time


class FlagService:
    def __init__(self):
        self.flags = {"recommendationV2": True}
        self.killed = set()

    def read(self, flag):
        return flag in self.flags and self.flags[flag] and flag not in self.killed

    def kill(self, flag):
        self.killed.add(flag)

    def recover(self, flag):
        self.killed.discard(flag)


class Service:
    """A consumer that caches the flag value — the failure mode that bites in prod."""

    def __init__(self, flag_service, name, ttl=0.0):
        self.fs = flag_service
        self.name = name
        self.ttl = ttl
        self._cached = None
        self._cached_at = 0.0

    def flag_value(self, flag):
        now = time.monotonic()
        if self._cached is None or (now - self._cached_at) > self.ttl:
            self._cached = self.fs.read(flag)
            self._cached_at = now
        return self._cached


def main():
    fs = FlagService()
    flag = "recommendationV2"
    services = [
        Service(fs, "web-api", ttl=0.05),
        Service(fs, "background-worker", ttl=10.0),  # no TTL in prod = stale forever
        Service(fs, "mobile-backend", ttl=0.05),
    ]

    print("== steady state: caches populated with flag ON ==")
    for s in services:
        print(f"{s.name:18} sees flag: {s.flag_value(flag)}")

    time.sleep(0.1)  # let short TTLs expire so healthy services refetch

    print("\n== kill switch activated ==")
    fs.kill(flag)
    for s in services:
        print(f"{s.name:18} sees flag: {s.flag_value(flag)}")
    print("background-worker still serves True — stale cache, no TTL")

    print("\n== recovery ==")
    time.sleep(0.1)
    fs.recover(flag)
    for s in services:
        print(f"{s.name:18} sees flag: {s.flag_value(flag)}")
    print("\nlesson: kill switches only work if every consumer's cache respects TTL.")


if __name__ == "__main__":
    main()
