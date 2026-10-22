# Social Media Test Cases — Companion

Companion resource for [Social Media Test Cases: Posts, Feed, Likes & DMs](https://qapractices.com/test-cases/social-media-test-cases/).

## Contents

- `social_feed.py` — stdlib-only model of the feed state machine: `SocialFeed` as source of truth with visibility scopes (public / followers / private / private profile), idempotent likes, comment-on-deleted races (`PostGone`), follow/unfollow/friend-request edges, two-way block, silent mute, hidden posts, report dedup, DM threads and scope-aware search.
- `feed.html` — static fixture implementing the like button + comment form contract for manual and Playwright verification: deduped like on an event flag, 410/404 handling when the post disappears mid-comment. Open it in any browser.
- `tests/conftest.py` — puts the model on `sys.path`.
- `tests/test_social_feed.py` — executable subset of the article's cases: like increment (TC-006), like idempotency (TC-007/edge), unlike no-negative (TC-007), comment persistence (TC-008), comment-on-deleted 410 (edge), followers-only scope (TC-005), retroactive private profile (TC-013), search visibility (TC-028), follow/unfollow counts (TC-014/015), friend-request dedup + accept (TC-016/017), reject (TC-018), report dedup (TC-023), two-way block + DM cutoff (TC-024), mute keeps follow (TC-025) and hidden post (TC-026).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `15 passed`.

## Related

- Article EN: https://qapractices.com/test-cases/social-media-test-cases/
- Article ES: https://qapractices.com/es/test-cases/social-media-test-cases/
