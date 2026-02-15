#!/usr/bin/env python3
"""
Clean and parse raw incident data into a structured CSV with proper dates,
durations, and categorized impact/component fields.
"""

import csv
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

INPUT = Path(__file__).parent / "github_incidents_raw.csv"
OUTPUT = Path(__file__).parent / "github_incidents_clean.csv"


def parse_date_text(date_text: str, month_str: str) -> Tuple[Optional[datetime], Optional[datetime], Optional[float]]:
    """
    Parse date_text like 'Feb 9, 19:01 - 20:09 UTC' or 'Feb 9, 19:01 - Feb 10, 02:30 UTC'
    using the month field (e.g. 'February 2026') for year context.

    Returns (start_dt, end_dt, duration_minutes).
    """
    if not date_text:
        return (None, None, None)

    # Extract year from month column
    year_match = re.search(r'(\d{4})', month_str)
    year = int(year_match.group(1)) if year_match else 2026

    date_text = date_text.replace("\xa0", " ").replace(" UTC", "").strip()

    # Split on ' - ' to get start and end
    parts = [p.strip() for p in date_text.split(" - ")]

    def parse_single(s: str, ref_year: int) -> Optional[datetime]:
        """Parse a single date/time string."""
        # Formats: 'Feb 9, 19:01' or 'Feb 9' or '19:01'
        formats = [
            ("%b %d, %H:%M", True),
            ("%b %d, %Y, %H:%M", False),
            ("%b %d", True),
        ]
        for fmt, needs_year in formats:
            try:
                dt = datetime.strptime(s, fmt)
                if needs_year:
                    dt = dt.replace(year=ref_year)
                return dt
            except ValueError:
                continue

        # Try just time (HH:MM) -- inherit date from start
        time_match = re.match(r'^(\d{1,2}):(\d{2})$', s)
        if time_match:
            return None  # will be handled by caller
        return None

    start_dt = parse_single(parts[0], year)
    end_dt = None
    duration = None

    if len(parts) > 1:
        end_dt = parse_single(parts[1], year)
        # If end is just a time, inherit date from start
        if end_dt is None and start_dt is not None:
            time_match = re.match(r'^(\d{1,2}):(\d{2})$', parts[1])
            if time_match:
                end_dt = start_dt.replace(
                    hour=int(time_match.group(1)),
                    minute=int(time_match.group(2))
                )
                # Handle overnight: if end < start, it rolled past midnight
                if end_dt < start_dt:
                    end_dt += timedelta(days=1)

    if start_dt and end_dt:
        duration = (end_dt - start_dt).total_seconds() / 60.0

    return (start_dt, end_dt, duration)


def categorize_component(title: str, body: str) -> str:
    """Categorize the incident by affected component based on title and body text."""
    text = (title + " " + body).lower()

    if "actions" in text or "workflow" in text or "runner" in text:
        return "Actions"
    if "copilot" in text:
        return "Copilot"
    if "codespaces" in text:
        return "Codespaces"
    if "pages" in text and "github pages" in text:
        return "Pages"
    if "pull request" in text:
        return "Pull Requests"
    if "git operations" in text or "git operation" in text:
        return "Git Operations"
    if "api" in text and ("rest" in text or "graphql" in text):
        return "API"
    if "packages" in text or "npm" in text or "container registry" in text:
        return "Packages"
    if "webhook" in text:
        return "Webhooks"
    if "dependabot" in text:
        return "Dependabot"
    if "issues" in text:
        return "Issues"
    if "notifications" in text:
        return "Notifications"
    if "authentication" in text or "login" in text or "sso" in text:
        return "Authentication"
    return "General"


def main():
    with open(INPUT) as f:
        rows = list(csv.DictReader(f))

    cleaned = []
    for row in rows:
        start_dt, end_dt, duration = parse_date_text(row["date_text"], row["month"])
        component = categorize_component(row["title"], row["body"])

        cleaned.append({
            "title": row["title"],
            "impact": row["impact"],
            "component": component,
            "start_date": start_dt.strftime("%Y-%m-%d %H:%M") if start_dt else "",
            "end_date": end_dt.strftime("%Y-%m-%d %H:%M") if end_dt else "",
            "duration_minutes": f"{duration:.0f}" if duration is not None else "",
            "year": start_dt.year if start_dt else "",
            "month_num": start_dt.month if start_dt else "",
            "date_text_raw": row["date_text"],
            "body": row["body"],
            "link": row["link"],
        })

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cleaned[0].keys())
        writer.writeheader()
        writer.writerows(cleaned)

    print(f"Cleaned {len(cleaned)} incidents -> {OUTPUT}")

    # Quick stats
    with_duration = [r for r in cleaned if r["duration_minutes"]]
    print(f"  With parseable duration: {len(with_duration)}")
    impacts = {}
    for r in cleaned:
        impacts[r["impact"]] = impacts.get(r["impact"], 0) + 1
    print(f"  Impact breakdown: {impacts}")


if __name__ == "__main__":
    main()
