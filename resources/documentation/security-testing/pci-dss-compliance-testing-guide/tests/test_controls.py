"""Tests for the PCI DSS control checks — pure logic, no live targets."""

import socket
import threading

from controls.pan_sweep import find_pans, luhn_valid, sweep_path
from controls.segmentation_check import check_segmentation
from controls.tls_check import TlsResult, evaluate_tls

# --- Luhn / PAN sweep -------------------------------------------------------

VISA_TEST_PAN = "4111111111111111"   # canonical Luhn-valid test card
MC_TEST_PAN = "5500005555555559"     # Luhn-valid test card
ORDER_ID = "202611070123456"         # 15 digits, not Luhn-valid


def test_luhn_accepts_valid_test_pans():
    assert luhn_valid(VISA_TEST_PAN)
    assert luhn_valid(MC_TEST_PAN)


def test_luhn_rejects_random_digits():
    assert not luhn_valid(ORDER_ID)
    assert not luhn_valid("4111111111111112")


def test_find_pans_ignores_non_luhn_candidates():
    text = f"order {ORDER_ID} paid with {VISA_TEST_PAN}"
    assert find_pans(text) == [VISA_TEST_PAN]


def test_sweep_flags_file_containing_pan(tmp_path):
    leaked = tmp_path / "app.log"
    leaked.write_text(f"charge ok card={VISA_TEST_PAN}")
    clean = tmp_path / "other.log"
    clean.write_text("nothing here")
    findings = sweep_path(tmp_path)
    assert str(leaked) in findings
    assert str(clean) not in findings


# --- TLS evaluation logic ----------------------------------------------------

def good_result() -> TlsResult:
    return TlsResult(host="cde.internal", port=443,
                     negotiated="TLSv1.3", cipher="TLS_AES_256_GCM_SHA384")


def test_evaluate_tls_passes_modern_config():
    assert evaluate_tls(good_result()).failures == []


def test_evaluate_tls_flags_tls10():
    r = good_result()
    r.negotiated = "TLSv1"
    assert "weak protocol negotiated: TLSv1" in evaluate_tls(r).failures


def test_evaluate_tls_flags_weak_cipher():
    r = good_result()
    r.cipher = "DES-CBC3-SHA"
    assert evaluate_tls(r).failures == ["weak cipher negotiated: DES-CBC3-SHA"]


def test_evaluate_tls_flags_connection_error():
    r = TlsResult(host="down.internal", port=443, error="timed out")
    assert evaluate_tls(r).failures == ["connection failed: timed out"]


# --- Segmentation -------------------------------------------------------------

def test_segmentation_detects_open_port():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    port = listener.getsockname()[1]
    threading.Thread(target=lambda: listener.accept(), daemon=True).start()
    try:
        assert check_segmentation("127.0.0.1", [port]) == [port]
    finally:
        listener.close()


def test_segmentation_passes_when_unreachable():
    closed_port = 59990
    assert check_segmentation("127.0.0.1", [closed_port]) == []
