import json
import time
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
import random


INPUT = "all_metadata_updated.json"
FAILURES_FILE = "downloadFailures.json"
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)
startindex = 26  # inclusive
endindex = 26  # inclusive
downloadWait = 1000*700  # 30 or more secoonds

# sanitize titles for filenames
def safe_filename(name):
    return re.sub(r"[^a-zA-Z0-9-_]+", "_", name).strip("_")

def run_batch(start, end):
    with open(INPUT, "r", encoding="utf-8") as f:
        releases = json.load(f)

    failures = []
    successes = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True once you trust it
        page = browser.new_page()

        for i in range(start, end + 1):
            r = releases[i]
            tr = r.get("tralbum", {})
            free_url = tr.get("freeDownloadPage")
            title = r.get("title", f"release_{i}")

            if not free_url:
                print(f"[{i}] Skipping {title} (no freeDownloadPage)")
                continue

            print(f"[{i}] Downloading {title}...")

            try:
                page.goto(free_url, timeout=60000)

                #Handle cookie banner if present
                try:
                    # Wait briefly, but don't fail if it's not there
                    accept_button = page.locator("text='Accept all'")
                    necessary_button = page.locator("text='Accept necessary only'")
                    
                    if accept_button.is_visible():
                        print("   🍪 Accepting cookies")
                        accept_button.click()
                        page.wait_for_timeout(1000)  # small pause to let banner dismiss
                    elif necessary_button.is_visible():
                        print("   🍪 Clicking 'Only necessary'")
                        necessary_button.click()
                        page.wait_for_timeout(1000)

                except Exception as e:
                    print("   (No cookie banner found)")

                # Select WAV in the format dropdown
                page.select_option("#format-type", "wav")

                # Wait up to 30s (or what you set at top) for the download link to appear
                page.wait_for_selector("a[data-bind*='downloadUrl']", timeout=downloadWait)

                # Capture download event
                with page.expect_download(timeout=1200000) as dl_info:
                    page.click("a[data-bind*='downloadUrl']")

                download = dl_info.value

                # Save file
                filename = safe_filename(title) + ".zip"
                save_path = DOWNLOAD_DIR / filename
                download.save_as(save_path)

                print(f"   ✓ Saved to {save_path}")
                successes += 1

                # polite wait
                time.sleep(random.uniform(5, 10))


            except Exception as e:
                print(f"   ✗ Failed on {title}: {e}")
                failures.append({
                    "index": i,
                    "title": title,
                    "url": r.get("url"),
                    "freeDownloadPage": free_url,
                    "error": str(e)
                })

        browser.close()

    # Append failures to a JSON log
    if failures:
        if Path(FAILURES_FILE).exists():
            existing = json.loads(Path(FAILURES_FILE).read_text())
        else:
            existing = []
        existing.extend(failures)
        Path(FAILURES_FILE).write_text(json.dumps(existing, indent=2))

    print(f"\nDone: {successes} successful, {len(failures)} failures logged.")


if __name__ == "__main__":
    # test small batch, e.g. index 1–1
    run_batch(startindex, endindex)