# SQL Window Functions Demo: E-commerce Sales Analysis

## 📌 Описание проекта
Демонстрация возможностей оконных функций в SQL на примере анализа продаж интернет-магазина.

## 🎯 Используемые оконные функции
- `ROW_NUMBER()` — нумерация строк
- `RANK()`, `DENSE_RANK()` — ранжирование
- `LAG()` — доступ к предыдущей строке
- `SUM() OVER` — накопительный итог
- `AVG() OVER` — скользящее среднее

## 📁 Файлы
- `query.sql` — все SQL-запросы с комментариями
- `sample_data.csv` — тестовые данные (можно сгенерировать из INSERT)

## 🚀 Как запустить

### Для SQL Server:
```sql
-- 1. Создайте базу данных или подключитесь к существующей
-- 2. Выполните query.sql целиком или по частям
-- 3. Включите статистику для анализа производительности:
SET STATISTICS IO, TIME ON;
```

### Для PostgreSQL:
```sql
-- Замените FORMAT() на DATE_TRUNC('month', order_date)
-- Используйте EXPLAIN ANALYZE для просмотра плана выполнения
```

## 📊 Примеры запросов

### 1. Ранжирование клиентов по сумме покупок
```sql
SELECT 
    customer_id,
    SUM(amount) AS total_spent,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS rank_num
FROM orders
GROUP BY customer_id;
```

### 2. Month-over-Month рост продаж
```sql
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
    ROUND((total_sales - LAG(total_sales, 1) OVER (ORDER BY month)) * 100.0 
          / NULLIF(LAG(total_sales, 1) OVER (ORDER BY month), 0), 2) AS growth_percent
FROM monthly_sales;
```

### 3. Накопительный итог по клиенту
```sql
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS UNBOUNDED PRECEDING
    ) AS cumulative_total
FROM orders;
```

## ⚡ Оптимизация

### Рекомендации по индексам:
```sql
-- Индекс для сортировки по дате
CREATE INDEX idx_orders_date ON orders(order_date);

-- Индекс для группировки по клиенту
CREATE INDEX idx_orders_customer ON orders(customer_id, order_date);

-- Покрывающий индекс для ускорения запросов
CREATE INDEX idx_orders_covering 
ON orders(customer_id, order_date) 
INCLUDE (amount, category);
```

### Анализ плана выполнения:
- Избегайте `Table Scan` — добавляйте индексы
- Следите за `Logical Reads` — должно быть < 1000 для небольших таблиц
- Используйте `EXPLAIN ANALYZE` или `SET STATISTICS IO, TIME ON`

## 📝 Что показать работодателю
1. Уверенное владение оконными функциями
2. Понимание оптимизации запросов
3. Умение работать с CTE и подзапросами
4. Знание планов выполнения и индексирования

## 🔗 Автор
Martin Minart  
GitHub: https://github.com/MartinMinart/data-portfolio
