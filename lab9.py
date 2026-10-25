



#lab 8 Logistic and Poisson Regression
# HSC4933 python for Health Analytics
#this script runs logistic or poisson regression.
#Amani Fargham
######################################

import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from statsmodels.stats.outliers_influence import variance_inflation_factor


# Step 1: Ask the user for a dataset
filename = input("Enter CSV filename: ")
data = pd.read_csv(filename)


# Step 2: Clean column names to snake_case
data.columns = (data.columns.str.strip().str.lower()
                .str.replace(" ", "_").str.replace("-", "_"))


# Step 3: Show available columns
print("\nAvailable columns:")
print(", ".join(data.columns))


# Step 4: Ask for predictors and response variable
predictors = input("\nPredictors (separate with commas): ")
predictors = [name.strip().lower() for name in predictors.split(",")]

response = input("Response column: ").strip().lower()

kind = input("Regression type (logistic or poisson): ").strip().lower()


# Check the user's selections
print("Invalid columns:")
for name in predictors + [response]:
    if name not in data.columns:
        print(name)
if kind not in ["logistic", "poisson"]:
    raise ValueError("Choose logistic or poisson.")

if not predictors or any(name not in data.columns for name in predictors + [response]):
    raise ValueError("One or more column names are invalid.")

if response in predictors or len(set(predictors)) != len(predictors):
    raise ValueError("Choose unique predictors different from the response.")


# Step 5: Remove missing values
selected = data[predictors + [response]].copy()

for name in selected.columns:
    selected[name] = pd.to_numeric(selected[name], errors="coerce")

selected = selected.dropna()

if selected.empty:
    raise ValueError("No complete rows available.")


# Prepare the regression variables
x = sm.add_constant(selected[predictors], has_constant="add")
y = selected[response]


# Step 6: Run the selected regression
if kind == "logistic":

    # Check that the response contains 0 and 1
    if not y.isin([0, 1]).all() or y.nunique() != 2:
        raise ValueError("Logistic response must contain both 0 and 1.")

    # Run logistic regression
    model = sm.Logit(y, x).fit(disp=False)

    # Make predictions
    predicted = (model.predict(x) >= 0.5).astype(int)

    # Create output
    output = str(model.summary())

    output += "\n\nConfusion Matrix:\n"
    output += str(confusion_matrix(y, predicted, labels=[0, 1]))

    output += "\n\nClassification Report:\n"
    output += classification_report(y, predicted, labels=[0, 1], zero_division=0)

    output += "\nAccuracy: " + str(round(accuracy_score(y, predicted), 4))


elif kind == "poisson":

    # Check for negative values
    if (y < 0).any():
        raise ValueError("Poisson response cannot be negative.")

    if (y % 1 != 0).any():
        print("WARNING: Response is not integer count data.")

    # Run Poisson regression
    model = sm.GLM(y, x, family=sm.families.Poisson()).fit()

    output = str(model.summary())

    # Calculate pseudo-R-squared
    null_model = sm.GLM(y, x[["const"]],
                        family=sm.families.Poisson()).fit()

    pseudo_r2 = 1 - model.llf / null_model.llf

    output += "\n\nMcFadden Pseudo-R-squared: "
    output += str(round(pseudo_r2, 6))

    # Calculate VIF
    vif = pd.DataFrame()

    vif["Predictor"] = predictors

    vif["VIF"] = [
        variance_inflation_factor(x.values, i + 1)
        for i in range(len(predictors))
    ]

    output += "\n\nVIF Results:\n"
    output += vif.to_string(index=False)

    if (y % 1 != 0).any():
        output += "\n\nWARNING: The response is not count data."
        output += "\nPoisson regression assumptions are not met."


# Display the results
output = "Dataset: " + filename + "\nRows used: " + str(len(selected)) + "\n\n" + output

print("\n" + output)

# Build the final output
# The regression output was already created above.
print("\n" + output)


# Step 7: Ask if the user wants to save the output
save = input("\nSave output to .txt? (yes/no): ").strip().lower()

if save == "yes" or save == "y":

    name = input("Enter output filename: ").strip()

    if not name.endswith(".txt"):
        name += ".txt"

    with open(name, "w", encoding="utf-8") as file:
        file.write(output)

    print("Saved:", name)
