#!/usr/bin/env python3
"""Take screenshot of GitHub repo."""

from playwright.sync_api import sync_playwright

def take_github_screenshot():
    """Navigate to GitHub repo and take a screenshot."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        try:
            print("Navigating to GitHub repo...")
            # Use 'load' instead of 'networkidle' for GitHub
            page.goto("https://github.com/varunr89/podcast_summarizer", wait_until='load', timeout=60000)

            # Wait for README to be visible
            page.wait_for_selector('article.markdown-body', timeout=10000)

            # Wait a bit for any lazy-loaded content
            page.wait_for_timeout(2000)

            # Take screenshot
            print("Taking screenshot...")
            page.screenshot(
                path="/Users/varunr/projects/short_projects/ai-tools-evolution/charts/v1_github_readme.png",
                full_page=True
            )

            title = page.title()
            print(f"SUCCESS - Page title: {title}")

            browser.close()
            return True

        except Exception as e:
            print(f"Error: {e}")
            browser.close()
            return False

if __name__ == "__main__":
    success = take_github_screenshot()
    exit(0 if success else 1)
