"""Find a user ID that hashes into an exact bucket — helper for TC-013.

Usage: python tests/find_bucket.py new-dashboard 50
"""

import sys

from flag_eval import bucket


def find(flag_key: str, target_bucket: int, limit: int = 100_000) -> str:
    for i in range(limit):
        user_id = f"user-{i:05d}"
        if bucket(flag_key, user_id) == target_bucket:
            return user_id
    raise ValueError(f"No user ID found for bucket {target_bucket} in {limit} tries")


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "new-dashboard"
    target = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    print(find(key, target))
