import json

with open("all_metadata.json", "r", encoding="utf-8") as f:
    releases = json.load(f)

paid_releases = []

for r in releases:
    tr = r.get("tralbum", {})
    free_url = tr.get("freeDownloadPage")

    if not free_url:  # if no free download link
        paid_releases.append({
            "title": r.get("title"),
            "url": r.get("url")
        })

print(f"Found {len(paid_releases)} paid releases out of {len(releases)} total")

with open("paidReleases.json", "w", encoding="utf-8") as out:
    json.dump(paid_releases, out, indent=2, ensure_ascii=False)

print("Saved paidReleases.json")