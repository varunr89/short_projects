#!/usr/bin/env python3
"""Take screenshots of the v1 podcast summarizer app."""

from playwright.sync_api import sync_playwright
import sys

def take_screenshot(url, output_path):
    """Navigate to URL and take a full-page screenshot."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        try:
            print(f"Navigating to {url}...")
            page.goto(url, wait_until='networkidle', timeout=30000)

            # Wait a bit for any dynamic content
            page.wait_for_timeout(2000)

            # Take screenshot
            print(f"Taking screenshot and saving to {output_path}...")
            page.screenshot(path=output_path, full_page=True)

            # Get page title and basic info
            title = page.title()
            print(f"Page title: {title}")

            browser.close()
            return True, title

        except Exception as e:
            print(f"Error: {e}")
            browser.close()
            return False, str(e)

if __name__ == "__main__":
    # Screenshot 1: The live app
    success1, info1 = take_screenshot(
        "https://mindcastdaily.netlify.app/",
        "/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v1_app_live.png"
    )

    # Screenshot 2: The GitHub repo
    success2, info2 = take_screenshot(
        "https://github.com/varunr89/podcast_summarizer",
        "/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v1_github_readme.png"
    )

    print("\n=== RESULTS ===")
    print(f"Live app: {'SUCCESS' if success1 else 'FAILED'} - {info1}")
    print(f"GitHub repo: {'SUCCESS' if success2 else 'FAILED'} - {info2}")
