import json
import random
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# --- SETTINGS ---
START_INDEX = 201    # inclusive
END_INDEX = 261      # inclusive
INPUT_FILE = "releases.json"
OUTPUT_FILE = f"metadata_{START_INDEX}_{END_INDEX}.json"

# Load releases
with open(INPUT_FILE, "r") as f:
    releases = json.load(f)

# Slice the batch
batch = releases[START_INDEX:END_INDEX+1]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for i, release in enumerate(batch, start=START_INDEX):
        url = release["link"]
        title = release["title"]

        print(f"[{i}] Fetching: {title} -> {url}")

        try:
            page.goto(url, timeout=60000)  # 60s timeout

            tralbum_data = page.evaluate("() => window.TralbumData")

            results.append({
                "title": title,
                "url": url,
                "tralbum": tralbum_data
            })

            # Random delay between 2–6 seconds
            delay = random.uniform(2, 6)
            print(f"   ✓ Done. Sleeping {delay:.1f}s...")
            time.sleep(delay)

        except Exception as e:
            print(f"   ✗ Error on {url}: {e}")

    browser.close()

# Save this batch
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved {len(results)} releases to {OUTPUT_FILE}")