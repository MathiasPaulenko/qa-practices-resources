# Race Conditions Testing — Runnable Java Stress Harness

Companion code for [How to Test Race Conditions: Concurrency Testing Guide](https://qapractices.com/documentation/race-conditions-testing/) on QAPractices.

Plain Java 17+, zero dependencies — `javac` and `java` are all you need.

## What is inside

| File | What it shows |
|------|---------------|
| `java/UnsafeInventory.java` | Check-then-act race: `stock > 0` check and `stock--` are not atomic, so two buyers can both win the last unit. |
| `java/SafeInventory.java` | Same contract made atomic with `AtomicInteger.compareAndSet` — the race disappears. |
| `java/RaceDemo.java` | Stress harness: a lost-update counter demo (8 threads, start gate) plus an oversell demo that loops until two buyers grab the same unit. |

## Run it

```bash
cd java
javac *.java
java RaceDemo
```

Typical output (numbers vary by machine and scheduler):

```text
Counter: expected 400000, got 234360 -> 165640 lost updates
Oversell: 37 rounds out of 20000 sold the same unit twice
```

Then swap `UnsafeInventory` for `SafeInventory` inside `RaceDemo.oversellDemo` and re-run: the oversell count drops to zero while the counter demo keeps showing lost updates — that contrast is the point of the exercise.

## Related resource

- [How to Test Race Conditions: Concurrency Testing Guide](https://qapractices.com/documentation/race-conditions-testing/) — strategies, tools (jcstress, ThreadSanitizer, rr, TLA+) and the runnable jcstress example this harness complements.
