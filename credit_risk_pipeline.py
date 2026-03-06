"""
Financial Risk Assessment – Random Forest

Purpose:
    Generate synthetic credit applicant data, preprocess it, train a 
    Random Forest classifier, and allow a user to test loan applications
    interactively through a simple terminal interface.

Author: Mansur Mohammed
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Step 1: Setup directories and paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "01_Data_Raw")
SQL_DIR = os.path.join(BASE_DIR, "02_SQL_Analysis")

# Ensure folders exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

# File paths for raw and processed datasets
RAW_CSV_PATH = os.path.join(RAW_DIR, "clean_credit_data.csv")
POWERBI_CSV_PATH = os.path.join(SQL_DIR, "PowerBI_Ready_Data.csv")

# Parameters
SAMPLE_SIZE = 100        # Number of synthetic applicants to generate
RISK_THRESHOLD = 0.45    # Loan-to-income ratio threshold for default

# Step 2: Generate synthetic credit applicant data
np.random.seed(42)  # Make results reproducible

data = {
    "id": range(1, SAMPLE_SIZE + 1),
    "age": np.random.randint(18, 70, SAMPLE_SIZE),
    "income": np.random.randint(20000, 150000, SAMPLE_SIZE),
    "home_status": np.random.choice(["RENT", "OWN", "MORTGAGE"], SAMPLE_SIZE),
    "loan_amount": np.random.randint(5000, 80000, SAMPLE_SIZE),
}

df = pd.DataFrame(data)

# Simple risk rule: loan-to-income ratio above threshold → default
df["default_status"] = (df["loan_amount"] / df["income"] > RISK_THRESHOLD).astype(int)

# Save raw dataset
df.to_csv(RAW_CSV_PATH, index=False)
print(f"✅ Raw dataset created → {RAW_CSV_PATH}")

# Step 3: Preprocess data for modeling & BI
encoder = LabelEncoder()
df["home_status_encoded"] = encoder.fit_transform(df["home_status"])

# Export a Power BI-friendly version
df.to_csv(POWERBI_CSV_PATH, index=False)
print(f"✅ Processed dataset exported → {POWERBI_CSV_PATH}")

# Step 4: Train the Random Forest classifier
features = ["age", "income", "home_status_encoded", "loan_amount"]
X = df[features]
y = df["default_status"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
print("✅ Random Forest model trained successfully.\n")

# Step 5: Interactive prediction terminal

print("=" * 45)
print("      FINANCIAL RISK PREDICTION TERMINAL")
print("=" * 45)

try:
    # Collect applicant info
    age = int(input("Applicant age: "))
    income = int(input("Annual income ($): "))
    loan = int(input("Requested loan amount ($): "))

    print("\nHome Status Options:")
    print("0 = Mortgage")
    print("1 = Own")
    print("2 = Rent")
    home = int(input("Enter home status (0/1/2): "))

    # Make prediction
    prediction = model.predict([[age, income, home, loan]])

    print("-" * 45)
    if prediction[0] == 1:
        print("Decision: HIGH RISK — Application Denied")
    else:
        print("Decision: LOW RISK — Application Approved")
    print("-" * 45)

except ValueError:
    print("\n❌ Error: Please enter valid numeric values only.")
