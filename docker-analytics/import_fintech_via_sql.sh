#!/bin/bash

echo "📊 Начинаем импорт финтех-данных через SQL..."

# Получаем данные из SQLite в CSV
echo "1️⃣ Экспортируем данные из SQLite..."
sqlite3 /workspaces/data-portfolio/project-02-sql-fintech/data/fintech_transactions.db << 'SQL'
.headers on
.mode csv
.output /tmp/customers.csv
SELECT * FROM customers;
.output /tmp/transactions.csv
SELECT * FROM transactions;
.quit
SQL

echo "2️⃣ Копируем CSV в контейнер..."
docker cp /tmp/customers.csv data-portfolio-postgres:/tmp/
docker cp /tmp/transactions.csv data-portfolio-postgres:/tmp/

echo "3️⃣ Импортируем в PostgreSQL..."
docker exec -i data-portfolio-postgres psql -U postgres -d analytics << 'PSQL'
-- Создаём схему если её нет
CREATE SCHEMA IF NOT EXISTS fintech;

-- Создаём таблицы
CREATE TABLE IF NOT EXISTS fintech.customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    registration_date DATE,
    country VARCHAR(50),
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS fintech.transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount DECIMAL(10,2),
    transaction_date DATE,
    transaction_type VARCHAR(50),
    status VARCHAR(20),
    is_fraud INTEGER,
    country VARCHAR(50)
);

-- Очищаем таблицы (на случай повторного импорта)
TRUNCATE fintech.customers CASCADE;
TRUNCATE fintech.transactions CASCADE;

-- Импортируем данные
\COPY fintech.customers FROM '/tmp/customers.csv' DELIMITER ',' CSV HEADER;
\COPY fintech.transactions FROM '/tmp/transactions.csv' DELIMITER ',' CSV HEADER;

-- Проверяем
SELECT 'customers' as table_name, COUNT(*) as count FROM fintech.customers
UNION ALL
SELECT 'transactions' as table_name, COUNT(*) as count FROM fintech.transactions;
PSQL

echo "4️⃣ Проверяем данные..."
docker exec data-portfolio-postgres psql -U postgres -d analytics -c "SELECT COUNT(*) FROM fintech.customers;"
docker exec data-portfolio-postgres psql -U postgres -d analytics -c "SELECT COUNT(*) FROM fintech.transactions;"
docker exec data-portfolio-postgres psql -U postgres -d analytics -c "SELECT * FROM fintech.customers LIMIT 5;"
docker exec data-portfolio-postgres psql -U postgres -d analytics -c "SELECT * FROM fintech.transactions LIMIT 5;"

echo "✅ Импорт завершён!"
