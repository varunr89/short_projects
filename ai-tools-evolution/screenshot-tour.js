import { chromium } from 'playwright';
import path from 'path';

async function takeScreenshotTour() {
  // Launch browser
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  const chartsDir = '/Users/varunr/projects/short_projects/ai-tools-evolution/charts';

  console.log('Starting screenshot tour...');

  try {
    // 1. Navigate to the site
    console.log('1. Navigating to Mindcast Daily...');
    await page.goto('https://mindcastdaily.netlify.app/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // 2. Click Library in nav
    console.log('2. Clicking Library in navigation...');
    await page.getByRole('link', { name: 'Library' }).click();
    await page.waitForTimeout(2000);

    // 3. Log in
    console.log('3. Logging in...');
    await page.locator('input[type="email"]').fill('varun.ramesh08@gmail.com');
    await page.locator('input[type="password"]').fill('Ayesha27!');
    await page.getByRole('button', { name: /sign in/i }).click();
    await page.waitForTimeout(3000);

    // 4. Screenshot Library page
    console.log('4. Taking screenshot of Library page...');
    await page.screenshot({ path: path.join(chartsDir, 'v1_auth_library.png'), fullPage: false });

    // 5. Check for podcast items and click one if available
    console.log('5. Looking for podcast items...');
    const podcastCards = await page.locator('article, .card, [class*="podcast"], [class*="episode"]').count();
    console.log(`   Found ${podcastCards} potential podcast items`);

    if (podcastCards > 0) {
      console.log('   Clicking first podcast item...');
      await page.locator('article, .card, [class*="podcast"], [class*="episode"]').first().click();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: path.join(chartsDir, 'v1_auth_podcast_detail.png'), fullPage: false });

      // Check for episode summary
      const summaryVisible = await page.getByText(/summary|episode/i).count() > 0;
      if (summaryVisible) {
        console.log('   Taking screenshot of episode summary...');
        await page.screenshot({ path: path.join(chartsDir, 'v1_auth_episode_summary.png'), fullPage: true });
      }

      // Go back to library
      await page.goBack();
      await page.waitForTimeout(1000);
    }

    // 6. Navigate to Discover
    console.log('6. Navigating to Discover...');
    await page.getByRole('link', { name: 'Discover' }).click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(chartsDir, 'v1_auth_discover.png'), fullPage: false });

    // 7. Interact with Discover (search/browse)
    console.log('7. Looking for search or browse features...');
    const searchInput = await page.locator('input[type="search"]').count();
    if (searchInput > 0) {
      await page.locator('input[type="search"]').fill('technology');
      await page.waitForTimeout(2000);
      await page.screenshot({ path: path.join(chartsDir, 'v1_auth_discover_browse.png'), fullPage: false });
    } else {
      // Just scroll down to show more content
      await page.mouse.wheel(0, 500);
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.join(chartsDir, 'v1_auth_discover_browse.png'), fullPage: false });
    }

    // 8. Navigate to Settings
    console.log('8. Navigating to Settings...');
    await page.getByRole('link', { name: 'Settings' }).click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(chartsDir, 'v1_auth_settings.png'), fullPage: true });

    // 9. Click notification bell
    console.log('9. Clicking notification bell...');
    try {
      const notifBell = page.locator('[class*="notif"], [aria-label*="notif"], button:has(svg)').first();
      await notifBell.click({ timeout: 3000 });
      await page.waitForTimeout(2000);
      await page.screenshot({ path: path.join(chartsDir, 'v1_auth_notifications.png'), fullPage: false });
      await page.keyboard.press('Escape');
      await page.waitForTimeout(500);
    } catch (e) {
      console.log('   Could not find/click notification bell');
    }

    // 10. Click user/profile icon
    console.log('10. Clicking user/profile icon...');
    try {
      const profileIcon = page.locator('[class*="profile"], [class*="user"], [aria-label*="profile"], [aria-label*="user"]').first();
      await profileIcon.click({ timeout: 3000 });
      await page.waitForTimeout(2000);
      await page.screenshot({ path: path.join(chartsDir, 'v1_auth_profile.png'), fullPage: false });
      await page.keyboard.press('Escape');
      await page.waitForTimeout(500);
    } catch (e) {
      console.log('   Could not find/click profile icon');
    }

    // 11. Go back to Home while logged in
    console.log('11. Navigating back to Home...');
    await page.getByRole('link', { name: 'Home' }).click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(chartsDir, 'v1_auth_home.png'), fullPage: false });

    // 12. Scroll down on home to capture more content
    console.log('12. Scrolling down to capture more content...');
    await page.mouse.wheel(0, 800);
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(chartsDir, 'v1_auth_home_scrolled.png'), fullPage: false });

    console.log('\nScreenshot tour complete!');
    console.log(`All screenshots saved to: ${chartsDir}`);

  } catch (error) {
    console.error('Error during screenshot tour:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

takeScreenshotTour();
