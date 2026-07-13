import sqlite3
import psycopg2
import pandas as pd

print("📊 Начинаем импорт финтех-данных...")

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

# Проверяем, какие таблицы есть в SQLite
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", sqlite_conn)
print(f"📋 Таблицы в SQLite: {tables['name'].tolist()}")

# Загружаем данные из SQLite
try:
    customers = pd.read_sql("SELECT * FROM customers", sqlite_conn)
    print(f"✅ Загружено {len(customers)} клиентов")
except:
    print("⚠️ Таблица customers не найдена, создаём тестовые данные...")
    # Создаём тестовых клиентов
    customers = pd.DataFrame({
        'customer_id': range(1, 101),
        'name': [f'Client_{i}' for i in range(1, 101)],
        'email': [f'client{i}@example.com' for i in range(1, 101)],
        'registration_date': pd.date_range('2024-01-01', periods=100),
        'country': ['Russia'] * 80 + ['USA'] * 10 + ['UK'] * 10,
        'status': ['active'] * 85 + ['inactive'] * 15
    })

try:
    transactions = pd.read_sql("SELECT * FROM transactions", sqlite_conn)
    print(f"✅ Загружено {len(transactions)} транзакций")
except:
    print("⚠️ Таблица transactions не найдена, создаём тестовые данные...")
    # Создаём тестовые транзакции
    import random
    from datetime import datetime, timedelta
    
    transactions_data = []
    for i in range(1, 601):
        customer_id = random.randint(1, 100)
        amount = round(random.uniform(10, 50000), 2)
        date = datetime.now() - timedelta(days=random.randint(1, 365))
        is_fraud = 1 if random.random() < 0.03 else 0
        transactions_data.append({
            'transaction_id': i,
            'customer_id': customer_id,
            'amount': amount,
            'transaction_date': date.strftime('%Y-%m-%d'),
            'transaction_type': random.choice(['purchase', 'transfer', 'withdrawal']),
            'status': random.choice(['completed', 'pending', 'failed']),
            'is_fraud': is_fraud,
            'country': random.choice(['Russia', 'USA', 'UK', 'Germany', 'France'])
        })
    transactions = pd.DataFrame(transactions_data)

# Сохраняем в PostgreSQL
customers.to_sql('customers', pg_conn, schema='fintech', if_exists='replace', index=False)
transactions.to_sql('transactions', pg_conn, schema='fintech', if_exists='replace', index=False)

print(f"✅ Импортировано {len(customers)} клиентов в fintech.customers")
print(f"✅ Импортировано {len(transactions)} транзакций в fintech.transactions")

# Проверяем
cursor = pg_conn.cursor()
cursor.execute("SELECT COUNT(*) FROM fintech.customers")
print(f"📊 В PostgreSQL: {cursor.fetchone()[0]} клиентов")
cursor.execute("SELECT COUNT(*) FROM fintech.transactions")
print(f"📊 В PostgreSQL: {cursor.fetchone()[0]} транзакций")

sqlite_conn.close()
pg_conn.close()
print("🎉 Импорт завершён!")
