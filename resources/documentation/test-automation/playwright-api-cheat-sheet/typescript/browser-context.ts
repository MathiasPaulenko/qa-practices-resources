// @playwright/test 1.x — launch a browser and an isolated context
import { test, expect, chromium, firefox, webkit } from '@playwright/test';

const browser = await chromium.launch({ headless: false });
const context = await browser.newContext();
const page = await context.newPage();
await browser.close();
