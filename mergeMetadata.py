import json
import glob

# Collect all batch files matching metadata_*.json
files = sorted(glob.glob("metadata_*.json"))

all_releases = []
for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        all_releases.extend(json.load(fh))

print(f"Merged {len(files)} files, {len(all_releases)} total releases")

with open("all_metadata.json", "w", encoding="utf-8") as out:
    json.dump(all_releases, out, indent=2, ensure_ascii=False)

print("Saved all_metadata.json")