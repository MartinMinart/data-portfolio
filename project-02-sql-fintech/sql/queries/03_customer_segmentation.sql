-- ============================================
-- Query 03: Customer Segmentation (Сегментация клиентов)
-- RFM-анализ с использованием NTILE и RANK
-- ============================================

-- Задача: Сегментировать клиентов по модели RFM (Recency, Frequency, Monetary)
-- и присвоить сегменты (Premium, Loyal, At Risk, Lost)

WITH rfm_raw AS (
    SELECT 
        customer_id,
        -- Recency: дней с последней транзакции (на 2024-02-01)
        CAST(JULIANDAY('2024-02-01') - JULIANDAY(MAX(transaction_date)) AS INTEGER) AS recency,
        -- Frequency: количество транзакций
        COUNT(*) AS frequency,
        -- Monetary: общая сумма транзакций
        SUM(amount) AS monetary,
        -- Средняя сумма транзакции
        AVG(amount) AS avg_transaction_value
    FROM transactions
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency,
        frequency,
        monetary,
        ROUND(avg_transaction_value, 2) AS avg_transaction_value,
        -- NTILE делит на квантили (5 групп от 1 до 5)
        -- Для Recency: меньше дней = лучше, поэтому ORDER BY ASC
        NTILE(5) OVER (ORDER BY recency ASC) AS r_score,
        -- Для Frequency: больше транзакций = лучше, ORDER BY DESC
        NTILE(5) OVER (ORDER BY frequency DESC) AS f_score,
        -- Для Monetary: больше сумма = лучше, ORDER BY DESC
        NTILE(5) OVER (ORDER BY monetary DESC) AS m_score,
        -- Ранг клиента по общей сумме
        RANK() OVER (ORDER BY monetary DESC) AS monetary_rank,
        -- Процентиль по сумме
        PERCENT_RANK() OVER (ORDER BY monetary ASC) AS monetary_percentile
    FROM rfm_raw
),
rfm_with_segments AS (
    SELECT 
        *,
        -- Комбинированный RFM счет (сумма баллов)
        (r_score + f_score + m_score) AS rfm_total_score,
        -- Сегмент на основе комбинации баллов
        CASE 
            -- Лучшие клиенты: высокие частота и сумма, недавние
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            -- Лояльные: частые покупки, но не обязательно большие суммы
            WHEN f_score >= 4 AND r_score >= 3 THEN 'Loyal Customers'
            -- Потенциальные лояльные: недавние, но мало транзакций
            WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
            -- Требуют внимания: были активны, но давно не покупали
            WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
            -- Почти потерянные
            WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
            -- Средний сегмент
            ELSE 'Regular'
        END AS customer_segment
    FROM rfm_scores
)
SELECT 
    rfs.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.segment AS original_segment,
    c.credit_score,
    rfs.recency,
    rfs.frequency,
    ROUND(rfs.monetary, 2) AS total_monetary,
    rfs.avg_transaction_value,
    rfs.r_score,
    rfs.f_score,
    rfs.m_score,
    rfs.rfm_total_score,
    rfs.monetary_rank,
    ROUND(rfs.monetary_percentile * 100, 1) AS monetary_percentile_pct,
    rfs.customer_segment,
    -- Рекомендации по работе с клиентом
    CASE 
        WHEN rfs.customer_segment = 'Champions' THEN 'Offer loyalty rewards, early access'
        WHEN rfs.customer_segment = 'Loyal Customers' THEN 'Upsell higher value products'
        WHEN rfs.customer_segment = 'New Customers' THEN 'Onboarding campaigns, welcome offers'
        WHEN rfs.customer_segment = 'At Risk' THEN 'Re-engagement campaigns, special discounts'
        WHEN rfs.customer_segment = 'Lost' THEN 'Win-back campaigns or reduce contact'
        ELSE 'Standard marketing communications'
    END AS recommended_action
FROM rfm_with_segments rfs
JOIN customers c ON rfs.customer_id = c.customer_id
ORDER BY rfs.rfm_total_score DESC, rfs.monetary DESC;

-- Комментарий для интервью:
-- NTILE(n) делит выборку на n равных групп (квантили)
-- RANK() присваивает ранги с пропусками при одинаковых значениях
-- PERCENT_RANK() возвращает относительный ранг (0.0 to 1.0)
-- RFM-сегментация — классический метод в ритейле и финтехе
-- Для больших данных можно использовать оконные функции с ROWS BETWEEN
