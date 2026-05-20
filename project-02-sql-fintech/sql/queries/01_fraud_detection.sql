-- ============================================
-- Query 01: Fraud Detection (Выявление мошенничества)
-- Использование оконных функций для поиска аномалий
-- ============================================

-- Задача: Найти транзакции, где сумма превышает среднее по клиенту более чем в 3 раза
-- ИЛИ транзакции из необычных стран (не RU)

WITH customer_stats AS (
    SELECT 
        customer_id,
        AVG(amount) AS avg_amount,
        STDDEV(amount) AS std_amount,
        COUNT(*) AS total_transactions
    FROM transactions
    GROUP BY customer_id
),
transaction_with_zscore AS (
    SELECT 
        t.transaction_id,
        t.customer_id,
        t.transaction_date,
        t.amount,
        t.category,
        t.merchant_name,
        t.country,
        t.is_fraud,
        cs.avg_amount,
        cs.std_amount,
        -- Z-score: сколько стандартных отклонений от среднего
        CASE 
            WHEN cs.std_amount > 0 THEN (t.amount - cs.avg_amount) / cs.std_amount
            ELSE 0 
        END AS z_score,
        -- Скользящее среднее за последние 5 транзакций клиента
        AVG(t.amount) OVER (
            PARTITION BY t.customer_id 
            ORDER BY t.transaction_date 
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_5,
        -- Ранг транзакции по сумме для клиента
        RANK() OVER (
            PARTITION BY t.customer_id 
            ORDER BY t.amount DESC
        ) AS amount_rank_by_customer
    FROM transactions t
    JOIN customer_stats cs ON t.customer_id = cs.customer_id
)
SELECT 
    transaction_id,
    customer_id,
    transaction_date,
    ROUND(amount, 2) AS amount,
    category,
    merchant_name,
    country,
    is_fraud AS actual_fraud,
    ROUND(avg_amount, 2) AS customer_avg_amount,
    ROUND(z_score, 2) AS z_score,
    ROUND(rolling_avg_5, 2) AS rolling_avg_5tr,
    amount_rank_by_customer,
    -- Флаг подозрительной транзакции
    CASE 
        WHEN z_score > 3.0 THEN 'High Z-Score'
        WHEN country != 'RU' THEN 'Foreign Country'
        WHEN amount > rolling_avg_5 * 3 THEN 'Spike vs Rolling Avg'
        ELSE 'Normal'
    END AS anomaly_flag
FROM transaction_with_zscore
WHERE z_score > 2.5 OR country != 'RU' OR amount > rolling_avg_5 * 3
ORDER BY z_score DESC, transaction_date;

-- Комментарий для интервью:
-- Этот запрос использует несколько оконных функций:
-- 1. AVG() OVER с ROWS BETWEEN для скользящего среднего
-- 2. RANK() для ранжирования транзакций по сумме
-- 3. CTE для предварительного расчета статистики по клиентам
-- Индексы: idx_transactions_customer, idx_transactions_date ускоряют PARTITION BY
