import { chromium } from 'playwright';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const chartsDir = join(__dirname, 'charts');

const pages = [
  {
    name: 'v1_github_repo',
    url: 'https://github.com/varunr89/podcast_summarizer',
    waitFor: 'networkidle',
    viewport: { width: 1280, height: 900 },
  },
  {
    name: 'v2_github_repo',
    url: 'https://github.com/varunr89/podcast-summarizer-v2',
    waitFor: 'networkidle',
    viewport: { width: 1280, height: 900 },
  },
  {
    name: 'v2_live_frontend',
    url: 'https://podcast.bhavanaai.com',
    waitFor: 'networkidle',
    viewport: { width: 1280, height: 900 },
  },
  {
    name: 'v1_github_files',
    url: 'https://github.com/varunr89/podcast_summarizer/find/main',
    waitFor: 'networkidle',
    viewport: { width: 1280, height: 900 },
  },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    colorScheme: 'dark',
  });

  for (const page of pages) {
    console.log(`Capturing: ${page.name} -> ${page.url}`);
    const tab = await context.newPage();
    await tab.setViewportSize(page.viewport);
    try {
      await tab.goto(page.url, { waitUntil: page.waitFor, timeout: 30000 });
      // Extra wait for dynamic content
      await tab.waitForTimeout(2000);
      const path = join(chartsDir, `${page.name}.png`);
      await tab.screenshot({ path, fullPage: false });
      console.log(`  Saved: ${path}`);
    } catch (err) {
      console.error(`  Error on ${page.name}: ${err.message}`);
    }
    await tab.close();
  }

  await browser.close();
  console.log('Done.');
})();
