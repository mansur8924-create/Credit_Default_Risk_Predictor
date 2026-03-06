-- Calculating the Default Rate by Home Status
SELECT 
    home_ownership_status, 
    COUNT(*) AS total_borrowers,
    SUM(is_default) AS total_failures,
    ROUND(AVG(is_default) * 100, 2) AS failure_percentage
FROM raw_loan_records
GROUP BY home_ownership_status;