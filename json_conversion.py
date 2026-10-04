


import pandas as pd

#read the CSV file
data = pd.read_csv("Maternal Health Risk Data Set.csv")

#remove duplicate columns
data = data.loc[:, ~data.columns.duplicated()]

#convert to JSON
data.to_json("Maternal_Health_Risk_Data.json", orient="records", indent=4)

print("JSON file created successfully.")