"""In-memory model of a social feed's state machine.

Covers the contracts the article's edge table tests: like idempotency,
comment-on-deleted races, visibility scopes, retroactive privacy,
two-way blocks, silent mutes, report dedup and feed filtering.

Only the standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class PostGone(Exception):
    """The post was deleted or moderated — the client would see 410/404."""


class PermissionDenied(Exception):
    """The viewer is outside the post's or profile's scope — 403/404."""


@dataclass
class Post:
    id: str
    author: str
    body: str
    visibility: str = "public"  # public | followers | private
    deleted: bool = False
    removed: bool = False
    hidden_by: set[str] = field(default_factory=set)
    likes: list[str] = field(default_factory=list)
    comments: list["Comment"] = field(default_factory=list)


@dataclass
class Comment:
    id: str
    post_id: str
    author: str
    body: str


@dataclass
class User:
    handle: str
    display_name: str = ""
    private_profile: bool = False
    active: bool = True


class SocialFeed:
    """Server-side model: the API is the contract, the feed is derived."""

    def __init__(self) -> None:
        self.users: dict[str, User] = {}
        self.posts: dict[str, Post] = {}
        self.follows: set[tuple[str, str]] = set()  # (follower, author)
        self.friends: set[frozenset[str]] = set()
        self.pending_requests: set[tuple[str, str]] = set()
        self.blocked: set[frozenset[str]] = set()
        self.muted: set[tuple[str, str]] = set()  # (muter, muted)
        self.reports: dict[tuple[str, str], str] = {}  # (reporter, post) -> reason
        self.dm_threads: dict[frozenset[str], list[dict]] = {}

    # -- users -------------------------------------------------------

    def add_user(self, handle: str, display_name: str = "", private: bool = False) -> None:
        self.users[handle] = User(handle, display_name or handle, private)

    def deactivate(self, handle: str) -> None:
        self.users[handle].active = False

    def set_private_profile(self, handle: str, private: bool) -> None:
        self.users[handle].private_profile = private

    # -- relationships -------------------------------------------------

    def follow(self, follower: str, author: str) -> None:
        if follower == author or self.is_blocked(follower, author):
            raise PermissionDenied("cannot follow")
        if not self.users[author].active:
            raise PostGone("target account is deactivated")
        self.follows.add((follower, author))

    def unfollow(self, follower: str, author: str) -> None:
        self.follows.discard((follower, author))  # idempotent

    def is_following(self, follower: str, author: str) -> bool:
        return (follower, author) in self.follows

    def follower_count(self, author: str) -> int:
        return sum(1 for f, a in self.follows if a == author and self.users[f].active)

    def block(self, blocker: str, blocked: str) -> None:
        self.blocked.add(frozenset((blocker, blocked)))
        self.follows.discard((blocker, blocked))
        self.follows.discard((blocked, blocker))

    def unblock(self, a: str, b: str) -> None:
        self.blocked.discard(frozenset((a, b)))

    def is_blocked(self, a: str, b: str) -> bool:
        return frozenset((a, b)) in self.blocked

    def mute(self, muter: str, muted: str) -> None:
        self.muted.add((muter, muted))

    def unmute(self, muter: str, muted: str) -> None:
        self.muted.discard((muter, muted))

    # -- friend requests ------------------------------------------------

    def send_friend_request(self, requester: str, target: str) -> None:
        if self.is_blocked(requester, target):
            raise PermissionDenied("cannot request friendship")
        if frozenset((requester, target)) in self.friends:
            raise ValueError("already friends")
        if (requester, target) in self.pending_requests:
            return  # idempotent: a second click is a no-op
        if (target, requester) in self.pending_requests:
            self.pending_requests.discard((target, requester))
            self.friends.add(frozenset((requester, target)))  # mutual send = accept
            return
        self.pending_requests.add((requester, target))

    def accept_friend_request(self, target: str, requester: str) -> None:
        if (requester, target) not in self.pending_requests:
            raise PostGone("no pending request")
        self.pending_requests.discard((requester, target))
        self.friends.add(frozenset((requester, target)))

    def reject_friend_request(self, target: str, requester: str) -> None:
        self.pending_requests.discard((requester, target))  # no relationship created

    def are_friends(self, a: str, b: str) -> bool:
        return frozenset((a, b)) in self.friends

    # -- posts ----------------------------------------------------------

    def create_post(self, author: str, body: str, post_id: str,
                    visibility: str = "public") -> Post:
        if len(body) > 280:
            raise ValueError("body exceeds 280 characters")
        post = Post(id=post_id, author=author, body=body, visibility=visibility)
        self.posts[post_id] = post
        return post

    def _can_view(self, post: Post, viewer: str) -> bool:
        if post.deleted or post.removed:
            return False
        if viewer == post.author:
            return True
        if self.is_blocked(viewer, post.author):
            return False
        if not self.users[post.author].active:
            return False
        if self.users[post.author].private_profile and not self.is_following(viewer, post.author):
            return False
        if post.visibility == "private":
            return False
        if post.visibility == "followers" and not self.is_following(viewer, post.author):
            return False
        return True

    def view_post(self, post_id: str, viewer: str) -> Post:
        post = self.posts.get(post_id)
        if post is None or post.deleted or post.removed:
            raise PostGone(post_id)
        if not self._can_view(post, viewer):
            raise PermissionDenied(post_id)
        return post

    def delete_post(self, post_id: str, author: str) -> None:
        post = self.posts[post_id]
        if post.author != author:
            raise PermissionDenied("only the author can delete")
        post.deleted = True

    def remove_post(self, post_id: str) -> None:
        """Moderation removal — stricter than author delete."""
        self.posts[post_id].removed = True

    def hide_post(self, post_id: str, viewer: str) -> None:
        self.posts[post_id].hidden_by.add(viewer)

    # -- interactions -----------------------------------------------------

    def like(self, post_id: str, user: str) -> int:
        post = self.view_post(post_id, user)
        if user not in post.likes:  # dedup: second identical write is a no-op
            post.likes.append(user)
        return len(post.likes)

    def unlike(self, post_id: str, user: str) -> int:
        post = self.view_post(post_id, user)
        if user in post.likes:
            post.likes.remove(user)
        return len(post.likes)  # repeated unlike never goes negative

    def comment(self, post_id: str, user: str, body: str) -> Comment:
        post = self.view_post(post_id, user)  # PostGone if deleted mid-flight
        comment = Comment(id=f"c-{len(post.comments) + 1}", post_id=post_id,
                          author=user, body=body)
        post.comments.append(comment)
        return comment

    # -- moderation --------------------------------------------------------

    def report_post(self, reporter: str, post_id: str, reason: str) -> int:
        self.view_post(post_id, reporter)
        key = (reporter, post_id)
        if key not in self.reports:  # one report per reporter+post
            self.reports[key] = reason
        return sum(1 for (_r, p) in self.reports if p == post_id)

    # -- messaging -----------------------------------------------------------

    def send_dm(self, sender: str, recipient: str, body: str) -> dict:
        if self.is_blocked(sender, recipient):
            raise PermissionDenied("DMs closed by block")
        thread = self.dm_threads.setdefault(frozenset((sender, recipient)), [])
        msg = {"sender": sender, "body": body, "read": False}
        thread.append(msg)
        return msg

    def dm_inbox(self, user: str) -> list[dict]:
        """Threads the user still sees: blocked threads are hidden."""
        out = []
        for pair, thread in self.dm_threads.items():
            other = next(h for h in pair if h != user)
            if not self.is_blocked(user, other):
                out.append({"with": other, "messages": thread})
        return out

    # -- feed & search ---------------------------------------------------------

    def feed_for(self, user: str) -> list[Post]:
        """Visible posts, in insertion order, with all filters applied."""
        return [
            p for p in self.posts.values()
            if self._can_view(p, user)
            and user not in p.hidden_by
            and (user, p.author) not in self.muted
        ]

    def search_users(self, query: str) -> list[User]:
        q = query.lower()
        return [
            u for u in self.users.values()
            if u.active and (q in u.handle.lower() or q in u.display_name.lower())
        ]

    def search_posts(self, query: str, viewer: str) -> list[Post]:
        q = query.lower()
        return [
            p for p in self.posts.values()
            if q in p.body.lower() and self._can_view(p, viewer)
        ]
