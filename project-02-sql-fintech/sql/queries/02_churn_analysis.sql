-- Churn Analysis: Identify customers at risk of leaving
WITH customer_transactions AS (
    SELECT 
        customer_id,
        transaction_date,
        amount,
        LAG(transaction_date) OVER (PARTITION BY customer_id ORDER BY transaction_date) AS prev_transaction_date,
        JULIANDAY(transaction_date) - JULIANDAY(
            LAG(transaction_date) OVER (PARTITION BY customer_id ORDER BY transaction_date)
        ) AS days_since_last_txn
    FROM transactions
),
customer_activity AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_transactions,
        MIN(transaction_date) AS first_activity,
        MAX(transaction_date) AS last_activity,
        JULIANDAY('now') - JULIANDAY(MAX(transaction_date)) AS days_inactive,
        AVG(days_since_last_txn) AS avg_days_between_txns,
        SUM(CASE WHEN days_since_last_txn > 30 THEN 1 ELSE 0 END) AS large_gaps_count
    FROM customer_transactions
    WHERE days_since_last_txn IS NOT NULL
    GROUP BY customer_id
)
SELECT 
    customer_id,
    total_transactions,
    days_inactive,
    ROUND(avg_days_between_txns, 1) AS avg_days_between_txns,
    large_gaps_count,
    CASE 
        WHEN days_inactive > 45 OR large_gaps_count >= 2 THEN 'High Churn Risk'
        WHEN days_inactive > 30 OR large_gaps_count >= 1 THEN 'Medium Churn Risk'
        ELSE 'Low Churn Risk'
    END AS churn_risk_category
FROM customer_activity
ORDER BY days_inactive DESC;
