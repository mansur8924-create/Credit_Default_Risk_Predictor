-- Creating a 'Risk Category' based on loan size vs income
SELECT 
    loan_id,
    person_income,
    loan_amount,
    (CAST(loan_amount AS FLOAT) / person_income) AS dti_ratio,
    CASE 
        WHEN (CAST(loan_amount AS FLOAT) / person_income) > 0.5 THEN 'High Danger'
        WHEN (CAST(loan_amount AS FLOAT) / person_income) BETWEEN 0.2 AND 0.5 THEN 'Medium Risk'
        ELSE 'Safe'
    END AS risk_bucket
FROM raw_loan_records;

-- The 'Cracked Egg' Report
SELECT 
    COUNT(*) - COUNT(person_age) AS missing_ages,
    COUNT(*) - COUNT(person_income) AS missing_incomes,
    COUNT(*) - COUNT(home_ownership_status) AS missing_home_info
FROM raw_loan_records;