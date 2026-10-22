"""Tests for the SW lifecycle + push pipeline simulator.

Maps to the TC-01..TC-20 cases in the article — each test name keeps the
case id so failures point at the scenario they cover.
"""

import pytest

from sw_lifecycle import (
    Application,
    CacheStorage,
    InsecureContextError,
    MAX_PUSH_PAYLOAD_BYTES,
    PushHandler,
    ServiceWorker,
)

SHELL = ["/", "/index.html", "/app.css", "/app.js", "/offline.html"]


def make_worker(version=1, cache="shell-v1", skip_waiting=False):
    return ServiceWorker(cache_name=cache, shell_assets=SHELL,
                         version=version, skip_waiting=skip_waiting)


# --- TC-09: registration & scope ----------------------------------------

def test_tc09_registers_at_root_scope():
    app = Application()
    sw = app.register(make_worker())
    assert sw.scope == "/"
    assert app.waiting is not None  # nothing controlling yet -> waits


def test_tc09_first_visit_with_skip_waiting_activates():
    app = Application()
    sw = app.register(make_worker(skip_waiting=True))
    assert sw.state == "activated"
    assert app.active is sw


# --- TC-10: install precaches the shell ---------------------------------

def test_tc10_install_precaches_shell():
    app = Application()
    app.register(make_worker())
    assert set(app.caches.open("shell-v1")) == set(SHELL)


# --- TC-11: activate purges stale caches ---------------------------------

def test_tc11_activate_deletes_old_cache():
    app = Application()
    app.register(make_worker())
    app.apply_update()  # v1 now active
    app.register(make_worker(version=2, cache="shell-v2"))
    app.apply_update()
    assert app.caches.keys() == ["shell-v2"]


# --- TC-12/13: update cycle + stuck detection ----------------------------

def test_tc12_waiting_sw_takes_control_after_update():
    app = Application()
    app.register(make_worker())
    app.apply_update()
    v2 = app.register(make_worker(version=2, cache="shell-v2"))
    assert app.is_update_stuck()
    assert app.apply_update() == "activated"
    assert app.active is v2
    assert app.active.state == "activated"


def test_tc13_stuck_update_detected():
    app = Application()
    app.register(make_worker())
    app.apply_update()
    app.register(make_worker(version=2, cache="shell-v2", skip_waiting=False))
    assert app.is_update_stuck()


def test_tc12_skip_waiting_avoids_stall():
    app = Application()
    app.register(make_worker())
    app.apply_update()
    app.register(make_worker(version=2, cache="shell-v2", skip_waiting=True))
    assert not app.is_update_stuck()
    assert app.active.version == 2


# --- TC-19: insecure context ---------------------------------------------

def test_tc19_insecure_context_refuses_registration():
    app = Application(secure_context=False)
    with pytest.raises(InsecureContextError):
        app.register(make_worker())


# --- TC-04/05: push render + malformed payload ---------------------------

def active_app() -> Application:
    app = Application()
    app.register(make_worker(skip_waiting=True))
    return app


def test_tc04_push_renders_notification_with_wait_until():
    app = active_app()
    app.resubscribe("https://push.example.com/ep1")
    out = app.push_handler.handle_push(
        b'{"title": "Order shipped", "body": "#A-1042", "url": "/orders/A-1042"}',
        wait_until=True)
    assert out["title"] == "Order shipped"
    assert out["url"] == "/orders/A-1042"


def test_tc04_push_without_wait_until_renders_nothing():
    app = active_app()
    app.resubscribe("https://push.example.com/ep1")
    assert app.push_handler.handle_push(b'{"title": "x"}', wait_until=False) is None
    assert app.active.rendered == []


def test_tc05_malformed_payload_falls_back():
    handler = PushHandler(make_worker())
    out = handler.handle_push(b"<not-json{{", wait_until=True)
    assert out["title"] == "New update"  # safe default, worker survives


def test_tc05_empty_payload_falls_back():
    handler = PushHandler(make_worker())
    out = handler.handle_push(b"", wait_until=True)
    assert out is not None and out["title"] == "New update"


# --- TC-06/07/08: notificationclick / close ------------------------------

def test_tc06_click_focuses_existing_tab():
    handler = PushHandler(make_worker())
    n = {"url": "/orders/A-1042"}
    assert handler.handle_click(n, "", ["/orders/A-1042", "/other"]) == {
        "result": "focused", "url": "/orders/A-1042"}


def test_tc06_click_opens_when_no_tab():
    handler = PushHandler(make_worker())
    assert handler.handle_click({"url": "/orders/A-1042"}, "", []) == {
        "result": "opened", "url": "/orders/A-1042"}


def test_tc07_dismiss_action_closes_without_navigation():
    handler = PushHandler(make_worker())
    assert handler.handle_click({"url": "/x"}, "dismiss", [])["result"] == "closed"


def test_tc08_notificationclose_tracked():
    worker = make_worker()
    PushHandler(worker).handle_close({"tag": "order"})
    assert worker.analytics == ["notificationclose"]


# --- TC-17: expired subscription -----------------------------------------

def test_tc17_expired_endpoint_deleted_and_resubscribed():
    app = active_app()
    app.resubscribe("https://push.example.com/dead")
    app.push.expire("https://push.example.com/dead")
    assert app.send_push(b'{"title": "x"}') == 410
    assert app.subscription is None
    app.resubscribe("https://push.example.com/fresh")
    assert app.send_push(b'{"title": "x"}') == 201


# --- edge cases: payload size, TTL, oversized ----------------------------

def test_edge_payload_over_4kb_rejected():
    app = active_app()
    app.resubscribe("https://push.example.com/ep1")
    assert app.send_push(b"x" * (MAX_PUSH_PAYLOAD_BYTES + 1)) == 413


def test_edge_ttl_zero_delivers_but_may_not_reach_offline():
    app = active_app()
    app.resubscribe("https://push.example.com/ep1")
    assert app.send_push(b'{"title": "x"}', ttl=0) == 201
    assert app.push.delivered[-1]["ttl"] == 0


# --- TC-20: opt-out --------------------------------------------------------

def test_tc20_opt_out_unregisters_and_clears():
    app = active_app()
    app.resubscribe("https://push.example.com/ep1")
    app.opt_out()
    assert app.active is None
    assert app.caches.keys() == []
    assert app.subscription is None
