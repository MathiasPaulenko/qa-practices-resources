# Redis cache patterns

```redis
# Cache a product for 5 minutes (EX = TTL in seconds)
SET product:123 '{"id":123,"name":"Widget","price":19.99}' EX 300

# Tag-based invalidation: group keys under a tag
SADD tag:electronics product:123 product:456

# To invalidate the tag: read members, DEL each key
SMEMBERS tag:electronics

# Cache warming pattern (application code)
# for product in featured: cache.set(key, serialize(product), 300)
```

Rules of thumb:

- TTL 5-30 min for query results, 15-60 min for sessions
- Tag-based invalidation when a write can affect many cached reads
- Warm the cache after deploys — cold caches cause thundering herd
