-- Схема базы данных для анализа финансовых транзакций
-- Таблица: transactions

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    transaction_date DATETIME NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    merchant_city TEXT,
    is_fraud INTEGER DEFAULT 0, -- 1 = мошенничество, 0 = норма
    channel TEXT -- online, offline, atm
);

-- Индексы для ускорения выборки
CREATE INDEX idx_customer ON transactions(customer_id);
CREATE INDEX idx_date ON transactions(transaction_date);
CREATE INDEX idx_fraud ON transactions(is_fraud);