# Push Notification Test Cases — Companion Files

Companion for [Push Notification Test Cases: Delivery, Permissions](https://qapractices.com/test-cases/push-notification-test-cases/). Real provider payload samples and a token-lifecycle verification script.

## Files

| File | Purpose |
| ---- | ------- |
| `payloads/fcm-notification.json` | FCM HTTP v1 notification message: title/body, data deep link, Android channel + HIGH priority, APNs alert with thread-id. |
| `payloads/fcm-data-silent.json` | Data-only (silent) push: FCM NORMAL priority, APNs `content-available: 1` + `apns-push-type: background`. |
| `payloads/web-push.json` | Web push payload with tag/renotify, icon/badge, actions and deep-link `data.url` — matches TC015/TC016. |
| `check_token_lifecycle.sh` | Token lifecycle checks mirroring TC003/004/005: registration exists, idempotent re-registration, stale-token pruning probe. |

## Usage

```bash
chmod +x check_token_lifecycle.sh
API_BASE="https://your-api" AUTH="Bearer $TOKEN" ./check_token_lifecycle.sh <device_id>
```

Send payloads with `POST https://fcm.googleapis.com/v1/projects/YOUR_PROJECT/messages:send` (FCM v1) or your web-push library of choice.

## Requirements

- `bash`, `curl`, Python 3 (for JSON parsing in the script)
- A backend with push-token endpoints — adapt paths to your API shape
