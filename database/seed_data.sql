-- HouseMate Seed Data
-- Test data for development and demonstration

-- =============================================================================
-- Test Users
-- All passwords are hashed version of 'test123'
-- =============================================================================

INSERT INTO users (user_id, email, password_hash, first_name, last_name) VALUES
(1, 'marin@test.com', '$2b$12$K1C7LmKXgFxVhQv6CqHjPO9QcJ4wEWdU2aH1IgxYvzKhMzQr5Qk7C', 'Marin', 'Student'),
(2, 'ana@test.com', '$2b$12$K1C7LmKXgFxVhQv6CqHjPO9QcJ4wEWdU2aH1IgxYvzKhMzQr5Qk7C', 'Ana', 'Kovač'),
(3, 'ivan@test.com', '$2b$12$K1C7LmKXgFxVhQv6CqHjPO9QcJ4wEWdU2aH1IgxYvzKhMzQr5Qk7C', 'Ivan', 'Horvat'),
(4, 'marija@test.com', '$2b$12$K1C7LmKXgFxVhQv6CqHjPO9QcJ4wEWdU2aH1IgxYvzKhMzQr5Qk7C', 'Marija', 'Novak');

-- =============================================================================
-- Test Households
-- =============================================================================

INSERT INTO households (household_id, name, address, country) VALUES
(1, 'Studentski Dom Zagreb', 'Savska cesta 25, Zagreb', 'Croatia'),
(2, 'Apartman Centar', 'Ilica 123, Zagreb', 'Croatia');

-- =============================================================================
-- Household Members
-- =============================================================================

-- Household 1: Marin, Ana, Ivan (3 members)
INSERT INTO household_members (household_id, user_id, role) VALUES
(1, 1, 'admin'),  -- Marin is admin
(1, 2, 'member'), -- Ana
(1, 3, 'member'); -- Ivan

-- Household 2: Marija (single member household for testing)
INSERT INTO household_members (household_id, user_id, role) VALUES
(2, 4, 'admin');

-- =============================================================================
-- Test Bills (Module 2 - Cost Distribution)
-- Demonstrates different distribution strategies
-- =============================================================================

-- Bill 1: Rent - Equal distribution
INSERT INTO bills (bill_id, household_id, payer_id, title, amount, category, is_recurring, frequency, payment_status, due_date) VALUES
(1, 1, 1, 'Rent - January 2025', 3000.00, 'rent', 1, 'monthly', 'paid', '2025-01-05');

-- Bill 2: Electricity - Equal distribution
INSERT INTO bills (bill_id, household_id, payer_id, title, amount, category, is_recurring, frequency, payment_status, due_date) VALUES
(2, 1, 2, 'Electricity Bill - December', 450.00, 'utilities', 0, 'one-time', 'paid', '2024-12-20');

-- Bill 3: Groceries - Fixed amount distribution
INSERT INTO bills (bill_id, household_id, payer_id, title, amount, category, payment_status, due_date) VALUES
(3, 1, 3, 'Weekly Groceries', 380.00, 'food', 'paid', '2025-01-10');

-- Bill 4: Internet - Percentage distribution
INSERT INTO bills (bill_id, household_id, payer_id, title, amount, category, is_recurring, frequency, payment_status, due_date) VALUES
(4, 1, 1, 'Internet - January', 200.00, 'utilities', 1, 'monthly', 'pending', '2025-01-15');

-- Bill 5: Furniture - Fixed amount distribution
INSERT INTO bills (bill_id, household_id, payer_id, title, amount, category, payment_status) VALUES
(5, 1, 2, 'Living Room Table', 600.00, 'other', 'pending');

-- =============================================================================
-- Bill Distributions
-- Demonstrates 3 different strategies: equal, percentage, fixed
-- =============================================================================

-- Bill 1 distributions: Equal split (3000 / 3 = 1000 each)
-- Strategy: EQUAL DISTRIBUTION
INSERT INTO bill_distributions (bill_id, user_id, amount, distribution_strategy, status) VALUES
(1, 1, 1000.00, 'equal', 'paid'),
(1, 2, 1000.00, 'equal', 'paid'),
(1, 3, 1000.00, 'equal', 'paid');

-- Bill 2 distributions: Equal split (450 / 3 = 150 each)
-- Strategy: EQUAL DISTRIBUTION
INSERT INTO bill_distributions (bill_id, user_id, amount, distribution_strategy, status) VALUES
(2, 1, 150.00, 'equal', 'paid'),
(2, 2, 150.00, 'equal', 'paid'),
(2, 3, 150.00, 'equal', 'paid');

-- Bill 3 distributions: Fixed amounts (custom split)
-- Strategy: FIXED AMOUNT DISTRIBUTION
INSERT INTO bill_distributions (bill_id, user_id, amount, distribution_strategy, status) VALUES
(3, 1, 100.00, 'fixed', 'paid'),  -- Marin bought less items
(3, 2, 150.00, 'fixed', 'paid'),  -- Ana
(3, 3, 130.00, 'fixed', 'paid');  -- Ivan

-- Bill 4 distributions: Percentage split (50%, 30%, 20%)
-- Strategy: PERCENTAGE DISTRIBUTION
-- Marin uses internet most for work/studies (50%), Ana (30%), Ivan (20%)
INSERT INTO bill_distributions (bill_id, user_id, amount, percentage, distribution_strategy, status) VALUES
(4, 1, 100.00, 50.00, 'percentage', 'pending'),
(4, 2, 60.00, 30.00, 'percentage', 'pending'),
(4, 3, 40.00, 20.00, 'percentage', 'pending');

