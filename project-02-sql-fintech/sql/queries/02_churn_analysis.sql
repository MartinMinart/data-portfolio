-- ============================================
-- Query 02: Churn Analysis (Анализ оттока)
-- Выявление клиентов с признаками оттока через LAG
-- ============================================

-- Задача: Найти клиентов, у которых увеличился интервал между транзакциями
-- (признак снижения активности / возможного оттока)

WITH customer_transactions AS (
    SELECT 
        customer_id,
        transaction_id,
        transaction_date,
        amount,
        -- Время с предыдущей транзакции (LAG)
        LAG(transaction_date) OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date
        ) AS prev_transaction_date,
        -- Количество дней между транзакциями
        JULIANDAY(transaction_date) - JULIANDAY(
            LAG(transaction_date) OVER (
                PARTITION BY customer_id 
                ORDER BY transaction_date
            )
        ) AS days_since_last_txn,
        -- Сумма транзакции
        amount AS current_amount,
        -- Предыдущая сумма
        LAG(amount) OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date
        ) AS prev_amount,
        -- Ранг транзакции по времени (для клиента)
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date
        ) AS txn_sequence
    FROM transactions
),
churn_signals AS (
    SELECT 
        customer_id,
        transaction_id,
        transaction_date,
        ROUND(current_amount, 2) AS amount,
        txn_sequence,
        prev_transaction_date,
        ROUND(days_since_last_txn, 1) AS days_gap,
        ROUND(prev_amount, 2) AS prev_amount,
        -- Изменение суммы в %
        CASE 
            WHEN prev_amount > 0 THEN ROUND((current_amount - prev_amount) / prev_amount * 100, 1)
            ELSE NULL 
        END AS amount_change_pct,
        -- Флаг "большого разрыва" (>30 дней)
        CASE WHEN days_since_last_txn > 30 THEN 1 ELSE 0 END AS large_gap_flag,
        -- Средний интервал для клиента (оконная функция AVG)
        AVG(JULIANDAY(transaction_date) - JULIANDAY(
            LAG(transaction_date) OVER (
                PARTITION BY customer_id 
                ORDER BY transaction_date
            )
        )) OVER (PARTITION BY customer_id) AS avg_days_gap_for_customer
    FROM customer_transactions
    WHERE prev_transaction_date IS NOT NULL
)
SELECT 
    cs.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.segment,
    c.credit_score,
    MAX(cs.txn_sequence) AS total_transactions,
    ROUND(AVG(cs.days_gap), 1) AS avg_days_between_txns,
    MAX(cs.days_gap) AS max_days_gap,
    SUM(cs.large_gap_flag) AS count_large_gaps,
    ROUND(AVG(cs.amount_change_pct), 1) AS avg_amount_change_pct,
    MIN(cs.transaction_date) AS first_txn,
    MAX(cs.transaction_date) AS last_txn,
    -- Дней с последней транзакции (на момент 2024-02-01)
    CAST(JULIANDAY('2024-02-01') - JULIANDAY(MAX(cs.transaction_date)) AS INTEGER) AS days_since_last_activity,
    -- Флаг оттока: последний раз был >45 дней назад ИЛИ много больших разрывов
    CASE 
        WHEN JULIANDAY('2024-02-01') - JULIANDAY(MAX(cs.transaction_date)) > 45 
             OR SUM(cs.large_gap_flag) >= 2 THEN 'High Churn Risk'
        WHEN JULIANDAY('2024-02-01') - JULIANDAY(MAX(cs.transaction_date)) > 30 THEN 'Medium Churn Risk'
        ELSE 'Low Risk'
    END AS churn_risk_level
FROM churn_signals cs
JOIN customers c ON cs.customer_id = c.customer_id
GROUP BY cs.customer_id, c.first_name, c.last_name, c.segment, c.credit_score
HAVING COUNT(*) > 1  -- Только клиенты с более чем 1 транзакцией
ORDER BY 
    CASE 
        WHEN JULIANDAY('2024-02-01') - JULIANDAY(MAX(cs.transaction_date)) > 45 THEN 1
        WHEN JULIANDAY('2024-02-01') - JULIANDAY(MAX(cs.transaction_date)) > 30 THEN 2
        ELSE 3
    END,
    days_since_last_activity DESC;

-- Комментарий для интервью:
-- LAG() позволяет получить значение из предыдущей строки без self-join
-- JULIANDAY() используется для расчета разницы дат в SQLite
-- Оконные агрегаты (AVG OVER PARTITION) дают среднее по клиенту
-- Индекс idx_transactions_date критичен для ORDER BY в оконных функциях
