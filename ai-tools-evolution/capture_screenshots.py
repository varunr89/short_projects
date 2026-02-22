"""
Script to capture screenshots of podcast.bhavanaai.com for documentation
"""
from playwright.sync_api import sync_playwright
import time
import json

def main():
    results = {
        "pages": [],
        "magic_link_sent": False
    }

    with sync_playwright() as p:
        # Connect to existing Chrome instance
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        try:
            # Step 1: Navigate to landing page
            print("Navigating to https://podcast.bhavanaai.com...")
            page.goto("https://podcast.bhavanaai.com", wait_until="networkidle", timeout=30000)
            time.sleep(2)  # Wait for any animations

            # Capture landing page details
            landing_info = {
                "page": "landing",
                "url": page.url,
                "title": page.title(),
                "viewport": page.viewport_size
            }

            # Take screenshot
            page.screenshot(path="/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v2_screen_landing.png", full_page=True)
            print("✓ Saved landing page screenshot")

            # Gather detailed information about the page
            landing_details = page.evaluate("""() => {
                const getStyles = (el) => {
                    const styles = window.getComputedStyle(el);
                    return {
                        color: styles.color,
                        backgroundColor: styles.backgroundColor,
                        fontSize: styles.fontSize,
                        fontFamily: styles.fontFamily,
                        fontWeight: styles.fontWeight,
                        lineHeight: styles.lineHeight,
                        padding: styles.padding,
                        margin: styles.margin
                    };
                };

                return {
                    backgroundColor: window.getComputedStyle(document.body).backgroundColor,
                    headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                        tag: h.tagName,
                        text: h.textContent.trim(),
                        styles: getStyles(h)
                    })),
                    buttons: Array.from(document.querySelectorAll('button, a[role="button"], .btn')).map(btn => ({
                        text: btn.textContent.trim(),
                        type: btn.tagName,
                        styles: getStyles(btn)
                    })),
                    paragraphs: Array.from(document.querySelectorAll('p')).slice(0, 5).map(p => ({
                        text: p.textContent.trim().substring(0, 100),
                        styles: getStyles(p)
                    }))
                };
            }""")
            landing_info["details"] = landing_details
            results["pages"].append(landing_info)

            # Step 2: Click "Get Started" button
            print("\nLooking for 'Get Started' button...")
            get_started_selector = 'button:has-text("Get Started"), a:has-text("Get Started")'

            if page.locator(get_started_selector).count() > 0:
                print("Clicking 'Get Started'...")
                page.locator(get_started_selector).first.click()
                page.wait_for_load_state("networkidle", timeout=10000)
                time.sleep(2)

                # Step 3: Capture auth/login page
                auth_info = {
                    "page": "auth",
                    "url": page.url,
                    "title": page.title()
                }

                page.screenshot(path="/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v2_screen_auth.png", full_page=True)
                print("✓ Saved auth page screenshot")

                # Gather auth page details
                auth_details = page.evaluate("""() => {
                    const getStyles = (el) => {
                        const styles = window.getComputedStyle(el);
                        return {
                            color: styles.color,
                            backgroundColor: styles.backgroundColor,
                            fontSize: styles.fontSize,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            padding: styles.padding,
                            margin: styles.margin,
                            borderRadius: styles.borderRadius,
                            border: styles.border
                        };
                    };

                    return {
                        backgroundColor: window.getComputedStyle(document.body).backgroundColor,
                        headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                            tag: h.tagName,
                            text: h.textContent.trim(),
                            styles: getStyles(h)
                        })),
                        inputs: Array.from(document.querySelectorAll('input')).map(inp => ({
                            type: inp.type,
                            placeholder: inp.placeholder,
                            name: inp.name,
                            styles: getStyles(inp)
                        })),
                        buttons: Array.from(document.querySelectorAll('button')).map(btn => ({
                            text: btn.textContent.trim(),
                            styles: getStyles(btn)
                        })),
                        formText: Array.from(document.querySelectorAll('p, label, span')).map(el => ({
                            tag: el.tagName,
                            text: el.textContent.trim().substring(0, 100)
                        }))
                    };
                }""")
                auth_info["details"] = auth_details
                results["pages"].append(auth_info)

                # Step 4: Fill in email and click send magic link
                print("\nLooking for email input field...")
                email_input = page.locator('input[type="email"], input[name*="email"], input[placeholder*="email" i]').first

                if email_input.count() > 0:
                    print("Entering email address...")
                    email_input.fill("varun.rajput03@gmail.com")
                    time.sleep(1)

                    # Look for send button
                    send_button = page.locator('button:has-text("Send Magic Link"), button:has-text("Send"), button[type="submit"]').first

                    if send_button.count() > 0:
                        print("Clicking 'Send Magic Link' button...")
                        send_button.click()
                        time.sleep(3)  # Wait for confirmation page

                        # Step 5: Capture confirmation page
                        confirm_info = {
                            "page": "confirmation",
                            "url": page.url,
                            "title": page.title()
                        }

                        page.screenshot(path="/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v2_screen_magic_link_sent.png", full_page=True)
                        print("✓ Saved confirmation page screenshot")

                        # Gather confirmation page details
                        confirm_details = page.evaluate("""() => {
                            const getStyles = (el) => {
                                const styles = window.getComputedStyle(el);
                                return {
                                    color: styles.color,
                                    backgroundColor: styles.backgroundColor,
                                    fontSize: styles.fontSize,
                                    fontFamily: styles.fontFamily,
                                    textAlign: styles.textAlign
                                };
                            };

                            return {
                                backgroundColor: window.getComputedStyle(document.body).backgroundColor,
                                allText: document.body.textContent.trim(),
                                headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                                    tag: h.tagName,
                                    text: h.textContent.trim(),
                                    styles: getStyles(h)
                                })),
                                paragraphs: Array.from(document.querySelectorAll('p')).map(p => ({
                                    text: p.textContent.trim(),
                                    styles: getStyles(p)
                                }))
                            };
                        }""")
                        confirm_info["details"] = confirm_details
                        results["pages"].append(confirm_info)
                        results["magic_link_sent"] = True
                    else:
                        print("ERROR: Could not find 'Send Magic Link' button")
                else:
                    print("ERROR: Could not find email input field")
            else:
                print("ERROR: Could not find 'Get Started' button")

            # Save results to JSON
            with open("/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v2_page_details.json", "w") as f:
                json.dump(results, f, indent=2)

            print("\n✓ All screenshots captured and details saved to v2_page_details.json")
            print("\nNOTE: Browser context left open for potential continuation.")
            print("User should check email for magic link to continue authenticated tour.")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

        # Don't close browser/context - leave it open as requested
        print("\nBrowser context kept alive (not closing).")

if __name__ == "__main__":
    main()
