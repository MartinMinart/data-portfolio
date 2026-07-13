import sqlite3
import psycopg2
import pandas as pd

# Подключение к SQLite
sqlite_conn = sqlite3.connect('/workspaces/data-portfolio/project-02-sql-fintech/data/fintech_transactions.db')

# Подключение к PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    port=5435,
    database="analytics",
    user="postgres",
    password="postgres123"
)

# Чтение таблиц из SQLite
customers = pd.read_sql("SELECT * FROM customers", sqlite_conn)
transactions = pd.read_sql("SELECT * FROM transactions", sqlite_conn)

print(f"✅ Загружено {len(customers)} клиентов")
print(f"✅ Загружено {len(transactions)} транзакций")

# Сохранение в PostgreSQL
customers.to_sql('customers', pg_conn, schema='fintech', if_exists='replace', index=False)
transactions.to_sql('transactions', pg_conn, schema='fintech', if_exists='replace', index=False)

print("✅ Данные импортированы в PostgreSQL!")

sqlite_conn.close()
pg_conn.close()
