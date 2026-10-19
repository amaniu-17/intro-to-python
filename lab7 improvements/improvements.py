



# lab 7 regression improvements
# amani fargham
# original code by Gabriel Murguia
# improvement 1: regression for selected data ranges
# improvement 2: user options for graph formatting
##################################################

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
import re


# Load the datasets
birthwt = pd.read_csv("birthwt.csv")
places = pd.read_csv("places_2025.csv")


# Clean column names
for df in [birthwt, places]:
    new_columns = []

    for column in df.columns:
        column = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", column)
        column = column.strip().lower()
        column = re.sub(r"[^a-z0-9]+", "_", column)
        new_columns.append(column.strip("_"))

    df.columns = new_columns


# Create folders for the graphs
os.makedirs("figures/birthweight_figures", exist_ok=True)
os.makedirs("figures/cdc_places_figures/housing", exist_ok=True)
os.makedirs("figures/cdc_places_figures/mental_health", exist_ok=True)


# Function to create scatterplots and regression graphs
def make_plots(df, x_column, y_column, fig1, fig2, folder):

    # Remove missing values
    df = df.copy()
    df[x_column] = pd.to_numeric(df[x_column], errors="coerce")
    df[y_column] = pd.to_numeric(df[y_column], errors="coerce")
    df = df.dropna(subset=[x_column, y_column])

    # Improvement 1: Select a data range
    print("\nAnalyzing:", x_column, "vs", y_column)

    answer = input("Do you want to select a data range? (y/n): ")

    if answer.lower() == "y":
        minimum = float(input("Enter minimum value: "))
        maximum = float(input("Enter maximum value: "))

        df = df[(df[x_column] >= minimum) &
                (df[x_column] <= maximum)]

    if len(df) < 3 or df[x_column].nunique() < 2:
        print("Not enough data for regression.")
        return

    x = df[x_column]
    y = df[y_column]

    # Improvement 2: Customize the graph
    print("\nGraph Formatting Options")

    color = input("Enter a graph color (blue, red, green): ")
    if color == "":
        color = "blue"

    title = input("Enter a graph title: ")
    if title == "":
        title = "Regression Graph"

    line_width = input("Enter line thickness (1, 2, or 3): ")
    if line_width == "":
        line_width = "2"

    grid = input("Show gridlines? (y/n): ")

    # Figure 1: Scatterplot without regression
    plt.scatter(x, y, color=color)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.grid(grid.lower() == "y")

    answer = input("Save " + fig1 + "? (y/n): ")

    if answer.lower() == "y":
        plt.savefig(folder + "/" + fig1 + ".png")

    plt.show()
    plt.close()

    # Perform linear regression
    x_constant = sm.add_constant(x, has_constant="add")
    model = sm.OLS(y, x_constant).fit()

    print("\nRegression Results:")
    print(model.summary())

    # Sort values for the regression line
    sorted_df = df.sort_values(x_column)
    sorted_x = sorted_df[x_column]
    sorted_constant = sm.add_constant(
        sorted_x, has_constant="add"
    )

    # Figure 2: Scatterplot with regression
    plt.scatter(x, y, color=color, label="Data")

    plt.plot(
        sorted_x,
        model.predict(sorted_constant),
        color="red",
        linewidth=float(line_width),
        label="Regression Line"
    )

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title + " with Regression")
    plt.grid(grid.lower() == "y")
    plt.legend()

    answer = input("Save " + fig2 + "? (y/n): ")

    if answer.lower() == "y":
        plt.savefig(folder + "/" + fig2 + ".png")

    plt.show()
    plt.close()


# Figures 1 and 2: Mother's weight vs birth weight
make_plots(
    birthwt,
    "lwt",
    "bwt",
    "fig_1",
    "fig_2",
    "figures/birthweight_figures"
)


# Figures 3 and 4: Population vs housing insecurity
make_plots(
    places,
    "total_population",
    "housinsecu_crude_prev",
    "fig_3",
    "fig_4",
    "figures/cdc_places_figures/housing"
)


# Figures 5 and 6: Obesity vs mental health
make_plots(
    places,
    "obesity_crude_prev",
    "mhlth_crude_prev",
    "fig_5",
    "fig_6",
    "figures/cdc_places_figures/mental_health"
)




































