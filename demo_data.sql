-- ============================================================
-- Budget AI - Fresh English Demo Data
-- Full database setup + demo users + demo transactions
--
-- Demo accounts:
--   admin / 1234
--   test  / 1234
--
-- This file uses the ENGLISH version of the schema:
--   amount   instead of montant
--   category instead of categorie
--   revenue  instead of revenu
--   expense  instead of depense
--
-- WARNING:
-- This script recreates the users and transactions tables.
-- It will delete existing data in these two tables.
-- ============================================================

CREATE DATABASE IF NOT EXISTS budget_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE budget_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================
-- USERS TABLE
-- =========================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- =========================
-- TRANSACTIONS TABLE
-- =========================

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('revenue', 'expense') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    date DATE NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_transactions_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =========================
-- DEMO USERS
-- =========================

INSERT INTO users (username, password)
VALUES
('admin', '1234'),
('test', '1234');

SET @admin_id = (SELECT id FROM users WHERE username = 'admin');
SET @test_id  = (SELECT id FROM users WHERE username = 'test');


-- ============================================================
-- ADMIN DEMO DATA
-- ============================================================

-- February 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 5200, 'Salary', 'Monthly salary', '2026-02-01', @admin_id),
('expense', 850, 'Food', 'Groceries and meals', '2026-02-05', @admin_id),
('expense', 300, 'Transport', 'Taxi and bus', '2026-02-08', @admin_id),
('expense', 1200, 'Housing', 'Rent contribution', '2026-02-10', @admin_id),
('expense', 250, 'Bills', 'Internet bill', '2026-02-15', @admin_id),
('expense', 400, 'Leisure', 'Weekend activity', '2026-02-21', @admin_id);

-- March 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 5200, 'Salary', 'Monthly salary', '2026-03-01', @admin_id),
('revenue', 800, 'Freelance', 'Small freelance task', '2026-03-07', @admin_id),
('expense', 900, 'Food', 'Groceries', '2026-03-04', @admin_id),
('expense', 350, 'Transport', 'Fuel and taxi', '2026-03-09', @admin_id),
('expense', 1200, 'Housing', 'Rent contribution', '2026-03-10', @admin_id),
('expense', 300, 'Bills', 'Electricity and internet', '2026-03-16', @admin_id),
('expense', 500, 'Other', 'Clothes', '2026-03-23', @admin_id);

-- April 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 5200, 'Salary', 'Monthly salary', '2026-04-01', @admin_id),
('expense', 950, 'Food', 'Groceries and snacks', '2026-04-05', @admin_id),
('expense', 400, 'Transport', 'Transport pass', '2026-04-08', @admin_id),
('expense', 1200, 'Housing', 'Rent contribution', '2026-04-10', @admin_id),
('expense', 320, 'Bills', 'Phone and internet', '2026-04-17', @admin_id),
('expense', 450, 'Leisure', 'Cinema and coffee', '2026-04-24', @admin_id);

-- May 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 5200, 'Salary', 'Monthly salary', '2026-05-01', @admin_id),
('expense', 1000, 'Food', 'Groceries', '2026-05-04', @admin_id),
('expense', 450, 'Transport', 'Taxi and fuel', '2026-05-09', @admin_id),
('expense', 1200, 'Housing', 'Rent contribution', '2026-05-10', @admin_id),
('expense', 350, 'Bills', 'Bills', '2026-05-16', @admin_id),
('expense', 550, 'Leisure', 'Restaurant and weekend', '2026-05-24', @admin_id);

-- June 2026 - current month demo
-- Includes a spending increase and high expenses for Analytics tests
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 5500, 'Salary', 'Monthly salary', '2026-06-01', @admin_id),
('revenue', 1000, 'Freelance', 'Freelance web task', '2026-06-06', @admin_id),
('expense', 1800, 'Food', 'Large food purchase', '2026-06-03', @admin_id),
('expense', 700, 'Transport', 'Fuel and taxi increase', '2026-06-05', @admin_id),
('expense', 1200, 'Housing', 'Rent contribution', '2026-06-10', @admin_id),
('expense', 380, 'Bills', 'Electricity and internet', '2026-06-12', @admin_id),
('expense', 600, 'Leisure', 'Weekend trip', '2026-06-15', @admin_id),
('expense', 250, 'Other', 'Small purchase', '2026-06-17', @admin_id),
('expense', 2300, 'Other', 'Emergency laptop repair', '2026-06-18', @admin_id),
('expense', 950, 'Food', 'Family dinner and groceries', '2026-06-20', @admin_id);


