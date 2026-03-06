"""
Financial Risk Assessment Pipeline
Generates synthetic applicant data, preprocesses it for machine learning,
trains a Random Forest classifier, and provides an interactive terminal for predictions.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# ---------------------------------------------------------
# CONFIGURATION & SETUP
# ---------------------------------------------------------
# Define relative paths for portability across different machines
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, '01_Data_Raw')
SQL_DIR = os.path.join(BASE_DIR, '02_SQL_Analysis')

# Ensure necessary directories exist to prevent path errors
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

RAW_CSV_PATH = os.path.join(RAW_DIR, 'clean_credit_data.csv')
POWERBI_CSV_PATH = os.path.join(SQL_DIR, 'PowerBI_Ready_Data.csv')

# Define business rules and generation parameters
SAMPLE_SIZE = 100
RISK_THRESHOLD = 0.45

# ---------------------------------------------------------
# SYNTHETIC DATA GENERATION
# ---------------------------------------------------------
# Set seed for reproducibility
np.random.seed(42)

# Construct applicant profiles
data = {
    'id': range(1, SAMPLE_SIZE + 1),
    'age': np.random.randint(18, 70, SAMPLE_SIZE),
    'income': np.random.randint(20000, 150000, SAMPLE_SIZE),
    'home_status': np.random.choice(['RENT', 'OWN', 'MORTGAGE'], SAMPLE_SIZE),
    'loan_amount': np.random.randint(5000, 80000, SAMPLE_SIZE),
}

df_raw = pd.DataFrame(data)

# Apply logic: Loan-to-income ratio exceeding the threshold indicates high risk (1)
df_raw['default_status'] = (df_raw['loan_amount'] / df_raw['income'] > RISK_THRESHOLD).astype(int)

# Export raw dataset
df_raw.to_csv(RAW_CSV_PATH, index=False)
print(f"[*] Raw data generated: {RAW_CSV_PATH}")

# ---------------------------------------------------------
# DATA PREPROCESSING
# ---------------------------------------------------------
# Encode categorical text into numeric values for the ML model
encoder = LabelEncoder()
df_raw['home_status_encoded'] = encoder.fit_transform(df_raw['home_status'])

# Export processed data for BI dashboard consumption
df_raw.to_csv(POWERBI_CSV_PATH, index=False)
print(f"[*] Processed data exported: {POWERBI_CSV_PATH}")

# ---------------------------------------------------------
# MODEL TRAINING
# ---------------------------------------------------------
# Isolate features (X) and target variable (y)
features = ['age', 'income', 'home_status_encoded', 'loan_amount']
X = df_raw[features]
y = df_raw['default_status']

# Initialize and train the classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
print("[*] Random Forest model training complete.\n")

# ---------------------------------------------------------
# INTERACTIVE TERMINAL
# ---------------------------------------------------------
print("=" * 45)
print("    FINANCIAL RISK ASSESSMENT TERMINAL")
print("=" * 45)

try:
    # Prompt for applicant details
    applicant_age = int(input("Applicant Age: "))
    applicant_income = int(input("Annual Income ($): "))
    applicant_loan = int(input("Requested Loan Amount ($): "))
    
    print("\nHome Status Key: 0=Mortgage, 1=Own, 2=Rent")
    applicant_home = int(input("Home Status (0, 1, or 2): "))

    # Generate prediction based on inputs
    prediction = model.predict([[applicant_age, applicant_income, applicant_home, applicant_loan]])
    
    # Display automated decision
    print("-" * 45)
    if prediction[0] == 1:
        print("RESULT: [!] HIGH RISK - APPLICATION DENIED")
    else:
        print("RESULT: [✔] LOW RISK - APPLICATION APPROVED")
    print("-" * 45)

except ValueError:
    print("\n[Error] Invalid input. Please enter numerical values only.")
