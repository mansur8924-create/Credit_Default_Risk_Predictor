"""
Simple Financial Risk Model

This script generates synthetic credit applicant data, preprocesses it,
trains a Random Forest classifier, and allows a user to test predictions
through a small terminal interface.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# -------------------------------------------------
# Basic setup
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DIR = os.path.join(BASE_DIR, "01_Data_Raw")
SQL_DIR = os.path.join(BASE_DIR, "02_SQL_Analysis")

# Create folders if they don't exist yet
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

RAW_CSV_PATH = os.path.join(RAW_DIR, "clean_credit_data.csv")
POWERBI_CSV_PATH = os.path.join(SQL_DIR, "PowerBI_Ready_Data.csv")

SAMPLE_SIZE = 100
RISK_THRESHOLD = 0.45

# -------------------------------------------------
# Generate synthetic applicant data
# -------------------------------------------------

# Seed so results stay consistent between runs
np.random.seed(42)

data = {
    "id": range(1, SAMPLE_SIZE + 1),
    "age": np.random.randint(18, 70, SAMPLE_SIZE),
    "income": np.random.randint(20000, 150000, SAMPLE_SIZE),
    "home_status": np.random.choice(["RENT", "OWN", "MORTGAGE"], SAMPLE_SIZE),
    "loan_amount": np.random.randint(5000, 80000, SAMPLE_SIZE),
}

df = pd.DataFrame(data)

# Simple rule: if loan-to-income ratio is too high → likely default
df["default_status"] = (
    df["loan_amount"] / df["income"] > RISK_THRESHOLD
).astype(int)

# Save the generated dataset
df.to_csv(RAW_CSV_PATH, index=False)
print(f"Raw dataset created → {RAW_CSV_PATH}")

# -------------------------------------------------
# Data preprocessing
# -------------------------------------------------

# Convert categorical text to numbers so the model can use it
encoder = LabelEncoder()
df["home_status_encoded"] = encoder.fit_transform(df["home_status"])

# Export version used for BI dashboards
df.to_csv(POWERBI_CSV_PATH, index=False)
print(f"Processed dataset exported → {POWERBI_CSV_PATH}")

# -------------------------------------------------
# Train machine learning model
# -------------------------------------------------

features = ["age", "income", "home_status_encoded", "loan_amount"]

X = df[features]
y = df["default_status"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("Random Forest model trained successfully.\n")

# -------------------------------------------------
# Interactive prediction terminal
# -------------------------------------------------

print("=" * 45)
print("      FINANCIAL RISK PREDICTION TERMINAL")
print("=" * 45)

try:
    age = int(input("Applicant age: "))
    income = int(input("Annual income ($): "))
    loan = int(input("Requested loan amount ($): "))

    print("\nHome Status:")
    print("0 = Mortgage")
    print("1 = Own")
    print("2 = Rent")

    home = int(input("Enter home status (0/1/2): "))

    prediction = model.predict([[age, income, home, loan]])

    print("-" * 45)

    if prediction[0] == 1:
        print("Decision: HIGH RISK — Application Denied")
    else:
        print("Decision: LOW RISK — Application Approved")

    print("-" * 45)

except ValueError:
    print("\nError: Please enter numeric values only.")
