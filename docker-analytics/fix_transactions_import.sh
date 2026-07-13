#!/bin/bash

echo "🔧 Исправляем импорт транзакций..."

# Экспортируем из SQLite с правильными колонками
sqlite3 /workspaces/data-portfolio/project-02-sql-fintech/data/fintech_transactions.db << 'SQL'
.headers on
.mode csv
.output /tmp/transactions_fixed.csv
SELECT 
  transaction_id,
  customer_id,
  amount,
  DATE(transaction_date) as transaction_date,
  category as transaction_type,
  merchant_name,
  'completed' as status,
  is_fraud,
  country
FROM transactions;
.quit
SQL

echo "📋 Первые 5 строк CSV:"
head -5 /tmp/transactions_fixed.csv

# Копируем в контейнер
docker cp /tmp/transactions_fixed.csv data-portfolio-postgres:/tmp/

# Создаём правильную структуру таблицы и импортируем
docker exec -i data-portfolio-postgres psql -U postgres -d analytics << 'PSQL'
-- Удаляем старую таблицу и создаём заново
DROP TABLE IF EXISTS fintech.transactions CASCADE;

CREATE TABLE fintech.transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount DECIMAL(10,2),
    transaction_date DATE,
    transaction_type VARCHAR(50),
    merchant_name VARCHAR(100),
    status VARCHAR(20),
    is_fraud INTEGER,
    country VARCHAR(50)
);

-- Импортируем данные
\COPY fintech.transactions FROM '/tmp/transactions_fixed.csv' DELIMITER ',' CSV HEADER;

-- Проверяем
SELECT COUNT(*) as transaction_count FROM fintech.transactions;
SELECT * FROM fintech.transactions LIMIT 5;
PSQL

echo "✅ Импорт завершён!"
