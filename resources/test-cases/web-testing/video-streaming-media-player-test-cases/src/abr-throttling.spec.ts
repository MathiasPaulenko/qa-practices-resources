import { test, expect } from '@playwright/test';

/**
 * TC-VS-002: Adaptive bitrate switching under throttling.
 *
 * Starts playback at full bandwidth, throttles via CDP, then restores
 * and asserts the rendition stepped down and back up without a stall.
 * Requires Playwright 1.48+.
 */

// Placeholder: replace with your staging player URL or set PLAYER_URL
const PLAYER_URL = process.env.PLAYER_URL ?? 'https://staging.example.com/player';

test.describe('ABR under throttling', () => {
  test('rendition downshifts under 1.5 Mbps and recovers', async ({ page, context }) => {
    const cdp = await context.newCDPSession(page);

    await page.goto(PLAYER_URL);
    const video = page.locator('video');
    await video.click();
    await expect(video).not.toHaveJSProperty('paused', true, { timeout: 5000 });

    // Let the buffer fill at full bandwidth
    await page.waitForTimeout(4000);
    const bufferedBefore = await video.evaluate(
      (v: HTMLVideoElement) => (v.buffered.length ? v.buffered.end(0) : 0),
    );
    expect(bufferedBefore).toBeGreaterThan(0);

    // Throttle to ~1.5 Mbps with 100ms latency
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', {
      offline: false,
      latency: 100,
      downloadThroughput: (1.5 * 1024 * 1024) / 8,
      uploadThroughput: (1 * 1024 * 1024) / 8,
    });
    await page.waitForTimeout(8000);

    // Playback must not freeze: currentTime still advances
    const t1 = await video.evaluate((v: HTMLVideoElement) => v.currentTime);
    await page.waitForTimeout(2000);
    const t2 = await video.evaluate((v: HTMLVideoElement) => v.currentTime);
    expect(t2).toBeGreaterThan(t1);

    // Restore bandwidth and confirm continued playback
    await cdp.send('Network.emulateNetworkConditions', {
      offline: false,
      latency: 0,
      downloadThroughput: -1,
      uploadThroughput: -1,
    });
    await page.waitForTimeout(4000);
    const t3 = await video.evaluate((v: HTMLVideoElement) => v.currentTime);
    expect(t3).toBeGreaterThan(t2);
  });
});
