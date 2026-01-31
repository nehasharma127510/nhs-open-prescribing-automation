import requests
from pathlib import Path

BASE = "https://opendata.nhsbsa.net"
OUT = Path("data/raw")

OUT.mkdir(parents=True, exist_ok=True)

# 1. Find the dataset
search = requests.get(
    f"{BASE}/api/3/action/package_search",
    params={"q": "English Prescribing Dataset (EPD) with SNOMED", "rows": 1}
).json()

dataset_id = search["result"]["results"][0]["id"]

# 2. Get monthly files
pkg = requests.get(
    f"{BASE}/api/3/action/package_show",
    params={"id": dataset_id}
).json()

resources = pkg["result"]["resources"]

# 3. Pick the newest file
resources = [r for r in resources if r.get("url")]
print("How many downloadable resources:", len(resources))
resources.sort(key=lambda r: r.get("last_modified") or r.get("created") or "", reverse=True)
latest = resources[0]
print("Latest file:", latest.get("name"))
print("Latest url:", latest.get("url"))



# 4. Download it (streaming)
url = latest["url"]
filename = OUT / "latest_prescribing_file"

with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

print("Saved to", filename)

