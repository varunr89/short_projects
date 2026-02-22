#!/usr/bin/env python3
"""
Comprehensive screenshot tour of the v1 podcast summarizer app.
Captures every screen, state, and interactive element.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os

def main():
    output_dir = "/Users/varunr/projects/short_projects/ai-tools-evolution/charts"
    os.makedirs(output_dir, exist_ok=True)

    base_url = "https://mindcastdaily.netlify.app/"

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        screenshots = []

        def take_screenshot(name, description, full_page=False):
            """Take a screenshot and record details"""
            path = os.path.join(output_dir, name)
            page.screenshot(path=path, full_page=full_page)
            screenshots.append({
                'name': name,
                'description': description,
                'path': path,
                'full_page': full_page
            })
            print(f"✓ Captured: {name}")
            time.sleep(0.5)

        def wait_for_load():
            """Wait for page to fully load"""
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
            except PlaywrightTimeoutError:
                page.wait_for_load_state('domcontentloaded')
            time.sleep(1)

        # Navigate to home page
        print(f"\n{'='*60}")
        print("STARTING COMPREHENSIVE SCREENSHOT TOUR")
        print(f"{'='*60}\n")

        print("1. HOME PAGE")
        page.goto(base_url)
        wait_for_load()
        take_screenshot('v1_screen_home.png', 'Home page - initial view', full_page=False)
        take_screenshot('v1_screen_home_full.png', 'Home page - full scrollable content', full_page=True)

        # Get page structure info
        print("\n   Analyzing home page structure...")
        try:
            # Check for nav items
            nav_items = page.locator('nav a, nav button').all_text_contents()
            print(f"   Navigation items: {nav_items}")
        except:
            pass

        # Click on notification bell if present
        print("\n2. NOTIFICATIONS")
        try:
            bell = page.locator('[aria-label*="otification"], .notification-bell, button:has-text("notification")').first
            if bell.is_visible(timeout=2000):
                bell.click()
                wait_for_load()
                take_screenshot('v1_screen_notifications.png', 'Notifications panel/page')
                # Close notification if it's a dropdown
                page.keyboard.press('Escape')
                time.sleep(0.5)
        except Exception as e:
            print(f"   No notification bell found or clickable: {e}")

        # Click on user profile icon
        print("\n3. USER PROFILE")
        try:
            # Try various selectors for user icon
            user_icon = page.locator('[aria-label*="ser"], [aria-label*="rofile"], .user-icon, .profile-icon, button:has-text("profile")').first
            if user_icon.is_visible(timeout=2000):
                user_icon.click()
                wait_for_load()
                take_screenshot('v1_screen_profile.png', 'User profile page/dropdown')
                # Go back if we navigated away
                if page.url != base_url:
                    page.goto(base_url)
                    wait_for_load()
                else:
                    page.keyboard.press('Escape')
                    time.sleep(0.5)
        except Exception as e:
            print(f"   No user icon found or clickable: {e}")

        # Navigate to Library
        print("\n4. LIBRARY PAGE")
        try:
            library_link = page.locator('nav a:has-text("Library"), nav button:has-text("Library"), a:has-text("Library")').first
            library_link.click()
            wait_for_load()
            take_screenshot('v1_screen_library.png', 'Library page - initial view')
            take_screenshot('v1_screen_library_full.png', 'Library page - full scrollable content', full_page=True)

            # Try clicking on first item in library
            try:
                first_item = page.locator('article, .card, .episode-card, .podcast-card, li').first
                if first_item.is_visible(timeout=2000):
                    first_item.click()
                    wait_for_load()
                    take_screenshot('v1_screen_library_detail.png', 'Library item detail view')
                    page.go_back()
                    wait_for_load()
            except Exception as e:
                print(f"   No clickable items in library: {e}")
        except Exception as e:
            print(f"   Could not navigate to Library: {e}")

        # Navigate to Discover
        print("\n5. DISCOVER PAGE")
        try:
            discover_link = page.locator('nav a:has-text("Discover"), nav button:has-text("Discover"), a:has-text("Discover")').first
            discover_link.click()
            wait_for_load()
            take_screenshot('v1_screen_discover.png', 'Discover page - initial view')
            take_screenshot('v1_screen_discover_full.png', 'Discover page - full scrollable content', full_page=True)

            # Try clicking on first discovered item
            try:
                first_item = page.locator('article, .card, .podcast-card, li').first
                if first_item.is_visible(timeout=2000):
                    first_item.click()
                    wait_for_load()
                    take_screenshot('v1_screen_discover_detail.png', 'Discovered item detail view')
                    page.go_back()
                    wait_for_load()
            except Exception as e:
                print(f"   No clickable items in discover: {e}")
        except Exception as e:
            print(f"   Could not navigate to Discover: {e}")

        # Navigate to Settings
        print("\n6. SETTINGS PAGE")
        try:
            settings_link = page.locator('nav a:has-text("Settings"), nav button:has-text("Settings"), a:has-text("Settings")').first
            settings_link.click()
            wait_for_load()
            take_screenshot('v1_screen_settings.png', 'Settings page - initial view')
            take_screenshot('v1_screen_settings_full.png', 'Settings page - full scrollable content', full_page=True)
        except Exception as e:
            print(f"   Could not navigate to Settings: {e}")

        # Go back to home to explore more
        print("\n7. EXPLORING INTERACTIVE ELEMENTS ON HOME")
        page.goto(base_url)
        wait_for_load()

        # Try to find and click episode cards
        try:
            episode_cards = page.locator('article, .episode-card, .card').all()
            if len(episode_cards) > 0:
                print(f"   Found {len(episode_cards)} cards on home page")
                # Click first episode card
                episode_cards[0].click()
                wait_for_load()
                take_screenshot('v1_screen_episode_detail.png', 'Episode detail page')
                take_screenshot('v1_screen_episode_detail_full.png', 'Episode detail - full page', full_page=True)
                page.go_back()
                wait_for_load()
        except Exception as e:
            print(f"   Could not explore episode cards: {e}")

        # Try to find podcast cards if different from episodes
        try:
            podcast_cards = page.locator('.podcast-card, [data-type="podcast"]').all()
            if len(podcast_cards) > 0:
                print(f"   Found {len(podcast_cards)} podcast cards")
                podcast_cards[0].click()
                wait_for_load()
                take_screenshot('v1_screen_podcast_detail.png', 'Podcast detail page')
                take_screenshot('v1_screen_podcast_detail_full.png', 'Podcast detail - full page', full_page=True)
        except Exception as e:
            print(f"   No separate podcast cards found: {e}")

        # Look for any modals or overlays
        print("\n8. CHECKING FOR MODALS/OVERLAYS")
        page.goto(base_url)
        wait_for_load()

        # Try to trigger search if present
        try:
            search = page.locator('input[type="search"], [placeholder*="earch"]').first
            if search.is_visible(timeout=2000):
                search.click()
                wait_for_load()
                take_screenshot('v1_screen_search_active.png', 'Search interface active')
                search.fill('podcast')
                wait_for_load()
                take_screenshot('v1_screen_search_results.png', 'Search with results')
        except Exception as e:
            print(f"   No search interface found: {e}")

        # Try to find and click any buttons (play, add, etc.)
        print("\n9. EXPLORING BUTTON STATES")
        page.goto(base_url)
        wait_for_load()

        try:
            play_button = page.locator('button:has-text("Play"), [aria-label*="Play"]').first
            if play_button.is_visible(timeout=2000):
                take_screenshot('v1_screen_before_play.png', 'Before clicking play button')
                play_button.click()
                wait_for_load()
                take_screenshot('v1_screen_playing.png', 'After clicking play button')
        except Exception as e:
            print(f"   No play button found: {e}")

        # Summary
        print(f"\n{'='*60}")
        print(f"TOUR COMPLETE - {len(screenshots)} screenshots captured")
        print(f"{'='*60}\n")

        for shot in screenshots:
            print(f"  • {shot['name']}")
            print(f"    {shot['description']}")
            if shot['full_page']:
                print(f"    (Full page capture)")
            print()

        browser.close()

if __name__ == '__main__':
    main()
