#!/usr/bin/env python3
"""
Capture episode summary with longer waits
"""

from playwright.sync_api import sync_playwright
import time
import os

def main():
    output_dir = "/Users/varunr/projects/short_projects/ai-tools-evolution/charts"
    magic_link = "https://podcast.bhavanaai.com/auth/verify?token=fYubTlAuxhBO6GzQIPUT4RpN-1TYyylUArv-vt4WADI"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        def screenshot(name, full_page=True):
            path = os.path.join(output_dir, name)
            page.screenshot(path=path, full_page=full_page)
            print(f"✓ {name}")

        print("\n=== EPISODE CAPTURE ===\n")

        # Auth
        page.goto(magic_link)
        time.sleep(3)
        
        # Go to subscriptions (more likely to have episode links)
        page.goto('https://podcast.bhavanaai.com/subscriptions')
        time.sleep(3)
        screenshot('v2_subscriptions_full.png')
        
        # Click on first podcast
        print("1. Clicking first podcast in subscriptions")
        try:
            first_podcast = page.locator('article, .card, li').first
            first_podcast.click()
            time.sleep(4)  # Wait longer for content to load
            screenshot('v2_podcast_with_episodes.png')
            
            # Now try to click an episode
            print("2. Looking for episode to click")
            # Wait for content to load
            page.wait_for_selector('article, .episode, [role="article"]', timeout=5000)
            episodes = page.locator('article, .episode, [role="article"]').all()
            print(f"   Found {len(episodes)} potential episodes")
            
            if len(episodes) > 0:
                episodes[0].click()
                time.sleep(4)
                screenshot('v2_episode_summary_full.png')
                
                # Scroll through the summary
                for i in range(1, 4):
                    page.evaluate(f"window.scrollTo(0, {i * 600})")
                    time.sleep(1)
                    screenshot(f'v2_episode_summary_scroll_{i}.png', full_page=False)
                
        except Exception as e:
            print(f"   Error: {e}")

        print("\n=== DONE ===\n")
        input("Press Enter to close...")
        browser.close()

if __name__ == '__main__':
    main()
