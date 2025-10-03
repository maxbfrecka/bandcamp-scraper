import json
from pathlib import Path

INPUT = "all_metadata_updated.json"
OUTPUT = "emailRequired.json"

with open(INPUT, "r", encoding="utf-8") as f:
    releases = json.load(f)

email_required = []

for r in releases:
    tr = r.get("tralbum", {})
    current = tr.get("current", {})

    if current.get("require_email") is not None:
        email_required.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "require_email": current.get("require_email")
        })

print(f"Found {len(email_required)} releases requiring email out of {len(releases)} total")

with open(OUTPUT, "w", encoding="utf-8") as out:
    json.dump(email_required, out, indent=2, ensure_ascii=False)

print(f"Saved {OUTPUT}")