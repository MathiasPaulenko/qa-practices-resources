/**
 * Time-testing primitives for the time-dependent testing guide.
 *
 * An injectable clock plus the behaviors the guide describes: a TTL cache
 * (absolute vs sliding expiration), month-end cron boundary rules, deadline
 * propagation, and a real DST fold detection against America/New_York.
 * Zero dependencies — runs on Node 20+.
 */

export const realClock = { now: () => Date.now() };

/** A manually advanced clock: the unit every time test should depend on. */
export function makeFakeClock(start = 0) {
  let t = start;
  return {
    now: () => t,
    advance: (ms) => {
      t += ms;
      return t;
    },
    set: (v) => {
      t = v;
    },
  };
}

/**
 * TTL cache honoring exact expiration semantics.
 * `sliding: false` (absolute) — entry expires at insert-time + ttlMs.
 * `sliding: true` — every read renews the TTL.
 */
export class TtlCache {
  constructor({ clock = realClock, ttlMs }) {
    if (!Number.isFinite(ttlMs) || ttlMs <= 0) {
      throw new Error('ttlMs must be a positive number');
    }
    this.clock = clock;
    this.ttlMs = ttlMs;
    this.store = new Map();
  }

  set(key, value, { sliding = false } = {}) {
    this.store.set(key, { value, expiresAt: this.clock.now() + this.ttlMs, sliding });
  }

  get(key) {
    const entry = this.store.get(key);
    if (!entry) return undefined;
    if (this.clock.now() >= entry.expiresAt) {
      this.store.delete(key);
      return undefined;
    }
    if (entry.sliding) entry.expiresAt = this.clock.now() + this.ttlMs;
    return entry.value;
  }

  has(key) {
    return this.get(key) !== undefined;
  }
}

/**
 * Month-end cron rule: a job scheduled for day-of-month `dom` must not run
 * when the month is shorter than `dom` (Feb 30, Apr 31 never fire).
 */
export function shouldRunCronOnDate(date, dom) {
  return date.getUTCDate() === dom;
}

/**
 * Deadline propagation: a nested call receives the budget that remains,
 * not a fresh timeout.
 */
export function remainingBudget(deadlineAt, clock = realClock) {
  return Math.max(0, deadlineAt - clock.now());
}

const ny = 'America/New_York';
const nyHour = new Intl.DateTimeFormat('en-US', {
  timeZone: ny,
  hour: 'numeric',
  minute: 'numeric',
  hour12: false,
});

/**
 * DST fold detection: two distinct UTC instants that map to the same
 * New York wall-clock hour — the 01:00–02:00 window that occurs twice on
 * fall-back Sunday. Returns the pair of UTC instants or null.
 */
export function findDstFold(isoDate, localHourLabel) {
  const start = Date.parse(`${isoDate}T00:00:00Z`);
  const hits = [];
  for (let m = 0; m < 24 * 60; m += 30) {
    const instant = start + m * 60_000;
    if (nyHour.format(new Date(instant)) === localHourLabel) hits.push(instant);
  }
  // The fold yields two separate 1-hour blocks mapping to the same label.
  const blocks = hits.reduce((acc, t) => {
    const last = acc[acc.length - 1];
    if (!last || t - last[last.length - 1] > 30 * 60_000) acc.push([]);
    acc[acc.length - 1].push(t);
    return acc;
  }, []);
  return blocks.length === 2 ? blocks.map((b) => b[0]) : null;
}
