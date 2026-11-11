"""N+1 query anti-pattern — the most common ORM performance bug.

Requires Django. Enable query logging (django.db.backends DEBUG)
to see the query count difference: N+1 vs 2 total.
"""

# Bad: N+1 queries — one extra query per author
authors = Author.objects.all()  # 1 query
for author in authors:
    print(author.books.count())  # N queries

# Good: 2 queries total — books prefetched in one go
authors = Author.objects.prefetch_related('books')
for author in authors:
    print(author.books.count())
