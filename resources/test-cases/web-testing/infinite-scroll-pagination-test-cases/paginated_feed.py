"""Paginated feed model — simulates an infinite-scroll API + client merge.

Standard library only. ``PaginatedAPI`` serves pages; ``ScrollFeed`` plays the
client: fetch on threshold, append + dedupe by id, hasMore / error / retry.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    title: str


@dataclass
class Page:
    items: list[Task]
    page: int
    has_more: bool


class ApiError(Exception):
    pass


class PaginatedAPI:
    """Offset-paginated task source, like GET /api/v1/tasks?project=x&page=n&limit=k."""

    def __init__(self, tasks: list[Task], page_size: int = 20):
        self.tasks = tasks
        self.page_size = page_size
        self.requests: list[int] = []
        self.fail_next: int = 0  # number of upcoming requests that must fail

    def fetch(self, page: int) -> Page:
        self.requests.append(page)
        if self.fail_next:
            self.fail_next -= 1
            raise ApiError("simulated 500 on page fetch")
        start = (page - 1) * self.page_size
        chunk = self.tasks[start : start + self.page_size]
        return Page(items=chunk, page=page, has_more=start + self.page_size < len(self.tasks))


@dataclass
class ScrollFeed:
    """Client-side feed: dedupe by id, track rendered ids, honor hasMore."""

    api: PaginatedAPI
    rendered: list[Task] = field(default_factory=list)
    seen_ids: set = field(default_factory=set)
    duplicates_rejected: int = 0
    last_error: str | None = None
    ended: bool = False

    def load_next(self) -> bool:
        """Return False when the feed is already at end-of-feed."""
        if self.ended:
            return False
        page = self.api.requests[-1] + 1 if self.api.requests else 1
        try:
            result = self.api.fetch(page)
        except ApiError as e:
            self.last_error = str(e)
            return False
        self.last_error = None
        for task in result.items:
            if task.id in self.seen_ids:
                self.duplicates_rejected += 1
                continue
            self.seen_ids.add(task.id)
            self.rendered.append(task)
        if not result.has_more:
            self.ended = True
        return True

    def retry(self) -> bool:
        """Retry after an error — idempotent thanks to id dedupe."""
        if self.last_error is None and not self.api.fail_next:
            return self.load_next()
        page = self.api.requests[-1]
        try:
            result = self.api.fetch(page)
        except ApiError as e:
            self.last_error = str(e)
            return False
        self.last_error = None
        for task in result.items:
            if task.id in self.seen_ids:
                self.duplicates_rejected += 1
                continue
            self.seen_ids.add(task.id)
            self.rendered.append(task)
        if not result.has_more:
            self.ended = True
        return True


def make_tasks(count: int, prefix: str = "T") -> list[Task]:
    return [Task(id=f"{prefix}-{i + 1:03d}", title=f"Task {i + 1}") for i in range(count)]
