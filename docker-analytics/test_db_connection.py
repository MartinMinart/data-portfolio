import psycopg2

try:
    # Подключаемся к PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        port=5435,
        database="analytics",
        user="postgres",
        password="postgres123"
    )
    
    print("✅ Подключение к PostgreSQL успешно!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analytics.users;")
    users = cursor.fetchall()
    
    print("\n📊 Список пользователей:")
    for user in users:
        print(f"  👤 ID: {user[0]}, Имя: {user[1]}, Email: {user[2]}")
    
    cursor.execute("SELECT COUNT(*) FROM analytics.products;")
    products_count = cursor.fetchone()[0]
    print(f"\n📦 Всего продуктов: {products_count}")
    
    cursor.close()
    conn.close()
    print("\n✅ Работа завершена успешно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
