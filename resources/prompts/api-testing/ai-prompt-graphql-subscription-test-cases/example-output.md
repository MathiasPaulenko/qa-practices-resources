# Example Output — Generated Test Matrix (fragment)

What the generated suite looks like for the chat-backend input above.

| Test | Query | Expected | Severity |
|---|---|---|---|
| Valid subscription receives events | `subscription { messageAdded(roomId: "r1") { id text } }` | Events arrive in order, correct shape | Critical |
| Expired JWT mid-subscription | `subscription { adminEvents }` | Connection terminated with auth error | Critical |
| Room filter respected | `subscription { messageAdded(roomId: "r2") }` | Only r2 events delivered | High |
| Network drop + resumption | `subscription { messageAdded }` | Auto-reconnect, missed events delivered | High |
| Slow consumer backpressure | `subscription { highFreqEvents }` | Server buffers/throttles, no OOM | High |
| 10K concurrent subscriptions | `subscription { presenceChanged }` | Fan-out < 5s, memory per connection < 10KB | High |

Each generated case also carries: transport, preconditions (auth, connection, pubsub state), execution steps, pass/fail criteria, and test type (functional/performance/security/resilience).
