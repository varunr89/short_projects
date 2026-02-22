import { chromium } from 'playwright';
import path from 'path';

async function discoverDetailTour() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  const chartsDir = '/Users/varunr/projects/short_projects/ai-tools-evolution/charts';

  console.log('Starting Discover detail tour...');

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

    console.log('On Discover page, looking for podcast cards...');

    // Look for clickable podcast cards
    const cards = await page.locator('a[href*="/"]').all();
    console.log(`Found ${cards.length} total links`);

    // Try to find a podcast card that's not a navigation link
    for (let i = 0; i < cards.length; i++) {
      const href = await cards[i].getAttribute('href');
      const text = await cards[i].textContent();

      // Skip navigation links
      if (href === '/dashboard' || href === '/library' || href === '/discover' || href === '/settings') {
        continue;
      }

      console.log(`\nTrying card ${i + 1}: ${href}`);
      console.log(`  Text: ${text?.substring(0, 100)}`);

      try {
        await cards[i].click({ timeout: 2000 });
        await page.waitForTimeout(3000);

        console.log('  Clicked! Taking screenshot of detail page...');
        await page.screenshot({
          path: path.join(chartsDir, 'v1_auth_podcast_detail.png'),
          fullPage: false
        });

        // Scroll down to see full content
        await page.mouse.wheel(0, 800);
        await page.waitForTimeout(1000);
        await page.screenshot({
          path: path.join(chartsDir, 'v1_auth_podcast_detail_scrolled.png'),
          fullPage: false
        });

        // Check for episodes or summaries
        const episodeLinks = await page.locator('a, button, [role="button"]').count();
        console.log(`  Found ${episodeLinks} clickable elements on detail page`);

        // Look for episode items
        const possibleEpisodes = await page.locator('[class*="episode"], article, .card').all();
        if (possibleEpisodes.length > 0) {
          console.log(`  Found ${possibleEpisodes.length} potential episode items`);

          try {
            await possibleEpisodes[0].click({ timeout: 2000 });
            await page.waitForTimeout(2000);

            console.log('  Clicked episode! Taking screenshot...');
            await page.screenshot({
              path: path.join(chartsDir, 'v1_auth_episode_summary.png'),
              fullPage: true
            });
          } catch (e) {
            console.log(`  Could not click episode: ${e.message}`);
          }
        }

        break;
      } catch (e) {
        console.log(`  Could not click: ${e.message}`);
      }
    }

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
}

discoverDetailTour();
