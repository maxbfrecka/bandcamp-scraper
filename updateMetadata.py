import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ALL_METADATA = "all_metadata.json"
PAID_RELEASES = "paidReleases.json"
OUTPUT = "all_metadata_updated.json"

# Load files
with open(ALL_METADATA, "r", encoding="utf-8") as f:
    all_data = json.load(f)

with open(PAID_RELEASES, "r", encoding="utf-8") as f:
    paid_list = json.load(f)

# Map all_data by URL for quick lookup
index_by_url = {entry["url"]: i for i, entry in enumerate(all_data)}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for release in paid_list:
        url = release["url"]
        title = release["title"]

        if url not in index_by_url:
            print(f"⚠️ Skipping {title}, not found in all_metadata.json")
            continue

        print(f"🔄 Refreshing {title} -> {url}")
        try:
            page.goto(url, timeout=60000)
            tralbum_data = page.evaluate("() => window.TralbumData")

            # Update the corresponding entry in all_data
            idx = index_by_url[url]
            all_data[idx]["tralbum"] = tralbum_data

            print(f"   ✓ Updated {title}")

        except Exception as e:
            print(f"   ✗ Error refreshing {title}: {e}")

    browser.close()

# Save the updated file
Path(OUTPUT).write_text(json.dumps(all_data, indent=2, ensure_ascii=False))

print(f"\n✅ Done. Saved updated metadata to {OUTPUT}")
