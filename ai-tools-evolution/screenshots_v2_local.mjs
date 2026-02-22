import { chromium } from 'playwright';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const chartsDir = join(__dirname, 'charts');

// Capture the v2 frontend after clicking "Get Started"
// and also try to capture the dashboard view
const pages = [
  {
    name: 'v2_frontend_dashboard',
    url: 'https://podcast.bhavanaai.com',
    viewport: { width: 1280, height: 900 },
    actions: async (tab) => {
      // Try clicking Get Started to see what happens
      try {
        const btn = tab.getByText('Get Started');
        await btn.click();
        await tab.waitForTimeout(3000);
      } catch {
        // If button not found, that's fine
      }
    }
  },
  {
    name: 'v2_frontend_dark',
    url: 'https://podcast.bhavanaai.com',
    viewport: { width: 1280, height: 900 },
    dark: true,
  },
];

(async () => {
  const browser = await chromium.launch({ headless: true });

  for (const page of pages) {
    console.log(`Capturing: ${page.name}`);
    const context = await browser.newContext({
      colorScheme: page.dark ? 'dark' : 'light',
    });
    const tab = await context.newPage();
    await tab.setViewportSize(page.viewport);
    try {
      await tab.goto(page.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await tab.waitForTimeout(3000);
      if (page.actions) {
        await page.actions(tab);
      }
      const path = join(chartsDir, `${page.name}.png`);
      await tab.screenshot({ path, fullPage: false });
      console.log(`  Saved: ${path}`);
    } catch (err) {
      console.error(`  Error: ${err.message}`);
    }
    await context.close();
  }

  await browser.close();
  console.log('Done.');
})();
