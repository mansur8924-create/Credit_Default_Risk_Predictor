-- Create a copy of the data so we don't ruin the original
CREATE TABLE cleaned_loan_records AS
SELECT * FROM raw_loan_records;
-- Filling in missing incomes with the average income
UPDATE cleaned_loan_records
SET person_income = (SELECT AVG(person_income) FROM raw_loan_records)
WHERE person_income IS NULL;
-- Removing 'Impossible' people who would confuse the AI
DELETE FROM cleaned_loan_records
WHERE person_age > 100 OR person_age < 18;
-- Making sure all text is in UPPERCASE so the computer doesn't get confused
UPDATE cleaned_loan_records
SET home_ownership_status = UPPER(home_ownership_status);
-- The 'Zero-Error' Report
SELECT 
    (SELECT COUNT(*) FROM cleaned_loan_records WHERE person_income IS NULL) AS null_incomes,
    (SELECT COUNT(*) FROM cleaned_loan_records WHERE person_age > 100) AS age_outliers,
    COUNT(*) AS total_clean_rows
FROM cleaned_loan_records;