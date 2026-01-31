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
resources.sort(key=lambda r: (r.get("last_modified") or r.get("created") or ""), reverse=True)

print("Latest file:", latest["name"])

# 4. Download it
url = latest["url"]
filename = OUT / "latest_prescribing_file"

response = requests.get(url)
filename.write_bytes(response.content)

print("Saved to", filename)
