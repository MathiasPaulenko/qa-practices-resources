"""Executable subset of the article's social media test cases.

Handles mirror the article's dataset: @qa_alice authors, @qa_bob follows,
@qa_carol is a stranger, @qa_dana is blocked.
"""

import pytest

from social_feed import PermissionDenied, PostGone, SocialFeed

ALICE, BOB, CAROL, DANA = "@qa_alice", "@qa_bob", "@qa_carol", "@qa_dana"


@pytest.fixture
def feed() -> SocialFeed:
    f = SocialFeed()
    for h in (ALICE, BOB, CAROL, DANA):
        f.add_user(h, display_name=h.replace("@qa_", "").title())
    f.create_post(ALICE, "Shipping v2.4 today", "p-1042")
    return f


# -- likes (TC-006, TC-007, edge row 1) -------------------------------------

def test_like_increments_once(feed):
    assert feed.like("p-1042", BOB) == 1
    assert feed.like("p-1042", CAROL) == 2


def test_like_is_idempotent(feed):
    feed.like("p-1042", BOB)
    assert feed.like("p-1042", BOB) == 1  # double-tap = one like


def test_unlike_never_goes_negative(feed):
    feed.like("p-1042", BOB)
    assert feed.unlike("p-1042", BOB) == 0
    assert feed.unlike("p-1042", BOB) == 0  # repeat is a no-op


# -- comments (TC-008, edge row 2) ------------------------------------------

def test_comment_persists_and_counts(feed):
    feed.comment("p-1042", BOB, "Congrats!")
    post = feed.view_post("p-1042", BOB)
    assert len(post.comments) == 1
    assert post.comments[0].author == BOB


def test_comment_on_deleted_post_raises_gone(feed):
    feed.delete_post("p-1042", ALICE)
    with pytest.raises(PostGone):
        feed.comment("p-1042", BOB, "too late")


# -- visibility (TC-005, TC-013, edge row 4) ---------------------------------

def test_followers_only_hidden_from_stranger(feed):
    feed.create_post(ALICE, "for followers", "p-1043", visibility="followers")
    feed.follow(BOB, ALICE)
    assert feed.view_post("p-1043", BOB).id == "p-1043"  # follower sees it
    with pytest.raises(PermissionDenied):
        feed.view_post("p-1043", CAROL)  # stranger gets 403


def test_private_profile_retro_hides_posts(feed):
    feed.create_post(ALICE, "was public", "p-1044")
    feed.view_post("p-1044", CAROL)  # visible while public
    feed.set_private_profile(ALICE, True)
    with pytest.raises(PermissionDenied):
        feed.view_post("p-1044", CAROL)


def test_search_respects_visibility(feed):
    feed.create_post(ALICE, "release day notes", "p-1050")
    feed.create_post(ALICE, "release day private", "p-1051", visibility="followers")
    results = feed.search_posts("release day", CAROL)
    assert [p.id for p in results] == ["p-1050"]


# -- relationships (TC-014..TC-018) ------------------------------------------

def test_follow_and_unfollow_counts(feed):
    feed.follow(BOB, ALICE)
    assert feed.follower_count(ALICE) == 1
    feed.unfollow(BOB, ALICE)
    feed.unfollow(BOB, ALICE)  # idempotent
    assert feed.follower_count(ALICE) == 0


def test_friend_request_dedup_and_accept(feed):
    feed.send_friend_request(BOB, CAROL)
    feed.send_friend_request(BOB, CAROL)  # second click = no-op
    assert len(feed.pending_requests) == 1
    feed.accept_friend_request(CAROL, BOB)
    assert feed.are_friends(BOB, CAROL)
    assert not feed.pending_requests


def test_reject_request_creates_no_relationship(feed):
    feed.send_friend_request(BOB, CAROL)
    feed.reject_friend_request(CAROL, BOB)
    assert not feed.are_friends(BOB, CAROL)
    assert not feed.pending_requests


# -- moderation (TC-023..TC-026, edge row 5) ----------------------------------

def test_report_is_deduped_per_reporter(feed):
    assert feed.report_post(CAROL, "p-1042", "Spam") == 1
    assert feed.report_post(CAROL, "p-1042", "Spam") == 1  # spam-click
    assert feed.report_post(BOB, "p-1042", "Spam") == 2


def test_block_is_two_way_and_kills_dms(feed):
    feed.follow(BOB, DANA)
    feed.create_post(BOB, "bob's post", "p-2077")
    feed.send_dm(DANA, BOB, "hi")
    feed.block(BOB, DANA)
    assert not feed.is_following(BOB, DANA)  # block severs the follow
    with pytest.raises(PermissionDenied):
        feed.view_post("p-2077", DANA)  # blocked can't see blocker's posts
    with pytest.raises(PermissionDenied):
        feed.send_dm(DANA, BOB, "still there?")
    assert feed.dm_inbox(BOB) == []  # old thread hidden


def test_mute_filters_feed_but_keeps_follow(feed):
    feed.follow(BOB, DANA)
    feed.create_post(DANA, "dana's post", "p-2000")
    feed.mute(BOB, DANA)
    assert feed.is_following(BOB, DANA)
    assert all(p.author != DANA for p in feed.feed_for(BOB))


def test_hidden_post_stays_out_of_feed(feed):
    feed.follow(BOB, ALICE)
    feed.hide_post("p-1042", BOB)
    assert feed.posts["p-1042"].id in [p.id for p in feed.posts.values()]
    assert "p-1042" not in [p.id for p in feed.feed_for(BOB)]
    assert feed.view_post("p-1042", ALICE)  # author unaffected
