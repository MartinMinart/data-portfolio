#!/bin/bash
# Скрипт для импорта данных из fintech проекта в PostgreSQL

echo "📊 Импорт данных в аналитическую БД..."

# Путь к твоей SQLite базе из fintech проекта
SQLITE_DB="../project-02-sql-fintech/data/fintech_transactions.db"

if [ -f "$SQLITE_DB" ]; then
    echo "✅ Найдена база fintech_transactions.db"
    
    # Импорт данных через временный CSV
    sqlite3 "$SQLITE_DB" << 'EOSQL'
.mode csv
.headers on
.output /tmp/transactions.csv
SELECT * FROM transactions;

.output /tmp/customers.csv
SELECT * FROM customers;
.output stdout
EOSQL
    
    # Загрузка в PostgreSQL
    docker exec -i data-portfolio-postgres psql -U analyst -d analytics << 'EOSQL'
\copy analytics.transactions FROM '/tmp/transactions.csv' DELIMITER ',' CSV HEADER;
\copy analytics.customers FROM '/tmp/customers.csv' DELIMITER ',' CSV HEADER;
EOSQL
    
    echo "✅ Данные импортированы!"
else
    echo "⚠️ База не найдена. Используются тестовые данные."
fi
