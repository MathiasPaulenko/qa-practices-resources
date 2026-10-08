import { test } from '@playwright/test';
import {
  Eyes, Target, ClassicRunner, Configuration, BatchInfo,
} from '@applitools/eyes-playwright'; // 1.49.4

const BASE_URL = 'https://staging.myshop.example'; // Placeholder: replace with your staging URL

// Requires APPLITOOLS_API_KEY as an environment variable.
test.describe('applitools visual tests @visual', () => {
  test('visual test with Applitools', async ({ page }) => {
    const runner = new ClassicRunner();
    const eyes = new Eyes(runner);
    const config = new Configuration();
    config.setApiKey(process.env.APPLITOOLS_API_KEY);
    config.setBatch(new BatchInfo('Visual Regression'));
    eyes.setConfiguration(config);

    await eyes.open(page, 'My Shop', 'Homepage Test', { width: 1280, height: 720 });
    await page.goto(BASE_URL);
    await eyes.check('Homepage', Target.window().fully());
    await page.click('#open-modal');
    await eyes.check('Modal', Target.region('#modal'));
    await eyes.closeAsync();
  });
});
