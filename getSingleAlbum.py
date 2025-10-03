import json
from playwright.sync_api import sync_playwright

URL = "pathsinglealbum.com"  # <-- replace with a single album URL

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # set headless=True once it works
    page = browser.new_page()
    page.goto(URL)

    # Evaluate JavaScript inside the page
    tralbum_data = page.evaluate("() => window.TralbumData")

    browser.close()

# Save to file
with open("single_album.json", "w") as f:
    json.dump(tralbum_data, f, indent=2)

print("Saved metadata to single_album.json")