#!/usr/bin/env python3
"""
Enhanced screenshot tour that explores the public-facing pages more thoroughly.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os

def main():
    output_dir = "/Users/varunr/projects/short_projects/ai-tools-evolution/charts"
    os.makedirs(output_dir, exist_ok=True)

    base_url = "https://mindcastdaily.netlify.app/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        def take_screenshot(name, description, full_page=False):
            """Take a screenshot and record details"""
            path = os.path.join(output_dir, name)
            page.screenshot(path=path, full_page=full_page)
            print(f"✓ {name}")
            time.sleep(0.3)
            return path

        def wait_for_load():
            """Wait for page to fully load"""
            try:
                page.wait_for_load_state('networkidle', timeout=5000)
            except:
                pass
            time.sleep(0.5)

        print("\n" + "="*70)
        print("ENHANCED SCREENSHOT TOUR - V1 PODCAST SUMMARIZER")
        print("="*70 + "\n")

        # 1. Home page - landing view
        print("1. HOME PAGE (Landing)")
        page.goto(base_url)
        wait_for_load()
        take_screenshot('v1_home_landing.png', 'Landing page - hero section', full_page=False)
        take_screenshot('v1_home_landing_full.png', 'Landing page - full scroll', full_page=True)

        # Try to scroll through the home page
        print("\n2. HOME PAGE SECTIONS")
        try:
            page.mouse.wheel(0, 500)
            time.sleep(0.5)
            take_screenshot('v1_home_features.png', 'Home page - features section')

            page.mouse.wheel(0, 500)
            time.sleep(0.5)
            take_screenshot('v1_home_cta.png', 'Home page - CTA section')
        except:
            pass

        # Click Get Started to see if there's a signup flow
        print("\n3. GET STARTED FLOW")
        page.goto(base_url)
        wait_for_load()
        try:
            get_started = page.locator('button:has-text("Get Started"), a:has-text("Get Started")').first
            if get_started.is_visible(timeout=2000):
                get_started.click()
                wait_for_load()
                take_screenshot('v1_signup_flow.png', 'Signup/onboarding flow')
        except Exception as e:
            print(f"   Could not trigger Get Started: {e}")

        # Click notification bell
        print("\n4. NOTIFICATION BELL")
        page.goto(base_url)
        wait_for_load()
        try:
            bell = page.locator('[aria-label*="notification"], button:has-text("notification"), .notification').first
            if bell.is_visible(timeout=1000):
                take_screenshot('v1_notification_before.png', 'Before clicking notification bell')
                bell.click()
                wait_for_load()
                take_screenshot('v1_notification_dropdown.png', 'Notification dropdown/panel')
        except Exception as e:
            print(f"   Notification bell not accessible: {e}")

        # Click user profile icon
        print("\n5. USER PROFILE MENU")
        page.goto(base_url)
        wait_for_load()
        try:
            # Try to find and click the user icon
            user_selectors = [
                'button[aria-label*="ser"]',
                'button[aria-label*="rofile"]',
                '.user-icon',
                '.profile-icon',
                'svg[data-icon*="user"]',
                'button:has(svg)',
            ]

            for selector in user_selectors:
                try:
                    user_icon = page.locator(selector).last  # Often profile is last button in nav
                    if user_icon.is_visible(timeout=1000):
                        take_screenshot('v1_profile_before.png', 'Before clicking profile icon')
                        user_icon.click()
                        wait_for_load()
                        take_screenshot('v1_profile_dropdown.png', 'Profile dropdown menu')

                        # Check if there's a Settings option in the dropdown
                        try:
                            settings_in_dropdown = page.locator('a:has-text("Settings"), button:has-text("Settings")').first
                            if settings_in_dropdown.is_visible(timeout=1000):
                                settings_in_dropdown.click()
                                wait_for_load()
                                take_screenshot('v1_settings_from_dropdown.png', 'Settings page from dropdown')
                        except:
                            pass
                        break
                except:
                    continue
        except Exception as e:
            print(f"   Could not access profile menu: {e}")

        # Navigate to each main section
        print("\n6. LIBRARY PAGE")
        page.goto(base_url)
        wait_for_load()
        try:
            lib_link = page.locator('a:has-text("Library"), button:has-text("Library")').first
            if lib_link.is_visible(timeout=2000):
                lib_link.click()
                wait_for_load()
                take_screenshot('v1_library_signin.png', 'Library page (sign-in required)')
                take_screenshot('v1_library_signin_full.png', 'Library page - full view', full_page=True)
        except Exception as e:
            print(f"   Could not navigate to Library: {e}")

        print("\n7. DISCOVER PAGE")
        page.goto(base_url)
        wait_for_load()
        try:
            disc_link = page.locator('a:has-text("Discover"), button:has-text("Discover")').first
            if disc_link.is_visible(timeout=2000):
                disc_link.click()
                wait_for_load()
                take_screenshot('v1_discover_signin.png', 'Discover page (sign-in required)')
                take_screenshot('v1_discover_signin_full.png', 'Discover page - full view', full_page=True)
        except Exception as e:
            print(f"   Could not navigate to Discover: {e}")

        print("\n8. SETTINGS PAGE")
        page.goto(base_url)
        wait_for_load()
        try:
            settings_link = page.locator('a:has-text("Settings"), button:has-text("Settings")').first
            if settings_link.is_visible(timeout=2000):
                settings_link.click()
                wait_for_load()
                take_screenshot('v1_settings_signin.png', 'Settings page (sign-in required)')
                take_screenshot('v1_settings_signin_full.png', 'Settings page - full view', full_page=True)
        except Exception as e:
            print(f"   Could not navigate to Settings: {e}")

        # Try to interact with the sign-in form
        print("\n9. SIGN-IN FORM DETAILS")
        page.goto(base_url + "library")
        wait_for_load()
        take_screenshot('v1_signin_form.png', 'Sign-in form details')

        # Check for password visibility toggle
        try:
            eye_icon = page.locator('button:has(svg), [type="button"]').filter(has=page.locator('svg')).last
            if eye_icon.is_visible(timeout=1000):
                take_screenshot('v1_signin_before_toggle.png', 'Before password visibility toggle')
                eye_icon.click()
                time.sleep(0.3)
                take_screenshot('v1_signin_after_toggle.png', 'After password visibility toggle')
        except:
            pass

        # Mobile responsiveness - resize viewport
        print("\n10. MOBILE VIEW")
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(base_url)
        wait_for_load()
        take_screenshot('v1_mobile_home.png', 'Mobile view - home page')
        take_screenshot('v1_mobile_home_full.png', 'Mobile view - home full scroll', full_page=True)

        # Check for mobile menu
        try:
            mobile_menu = page.locator('button[aria-label*="menu"], .hamburger, button:has-text("Menu")').first
            if mobile_menu.is_visible(timeout=1000):
                mobile_menu.click()
                wait_for_load()
                take_screenshot('v1_mobile_menu.png', 'Mobile navigation menu')
        except:
            print("   No mobile menu found")

        # Tablet view
        print("\n11. TABLET VIEW")
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(base_url)
        wait_for_load()
        take_screenshot('v1_tablet_home.png', 'Tablet view - home page')

        # Back to desktop
        page.set_viewport_size({"width": 1280, "height": 900})

        # Check page structure
        print("\n12. PAGE ANALYSIS")
        page.goto(base_url)
        wait_for_load()

        # Get all interactive elements
        try:
            buttons = page.locator('button').count()
            links = page.locator('a').count()
            inputs = page.locator('input').count()
            print(f"   Interactive elements: {buttons} buttons, {links} links, {inputs} inputs")
        except:
            pass

        print("\n" + "="*70)
        print("TOUR COMPLETE")
        print("="*70)

        browser.close()

if __name__ == '__main__':
    main()
