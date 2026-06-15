"""
============================================
SQL Fintech Analysis Project
Инициализация базы данных SQLite
Генерация тестовых данных (100 клиентов, ~500 транзакций)
============================================
"""

import sqlite3
import random
from datetime import datetime, timedelta
import os

# Константы
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'fintech_transactions.db')
NUM_CUSTOMERS = 100
NUM_TRANSACTIONS_PER_CUSTOMER = 5  # в среднем

# Категории транзакций с весами и типичными суммами
CATEGORIES = {
    'Groceries': {'weight': 25, 'min_amount': 300, 'max_amount': 5000, 'fraud_prob': 0.01},
    'Electronics': {'weight': 15, 'min_amount': 2000, 'max_amount': 50000, 'fraud_prob': 0.08},
    'Restaurants': {'weight': 20, 'min_amount': 500, 'max_amount': 5000, 'fraud_prob': 0.02},
    'Transport': {'weight': 15, 'min_amount': 200, 'max_amount': 2000, 'fraud_prob': 0.01},
    'Clothing': {'weight': 10, 'min_amount': 1000, 'max_amount': 15000, 'fraud_prob': 0.03},
    'Travel': {'weight': 5, 'min_amount': 3000, 'max_amount': 100000, 'fraud_prob': 0.05},
    'Entertainment': {'weight': 5, 'min_amount': 500, 'max_amount': 10000, 'fraud_prob': 0.02},
    'Health': {'weight': 5, 'min_amount': 500, 'max_amount': 20000, 'fraud_prob': 0.01},
}

# Страны для транзакций
COUNTRIES_NORMAL = ['RU'] * 90 + ['KZ', 'BY', 'AM']  # 90% Россия
COUNTRIES_SUSPICIOUS = ['NG', 'US', 'CN', 'CY', 'GB']  # Подозрительные юрисдикции

# Мерчанты по категориям
MERCHANTS = {
    'Groceries': ['Перекресток', 'Пятерочка', 'ВкусВилл', 'Азбука Вкуса', 'Магнит'],
    'Electronics': ['М.Видео', 'DNS', 'Ситилинк', 'Apple Store', 'Samsung'],
    'Restaurants': ['Теремок', 'Кофемания', 'Макдоналдс', 'Бургер Кинг', 'Суши Вок'],
    'Transport': ['Яндекс.Такси', 'Ситимобил', 'Делимобиль', 'Метро', 'РЖД'],
    'Clothing': ['Zara', 'H&M', 'Uniqlo', 'Sportmaster', 'Лэтуаль'],
    'Travel': ['Аэрофлот', 'S7 Airlines', 'Booking.com', 'Ostrovok', 'Туту.ру'],
    'Entertainment': ['Кино Окко', 'Иви', 'Яндекс.Плюс', 'Ticketland', 'Москино'],
    'Health': ['Аптека Ригла', 'Еаптека', 'Здравсити', 'Инвитро', 'Гемотест'],
}


def create_database():
    """Создание базы данных и таблиц"""
    # Удаляем старый файл БД если существует
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    # Создаем директорию data если нет
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Читаем SQL схему из файла
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Выполняем схему (создание таблиц и индексов)
    cursor.executescript(schema_sql)
    conn.commit()
    print(f"✓ База данных создана: {DB_PATH}")
    
    return conn, cursor


