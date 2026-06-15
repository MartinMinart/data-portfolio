-- Fraud Detection: Identify suspicious transaction patterns
-- Flag customers with unusual spending behavior

WITH customer_stats AS (
    SELECT 
        customer_id,
        COUNT(*) AS transaction_count,
        AVG(amount) AS avg_amount,
        SQRT(AVG(amount*amount) - AVG(amount)*AVG(amount)) AS std_amount,
        SUM(CASE WHEN amount > 1000 THEN 1 ELSE 0 END) AS high_value_count,
        MAX(amount) AS max_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT 
    customer_id,
    transaction_count,
    ROUND(avg_amount, 2) AS avg_amount,
    ROUND(std_amount, 2) AS std_amount,
    high_value_count,
    max_amount,
    CASE 
        WHEN std_amount > avg_amount * 2 THEN 'High Volatility'
        WHEN high_value_count > 3 THEN 'Multiple High-Value'
        WHEN max_amount > 5000 THEN 'Extreme Outlier'
        ELSE 'Normal'
    END AS risk_flag
FROM customer_stats
WHERE std_amount > avg_amount * 2 
   OR high_value_count > 3
   OR max_amount > 5000
ORDER BY std_amount DESC;
