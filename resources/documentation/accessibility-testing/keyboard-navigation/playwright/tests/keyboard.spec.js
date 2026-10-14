import { test, expect } from '@playwright/test';

// All fixtures render inline with page.setContent() — no external site needed.

const GOOD_MODAL_PAGE = `
<!doctype html><html><body>
  <a href="#main" class="skip-link">Skip to main content</a>
  <nav><a href="/home">Home</a><a href="/about">About</a></nav>
  <main id="main">
    <button id="open">Open modal</button>
    <div id="modal" role="dialog" aria-modal="true" hidden>
      <h2 id="title">Confirm action</h2>
      <button id="cancel">Cancel</button>
      <button id="ok">OK</button>
    </div>
  </main>
  <script>
    const modal = document.getElementById('modal');
    const trigger = document.getElementById('open');
    trigger.addEventListener('click', () => {
      modal.hidden = false;
      document.getElementById('cancel').focus();
    });
    modal.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { modal.hidden = true; trigger.focus(); }
      if (e.key === 'Tab') {
        const items = modal.querySelectorAll('button');
        const first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
        else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
      }
    });
  </script>
</body></html>`;

const BROKEN_TABINDEX_PAGE = `
<!doctype html><html><body>
  <input id="first" tabindex="3" placeholder="first field">
  <input id="second" tabindex="1" placeholder="second field">
  <input id="third" tabindex="2" placeholder="third field">
</body></html>`;

const OFFSCREEN_FOCUSABLE_PAGE = `
<!doctype html><html><body>
  <a href="/visible">Visible link</a>
  <a href="/ghost" style="position:absolute;left:-9999px">Ghost link</a>
  <button>Real button</button>
</body></html>`;

const SKIP_LINK_PAGE = `
<!doctype html><html><head><style>
  .skip-link { position:absolute; left:-9999px; }
  .skip-link:focus { position:static; }
</style></head><body>
  <a href="#main" class="skip-link">Skip to main content</a>
  <nav><a href="/a">A</a><a href="/b">B</a><a href="/c">C</a></nav>
  <main id="main" tabindex="-1"><p>Main content</p></main>
</body></html>`;

test.describe('keyboard navigation', () => {
  test('tab order follows DOM order when no positive tabindex is set', async ({ page }) => {
    await page.setContent(`<a href="/x">Link A</a><button>Btn B</button><input placeholder="C">`);
    await page.keyboard.press('Tab');
    await expect(page.locator('a:text("Link A")')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('button:text("Btn B")')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('input')).toBeFocused();
  });

  test('positive tabindex reorders focus — demonstrates the anti-pattern', async ({ page }) => {
    await page.setContent(BROKEN_TABINDEX_PAGE);
    await page.keyboard.press('Tab');
    // tabindex="1" wins before DOM order — this is the bug pattern to catch in review
    await expect(page.locator('#second')).toBeFocused();
  });

  test('modal opens on Enter, traps focus, Escape returns focus to trigger', async ({ page }) => {
    await page.setContent(GOOD_MODAL_PAGE);
    await page.locator('#open').focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('#modal')).toBeVisible();
    await expect(page.locator('#cancel')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('#ok')).toBeFocused();
    await page.keyboard.press('Tab'); // wraps back inside the dialog
    await expect(page.locator('#cancel')).toBeFocused();
    await page.keyboard.press('Escape');
    await expect(page.locator('#modal')).toBeHidden();
    await expect(page.locator('#open')).toBeFocused();
  });

  test('off-screen positioned links still receive Tab focus — flagged as a bug', async ({ page }) => {
    await page.setContent(OFFSCREEN_FOCUSABLE_PAGE);
    await page.keyboard.press('Tab');
    await expect(page.locator('a:text("Visible link")')).toBeFocused();
    await page.keyboard.press('Tab');
    // left:-9999px keeps it focusable — a real-world keyboard trap
    await expect(page.locator('a:text("Ghost link")')).toBeFocused();
  });

  test('skip link is the first tab stop and targets main content', async ({ page }) => {
    await page.setContent(SKIP_LINK_PAGE);
    await page.keyboard.press('Tab');
    await expect(page.locator('.skip-link')).toBeFocused();
    await page.keyboard.press('Enter');
    // after activation, focus/context moves past the nav
    await expect(page.locator('#main')).toBeFocused();
  });
});
