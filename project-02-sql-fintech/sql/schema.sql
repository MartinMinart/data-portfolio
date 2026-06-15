-- ============================================
-- SQL Fintech Analysis Project
-- Schema: Transactions, Customers, Fraud Labels
-- Database: SQLite
-- ============================================

-- Таблица клиентов
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    registration_date DATE NOT NULL,
    credit_score INTEGER CHECK(credit_score BETWEEN 300 AND 850),
    segment TEXT CHECK(segment IN ('Premium', 'Standard', 'Basic'))
);

-- Таблица транзакций
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    category TEXT NOT NULL,
    merchant_name TEXT,
    country TEXT DEFAULT 'RU',
    is_fraud INTEGER DEFAULT 0 CHECK(is_fraud IN (0, 1)),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Индексы для ускорения запросов
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_fraud ON transactions(is_fraud);
CREATE INDEX IF NOT EXISTS idx_customers_segment ON customers(segment);
