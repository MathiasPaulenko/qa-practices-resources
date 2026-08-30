import hmac
import hashlib
import pytest
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_SECRET = b"webhook-secret"


def verify_signature(payload, signature):
    expected = hmac.new(WEBHOOK_SECRET, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Signature", "")
    if not verify_signature(request.get_data(), signature):
        return jsonify({"error": "invalid signature"}), 400
    return jsonify({"status": "processed"}), 200


@pytest.fixture
def client():
    return app.test_client()


def test_valid_webhook(client):
    payload = b'{"event":"payment.created"}'
    signature = hmac.new(WEBHOOK_SECRET, payload, hashlib.sha256).hexdigest()
    response = client.post(
        "/webhook",
        data=payload,
        headers={"X-Signature": f"sha256={signature}", "Content-Type": "application/json"},
    )
    assert response.status_code == 200


def test_invalid_webhook(client):
    payload = b'{"event":"payment.created"}'
    response = client.post(
        "/webhook",
        data=payload,
        headers={"X-Signature": "sha256=bad", "Content-Type": "application/json"},
    )
    assert response.status_code == 400
