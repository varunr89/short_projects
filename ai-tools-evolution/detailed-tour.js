import { chromium } from 'playwright';
import path from 'path';

async function detailedTour() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  const chartsDir = '/Users/varunr/projects/short_projects/ai-tools-evolution/charts';

  console.log('Starting detailed tour...');

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

    // Get page content to analyze
    const libraryContent = await page.content();
    console.log('=== LIBRARY PAGE STRUCTURE ===');

    // Look for any clickable cards/items
    const clickableItems = await page.locator('a, button, [role="button"]').count();
    console.log(`Total clickable items: ${clickableItems}`);

    // Try to find podcast cards by various selectors
    const selectors = [
      'article',
      '.card',
      '[class*="podcast"]',
      '[class*="episode"]',
      'a[href*="/podcast"]',
      'a[href*="/episode"]',
      'a[href*="/show"]',
      '.podcast-card',
      '[data-testid*="podcast"]',
      '[data-testid*="episode"]'
    ];

    for (const selector of selectors) {
      const count = await page.locator(selector).count();
      if (count > 0) {
        console.log(`Found ${count} elements with selector: ${selector}`);

        // Try clicking the first one
        try {
          const firstItem = page.locator(selector).first();
          const text = await firstItem.textContent();
          console.log(`  First item text: ${text?.substring(0, 100)}`);

          await firstItem.click({ timeout: 2000 });
          await page.waitForTimeout(2000);

          console.log(`  Successfully clicked! Taking screenshot...`);
          await page.screenshot({
            path: path.join(chartsDir, 'v1_auth_podcast_detail_found.png'),
            fullPage: true
          });

          // Go back
          await page.goBack();
          await page.waitForTimeout(1000);
          break;
        } catch (e) {
          console.log(`  Could not click: ${e.message}`);
        }
      }
    }

    // Also check if there are any links in the library
    const links = await page.locator('a[href]').all();
    console.log(`\nTotal links found: ${links.length}`);

    for (let i = 0; i < Math.min(links.length, 10); i++) {
      const href = await links[i].getAttribute('href');
      const text = await links[i].textContent();
      console.log(`  Link ${i + 1}: ${href} - ${text?.substring(0, 50)}`);
    }

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
}

detailedTour();
