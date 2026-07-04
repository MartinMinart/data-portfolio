-- Создаём схему для аналитики
CREATE SCHEMA IF NOT EXISTS analytics;

-- Таблица для транзакций (из твоего fintech проекта)
CREATE TABLE IF NOT EXISTS analytics.transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    amount DECIMAL(10,2),
    transaction_date DATE,
    transaction_type VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица для клиентов
CREATE TABLE IF NOT EXISTS analytics.customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    registration_date DATE,
    country VARCHAR(50),
    risk_score INTEGER DEFAULT 0
);

-- Вставляем пример данных (можно загрузить из твоих CSV)
INSERT INTO analytics.customers (name, email, registration_date, country) VALUES
    ('Тестовый Клиент 1', 'test1@example.com', '2024-01-01', 'RU'),
    ('Тестовый Клиент 2', 'test2@example.com', '2024-02-15', 'RU'),
    ('Тестовый Клиент 3', 'test3@example.com', '2024-03-20', 'KZ');

INSERT INTO analytics.transactions (customer_id, amount, transaction_date, transaction_type, status) VALUES
    (1, 1500.00, '2024-06-01', 'payment', 'completed'),
    (1, 2500.00, '2024-06-05', 'transfer', 'completed'),
    (2, 500.00, '2024-06-02', 'payment', 'completed'),
    (3, 10000.00, '2024-06-03', 'payment', 'pending'),
    (1, 3500.00, '2024-06-07', 'transfer', 'completed');

-- Гранты на доступ
GRANT ALL PRIVILEGES ON SCHEMA analytics TO analyst;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO analyst;
