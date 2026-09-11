import jwt
from datetime import datetime, timedelta, timezone

payload = {
    "sub": "user-123",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
}

token = jwt.encode(payload, "secret", algorithm="HS256")
decoded = jwt.decode(token, "secret", algorithms=["HS256"])

assert decoded["sub"] == "user-123"
assert decoded["exp"] > datetime.now(timezone.utc).timestamp()