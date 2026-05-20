# Дашборд Power BI: Анализ продаж E-commerce

## 📌 Описание проекта
Интерактивный дашборд для анализа продаж интернет-магазина с ключевыми метриками, трендами и возможностью детализации.

## 🎯 Бизнес-задачи
1. Мониторинг общих продаж и динамики
2. Анализ performance по категориям товаров
3. Выявление топ-клиентов и паттернов покупок
4. Отслеживание месяц-к-месяцу изменений

---

## 📊 Структура дашборда

### Страница 1: Executive Summary (Главная)

#### Верхняя панель (KPI Cards)
| Метрика | Формула | Формат |
|---------|---------|--------|
| **Total Revenue** | `SUM(orders[amount])` | $#,##0 |
| **Total Orders** | `COUNT(orders[order_id])` | #,##0 |
| **Avg Order Value** | `DIVIDE([Total Revenue], [Total Orders])` | $#,##0.00 |
| **MoM Growth %** | `(This Month - Last Month) / Last Month` | +0.0%;-0.0% |

#### Визуализации
1. **Line Chart**: Monthly Sales Trend
   - X-axis: Order Date (Month)
   - Y-axis: Sum of Amount
   - Дополнительно: Moving Average (3 месяца)

2. **Bar Chart**: Sales by Category
   - Legend: Category
   - Values: Sum of Amount
   - Сортировка: по убыванию

3. **Map или Tree Map**: Geographic Distribution (если есть данные о регионах)

4. **Table**: Top 10 Customers
   - Columns: Customer ID, Total Spent, Order Count, Avg Order Value
   - Сортировка: по Total Spent

---

### Страница 2: Deep Dive Analytics (Детальный анализ)

#### Slicers (Фильтры)
- 📅 Date Range (Date Picker)
- 🏷️ Category (Dropdown, Multi-select)
- 👥 Customer Segment (Checkbox)
- 💰 Amount Range (Slider)

#### Визуализации
1. **Matrix**: Sales by Category × Month
   - Rows: Category
   - Columns: Month
   - Values: Sum of Amount, Count of Orders
   - Conditional Formatting: цвет по значению

2. **Clustered Bar Chart**: Customer Cohort Analysis
   - Legend: First Purchase Month
   - Axis: Months Since First Purchase
   - Values: Number of Active Customers

3. **Scatter Plot**: Order Amount vs Order Frequency
   - X-axis: Number of Orders (per customer)
   - Y-axis: Average Order Amount
   - Legend: Customer Category (High/Medium/Low spender)

4. **Gauge Chart**: Revenue vs Target
   - Value: Current Month Revenue
   - Target: Planned Target (например, +10% к прошлому месяцу)
   - Zones: Red (<80%), Yellow (80-100%), Green (>100%)

---

### Страница 3: Customer Insights (Клиентская аналитика)

#### Визуализации
1. **Donut Chart**: Customer Distribution by Segment
   - Segments: High (>1000), Medium (500-1000), Low (<500)
   - Values: Count of Customers

2. **Waterfall Chart**: Revenue Contribution by Category
   - Показывает вклад каждой категории в общую выручку

3. **Decomposition Tree**: Root Cause Analysis
   - Root: Total Revenue
   - Branches: Category → Month → Customer Segment
   - AI-powered: автоматическое выявление аномалий

4. **Table**: Customer Lifetime Value (CLV)
   - Columns: Customer ID, First Order, Last Order, Total Orders, Total Revenue, CLV Score
   - CLV Score = Total Revenue × (1 + Order Frequency Factor)

---

## 🔧 Техническая реализация

### Источник данных
```sql
-- Предварительная подготовка данных (SQL View)
CREATE VIEW vw_sales_dashboard AS
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.amount,
    o.category,
    FORMAT(o.order_date, 'yyyy-MM') AS order_month,
    CASE 
        WHEN o.amount > 1000 THEN 'High'
        WHEN o.amount > 500 THEN 'Medium'
        ELSE 'Low'
    END AS amount_category,
    -- Оконные функции для дополнительных метрик
    SUM(o.amount) OVER (PARTITION BY o.customer_id) AS customer_lifetime_value,
    COUNT(o.order_id) OVER (PARTITION BY o.customer_id) AS customer_order_count,
    AVG(o.amount) OVER (PARTITION BY o.customer_id) AS customer_avg_order
FROM orders o
WHERE o.status = 'completed';
```

### DAX Measures (ключевые формулы)

