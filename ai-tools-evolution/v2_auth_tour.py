#!/usr/bin/env python3
"""
Comprehensive screenshot tour of the v2 podcast summarizer app (authenticated).
Uses magic link to authenticate and capture every screen, state, and feature.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os
import json

def main():
    output_dir = "/Users/varunr/projects/short_projects/ai-tools-evolution/charts"
    os.makedirs(output_dir, exist_ok=True)

    magic_link = "https://podcast.bhavanaai.com/auth/verify?token=fYubTlAuxhBO6GzQIPUT4RpN-1TYyylUArv-vt4WADI"

    with sync_playwright() as p:
        # Launch browser in non-headless mode to see what's happening
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        screenshots = []

        def take_screenshot(name, description, full_page=False, wait_after=0.5):
            """Take a screenshot and record details"""
            path = os.path.join(output_dir, name)
            page.screenshot(path=path, full_page=full_page)
            screenshots.append({
                'name': name,
                'description': description,
                'path': path,
                'url': page.url,
                'full_page': full_page
            })
            print(f"✓ Captured: {name}")
            time.sleep(wait_after)

        def wait_for_load(timeout=10000):
            """Wait for page to fully load"""
            try:
                page.wait_for_load_state('networkidle', timeout=timeout)
            except PlaywrightTimeoutError:
                page.wait_for_load_state('domcontentloaded', timeout=5000)
            time.sleep(1)

        def safe_click(selector, description, timeout=3000):
            """Safely click an element with error handling"""
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=timeout):
                    element.click()
                    wait_for_load()
                    return True
                else:
                    print(f"   Element not visible: {description}")
                    return False
            except Exception as e:
                print(f"   Could not click {description}: {e}")
                return False

        # ===== START TOUR =====
        print(f"\n{'='*70}")
        print("V2 PODCAST SUMMARIZER - AUTHENTICATED SCREENSHOT TOUR")
        print(f"{'='*70}\n")

        # 1. Navigate to magic link and authenticate
        print("1. AUTHENTICATION")
        print(f"   Navigating to magic link...")
        page.goto(magic_link)
        wait_for_load()
        print(f"   Current URL: {page.url}")
        
        # Wait for auth to complete and redirect
        time.sleep(3)
        take_screenshot('v2_auth_dashboard.png', 'Landing page after authentication', full_page=True)

        # Get page title and basic info
        title = page.title()
        print(f"   Page title: {title}")

        # 2. Analyze main navigation structure
        print("\n2. NAVIGATION STRUCTURE")
        try:
            # Look for all navigation links
            nav_links = page.locator('nav a, nav button, [role="navigation"] a, [role="navigation"] button').all()
            print(f"   Found {len(nav_links)} navigation elements")
            
            # Get text content of nav items
            nav_texts = []
            for link in nav_links[:10]:  # First 10 to avoid overwhelming output
                try:
                    text = link.text_content()
                    if text and text.strip():
                        nav_texts.append(text.strip())
                except:
                    pass
            print(f"   Navigation items: {nav_texts}")
        except Exception as e:
            print(f"   Could not analyze navigation: {e}")

        # 3. Channels/Podcasts page
        print("\n3. CHANNELS PAGE")
        # Try multiple ways to get to channels
        channels_found = False
        for selector in [
            'a[href*="channel"]',
            'a:has-text("Channels")',
            'button:has-text("Channels")',
            'nav a:has-text("Channel")',
        ]:
            if safe_click(selector, "Channels link"):
                channels_found = True
                take_screenshot('v2_auth_channels.png', 'Channels/podcasts list page', full_page=True)
                break
        
        if not channels_found:
            print("   Channels page not found, staying on current page")

        # 4. Click on first podcast/channel
        print("\n4. PODCAST DETAIL PAGE")
        try:
            # Try various selectors for podcast items
            podcast_selectors = [
                'article:first-child',
                '.card:first-child',
                '[role="article"]:first-child',
                'a[href*="podcast"]:first-child',
                'a[href*="channel"]:first-child',
                'li:first-child a',
            ]
            
            clicked = False
            for selector in podcast_selectors:
                try:
                    elem = page.locator(selector).first
                    if elem.is_visible(timeout=2000):
                        elem.click()
                        wait_for_load()
                        clicked = True
                        take_screenshot('v2_auth_podcast_detail.png', 'Individual podcast/channel detail page', full_page=True)
                        break
                except:
                    continue
            
            if not clicked:
                print("   Could not find clickable podcast item")
        except Exception as e:
            print(f"   Error navigating to podcast: {e}")

        # 5. Episodes list
        print("\n5. EPISODES LIST")
        try:
            # Look for episode listings
            episode_selectors = [
                'article',
                '.episode',
                'li a[href*="episode"]',
                '[role="article"]',
            ]
            
            episode_found = False
            for selector in episode_selectors:
                try:
                    episodes = page.locator(selector).all()
                    if len(episodes) > 0:
                        print(f"   Found {len(episodes)} episodes")
                        take_screenshot('v2_auth_episodes.png', 'Episodes list view', full_page=True)
                        
                        # Click first episode
                        episodes[0].click()
                        wait_for_load()
                        episode_found = True
                        break
                except:
                    continue
            
            if not episode_found:
                print("   No episodes found")
        except Exception as e:
            print(f"   Error finding episodes: {e}")

        # 6. Episode summary page
        print("\n6. EPISODE SUMMARY")
        take_screenshot('v2_auth_summary.png', 'Full episode summary page', full_page=True)
        
        # Try to scroll to see more of summary
        try:
            page.evaluate("window.scrollTo(0, 500)")
            time.sleep(0.5)
            take_screenshot('v2_auth_summary_scrolled.png', 'Episode summary scrolled view', full_page=False)
        except:
            pass

        # 7. Look for email preview
        print("\n7. EMAIL PREVIEW")
        for selector in [
            'button:has-text("Email")',
            'button:has-text("Preview")',
            'a:has-text("Email")',
            '[aria-label*="email"]',
        ]:
            if safe_click(selector, "Email preview button"):
                take_screenshot('v2_auth_email_preview.png', 'Email preview modal/page', full_page=True)
                page.keyboard.press('Escape')
                time.sleep(0.5)
                break

        # 8. Navigate to main dashboard/home
        print("\n8. DASHBOARD/HOME")
        try:
            # Try to go home
            for selector in ['a[href="/"]', 'a:has-text("Home")', 'a:has-text("Dashboard")']:
                if safe_click(selector, "Home/Dashboard link"):
                    take_screenshot('v2_auth_home.png', 'Main dashboard/home page', full_page=True)
                    break
        except Exception as e:
            print(f"   Could not navigate home: {e}")

        # 9. Settings page
        print("\n9. SETTINGS")
        for selector in [
            'a[href*="settings"]',
            'button:has-text("Settings")',
            'a:has-text("Settings")',
            '[aria-label*="settings"]',
        ]:
            if safe_click(selector, "Settings link"):
                take_screenshot('v2_auth_settings.png', 'Settings page', full_page=True)
                break

        # 10. Admin page
        print("\n10. ADMIN FEATURES")
        for selector in [
            'a[href*="admin"]',
            'button:has-text("Admin")',
            'a:has-text("Admin")',
        ]:
            if safe_click(selector, "Admin link"):
                take_screenshot('v2_auth_admin.png', 'Admin page', full_page=True)
                break

        # 11. Add/Subscribe functionality
        print("\n11. ADD CHANNEL")
        for selector in [
            'button:has-text("Add")',
            'button:has-text("Subscribe")',
            'button:has-text("New")',
            'a:has-text("Add")',
        ]:
            if safe_click(selector, "Add channel button"):
                take_screenshot('v2_auth_add_channel.png', 'Add channel modal/page', full_page=True)
                page.keyboard.press('Escape')
                time.sleep(0.5)
                break

        # 12. Validation/Testing features
        print("\n12. VALIDATION/TESTING")
        for selector in [
            'a[href*="validation"]',
            'a[href*="test"]',
            'button:has-text("Validation")',
            'button:has-text("Test")',
        ]:
            if safe_click(selector, "Validation/test link"):
                take_screenshot('v2_auth_validation.png', 'Validation/testing page', full_page=True)
                break

        # 13. Search functionality
        print("\n13. SEARCH")
        try:
            search = page.locator('input[type="search"], input[placeholder*="earch"]').first
            if search.is_visible(timeout=2000):
                search.click()
                time.sleep(0.5)
                take_screenshot('v2_auth_search_empty.png', 'Search interface empty')
                search.fill('test')
                wait_for_load()
                take_screenshot('v2_auth_search_results.png', 'Search with query')
        except Exception as e:
            print(f"   Search not found: {e}")

        # 14. User profile/account
        print("\n14. USER PROFILE")
        for selector in [
            'button[aria-label*="rofile"]',
            'button[aria-label*="ser"]',
            '.user-icon',
            '.profile-icon',
        ]:
            if safe_click(selector, "User profile button"):
                take_screenshot('v2_auth_profile_menu.png', 'User profile dropdown/menu')
                page.keyboard.press('Escape')
                time.sleep(0.5)
                break

        # 15. Try to find any additional unique features
        print("\n15. EXPLORING ADDITIONAL FEATURES")
        # Take one final screenshot of current state
        take_screenshot('v2_auth_final_state.png', 'Final application state', full_page=True)

        # ===== SUMMARY =====
        print(f"\n{'='*70}")
        print(f"TOUR COMPLETE - {len(screenshots)} screenshots captured")
        print(f"{'='*70}\n")

        # Save manifest
        manifest_path = os.path.join(output_dir, 'v2_screenshot_manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(screenshots, f, indent=2)
        print(f"Manifest saved: {manifest_path}\n")

        # Print summary
        for shot in screenshots:
            print(f"  • {shot['name']}")
            print(f"    {shot['description']}")
            print(f"    URL: {shot['url']}")
            if shot['full_page']:
                print(f"    (Full page capture)")
            print()

        # Keep browser open for manual exploration
        print("\nBrowser will stay open for manual exploration...")
        print("Press Enter when done to close browser...")
        input()

        browser.close()

if __name__ == '__main__':
    main()
