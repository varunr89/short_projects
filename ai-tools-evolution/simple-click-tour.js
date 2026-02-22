import { chromium } from 'playwright';
import path from 'path';

async function simpleClickTour() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  const chartsDir = '/Users/varunr/projects/short_projects/ai-tools-evolution/charts';

  console.log('Starting simple click tour...');

  try {
    // Navigate and login
    await page.goto('https://mindcastdaily.netlify.app/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.getByRole('link', { name: 'Library' }).click();
    await page.waitForTimeout(2000);
    await page.locator('input[type="email"]').fill('varun.ramesh08@gmail.com');
    await page.locator('input[type="password"]').fill('Ayesha27!');
    await page.getByRole('button', { name: /sign in/i }).click();
    await page.waitForTimeout(3000);

    // Go to Discover
    await page.getByRole('link', { name: 'Discover' }).click();
    await page.waitForTimeout(2000);

    console.log('Clicking on first visible podcast card...');

    // Click at a specific coordinate where we can see a card in the screenshot
    // Looking at v1_auth_discover.png, there are cards around y=80-150
    await page.mouse.click(100, 100);
    await page.waitForTimeout(3000);

    console.log('Took a click, checking if page changed...');
    const url = page.url();
    console.log(`Current URL: ${url}`);

    if (url !== 'https://mindcastdaily.netlify.app/discover') {
      console.log('Page changed! Taking screenshot...');
      await page.screenshot({
        path: path.join(chartsDir, 'v1_auth_podcast_detail.png'),
        fullPage: false
      });

      // Scroll down
      await page.mouse.wheel(0, 800);
      await page.waitForTimeout(1000);
      await page.screenshot({
        path: path.join(chartsDir, 'v1_auth_podcast_detail_scrolled.png'),
        fullPage: false
      });

      // Look for episodes
      await page.mouse.click(640, 400);
      await page.waitForTimeout(2000);

      const newUrl = page.url();
      if (newUrl !== url) {
        console.log('Navigated to episode! Taking screenshot...');
        await page.screenshot({
          path: path.join(chartsDir, 'v1_auth_episode_summary.png'),
          fullPage: true
        });
      }
    }

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
}

simpleClickTour();
