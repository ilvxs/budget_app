-- Demo data for Budget AI - VERSION 2
-- ONLY two demo users:
--   admin / 1234
--   test  / 1234
--
-- This file inserts many transactions for each user across 5 months.
-- It does NOT create or use the ilvxs user.

USE budget_db;

-- =========================
-- USERS
-- =========================

INSERT IGNORE INTO users (username, password)
VALUES
('admin', '1234'),
('test', '1234');

SET @admin_id = (SELECT id FROM users WHERE username = 'admin');
SET @test_id  = (SELECT id FROM users WHERE username = 'test');

-- Clean old demo transactions for these two users only
DELETE FROM transactions
WHERE user_id IN (@admin_id, @test_id);

-- =====================================================
-- ADMIN DEMO DATA
-- =====================================================

-- 4 months ago
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 5200, 'Salaire', 'Salaire mensuel', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @admin_id),
('depense', 850, 'Food', 'Groceries and meals', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @admin_id),
('depense', 300, 'Transport', 'Taxi and bus', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @admin_id),
('depense', 1200, 'Logement', 'Rent contribution', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @admin_id),
('depense', 250, 'Factures', 'Internet bill', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @admin_id),
('depense', 400, 'Loisirs', 'Weekend activity', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @admin_id);

-- 3 months ago
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 5200, 'Salaire', 'Salaire mensuel', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id),
('revenu', 800, 'Freelance', 'Small freelance task', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id),
('depense', 900, 'Food', 'Groceries', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id),
('depense', 350, 'Transport', 'Fuel and taxi', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id),
('depense', 1200, 'Logement', 'Rent contribution', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id),
('depense', 300, 'Factures', 'Electricity and internet', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id),
('depense', 500, 'Autre', 'Clothes', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @admin_id);

-- 2 months ago
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 5200, 'Salaire', 'Salaire mensuel', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @admin_id),
('depense', 950, 'Food', 'Groceries and snacks', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @admin_id),
('depense', 400, 'Transport', 'Transport pass', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @admin_id),
('depense', 1200, 'Logement', 'Rent contribution', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @admin_id),
('depense', 320, 'Factures', 'Phone and internet', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @admin_id),
('depense', 450, 'Loisirs', 'Cinema and coffee', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @admin_id);

-- Previous month
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 5200, 'Salaire', 'Salaire mensuel', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @admin_id),
('depense', 1000, 'Food', 'Groceries', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @admin_id),
('depense', 450, 'Transport', 'Taxi and fuel', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @admin_id),
('depense', 1200, 'Logement', 'Rent contribution', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @admin_id),
('depense', 350, 'Factures', 'Bills', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @admin_id),
('depense', 550, 'Loisirs', 'Restaurant and weekend', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @admin_id);

-- Current month
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 5500, 'Salaire', 'Salaire mensuel', CURDATE(), @admin_id),
('revenu', 1000, 'Freelance', 'Freelance web task', CURDATE(), @admin_id),
('depense', 1800, 'Food', 'Large food purchase', CURDATE(), @admin_id),
('depense', 700, 'Transport', 'Fuel and taxi increase', CURDATE(), @admin_id),
('depense', 1200, 'Logement', 'Rent contribution', CURDATE(), @admin_id),
('depense', 380, 'Factures', 'Electricity and internet', CURDATE(), @admin_id),
('depense', 600, 'Loisirs', 'Weekend trip', CURDATE(), @admin_id),
('depense', 250, 'Autre', 'Small purchase', CURDATE(), @admin_id);


-- =====================================================
-- TEST USER DEMO DATA
-- =====================================================

-- 4 months ago
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 4000, 'Freelance', 'Client project', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @test_id),
('depense', 600, 'Food', 'Groceries', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @test_id),
('depense', 200, 'Transport', 'Bus', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @test_id),
('depense', 900, 'Logement', 'Room rent', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @test_id),
('depense', 180, 'Factures', 'Phone bill', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @test_id),
('depense', 350, 'Loisirs', 'Gaming and coffee', DATE_SUB(CURDATE(), INTERVAL 4 MONTH), @test_id);

-- 3 months ago
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 4200, 'Freelance', 'Mobile app task', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @test_id),
('depense', 650, 'Food', 'Food and snacks', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @test_id),
('depense', 250, 'Transport', 'Taxi', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @test_id),
('depense', 900, 'Logement', 'Room rent', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @test_id),
('depense', 220, 'Factures', 'Internet', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @test_id),
('depense', 300, 'Autre', 'Accessories', DATE_SUB(CURDATE(), INTERVAL 3 MONTH), @test_id);

-- 2 months ago
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 4300, 'Freelance', 'Design task', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @test_id),
('depense', 700, 'Food', 'Groceries', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @test_id),
('depense', 300, 'Transport', 'Fuel', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @test_id),
('depense', 900, 'Logement', 'Room rent', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @test_id),
('depense', 250, 'Factures', 'Bills', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @test_id),
('depense', 450, 'Loisirs', 'Gym and movies', DATE_SUB(CURDATE(), INTERVAL 2 MONTH), @test_id);

-- Previous month
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 4500, 'Freelance', 'Backend development', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @test_id),
('depense', 750, 'Food', 'Groceries and restaurant', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @test_id),
('depense', 350, 'Transport', 'Taxi and bus', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @test_id),
('depense', 900, 'Logement', 'Room rent', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @test_id),
('depense', 260, 'Factures', 'Internet and phone', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @test_id),
('depense', 500, 'Loisirs', 'Shopping and entertainment', DATE_SUB(CURDATE(), INTERVAL 1 MONTH), @test_id);

-- Current month
INSERT INTO transactions (type, montant, categorie, description, date, user_id)
VALUES
('revenu', 4700, 'Freelance', 'Full-stack project', CURDATE(), @test_id),
('revenu', 700, 'Autre', 'Small bonus', CURDATE(), @test_id),
('depense', 800, 'Food', 'Restaurants and groceries', CURDATE(), @test_id),
('depense', 1200, 'Transport', 'Car repair and fuel', CURDATE(), @test_id),
('depense', 900, 'Logement', 'Room rent', CURDATE(), @test_id),
('depense', 280, 'Factures', 'Internet and phone', CURDATE(), @test_id),
('depense', 550, 'Loisirs', 'Weekend activity', CURDATE(), @test_id),
('depense', 320, 'Autre', 'Personal items', CURDATE(), @test_id);

-- Quick verification
SELECT 'admin transaction count' AS info, COUNT(*) AS total
FROM transactions
WHERE user_id = @admin_id;

SELECT 'test transaction count' AS info, COUNT(*) AS total
FROM transactions
WHERE user_id = @test_id;