-- ============================================================
-- TEST USER DEMO DATA
-- ============================================================

-- February 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 4000, 'Freelance', 'Client project', '2026-02-02', @test_id),
('expense', 600, 'Food', 'Groceries', '2026-02-05', @test_id),
('expense', 200, 'Transport', 'Bus', '2026-02-08', @test_id),
('expense', 900, 'Housing', 'Room rent', '2026-02-10', @test_id),
('expense', 180, 'Bills', 'Phone bill', '2026-02-16', @test_id),
('expense', 350, 'Leisure', 'Gaming and coffee', '2026-02-22', @test_id);

-- March 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 4200, 'Freelance', 'Mobile app task', '2026-03-02', @test_id),
('expense', 650, 'Food', 'Food and snacks', '2026-03-05', @test_id),
('expense', 250, 'Transport', 'Taxi', '2026-03-09', @test_id),
('expense', 900, 'Housing', 'Room rent', '2026-03-10', @test_id),
('expense', 220, 'Bills', 'Internet', '2026-03-16', @test_id),
('expense', 300, 'Other', 'Accessories', '2026-03-25', @test_id);

-- April 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 4300, 'Freelance', 'Design task', '2026-04-02', @test_id),
('expense', 700, 'Food', 'Groceries', '2026-04-05', @test_id),
('expense', 300, 'Transport', 'Fuel', '2026-04-08', @test_id),
('expense', 900, 'Housing', 'Room rent', '2026-04-10', @test_id),
('expense', 250, 'Bills', 'Bills', '2026-04-16', @test_id),
('expense', 450, 'Leisure', 'Gym and movies', '2026-04-24', @test_id);

-- May 2026
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 4500, 'Freelance', 'Backend development', '2026-05-02', @test_id),
('expense', 750, 'Food', 'Groceries and restaurant', '2026-05-05', @test_id),
('expense', 350, 'Transport', 'Taxi and bus', '2026-05-08', @test_id),
('expense', 900, 'Housing', 'Room rent', '2026-05-10', @test_id),
('expense', 260, 'Bills', 'Internet and phone', '2026-05-16', @test_id),
('expense', 500, 'Leisure', 'Shopping and entertainment', '2026-05-23', @test_id);

-- June 2026 - current month demo
-- Includes transport spike and one high expense for Analytics tests
INSERT INTO transactions (type, amount, category, description, date, user_id)
VALUES
('revenue', 4700, 'Freelance', 'Full-stack project', '2026-06-02', @test_id),
('revenue', 700, 'Other', 'Small bonus', '2026-06-07', @test_id),
('expense', 800, 'Food', 'Restaurants and groceries', '2026-06-04', @test_id),
('expense', 1200, 'Transport', 'Car repair and fuel', '2026-06-06', @test_id),
('expense', 900, 'Housing', 'Room rent', '2026-06-10', @test_id),
('expense', 280, 'Bills', 'Internet and phone', '2026-06-13', @test_id),
('expense', 550, 'Leisure', 'Weekend activity', '2026-06-15', @test_id),
('expense', 320, 'Other', 'Personal items', '2026-06-17', @test_id),
('expense', 2100, 'Transport', 'Major car repair', '2026-06-18', @test_id),
('expense', 620, 'Food', 'Groceries before exams', '2026-06-21', @test_id);


-- ============================================================
-- QUICK VERIFICATION
-- ============================================================

SELECT 'admin transaction count' AS info, COUNT(*) AS total
FROM transactions
WHERE user_id = @admin_id;

SELECT 'test transaction count' AS info, COUNT(*) AS total
FROM transactions
WHERE user_id = @test_id;

SELECT 'June transactions count' AS info, COUNT(*) AS total
FROM transactions
WHERE MONTH(date) = 6 AND YEAR(date) = 2026;
