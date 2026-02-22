#!/usr/bin/env python3
"""
Enhanced v2 tour - capture missing screens and details.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os

def main():
    output_dir = "/Users/varunr/projects/short_projects/ai-tools-evolution/charts"
    magic_link = "https://podcast.bhavanaai.com/auth/verify?token=fYubTlAuxhBO6GzQIPUT4RpN-1TYyylUArv-vt4WADI"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        def screenshot(name, full_page=True):
            path = os.path.join(output_dir, name)
            page.screenshot(path=path, full_page=full_page)
            print(f"✓ {name}")
            time.sleep(0.5)

        def wait():
            try:
                page.wait_for_load_state('networkidle', timeout=8000)
            except:
                time.sleep(1.5)

        print("\n=== ENHANCED V2 TOUR ===\n")

        # Auth
        page.goto(magic_link)
        wait()

        # 1. Subscriptions page
        print("1. Subscriptions")
        try:
            page.click('a:has-text("Subscriptions")')
            wait()
            screenshot('v2_subscriptions.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 2. Account page
        print("2. Account")
        try:
            page.click('a:has-text("Account")')
            wait()
            screenshot('v2_account.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 3. Go to Channels and click on a specific channel
        print("3. Individual Channel Detail")
        try:
            page.goto('https://podcast.bhavanaai.com/channels')
            wait()
            
            # Click first channel
            channel_cards = page.locator('article, .card, li').all()
            if len(channel_cards) > 0:
                channel_cards[0].click()
                wait()
                screenshot('v2_channel_detail.png')
                
                # Try to see if there are episodes on this page
                episodes = page.locator('article, li, .episode').all()
                print(f"   Found {len(episodes)} potential episode elements")
                
                # Click first episode if visible
                if len(episodes) > 0:
                    try:
                        episodes[0].click()
                        wait()
                        screenshot('v2_episode_detail.png')
                    except:
                        print("   Could not click episode")
        except Exception as e:
            print(f"   Error: {e}")

        # 4. Admin Dashboard
        print("4. Admin - Dashboard")
        page.goto('https://podcast.bhavanaai.com/admin')
        wait()
        screenshot('v2_admin_dashboard.png')

        # 5. Admin - Users
        print("5. Admin - Users")
        try:
            page.click('a:has-text("Users")')
            wait()
            screenshot('v2_admin_users.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 6. Admin - Channels
        print("6. Admin - Channels")
        try:
            page.click('a:has-text("Channels")')
            wait()
            screenshot('v2_admin_channels.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 7. Admin - Requests
        print("7. Admin - Requests")
        try:
            page.click('a:has-text("Requests")')
            wait()
            screenshot('v2_admin_requests.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 8. Admin - Deliveries
        print("8. Admin - Deliveries")
        try:
            page.click('a:has-text("Deliveries")')
            wait()
            screenshot('v2_admin_deliveries.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 9. Admin - Episodes
        print("9. Admin - Episodes")
        try:
            page.click('a:has-text("Episodes")')
            wait()
            screenshot('v2_admin_episodes.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 10. Admin - YouTube Audio
        print("10. Admin - YouTube Audio")
        try:
            page.click('a:has-text("YouTube Audio")')
            wait()
            screenshot('v2_admin_youtube.png')
        except Exception as e:
            print(f"   Error: {e}")

        # 11. Click on an admin item for detail view
        print("11. Admin - Detail Views")
        try:
            # Go to users and click first user
            page.goto('https://podcast.bhavanaai.com/admin')
            page.click('a:has-text("Users")')
            wait()
            
            # Look for clickable user row
            rows = page.locator('tr, article, .card').all()
            if len(rows) > 1:
                rows[1].click()  # Skip header row
                wait()
                screenshot('v2_admin_user_detail.png')
        except Exception as e:
            print(f"   Error: {e}")

        print("\n=== ENHANCED TOUR COMPLETE ===\n")
        browser.close()

if __name__ == '__main__':
    main()
