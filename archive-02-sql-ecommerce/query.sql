-- ============================================================================
-- SQL Window Functions Demo: E-commerce Sales Analysis
-- Автор: Martin Minart
-- Описание: Анализ продаж с использованием оконных функций
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 1. Подготовка данных (создание тестовой таблицы)
-- -----------------------------------------------------------------------------

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10, 2),
    category VARCHAR(50)
);

-- Пример данных (в реальности — загрузка из CSV)
INSERT INTO orders VALUES
(1, 101, '2024-01-15', 1500.00, 'Electronics'),
(2, 102, '2024-01-16', 800.00, 'Clothing'),
(3, 101, '2024-01-20', 2200.00, 'Electronics'),
(4, 103, '2024-01-22', 450.00, 'Home'),
(5, 102, '2024-02-01', 1200.00, 'Clothing'),
(6, 104, '2024-02-05', 3500.00, 'Electronics'),
(7, 101, '2024-02-10', 900.00, 'Home'),
(8, 103, '2024-02-15', 600.00, 'Clothing'),
(9, 105, '2024-02-20', 1800.00, 'Electronics'),
(10, 102, '2024-03-01', 950.00, 'Home');

-- -----------------------------------------------------------------------------
-- 2. Основные оконные функции
-- -----------------------------------------------------------------------------

-- ЗАПРОС 1: Ранжирование клиентов по общей сумме покупок
-- Используем ROW_NUMBER, RANK, DENSE_RANK
SELECT 
    customer_id,
    SUM(amount) AS total_spent,
    ROW_NUMBER() OVER (ORDER BY SUM(amount) DESC) AS row_num,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS rank_num,
    DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS dense_rank_num
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- -----------------------------------------------------------------------------

-- ЗАПРОС 2: Скользящее среднее продаж по месяцам
-- Используем AVG OVER с ROWS BETWEEN
-- Для SQL Server используем FORMAT вместо DATE_TRUNC:
SELECT 
    FORMAT(order_date, 'yyyy-MM') AS month,
    SUM(amount) AS monthly_sales,
    AVG(SUM(amount)) OVER (
        ORDER BY FORMAT(order_date, 'yyyy-MM')
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3months
FROM orders
GROUP BY FORMAT(order_date, 'yyyy-MM')
ORDER BY month;

-- -----------------------------------------------------------------------------

-- ЗАПРОС 3: Сравнение с предыдущим месяцем (Month-over-Month growth)
-- Используем LAG для получения предыдущего значения
WITH monthly_sales AS (
    SELECT 
        FORMAT(order_date, 'yyyy-MM') AS month,
        SUM(amount) AS total_sales
    FROM orders
    GROUP BY FORMAT(order_date, 'yyyy-MM')
)
SELECT 
    month,
    total_sales,
    LAG(total_sales, 1) OVER (ORDER BY month) AS prev_month_sales,
    total_sales - LAG(total_sales, 1) OVER (ORDER BY month) AS sales_diff,
    ROUND(
        (total_sales - LAG(total_sales, 1) OVER (ORDER BY month)) * 100.0 
        / NULLIF(LAG(total_sales, 1) OVER (ORDER BY month), 0), 
        2
    ) AS growth_percent
FROM monthly_sales
ORDER BY month;

-- -----------------------------------------------------------------------------

-- ЗАПРОС 4: Накопительный итог (Cumulative Sum)
-- Используем SUM OVER без ограничения строк
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS UNBOUNDED PRECEDING
    ) AS cumulative_total
FROM orders
ORDER BY customer_id, order_date;

-- -----------------------------------------------------------------------------

-- ЗАПРОС 5: Топ-3 заказа в каждой категории
-- Используем оконную функцию с подзапросом или CTE
WITH ranked_orders AS (
    SELECT 
        order_id,
        customer_id,
        category,
        amount,
        order_date,
        RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS rank_in_category
    FROM orders
)
SELECT *
FROM ranked_orders
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;

-- -----------------------------------------------------------------------------
-- 3. ОПТИМИЗАЦИЯ ЗАПРОСОВ
-- -----------------------------------------------------------------------------

/*
Проблемы производительности и решения:

1. ПРОБЛЕМА: Оконные функции требуют сортировки всего датасета
   РЕШЕНИЕ: Создать индекс по полям сортировки
   
   CREATE INDEX idx_orders_date ON orders(order_date);
   CREATE INDEX idx_orders_customer ON orders(customer_id, order_date);

2. ПРОБЛЕМА: Повторяющиеся вычисления в CTE
   РЕШЕНИЕ: Использовать временные таблицы для больших данных
   
   SELECT ... INTO #temp_table FROM orders WHERE ...;
   CREATE INDEX idx_temp ON #temp_table(...);

3. ПРОБЛЕМА: Сканирование всей таблицы
   РЕШЕНИЕ: Добавить фильтрацию по дате в WHERE
   
   WHERE order_date >= '2024-01-01' AND order_date < '2024-12-31'

4. ПЛАН ВЫПОЛНЕНИЯ:
   - Используй EXPLAIN ANALYZE (PostgreSQL) или 
     SET STATISTICS IO, TIME ON (SQL Server)
   - Смотри на Cost % и Number of Rows
   - Избегай Key Lookup и Table Scan

5. ИНДЕКСЫ для оконных функций:
   -- Покрывающий индекс (covering index)
   CREATE INDEX idx_orders_covering 
   ON orders(customer_id, order_date) 
   INCLUDE (amount, category);
*/

-- -----------------------------------------------------------------------------
-- 4. Проверка плана выполнения (для SQL Server)
-- -----------------------------------------------------------------------------

SET STATISTICS IO, TIME ON;

-- Запусти любой запрос выше и посмотри:
-- - Logical reads (должно быть мало)
-- - CPU time
-- - Elapsed time

SET STATISTICS IO, TIME OFF;

-- ============================================================================
-- Конец демонстрации оконных функций
-- ============================================================================
