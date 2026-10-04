


import pandas as pd

#read the CSV file
data = pd.read_csv("Maternal Health Risk Data Set.csv")

#remove duplicate columns
data = data.loc[:, ~data.columns.duplicated()]

#convert to Parquet
data.to_parquet("Maternal_Health_Risk_Data.parquet", index=False)

print("Parquet file created successfully.")