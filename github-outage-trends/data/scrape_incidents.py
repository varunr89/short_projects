#!/usr/bin/env python3
"""
Scrape all GitHub incident history from githubstatus.com/history.

Iterates through paginated history pages (each covering ~3 months) and
extracts incident title, impact level, date range, body, and link.
Outputs a CSV with one row per incident.
"""

import csv
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.githubstatus.com/history?page={}"
OUTPUT = Path(__file__).parent / "github_incidents_raw.csv"
MAX_PAGES = 50  # safety limit; will stop early if a page has no incidents


def parse_date_range(date_text: str) -> tuple[str, str]:
    """Parse date text like 'Feb 9, 19:01 - 20:09 UTC' into start/end strings."""
    if not date_text:
        return ("", "")
    # Remove UTC suffix
    date_text = date_text.replace(" UTC", "").strip()
    parts = date_text.split(" - ")
    start = parts[0].strip()
    end = parts[1].strip() if len(parts) > 1 else ""
    return (start, end)


def scrape_page(page, page_num: int) -> list[dict]:
    """Scrape a single history page and return list of incident dicts."""
    url = BASE_URL.format(page_num)
    page.goto(url, wait_until="networkidle")

    try:
        page.wait_for_selector(".incident-title", timeout=8000)
    except Exception:
        # No incidents on this page -- we've gone past the last page
        return []

    # Click all "Show All X Incidents" expand buttons to reveal hidden incidents
    expand_buttons = page.query_selector_all(".expand-incidents")
    for btn in expand_buttons:
        btn.click()
    if expand_buttons:
        time.sleep(0.5)  # wait for expansion

    data = page.evaluate('''() => {
        const months = document.querySelectorAll(".month");
        const results = [];
        months.forEach(month => {
            const monthLabel = month.querySelector("h4, .month-label")?.textContent?.trim() || "";
            const incidents = month.querySelectorAll(".incident-container");
            incidents.forEach(inc => {
                const titleEl = inc.querySelector(".incident-title");
                const title = titleEl?.textContent?.trim() || "";
                const link = titleEl?.href || "";
                const impact = [...(titleEl?.classList || [])].find(c => c.startsWith("impact-")) || "";
                const body = inc.querySelector(".incident-body")?.textContent?.trim() || "";
                const dateText = inc.querySelector(".secondary")?.textContent?.trim() || "";
                results.push({monthLabel, title, link, impact, body, dateText});
            });
        });
        return results;
    }''')

    return data


def main():
    all_incidents = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for page_num in range(1, MAX_PAGES + 1):
            print(f"Scraping page {page_num}...", end=" ", flush=True)
            incidents = scrape_page(page, page_num)

            if not incidents:
                print("no incidents found, stopping.")
                break

            all_incidents.extend(incidents)
            print(f"{len(incidents)} incidents")
            time.sleep(0.5)  # polite delay

        browser.close()

    print(f"\nTotal incidents scraped: {len(all_incidents)}")

    # Write CSV
    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "month", "title", "impact", "date_text", "body", "link"
        ])
        writer.writeheader()
        for inc in all_incidents:
            writer.writerow({
                "month": inc["monthLabel"].replace("\xa0", " "),
                "title": inc["title"],
                "impact": inc["impact"].replace("impact-", ""),
                "date_text": inc["dateText"],
                "body": inc["body"],
                "link": inc["link"],
            })

    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    main()
