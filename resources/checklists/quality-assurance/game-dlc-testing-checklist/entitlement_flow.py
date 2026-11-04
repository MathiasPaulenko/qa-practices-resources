"""Entitlement flow simulation — the refund bug in miniature.

Shows why removing the store entitlement isn't enough: the game must also
re-evaluate access, and saves made with the DLC must survive the revoke.
"""


class Store:
    def __init__(self):
        self.entitlements = {}

    def grant(self, account, dlc):
        self.entitlements.setdefault(account, set()).add(dlc)

    def revoke(self, account, dlc):
        self.entitlements.get(account, set()).discard(dlc)

    def owns(self, account, dlc):
        return dlc in self.entitlements.get(account, set())


class Game:
    """Mirrors a real bug: unlock flag cached in the save, never re-checked."""

    def __init__(self, store, recheck_on_load=False):
        self.store = store
        self.recheck = recheck_on_load
        self.unlocked = {}

    def unlock_content(self, account, dlc):
        if self.store.owns(account, dlc):
            self.unlocked.setdefault(account, set()).add(dlc)

    def content_visible(self, account, dlc):
        if self.recheck:
            return self.store.owns(account, dlc)
        return dlc in self.unlocked.get(account, set())


def main():
    store = Store()
    buggy = Game(store, recheck_on_load=False)
    fixed = Game(store, recheck_on_load=True)

    store.grant("player-1", "season-pass-1")
    buggy.unlock_content("player-1", "season-pass-1")
    fixed.unlock_content("player-1", "season-pass-1")

    print("== after purchase ==")
    print("buggy game sees DLC:", buggy.content_visible("player-1", "season-pass-1"))

    store.revoke("player-1", "season-pass-1")  # refund — store side done right

    print("\n== after refund ==")
    print("buggy game sees DLC:", buggy.content_visible("player-1", "season-pass-1"),
          "<- stale unlock flag, player keeps paid content free")
    print("fixed game sees DLC:", fixed.content_visible("player-1", "season-pass-1"),
          "<- re-checks entitlement on load")
    print("\nlesson: test the revoke path, not just the purchase path.")


if __name__ == "__main__":
    main()
