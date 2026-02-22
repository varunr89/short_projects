#!/usr/bin/env python3
"""
Final captures - channel detail and episode summary pages
"""

from playwright.sync_api import sync_playwright
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
                time.sleep(2)

        print("\n=== FINAL V2 CAPTURES ===\n")

        # Auth and go to channels
        page.goto(magic_link)
        wait()
        page.goto('https://podcast.bhavanaai.com/channels')
        wait()
        
        # Take better channels list screenshot
        print("1. Channels List (Better View)")
        screenshot('v2_channels_list.png')
        
        # Click on first channel by finding actual link/button
        print("2. Click First Channel")
        try:
            # Try finding by text content or href
            links = page.locator('a').all()
            clicked = False
            for link in links[:50]:  # Check first 50 links
                try:
                    href = link.get_attribute('href')
                    if href and '/channels/' in href and href != '/channels':
                        print(f"   Clicking: {href}")
                        link.click()
                        wait()
                        clicked = True
                        break
                except:
                    continue
            
            if clicked:
                screenshot('v2_channel_page.png')
                print(f"   Current URL: {page.url}")
                
                # Look for episodes section on this page
                print("3. Looking for Episodes on Channel Page")
                
                # Try to find episode links
                episode_links = page.locator('a').all()
                episode_clicked = False
                for link in episode_links[:100]:
                    try:
                        href = link.get_attribute('href')
                        if href and '/episodes/' in href:
                            print(f"   Clicking episode: {href}")
                            link.click()
                            wait()
                            episode_clicked = True
                            break
                    except:
                        continue
                
                if episode_clicked:
                    screenshot('v2_episode_page.png')
                    print(f"   Episode URL: {page.url}")
                    
                    # Scroll down to see more of the summary
                    page.evaluate("window.scrollTo(0, 400)")
                    time.sleep(0.5)
                    screenshot('v2_episode_page_mid.png', full_page=False)
                    
                    page.evaluate("window.scrollTo(0, 800)")
                    time.sleep(0.5)
                    screenshot('v2_episode_page_bottom.png', full_page=False)
                    
                else:
                    print("   No episode links found")
        except Exception as e:
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()

        print("\n=== FINAL CAPTURES COMPLETE ===\n")
        browser.close()

if __name__ == '__main__':
    main()
