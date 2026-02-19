#!/usr/bin/env python3
"""
Download all Words of Brandon entries from Arcanum API.
Features:
- Random jitter (60-120s between requests)
- Rotating User-Agents
- Exponential backoff on failures
- Checkpoint/resume capability
- Quits after 1 hour of continuous failures
"""

import gzip
import json
import os
import random
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path

# Config
BASE_URL = "https://wob.coppermind.net/api/entry/"
DATA_DIR = Path("/home/moltbot/clawd/data")
ENTRIES_FILE = DATA_DIR / "wob_entries.json"
CHECKPOINT_FILE = DATA_DIR / "wob_checkpoint.json"
LOG_FILE = DATA_DIR / "wob_download.log"

MIN_DELAY = 60
MAX_DELAY = 120
MAX_CONTINUOUS_FAILURE_SECONDS = 3600  # 1 hour

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
]

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"last_page": 0, "total_entries": 0, "total_pages": None}

def save_checkpoint(checkpoint: dict):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f)

def load_entries() -> list:
    if ENTRIES_FILE.exists():
        with open(ENTRIES_FILE) as f:
            return json.load(f)
    return []

def save_entries(entries: list):
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f)

def fetch_page(page: int) -> dict | None:
    url = f"{BASE_URL}?page={page}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.9", "en;q=0.8"]),
        "Connection": "keep-alive",
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            return json.loads(data.decode("utf-8"))
    except Exception as e:
        raise e

def main():
    log("Starting WoB download...")
    
    checkpoint = load_checkpoint()
    entries = load_entries()
    
    current_page = checkpoint["last_page"] + 1
    total_pages = checkpoint.get("total_pages")
    
    log(f"Resuming from page {current_page}, {len(entries)} entries already saved")
    
    first_failure_time = None
    backoff = 1
    
    while True:
        try:
            log(f"Fetching page {current_page}...")
            data = fetch_page(current_page)
            
            # Reset failure tracking on success
            first_failure_time = None
            backoff = 1
            
            # Calculate total pages from first response
            if total_pages is None:
                count = data["count"]
                page_size = len(data["results"])
                total_pages = (count + page_size - 1) // page_size
                log(f"Total entries: {count}, estimated pages: {total_pages}")
            
            # Append new entries
            entries.extend(data["results"])
            
            # Save checkpoint
            checkpoint = {
                "last_page": current_page,
                "total_entries": len(entries),
                "total_pages": total_pages,
            }
            save_checkpoint(checkpoint)
            save_entries(entries)
            
            log(f"Page {current_page}/{total_pages} done. Total entries: {len(entries)}")
            
            # Check if we're done
            if data["next"] is None:
                log(f"Download complete! {len(entries)} entries saved to {ENTRIES_FILE}")
                break
            
            current_page += 1
            
            # Random jitter
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            log(f"Sleeping {delay:.1f}s...")
            time.sleep(delay)
            
        except Exception as e:
            log(f"Error on page {current_page}: {e}")
            
            # Track continuous failure time
            if first_failure_time is None:
                first_failure_time = datetime.now()
            
            # Check if we've been failing for too long
            failure_duration = (datetime.now() - first_failure_time).total_seconds()
            if failure_duration >= MAX_CONTINUOUS_FAILURE_SECONDS:
                log(f"QUIT: Continuous failures for {failure_duration/60:.1f} minutes. Giving up.")
                log(f"Progress saved: {len(entries)} entries, last successful page: {checkpoint['last_page']}")
                break
            
            # Exponential backoff
            sleep_time = min(backoff * 30, 600)  # Max 10 minutes
            log(f"Backing off {sleep_time}s (attempt backoff: {backoff})")
            time.sleep(sleep_time)
            backoff *= 2

if __name__ == "__main__":
    main()
