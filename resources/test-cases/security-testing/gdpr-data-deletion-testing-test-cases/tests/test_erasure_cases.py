"""pytest suite mapped to the TC ids of the GDPR erasure resource."""

from conftest import EMAIL, USER_ID


def test_tc001_user_initiated_deletion(engine):
    result = engine.request_erasure(USER_ID, verified=True)
    assert result["status"] == "fulfilled"
    assert engine.db.execute(
        "SELECT COUNT(*) c FROM users WHERE id=?", (USER_ID,)
    ).fetchone()["c"] == 0


def test_tc002_cascade_deletion(engine):
    engine.request_erasure(USER_ID)
    # sessions and index rows are deleted outright
    for table in ("sessions", "search_index"):
        assert engine.db.execute(
            f"SELECT COUNT(*) c FROM {table} WHERE user_id=?", (USER_ID,)
        ).fetchone()["c"] == 0
    # orders survive as aggregates but carry no PII
    orphans = engine.db.execute(
        "SELECT COUNT(*) c FROM orders WHERE user_id=? AND"
        " (email IS NOT NULL OR name IS NOT NULL)", (USER_ID,)
    ).fetchone()["c"]
    assert orphans == 0


def test_tc003_cache_and_index_cleanup(engine):
    engine.request_erasure(USER_ID)
    assert engine.db.execute(
        "SELECT COUNT(*) c FROM cache WHERE key=?", (f"user:{USER_ID}",)
    ).fetchone()["c"] == 0
    assert engine.db.execute(
        "SELECT COUNT(*) c FROM search_index WHERE user_id=?", (USER_ID,)
    ).fetchone()["c"] == 0


def test_tc004_backup_restore_replays_deletion(engine):
    snap = engine.snapshot()          # pre-erasure backup contains the user
    engine.request_erasure(USER_ID)
    engine.restore(snap)              # restore resurrects, replay fixes it
    assert engine.db.execute(
        "SELECT COUNT(*) c FROM users WHERE id=?", (USER_ID,)
    ).fetchone()["c"] == 0
    assert engine.pii_residue(EMAIL) == 0


def test_tc005_audit_trail_entry(engine):
    engine.request_erasure(USER_ID, request_id="dsar-2026-0142")
    entries = engine.audit_entries(USER_ID)
    assert len(entries) == 1
    entry = entries[0]
    assert entry["status"] == "fulfilled"
    assert "users" in entry["scope"] and "orders" in entry["scope"]
    # the audit stores identifiers and scope, never the erased values
    assert EMAIL not in (entry["scope"] or "")


def test_tc006_third_party_notification(engine):
    engine.processors = ["crm", "email-platform", "analytics"]
    engine.request_erasure(USER_ID)
    assert {m["processor"] for m in engine.outbox} == {
        "crm", "email-platform", "analytics"}
    engine.confirm_processors()
    assert all(m["status"] == "confirmed" for m in engine.outbox)


def test_tc007_legal_hold_defers_then_resumes(engine):
    engine.add_legal_hold(USER_ID, "pending litigation")
    assert engine.request_erasure(USER_ID)["status"] == "deferred"
    # PII untouched while held
    assert engine.pii_residue(EMAIL) > 0
    engine.release_legal_hold(USER_ID)
    assert engine.request_erasure(USER_ID)["status"] == "fulfilled"
    assert engine.pii_residue(EMAIL) == 0


def test_tc008_anonymization_keeps_aggregates(engine):
    engine.request_erasure(USER_ID)
    # 5 order rows retained as aggregates with amounts
    rows = engine.db.execute(
        "SELECT * FROM orders WHERE user_id=?", (USER_ID,)
    ).fetchall()
    assert len(rows) == 5
    assert all(r["amount"] == 49.99 for r in rows)
    assert all(r["email"] is None and r["name"] is None for r in rows)


def test_tc009_within_statutory_deadline(engine):
    received = 1_700_000_000.0        # fixed receipt timestamp
    completed = received + 20 * 86_400  # fulfilled 20 days later
    result = engine.request_erasure(USER_ID, now=completed)
    assert result["status"] == "fulfilled"
    assert completed - received <= 30 * 86_400  # Art. 12(3): one month


def test_tc010_unverified_request_rejected(engine):
    result = engine.request_erasure(USER_ID, verified=False)
    assert result["status"] == "rejected"
    assert engine.db.execute(
        "SELECT COUNT(*) c FROM users WHERE id=?", (USER_ID,)
    ).fetchone()["c"] == 1            # nothing deleted
    rejected = engine.audit_entries(USER_ID)[0]
    assert rejected["status"] == "rejected"  # attempt is logged for fraud review


def test_tc011_logs_scrubbed(engine):
    engine.request_erasure(USER_ID)
    assert engine.pii_residue(EMAIL) == 0
    assert engine.pii_residue(USER_ID) == 0
    line = engine.db.execute("SELECT line FROM app_logs").fetchone()["line"]
    assert "[redacted]" in line


def test_tc012_no_reidentification(engine):
    engine.request_erasure(USER_ID)
    assert engine.reidentify(USER_ID) == 0


def test_tc013_idempotent_repeat(engine):
    engine.request_erasure(USER_ID)
    assert engine.request_erasure(USER_ID)["status"] == "noop"
    assert engine.request_erasure("u-0000")["status"] == "noop"
    assert len(engine.outbox) == 0    # no processors configured → nothing sent
    # one fulfilled audit entry only, no duplicates
    assert len(engine.audit_entries(USER_ID)) == 1


def test_tc014_consent_withdrawal_scope(engine):
    removed = engine.withdraw_consent(USER_ID)
    assert removed == 1
    # account stays active, consent-scoped data is gone
    user = engine.db.execute(
        "SELECT * FROM users WHERE id=?", (USER_ID,)).fetchone()
    assert user is not None and user["marketing_consent"] == 0
    assert engine.db.execute(
        "SELECT COUNT(*) c FROM marketing_segments WHERE user_id=?",
        (USER_ID,)).fetchone()["c"] == 0


def test_tc015_confirmation_content(engine):
    engine.request_erasure(USER_ID, request_id="dsar-2026-0142")
    conf = engine.confirmation_for("dsar-2026-0142")
    assert conf is not None
    assert "users" in conf["scope"] and "search_index" in conf["scope"]
    assert EMAIL not in str(conf)     # the confirmation leaks no residual PII


def test_tc016_export_regenerated_without_user(engine):
    before = engine.generate_export()
    assert any(r["email"] == EMAIL for r in before)
    engine.request_erasure(USER_ID)
    after = engine.generate_export()  # regenerated export excludes the user
    assert all(r["email"] != EMAIL for r in after)
