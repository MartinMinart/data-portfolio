-- ==========================================
-- Продвинутый финтех-анализ с оконными функциями
-- ==========================================

-- 1. ВЫЯВЛЕНИЕ МОШЕННИЧЕСТВА (Fraud Detection)
-- Ищем аномалии: транзакции, где сумма превышает среднее по клиенту в 3 раза
SELECT 
    t.transaction_id,
    t.customer_id,
    t.amount,
    t.transaction_date,
    avg_amount_by_customer,
    CASE 
        WHEN t.amount > (avg_amount_by_customer * 3) THEN 'SUSPICIOUS'
        ELSE 'NORMAL'
    END AS fraud_flag
FROM (
    SELECT 
        *,
        AVG(amount) OVER (PARTITION BY customer_id) as avg_amount_by_customer,
        COUNT(*) OVER (PARTITION BY customer_id) as total_txns
    FROM transactions
) t
ORDER BY amount DESC;

-- 2. АНАЛИЗ ОТТОКА (Churn Analysis)
-- Считаем время между транзакциями. Если разрыв > 30 дней - риск оттока
SELECT 
    customer_id,
    transaction_date,
    amount,
    LAG(transaction_date) OVER (PARTITION BY customer_id ORDER BY transaction_date) as prev_date,
    JULIANDAY(transaction_date) - JULIANDAY(LAG(transaction_date) OVER (PARTITION BY customer_id ORDER BY transaction_date)) as days_since_last_txn
FROM transactions
WHERE customer_id IN (101, 103, 104) -- Пример для конкретных клиентов
ORDER BY customer_id, transaction_date;

-- 3. СЕГМЕНТАЦИЯ КЛИЕНТОВ (RFM-like анализ)
-- Делим клиентов на квантили по сумме трат
SELECT 
    customer_id,
    SUM(amount) as total_spend,
    COUNT(*) as txn_count,
    NTILE(4) OVER (ORDER BY SUM(amount) DESC) as spend_quartile, -- 1 = VIP, 4 = Low
    RANK() OVER (ORDER BY SUM(amount) DESC) as spend_rank
FROM transactions
GROUP BY customer_id
ORDER BY total_spend DESC;

-- 4. НАКОПИТЕЛЬНЫЙ ИТОГ (Cumulative Sum)
-- Динамика расходов клиента по времени
SELECT 
    customer_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY transaction_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM transactions
WHERE customer_id = 101
ORDER BY transaction_date;