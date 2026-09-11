import requests

response = requests.get("https://auth.staging.local/login")

assert response.headers.get("X-Frame-Options") in ["DENY", "SAMEORIGIN"]
assert "no-store" in response.headers.get("Cache-Control", "")
assert response.headers.get("X-Content-Type-Options") == "nosniff"