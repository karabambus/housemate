-- HouseMate Database Schema
-- Based on teammates' ER diagram (Otherspart/ERDijagram(Modul_1,2,3).drawio)
-- SQLite database for fast development

-- =============================================================================
-- Core Tables
-- =============================================================================

-- Users table (Korisnik)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    avatar_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Households table (Kucanstvo)
CREATE TABLE IF NOT EXISTS households (
    household_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    country TEXT DEFAULT 'Croatia',
    avatar_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Household Members (N:M relationship between users and households)
CREATE TABLE IF NOT EXISTS household_members (
    household_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT DEFAULT 'member' CHECK(role IN ('member', 'admin')),
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (household_id, user_id),
    FOREIGN KEY (household_id) REFERENCES households(household_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =============================================================================
-- Module 2: Cost Distribution (Raspodjela troškova)
-- PRIMARY MODULE for demonstrating ALL SOLID principles
-- =============================================================================

-- Bills table (Trosak)
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL,
    payer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK(amount > 0),
    category TEXT DEFAULT 'other' CHECK(category IN ('rent', 'utilities', 'food', 'transport', 'entertainment', 'other')),
    is_recurring BOOLEAN DEFAULT 0,
    frequency TEXT DEFAULT 'one-time' CHECK(frequency IN ('one-time', 'weekly', 'monthly', 'yearly')),
    payment_status TEXT DEFAULT 'pending' CHECK(payment_status IN ('pending', 'paid')),
    receipt_url TEXT,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (household_id) REFERENCES households(household_id) ON DELETE CASCADE,
    FOREIGN KEY (payer_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Bill Distributions table (Raspodjela troška)
-- Stores how much each household member owes for a bill
-- Supports different distribution strategies: equal, percentage, fixed
CREATE TABLE IF NOT EXISTS bill_distributions (
    distribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK(amount >= 0),
    percentage DECIMAL(5, 2) CHECK(percentage >= 0 AND percentage <= 100),
    distribution_strategy TEXT DEFAULT 'equal' CHECK(distribution_strategy IN ('equal', 'percentage', 'fixed')),
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'paid')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Transactions table (Transakcija)
-- Records actual payments made by users
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK(amount > 0),
    status TEXT DEFAULT 'completed' CHECK(status IN ('pending', 'completed', 'failed')),
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =============================================================================
-- Module 3: Shopping List (Shopping lista)
-- SECONDARY MODULE - demonstrates SRP and DIP
-- =============================================================================

-- Shopping Lists table
CREATE TABLE IF NOT EXISTS shopping_lists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    created_by INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (household_id) REFERENCES households(household_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Shopping Items table
CREATE TABLE IF NOT EXISTS shopping_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    quantity TEXT,
    notes TEXT,
    completed BOOLEAN DEFAULT 0,
    added_by INTEGER,
    completed_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (list_id) REFERENCES shopping_lists(list_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (completed_by) REFERENCES users(user_id) ON DELETE SET NULL
);

-- =============================================================================
-- Module 4: Task List (Lista zadataka)
-- TERTIARY MODULE - additional SOLID examples
-- =============================================================================

-- Tasks table (Zadatak)
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    assigned_to INTEGER,
    created_by INTEGER NOT NULL,
    difficulty TEXT DEFAULT 'medium' CHECK(difficulty IN ('easy', 'medium', 'hard')),
    estimated_duration INTEGER, -- in minutes
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed')),
    priority INTEGER DEFAULT 2 CHECK(priority BETWEEN 1 AND 5), -- 1=lowest, 5=highest
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (household_id) REFERENCES households(household_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =============================================================================
-- Indexes for performance
-- =============================================================================

-- User indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Household members indexes
CREATE INDEX IF NOT EXISTS idx_household_members_household ON household_members(household_id);
CREATE INDEX IF NOT EXISTS idx_household_members_user ON household_members(user_id);

-- Bills indexes
CREATE INDEX IF NOT EXISTS idx_bills_household ON bills(household_id);
CREATE INDEX IF NOT EXISTS idx_bills_payer ON bills(payer_id);
CREATE INDEX IF NOT EXISTS idx_bills_created_at ON bills(created_at);

-- Bill distributions indexes
CREATE INDEX IF NOT EXISTS idx_bill_distributions_bill ON bill_distributions(bill_id);
CREATE INDEX IF NOT EXISTS idx_bill_distributions_user ON bill_distributions(user_id);

-- Shopping lists indexes
CREATE INDEX IF NOT EXISTS idx_shopping_lists_household ON shopping_lists(household_id);
CREATE INDEX IF NOT EXISTS idx_shopping_items_list ON shopping_items(list_id);

-- Tasks indexes
CREATE INDEX IF NOT EXISTS idx_tasks_household ON tasks(household_id);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);

-- =============================================================================
-- Views for convenience
-- =============================================================================

-- View: User's household information
CREATE VIEW IF NOT EXISTS user_households AS
SELECT
    u.user_id,
    u.email,
    u.first_name,
    u.last_name,
    h.household_id,
    h.name AS household_name,
    hm.role,
    hm.joined_at
FROM users u
JOIN household_members hm ON u.user_id = hm.user_id
JOIN households h ON hm.household_id = h.household_id;

-- View: Bill summary with payer information
CREATE VIEW IF NOT EXISTS bill_summary AS
SELECT
    b.bill_id,
    b.title,
    b.amount,
    b.category,
    b.payment_status,
    b.created_at,
    u.first_name || ' ' || u.last_name AS payer_name,
    u.email AS payer_email,
    h.household_id,
    h.name AS household_name
FROM bills b
JOIN users u ON b.payer_id = u.user_id
JOIN households h ON b.household_id = h.household_id;

-- View: Bill distributions with user details
CREATE VIEW IF NOT EXISTS distribution_details AS
SELECT
    bd.distribution_id,
    bd.bill_id,
    b.title AS bill_title,
    b.amount AS total_amount,
    bd.amount AS user_amount,
    bd.percentage,
    bd.distribution_strategy,
    bd.status,
    u.user_id,
    u.first_name || ' ' || u.last_name AS user_name,
    u.email AS user_email
FROM bill_distributions bd
JOIN bills b ON bd.bill_id = b.bill_id
JOIN users u ON bd.user_id = u.user_id;

-- View: Task assignments
CREATE VIEW IF NOT EXISTS task_assignments AS
SELECT
    t.task_id,
    t.title,
    t.description,
    t.difficulty,
    t.status,
    t.due_date,
    assigned.first_name || ' ' || assigned.last_name AS assigned_to_name,
    assigned.email AS assigned_to_email,
    creator.first_name || ' ' || creator.last_name AS created_by_name,
    h.household_id,
    h.name AS household_name
FROM tasks t
LEFT JOIN users assigned ON t.assigned_to = assigned.user_id
JOIN users creator ON t.created_by = creator.user_id
JOIN households h ON t.household_id = h.household_id;
