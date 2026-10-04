


import pandas as pd

#read the CSV file
data = pd.read_csv("Maternal Health Risk Data Set.csv")

#remove duplicate columns
data = data.loc[:, ~data.columns.duplicated()]

#convert to Excel
data.to_excel("Maternal_Health_Risk_Data.xlsx", index=False)

print("Excel file created successfully.")