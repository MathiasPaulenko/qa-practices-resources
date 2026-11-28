```text
RL-003 — Burst boundary
Requests: 20 POST /payments in <2s with a Pro key, fresh bucket
Expected: all 20 return 200; the 21st returns 429 within the same window
Bug it catches: burst allowance applied twice — once to bucket size,
  once to refill — letting 40 through.

RL-010 — Shared counter across instances
Requests: 60 requests to instance A, 50 to instance B, same Pro key
Expected: the counter is shared — request 101 is rejected whichever
  instance it lands on
Bug it catches: per-instance counters falling back silently when Redis
  is partitioned, giving clients 3× their real limit.

BOUNDARY MATH (Pro tier, 100/min + burst 20)
Request 1-100: 200 — bucket drains normally
Request 101-120: 200 — burst tokens consumed
Request 121: 429 + Retry-After ≈ (60/rate) seconds
Allowed tolerance: ±1 request for clock skew between app and Redis.

FAILOVER EXPECTATION
Choice: fail closed (payments — a limit bypass costs money)
Test: block Redis with a firewall rule, send 10 requests
Expected: 503 with a clear error — not 200s sailing through.
```
