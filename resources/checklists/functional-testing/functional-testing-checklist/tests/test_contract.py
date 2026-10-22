import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = json.loads((ROOT / "fixtures" / "profile-response.json").read_text())


def test_profile_response_shape():
    assert set(SAMPLE.keys()) == {"id", "email", "name", "role"}
    assert isinstance(SAMPLE["id"], int)
    assert "@" in SAMPLE["email"]
    assert SAMPLE["role"] in {"admin", "editor", "viewer"}


def test_checklist_csv_is_complete_and_risk_tagged():
    rows = list(csv.DictReader((ROOT / "checklist-items.csv").read_text().splitlines()))
    assert len(rows) == 139
    assert all(r["risk"] in {"High", "Medium", "Low"} for r in rows)
    assert [int(r["id"]) for r in rows] == list(range(1, 140))
    assert len({r["area"] for r in rows}) == 11


def test_login_form_fixture_has_required_testids():
    html = (ROOT / "login-form.html").read_text()
    for testid in ["email", "password", "age", "age-error", "login-button", "save", "welcome"]:
        assert f'data-testid="{testid}"' in html
