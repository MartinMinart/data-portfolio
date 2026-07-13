-- Создаём схему
CREATE SCHEMA IF NOT EXISTS analytics;

-- Создаём таблицу users
CREATE TABLE IF NOT EXISTS analytics.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Создаём таблицу products
CREATE TABLE IF NOT EXISTS analytics.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50)
);

-- Вставляем тестовые данные
INSERT INTO analytics.users (username, email) VALUES
    ('john_doe', 'john@example.com'),
    ('jane_smith', 'jane@example.com'),
    ('bob_wilson', 'bob@example.com');

INSERT INTO analytics.products (product_name, price, category) VALUES
    ('Laptop', 999.99, 'Electronics'),
    ('Mouse', 29.99, 'Accessories'),
    ('Keyboard', 79.99, 'Accessories'),
    ('Monitor', 299.99, 'Electronics'),
    ('Desk', 199.99, 'Furniture');

-- Проверяем
SELECT 'users_count' as metric, COUNT(*) as value FROM analytics.users
UNION ALL
SELECT 'products_count' as metric, COUNT(*) as value FROM analytics.products;
