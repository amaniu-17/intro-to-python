


import requests

state_fips = input("Enter the State FIPS code that you would like data for: ")

variables = input("Enter the variable names that you would like data for: ")

url = (
    "https://api.census.gov/data/2024/acs/acs1"
    "?get=NAME," + variables +
    "&for=state:" + state_fips
)

response = requests.get(url)

data = response.json()

print("\nFound", len(data) - 1, "Rows of Data.\n")

for row in data:
    print(row)