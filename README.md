# Mortgage & Credit Insights: Predictive Risk Analysis

Project Overview

This project is an automated financial risk assessment pipeline. It acts as a digital loan officer. The system generates customer financial profiles, analyzes the data for risk, and predicts whether a loan should be approved or denied based on strict financial ratios. The final results are displayed on an interactive visual dashboard.

How the System Works

The pipeline moves information through four distinct stages:

Data Creation: A Python script generates 100 realistic customer records. It builds profiles using details like age, income, housing status, and requested loan amounts.

Data Preparation: Computers require numbers to perform calculations. The system translates text descriptions (like "RENT" or "OWN") into numerical codes so the predictive algorithm can process them.

The Predictive Brain: The system uses a Machine Learning model called a Random Forest. Think of this as a room full of 100 financial experts. Each expert looks at the customer's details and casts a vote on whether the loan is safe. The system takes the majority vote to make the final approval or denial decision.

Executive Dashboard: The processed data flows directly into a Power BI dashboard. This creates a visual showroom where decision-makers can instantly see risk trends across different income levels and housing categories.

Technology Stack

Python: The core programming language used to construct the pipeline.

Pandas & NumPy: Tools used to structure and calculate the data, acting like a highly advanced virtual spreadsheet.

Scikit-Learn: The machine learning library used to train the predictive algorithm.

Power BI: The business intelligence software used to create the interactive visual charts.

Execution Instructions

Follow these steps to operate the pipeline locally:

Download the complete project repository to a local computer. Ensure the folder structure remains intact.

Execute the main Python file in a code editor or terminal.

Follow the interactive prompts on the screen to enter a test applicant's financial details.

Read the terminal output to see the automated risk decision.

Open the connected Power BI file and refresh the data source to view the updated visual dashboard.

