# Email Deliverability Testing — Companion

Runnable files for the [How to Test Email Deliverability](https://qapractices.com/documentation/email-deliverability-testing) guide.

## Files

| File | Purpose |
|------|---------|
| `scripts/dns-auth-check.sh` | Verifies SPF, DKIM and DMARC records for a sending domain with `dig` |
| `scripts/seed-send.sh` | Sends a tracked test message to a seed list through your real SMTP relay with `swaks` |
| `tests/seed_inbox_check.py` | Polls a seed mailbox over IMAP and reports whether the message landed in INBOX or spam |

## Quick Start

```bash
# 1. Check the three DNS authentication records
bash scripts/dns-auth-check.sh staging.qapractices.com s1

# 2. Send a tracked test through the real pipeline
export SMTP_HOST=smtp.staging.qapractices.com SMTP_USER=app-smtp SMTP_PASS='***'
bash scripts/seed-send.sh seeds.txt noreply@staging.qapractices.com

# 3. Check where the message landed in a seed mailbox
python tests/seed_inbox_check.py \
  --host imap.gmail.com --user qa-seed+001@gmail.com \
  --password 'app-password' --token <token-from-step-2>
```

## CI Integration

`dns-auth-check.sh` is safe for CI — it only reads public DNS. `seed-send.sh` and `seed_inbox_check.py` need real credentials, so run them in a scheduled job with secrets, not on every push.

Requirements: `dig` (bind-utils/dnsutils), `swaks` v20240103+, Python 3.10+ stdlib only.
