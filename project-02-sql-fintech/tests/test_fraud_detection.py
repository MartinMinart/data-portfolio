import sqlite3
import pytest
from pathlib import Path

@pytest.fixture
def db_connection():
    """Создаёт тестовую БД"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE transactions (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            transaction_date TEXT,
            is_fraud INTEGER
        )
    ''')
    
    test_data = [
        (1, 101, 150.0, '2024-01-01', 0),
        (2, 101, 5000.0, '2024-01-02', 1),
        (3, 102, 75.0, '2024-01-01', 0),
        (4, 103, 10000.0, '2024-01-03', 1),
        (5, 104, 200.0, '2024-01-01', 0),
    ]
    
    cursor.executemany(
        'INSERT INTO transactions VALUES (?, ?, ?, ?, ?)',
        test_data
    )
    conn.commit()
    
    yield conn
    conn.close()

def test_fraud_detection_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) as fraud_count FROM transactions WHERE is_fraud = 1')
    result = cursor.fetchone()
    assert result[0] == 2

def test_high_amount_transactions(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) as high_amount_count FROM transactions WHERE amount > 1000')
    result = cursor.fetchone()
    assert result[0] == 2

def test_customer_transaction_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT customer_id, COUNT(*) as tx_count
        FROM transactions
        GROUP BY customer_id
        ORDER BY tx_count DESC
        LIMIT 1
    ''')
    result = cursor.fetchone()
    assert result[0] == 101
    assert result[1] == 2
