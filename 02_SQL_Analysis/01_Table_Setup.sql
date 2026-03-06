-- Creating the landing table for our bank data
CREATE TABLE raw_loan_records (
    loan_id INT PRIMARY KEY,
    person_age INT,
    person_income INT,
    home_ownership_status VARCHAR(50),
    loan_amount INT,
    is_default INT -- 1 means they failed to pay, 0 means they paid
);