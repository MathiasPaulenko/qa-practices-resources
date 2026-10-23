# MQTT Protocol Testing Checklist — Companion

Companion resource for [MQTT Protocol Testing Checklist](https://qapractices.com/checklists/mqtt-protocol-testing-checklist/).

## Contents

- `mqtt_model.py` — dependency-free model of the protocol semantics the checklist verifies: wildcard matching (`+`, `#`, `$SYS` exclusion), filter validation (65 535-byte limit, `#` last level only), QoS downgrade (`min(publish, subscribe)`), retained-message store (last wins, empty payload deletes), persistent-session redelivery, LWT triggering (ungraceful only) and clientID takeover.
- `tests/test_mqtt_checklist.py` — executable subset of the checklist: wildcard levels and malformed filters, `$SYS` exclusion, oversized filter rejection, QoS downgrade and invalid-QoS rejection, retained last-wins/clear/subscribe-delivery, persistent vs clean session, LWT graceful/ungraceful, duplicate clientID takeover.

## Requirements

- Python 3.10+, `pip install -r requirements.txt` (pytest only — the model itself is stdlib)

## Usage

```bash
pytest tests/ -q
```

Expected output: `15 passed`.

The broker-level checks (TLS, ACLs, load, interop) run against a real broker per the checklist — `mosquitto` locally or `test.mosquitto.org` — with `mosquitto_pub`/`mosquitto_sub` or the paho example from the article.

## Related

- Article EN: https://qapractices.com/checklists/mqtt-protocol-testing-checklist/
- Article ES: https://qapractices.com/es/checklists/mqtt-protocol-testing-checklist/