-- Bill 5 distributions: Fixed amounts (not equal)
-- Strategy: FIXED AMOUNT DISTRIBUTION
INSERT INTO bill_distributions (bill_id, user_id, amount, distribution_strategy, status) VALUES
(5, 1, 250.00, 'fixed', 'pending'),
(5, 2, 250.00, 'fixed', 'pending'),
(5, 3, 100.00, 'fixed', 'pending'); -- Ivan contributed less

-- =============================================================================
-- Transactions (some payments completed)
-- =============================================================================

INSERT INTO transactions (bill_id, user_id, amount, status, notes) VALUES
(1, 1, 1000.00, 'completed', 'Rent payment - January'),
(1, 2, 1000.00, 'completed', 'Rent payment - January'),
(1, 3, 1000.00, 'completed', 'Rent payment - January'),
(2, 1, 150.00, 'completed', 'Electricity - December'),
(2, 2, 150.00, 'completed', 'Electricity - December'),
(2, 3, 150.00, 'completed', 'Electricity - December'),
(3, 1, 100.00, 'completed', 'Groceries share'),
(3, 2, 150.00, 'completed', 'Groceries share'),
(3, 3, 130.00, 'completed', 'Groceries share');

-- =============================================================================
-- Shopping Lists (Module 3)
-- =============================================================================

INSERT INTO shopping_lists (list_id, household_id, name, created_by, is_active) VALUES
(1, 1, 'Weekly Groceries', 1, 1),
(2, 1, 'Household Supplies', 2, 1),
(3, 1, 'Party Shopping', 3, 0); -- Completed list

-- =============================================================================
-- Shopping Items
-- =============================================================================

-- List 1: Weekly Groceries (active)
INSERT INTO shopping_items (list_id, name, quantity, notes, completed, added_by) VALUES
(1, 'Milk', '2 liters', 'Low-fat', 0, 1),
(1, 'Bread', '3 pieces', 'Whole grain', 0, 1),
(1, 'Eggs', '1 dozen', '', 0, 2),
(1, 'Chicken breast', '1 kg', '', 0, 2),
(1, 'Tomatoes', '1 kg', '', 0, 3),
(1, 'Onions', '0.5 kg', '', 0, 3),
(1, 'Pasta', '2 packages', 'Spaghetti', 1, 1),
(1, 'Coffee', '1 pack', 'Ground coffee', 1, 2);

-- List 2: Household Supplies
INSERT INTO shopping_items (list_id, name, quantity, notes, completed, added_by) VALUES
(2, 'Dish soap', '1 bottle', '', 0, 2),
(2, 'Laundry detergent', '1 box', '', 0, 2),
(2, 'Toilet paper', '12 rolls', '', 1, 1),
(2, 'Paper towels', '6 rolls', '', 0, 3);

-- List 3: Party Shopping (completed)
INSERT INTO shopping_items (list_id, name, quantity, notes, completed, added_by) VALUES
(3, 'Pizza', '3 large', 'Margherita', 1, 3),
(3, 'Soda', '6 bottles', '2L each', 1, 3),
(3, 'Chips', '5 bags', '', 1, 1);

-- =============================================================================
-- Tasks (Module 4)
-- =============================================================================

INSERT INTO tasks (task_id, household_id, title, description, assigned_to, created_by, difficulty, estimated_duration, status, priority, due_date) VALUES
(1, 1, 'Clean kitchen', 'Deep clean kitchen including oven and refrigerator', 1, 1, 'medium', 90, 'pending', 3, '2025-01-20'),
(2, 1, 'Take out trash', 'Take all trash bins to street for pickup', 2, 1, 'easy', 15, 'pending', 2, '2025-01-18'),
(3, 1, 'Vacuum living room', 'Vacuum and mop living room floor', 3, 2, 'easy', 30, 'in_progress', 2, '2025-01-19'),
(4, 1, 'Clean bathroom', 'Clean toilet, shower, sink, and mirrors', 1, 2, 'medium', 60, 'completed', 3, '2025-01-15'),
(5, 1, 'Water plants', 'Water all indoor plants', 2, 3, 'easy', 10, 'pending', 1, '2025-01-21'),
(6, 1, 'Organize storage', 'Sort and organize storage room', 3, 3, 'hard', 120, 'pending', 2, '2025-01-25'),
(7, 1, 'Buy light bulbs', 'Replace burnt light bulbs in hallway', NULL, 1, 'easy', 20, 'pending', 4, '2025-01-17');

-- =============================================================================
-- Summary Statistics
-- =============================================================================

-- Total users: 4
-- Total households: 2
-- Total bills: 5
-- Total distributions: 14 (demonstrating 3 different strategies)
-- Total shopping lists: 3
-- Total shopping items: 15
-- Total tasks: 7

-- Distribution Strategies Demonstrated:
-- 1. Equal Distribution: Bills 1, 2 (rent, electricity)
-- 2. Percentage Distribution: Bill 4 (internet - 50%, 30%, 20%)
-- 3. Fixed Amount Distribution: Bills 3, 5 (groceries, furniture)
