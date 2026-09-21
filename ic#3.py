


import requests

YEAR = 2023
DATASET = "dec/pl"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "CENSUS KEY GOES HERE"

params = {
    "get": "NAME,P01_001N",
    "for": "state:*",
    "key": API_KEY,
}

response = requests.get(URL, params=params)

if response.status_code != 200:
    print(f"Request failed ({response.status_code}): {response.text}")
    raise SystemExit(1)

data = response.json()

print(f"Got {len(data) - 1} states back.\n")

for i in data:
    print(data)

