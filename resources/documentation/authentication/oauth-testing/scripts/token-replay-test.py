"""Token replay test: verify that a revoked access token is rejected.

Usage: python token-replay-test.py <api-base-url> <access-token>
Requires: pip install requests==2.31.0
"""
import sys
import requests

if len(sys.argv) < 3:
    print("Usage: python token-replay-test.py <api-base-url> <access-token>")
    sys.exit(1)

api_base = sys.argv[1].rstrip("/")
token = sys.argv[2]
headers = {"Authorization": f"Bearer {token}"}

# Step 1: call protected API with valid token
print("Step 1: calling protected API with valid token...")
r1 = requests.get(f"{api_base}/me", headers=headers, timeout=10)
print(f"  Status: {r1.status_code}")
if r1.status_code != 200:
    print("  FAIL: expected 200 OK before logout")
    sys.exit(2)
print("  PASS: token works before logout")

# Step 2: trigger logout (revoke tokens)
print("Step 2: triggering logout...")
r2 = requests.post(f"{api_base}/logout", headers=headers, timeout=10)
print(f"  Status: {r2.status_code}")

# Step 3: replay the same token after logout
print("Step 3: replaying same token after logout...")
r3 = requests.get(f"{api_base}/me", headers=headers, timeout=10)
print(f"  Status: {r3.status_code}")
if r3.status_code == 401:
    print("  PASS: token rejected after logout (401 invalid_token)")
    sys.exit(0)
elif r3.status_code == 200:
    print("  CRITICAL: token still valid after logout — token replay vulnerability")
    sys.exit(3)
else:
    print(f"  UNEXPECTED: status {r3.status_code}")
    sys.exit(4)
