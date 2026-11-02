


# ---------------------------------------------------------
# Heart Failure Survival Analysis
# Amani Fargham
# This script compares hospital readmission between
# treatment groups
#####################################################

import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

#part 1: kaplan-meier log-rank test

data = pd.read_csv("km_logrank_readmission.csv")

standard = data[data["treatment_group"] == "Standard care"]
telehealth = data[data["treatment_group"] == "Telehealth follow-up"]

result = logrank_test(
    standard["time_days"],
    telehealth["time_days"],
    standard["readmitted"],
    telehealth["readmitted"]
)

print("Log-rank p-value:", result.p_value)

km = KaplanMeierFitter()

km.fit(standard["time_days"], standard["readmitted"], label="Standard Care")
km.plot_survival_function()

km.fit(telehealth["time_days"], telehealth["readmitted"], label="Telehealth")
km.plot_survival_function()

plt.title("Kaplan-Meier: Hospital Readmission")
plt.xlabel("Time After Discharge (Days)")
plt.ylabel("Probability of No Readmission")
plt.xlim(0, 180)
plt.savefig("logrank_readmission.png")
plt.show()


#part 2: cox proportional hazards

data = pd.read_csv("cox_ph_heart_failure_survival.csv")

data = data.drop(columns=["patient_id"])
data = pd.get_dummies(data, drop_first=True, dtype=int)

cox = CoxPHFitter()
cox.fit(data, duration_col="time_months", event_col="death")

cox.print_summary()
cox.plot(hazard_ratios=True)

plt.title("Cox Proportional Hazards: Heart Failure Survival")
plt.xlabel("Hazard Ratio (95% Confidence Interval)")
plt.axvline(1, color="red", linestyle="--")
plt.savefig("cox_hazard_ratios.png")
plt.show()
