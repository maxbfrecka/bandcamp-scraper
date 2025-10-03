# this script fetches all album titles and links from a specified Bandcamp artist page 
# and saves them to a JSON file

import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

USERNAME = "declarationofdecimation"  # <-- your Bandcamp username
URL = f"https://{USERNAME}.bandcamp.com/music"

releases = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)

    # Grab page HTML after JS is loaded
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.select("li.music-grid-item a"):
        href = item.get("href")
        if href.startswith("/"):
            link = f"https://{USERNAME}.bandcamp.com{href}"
        else:
            link = href

        title = item.text.strip()
        releases.append({"title": title, "link": link})

    browser.close()

with open("releases.json", "w") as f:
    json.dump(releases, f, indent=2)

print(f"Saved {len(releases)} releases to releases.json")