def generate_customers(cursor, num_customers=100):
    """Генерация тестовых клиентов"""
    first_names = [
        'Иван', 'Алексей', 'Дмитрий', 'Сергей', 'Андрей', 'Максим', 'Александр', 'Михаил',
        'Мария', 'Елена', 'Ольга', 'Наталья', 'Анна', 'Екатерина', 'Светлана', 'Татьяна',
        'Петр', 'Владимир', 'Николай', 'Игорь', 'Юлия', 'Анастасия', 'Виктория', 'Дарья'
    ]
    last_names = [
        'Петров', 'Иванов', 'Сидоров', 'Козлов', 'Новиков', 'Волков', 'Лебедев', 'Морозов',
        'Павлов', 'Соколов', 'Федоров', 'Крылов', 'Зайцев', 'Орлов', 'Титов', 'Смирнов',
        'Кузнецов', 'Попов', 'Васильев', 'Михайлов', 'Захаров', 'Алексеев', 'Борисов'
    ]
    segments = ['Premium', 'Standard', 'Basic']
    segment_weights = [20, 50, 30]  # 20% премиум, 50% стандарт, 30% базовый
    
    customers = []
    for i in range(1, num_customers + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        # Дата регистрации: от 2 года назад до 1 месяца назад
        days_ago = random.randint(30, 730)
        reg_date = datetime.now() - timedelta(days=days_ago)
        credit_score = random.randint(450, 850)
        segment = random.choices(segments, weights=segment_weights)[0]
        
        customers.append((i, first_name, last_name, reg_date.strftime('%Y-%m-%d'), credit_score, segment))
    
    cursor.executemany('''
        INSERT INTO customers (customer_id, first_name, last_name, registration_date, credit_score, segment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', customers)
    
    print(f"✓ Сгенерировано {num_customers} клиентов")
    return customers


def generate_transactions(cursor, customers):
    """Генерация транзакций для клиентов"""
    transactions = []
    transaction_id = 1
    
    start_date = datetime.now() - timedelta(days=365)  # Данные за последний год
    
    for customer_id, first_name, last_name, reg_date_str, credit_score, segment in customers:
        reg_date = datetime.strptime(reg_date_str, '%Y-%m-%d')
        # Количество транзакций зависит от сегмента
        if segment == 'Premium':
            num_txns = random.randint(8, 15)
        elif segment == 'Standard':
            num_txns = random.randint(4, 8)
        else:  # Basic
            num_txns = random.randint(2, 5)
        
        for _ in range(num_txns):
            # Случайная дата между регистрацией и сейчас
            days_since_reg = (datetime.now() - reg_date).days
            if days_since_reg < 1:
                continue
            txn_date = reg_date + timedelta(days=random.randint(0, days_since_reg))
            
            # Выбор категории с учетом весов
            category = random.choices(
                list(CATEGORIES.keys()),
                weights=[CATEGORIES[c]['weight'] for c in CATEGORIES.keys()]
            )[0]
            
            cat_info = CATEGORIES[category]
            amount = round(random.uniform(cat_info['min_amount'], cat_info['max_amount']), 2)
            
            # Определение мошенничества
            is_fraud = 0
            country = random.choice(COUNTRIES_NORMAL)
            
            # Фрод более вероятен для Electronics, больших сумм, подозрительных стран
            if random.random() < cat_info['fraud_prob']:
                is_fraud = 1
                country = random.choice(COUNTRIES_SUSPICIOUS)
                # Для фрода увеличиваем сумму
                amount = round(amount * random.uniform(2, 10), 2)
            
            merchant = random.choice(MERCHANTS.get(category, ['Unknown Merchant']))
            
            transactions.append((
                transaction_id,
                customer_id,
                txn_date.strftime('%Y-%m-%d %H:%M:%S'),
                amount,
                category,
                merchant,
                country,
                is_fraud
            ))
            transaction_id += 1
    
    # Сортируем транзакции по дате
    transactions.sort(key=lambda x: x[2])
    
    cursor.executemany('''
        INSERT INTO transactions (transaction_id, customer_id, transaction_date, amount, category, merchant_name, country, is_fraud)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', transactions)
    
    print(f"✓ Сгенерировано {len(transactions)} транзакций")
    return len(transactions)


def print_statistics(cursor):
    """Вывод статистики по базе данных"""
    print("\n" + "="*50)
    print("СТАТИСТИКА БАЗЫ ДАННЫХ")
    print("="*50)
    
    # Общее количество клиентов
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]
    print(f"Всего клиентов: {total_customers}")
    
    # Общее количество транзакций
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]
    print(f"Всего транзакций: {total_transactions}")
    
    # Объем транзакций
    cursor.execute("SELECT SUM(amount), AVG(amount) FROM transactions")
    total_volume, avg_amount = cursor.fetchone()
    print(f"Общий объем: {total_volume:,.2f} RUB")
    print(f"Средняя транзакция: {avg_amount:,.2f} RUB")
    
    # Фрод статистика
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN is_fraud = 1 THEN 1 END),
            SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END),
            COUNT(*)
        FROM transactions
    """)
    fraud_count, fraud_volume, total = cursor.fetchone()
    fraud_rate = fraud_count / total * 100 if total > 0 else 0
    print(f"\nФрод-транзакции: {fraud_count} ({fraud_rate:.2f}%)")
    print(f"Объем фрода: {fraud_volume:,.2f} RUB")
    
    # Распределение по сегментам
    cursor.execute("""
        SELECT segment, COUNT(*) 
        FROM customers 
        GROUP BY segment
    """)
    print("\nКлиенты по сегментам:")
    for segment, count in cursor.fetchall():
        print(f"  {segment}: {count}")
    
    # Топ категорий по объему
    cursor.execute("""
        SELECT category, COUNT(*), SUM(amount)
        FROM transactions
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 5
    """)
    print("\nТоп-5 категорий по объему:")
    for category, count, volume in cursor.fetchall():
        print(f"  {category}: {count} транзакций, {volume:,.2f} RUB")
    
    print("="*50)


def main():
    """Основная функция"""
    print("Запуск инициализации базы данных...")
    
    # Создание БД
    conn, cursor = create_database()
    
    try:
        # Генерация клиентов
        customers = generate_customers(cursor, NUM_CUSTOMERS)
        
        # Генерация транзакций
        total_txns = generate_transactions(cursor, customers)
        
        # Коммит изменений
        conn.commit()
        
        # Вывод статистики
        print_statistics(cursor)
        
        print(f"\n✓ База данных успешно создана и заполнена!")
        print(f"Путь к файлу: {os.path.abspath(DB_PATH)}")
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