```dax
-- Общая выручка
Total Revenue = SUM(orders[amount])

-- Количество заказов
Total Orders = COUNT(orders[order_id])

-- Средний чек
Avg Order Value = DIVIDE([Total Revenue], [Total Orders])

-- Выручка прошлого месяца
Last Month Revenue = 
CALCULATE(
    [Total Revenue],
    PREVIOUSMONTH('Calendar'[Date])
)

-- Месячный рост %
MoM Growth % = 
VAR ThisMonth = [Total Revenue]
VAR LastMonth = [Last Month Revenue]
RETURN
DIVIDE(ThisMonth - LastMonth, LastMonth)

-- Скользящее среднее (3 месяца)
Moving Avg 3M = 
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(
        'Calendar'[Date],
        LASTDATE('Calendar'[Date]),
        -3,
        MONTH
    )
) / 3

-- Процент от категории
% of Category Total = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(orders[category]))
)

-- Ранг клиента по выручке
Customer Rank = 
RANKX(
    ALL(orders[customer_id]),
    [Total Revenue],
    ,
    DESC
)
```

### Calendar Table (обязательно для time intelligence)

```dax
Calendar = 
ADDCOLUMNS(
    CALENDAR(DATE(2024, 1, 1), DATE(2024, 12, 31)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNum", MONTH([Date]),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & QUARTER([Date])
)
```

---

## 🎨 Дизайн-рекомендации

### Цветовая палитра
- Primary: #2E86AB (синий)
- Secondary: #A23B72 (фиолетовый)
- Accent: #F18F01 (оранжевый)
- Success: #2ECC71 (зелёный)
- Warning: #F39C12 (жёлтый)
- Danger: #E74C3C (красный)

### Шрифты
- Заголовки: Segoe UI Semibold, 14-16pt
- Основной текст: Segoe UI Regular, 10-12pt
- KPI: Segoe UI Bold, 24-32pt

### Layout
- Сетка: 4 колонки, выравнивание по верху
- Отступы: 8px между визуализациями
- Группировка: связанные графики в одном контейнере

---

## 📸 Макет дашборда (текстовое описание для скриншота)

```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 E-COMMERCE SALES DASHBOARD                    Martin Minart     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ $12,450  │  │   45     │  │  $276.67 │  │  +8.5%   │           │
│  │ Revenue  │  │  Orders  │  │  AOV     │  │  MoM     │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                     │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐  │
│  │                             │  │  Sales by Category          │  │
│  │   Monthly Sales Trend       │  │  ████████ Electronics  45%  │  │
│  │   ╱╲  ╱╲╱╲                  │  │  ████ Clothing        30%   │  │
│  │  ╱  ╲╱    ╲╱                │  │  ██ Home              25%   │  │
│  │                             │  │                             │  │
│  └─────────────────────────────┘  └─────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Top 10 Customers                                            │  │
│  │  Customer ID │ Total Spent │ Orders │ Avg Order │ Rank      │  │
│  │  104         │ $3,500      │ 1      │ $3,500    │ 1         │  │
│  │  101         │ $4,600      │ 3      │ $1,533    │ 2         │  │
│  │  ...         │ ...         │ ...    │ ...       │ ...       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ 📅       │  │ 🏷️       │  │ 👥       │  │ 💰       │           │
│  │ Jan-Dec  │  │ All Cats │  │ All Seg  │  │ $0-$5000 │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Как собрать дашборд (пошаговая инструкция)

### Шаг 1: Подготовка данных (10 мин)
1. Открыть Power BI Desktop
2. Get Data → SQL Server / CSV
3. Загрузить таблицу `orders`
4. Создать Calendar Table через DAX

### Шаг 2: Создание мер (15 мин)
1. Создать все DAX measures из раздела выше
2. Проверить расчёты на тестовых данных
3. Настроить форматирование (валюта, проценты)

### Шаг 3: Визуализации (20 мин)
1. Добавить KPI cards на главную страницу
2. Построить Line Chart для тренда
3. Добавить Bar Chart по категориям
4. Создать таблицу Top Customers

### Шаг 4: Фильтры и интерактивность (5 мин)
1. Добавить slicers для фильтров
2. Настроить cross-filtering между графиками
3. Протестировать взаимодействие

### Шаг 5: Форматирование и публикация (10 мин)
1. Применить цветовую схему
2. Добавить заголовки и подписи
3. Сохранить как `.pbix`
4. Опубликовать в Power BI Service (опционально)

**Общее время: ~60 минут**

---

## 📝 Что показать работодателю

1. **Скриншот дашборда** (сделай после сборки)
2. **Описание бизнес-метрик** (KPI, формулы)
3. **Примеры DAX-формул** (time intelligence, оконные функции)
4. **Архитектура данных** (источники, трансформации)
5. **Интерактивные возможности** (фильтры, drill-down)

## 💡 Идеи для расширения
- Добавить прогнозирование через AI Visuals
- Интеграция с Real-time данными
- Email-рассылка отчётов через Power BI Service
- Мобильная версия дашборда

## 🔗 Автор
Martin Minart  
GitHub: https://github.com/MartinMinart/data-portfolio

---

*Примечание: После сборки дашборда в Power BI сделай скриншот (Win+Shift+S) и сохрани как `dashboard_screenshot.png` в эту папку.*
