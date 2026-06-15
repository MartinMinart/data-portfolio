-- ============================================
-- Query 04: Risk Metrics (Метрики риска)
-- Расчет NPL, Cost of Risk, Vintage Analysis
-- ============================================

-- Задача: Рассчитать ключевые метрики кредитного риска
-- NPL (Non-Performing Loans), Cost of Risk, Roll Rates

-- Часть 1: Общие метрики риска по портфелю
WITH portfolio_metrics AS (
    SELECT 
        COUNT(DISTINCT customer_id) AS total_customers,
        COUNT(*) AS total_transactions,
        SUM(amount) AS total_volume,
        AVG(amount) AS avg_transaction_amount,
        SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) AS fraud_volume,
        COUNT(CASE WHEN is_fraud = 1 THEN 1 END) AS fraud_count,
        SUM(CASE WHEN is_fraud = 0 THEN amount ELSE 0 END) AS legitimate_volume
    FROM transactions
),
fraud_metrics AS (
    SELECT 
        total_customers,
        total_transactions,
        total_volume,
        avg_transaction_amount,
        fraud_volume,
        fraud_count,
        legitimate_volume,
        -- Fraud Rate (% от объема)
        ROUND(fraud_volume * 100.0 / NULLIF(total_volume, 0), 4) AS fraud_rate_pct,
        -- Fraud Count Rate (% от количества транзакций)
        ROUND(fraud_count * 100.0 / NULLIF(total_transactions, 0), 2) AS fraud_count_rate_pct,
        -- Средняя сумма мошеннической транзакции
        ROUND(fraud_volume * 1.0 / NULLIF(fraud_count, 0), 2) AS avg_fraud_amount,
        -- Средняя сумма легальной транзакции
        ROUND(legitimate_volume * 1.0 / NULLIF(total_transactions - fraud_count, 0), 2) AS avg_legitimate_amount
    FROM portfolio_metrics
)
SELECT 
    'Portfolio Overview' AS metric_category,
    total_customers,
    total_transactions,
    ROUND(total_volume, 2) AS total_volume,
    ROUND(avg_transaction_amount, 2) AS avg_transaction_amount,
    fraud_count,
    ROUND(fraud_volume, 2) AS fraud_volume,
    fraud_rate_pct,
    fraud_count_rate_pct,
    ROUND(avg_fraud_amount, 2) AS avg_fraud_amount,
    ROUND(avg_legitimate_amount, 2) AS avg_legitimate_amount,
    -- Cost of Risk (упрощенно: потери от фрода / общий объем)
    fraud_rate_pct AS cost_of_risk_pct
FROM fraud_metrics;

-- ============================================
-- Часть 2: Метрики по категориям транзакций
-- ============================================

SELECT 
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS fraud_amount,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS fraud_rate_by_count,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) * 100.0 / NULLIF(SUM(amount), 0), 4) AS fraud_rate_by_amount,
    AVG(amount) AS avg_amount,
    MAX(amount) AS max_amount
FROM transactions
GROUP BY category
ORDER BY fraud_rate_by_amount DESC;

-- ============================================
-- Часть 3: Динамика фрода по месяцам (Trend Analysis)
-- ============================================

SELECT 
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_volume,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
    SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) AS fraud_volume,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS fraud_rate_pct,
    -- MoM изменение количества фрод-транзакций (LAG)
    LAG(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)) OVER (ORDER BY strftime('%Y-%m', transaction_date)) AS prev_month_fraud_count,
    CASE 
        WHEN LAG(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)) OVER (ORDER BY strftime('%Y-%m', transaction_date)) > 0
        THEN ROUND(
            (SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) - 
             LAG(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)) OVER (ORDER BY strftime('%Y-%m', transaction_date))) * 100.0 /
            LAG(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)) OVER (ORDER BY strftime('%Y-%m', transaction_date)), 2)
        ELSE NULL
    END AS mom_fraud_change_pct
FROM transactions
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month;

-- ============================================
-- Часть 4: Risk by Customer Segment (Сегментация по риску)
-- ============================================

SELECT 
    c.segment AS customer_segment,
    COUNT(DISTINCT t.customer_id) AS customers_count,
    COUNT(*) AS total_transactions,
    SUM(t.amount) AS total_volume,
    SUM(CASE WHEN t.is_fraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
    SUM(CASE WHEN t.is_fraud = 1 THEN t.amount ELSE 0 END) AS fraud_volume,
    ROUND(SUM(CASE WHEN t.is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS fraud_rate_pct,
    ROUND(AVG(t.amount), 2) AS avg_transaction_amount,
    ROUND(SUM(CASE WHEN t.is_fraud = 1 THEN t.amount ELSE 0 END) * 100.0 / NULLIF(SUM(t.amount), 0), 4) AS cost_of_risk_pct
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY fraud_rate_pct DESC;

-- Комментарий для интервью:
-- NPL (Non-Performing Loan) — кредит с просрочкой 90+ дней
-- Cost of Risk = Потери от дефолтов / Средний портфель за период
-- Roll Rates — вероятность перехода из одной стадии просрочки в другую
-- В этом запросе показаны: Fraud Rate, Trend Analysis (MoM), Risk by Segment
-- Оконные функции LAG используются для расчета динамики (Month-over-Month)
