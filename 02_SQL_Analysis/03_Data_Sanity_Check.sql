-- Searching for 'Impossible' people
SELECT * FROM raw_loan_records
WHERE person_age > 100 
   OR person_age < 18
   OR person_income <= 0;
   
   -- Finding the 'Whales' (The extremely wealthy outliers)
SELECT * FROM raw_loan_records
WHERE person_income > (SELECT AVG(person_income) * 3 FROM raw_loan_records);