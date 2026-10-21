import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import {
  makeFakeClock,
  TtlCache,
  shouldRunCronOnDate,
  remainingBudget,
  findDstFold,
} from '../time-testing.mjs';

describe('fake clock', () => {
  test('advances and sets deterministically', () => {
    const clock = makeFakeClock(1000);
    assert.equal(clock.now(), 1000);
    assert.equal(clock.advance(500), 1500);
    clock.set(0);
    assert.equal(clock.now(), 0);
  });
});

describe('TTL cache — absolute expiration', () => {
  test('item expires exactly at the TTL boundary', () => {
    const clock = makeFakeClock(0);
    const cache = new TtlCache({ clock, ttlMs: 3600_000 });
    cache.set('k', 'v');
    clock.advance(3599_000);
    assert.equal(cache.get('k'), 'v');
    clock.advance(1000);
    assert.equal(cache.get('k'), undefined);
  });

  test('read does not extend absolute TTL', () => {
    const clock = makeFakeClock(0);
    const cache = new TtlCache({ clock, ttlMs: 1000 });
    cache.set('k', 'v');
    clock.advance(500);
    assert.equal(cache.get('k'), 'v');
    clock.advance(600);
    assert.equal(cache.get('k'), undefined);
  });
});

describe('TTL cache — sliding expiration', () => {
  test('repeated reads keep the item alive', () => {
    const clock = makeFakeClock(0);
    const cache = new TtlCache({ clock, ttlMs: 1000 });
    cache.set('k', 'v', { sliding: true });
    for (let i = 0; i < 5; i++) {
      clock.advance(900);
      assert.equal(cache.get('k'), 'v');
    }
    clock.advance(1100);
    assert.equal(cache.get('k'), undefined);
  });
});

describe('cron month-end rules', () => {
  test('day 30 never fires in February', () => {
    assert.equal(shouldRunCronOnDate(new Date('2026-02-28T00:00:00Z'), 30), false);
    assert.equal(shouldRunCronOnDate(new Date('2026-03-30T00:00:00Z'), 30), true);
  });

  test('day 31 never fires in 30-day months', () => {
    assert.equal(shouldRunCronOnDate(new Date('2026-04-30T00:00:00Z'), 31), false);
    assert.equal(shouldRunCronOnDate(new Date('2026-05-31T00:00:00Z'), 31), true);
  });

  test('day 29 fires on leap Feb 29 only', () => {
    assert.equal(shouldRunCronOnDate(new Date('2024-02-29T00:00:00Z'), 29), true);
    // 2026-02-29 does not exist; the scheduler skips silently
    assert.equal(shouldRunCronOnDate(new Date('2026-02-28T00:00:00Z'), 29), false);
  });
});

describe('deadline propagation', () => {
  test('nested call receives remaining budget, not a fresh timeout', () => {
    const clock = makeFakeClock(0);
    const deadline = 10_000;
    clock.advance(4000);
    assert.equal(remainingBudget(deadline, clock), 6000);
    clock.advance(7000);
    assert.equal(remainingBudget(deadline, clock), 0);
  });
});

describe('DST fold — real America/New_York data', () => {
  test('01:30 occurs twice on fall-back Sunday 2026-11-01', () => {
    const fold = findDstFold('2026-11-01', '01:30');
    assert.ok(fold, 'expected a fold for 01:30');
    // The two occurrences are one hour apart in UTC
    assert.equal(fold[1] - fold[0], 3_600_000);
  });

  test('no fold on a normal day', () => {
    assert.equal(findDstFold('2026-11-08', '01:30'), null);
  });
});
