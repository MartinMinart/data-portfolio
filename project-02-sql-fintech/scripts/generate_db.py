import sqlite3
import random
from datetime import datetime, timedelta

# Настройки
DB_PATH = 'data/transactions.db'
NUM_RECORDS = 500

# Данные для генерации
categories = ['Groceries', 'Electronics', 'Restaurants', 'Travel', 'Utilities', 'Entertainment', 'Fuel']
cities = ['Moscow', 'St.Petersburg', 'Kazan', 'Novosibirsk', 'Yekaterinburg']
channels = ['online', 'offline', 'atm']

def generate_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создаем таблицы
    with open('sql/schema.sql', 'r') as f:
        cursor.executescript(f.read())
    
    # Генерируем записи
    records = []
    start_date = datetime(2026, 1, 1)
    
    for i in range(NUM_RECORDS):
        txn_id = i + 1
        cust_id = random.randint(101, 150) # 50 клиентов
        
        # Разброс дат
        days_offset = random.randint(0, 90)
        txn_date = start_date + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        amount = round(random.uniform(100, 15000), 2)
        # Шанс на крупную сумму
        if random.random() < 0.05:
            amount = round(random.uniform(50000, 200000), 2)
            
        category = random.choice(categories)
        city = random.choice(cities)
        channel = random.choice(channels)
        
        # Логика фрода: крупные суммы ночью или в азартных играх
        is_fraud = 0
        if amount > 100000 and (txn_date.hour < 6 or txn_date.hour > 23):
            is_fraud = 1
        if category == 'Gambling': # Добавим категорию если нужно
             pass 

        records.append((txn_id, cust_id, txn_date.strftime('%Y-%m-%d %H:%M:%S'), amount, category, city, is_fraud, channel))
    
    cursor.executemany("""
        INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    conn.close()
    print(f"✅ База данных создана: {DB_PATH}")
    print(f"📊 Записей: {NUM_RECORDS}")

if __name__ == "__main__":
    generate_data()