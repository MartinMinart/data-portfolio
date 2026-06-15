# SQL Fintech Analysis Project

## 📊 Анализ транзакций с оконными функциями SQL

Проект демонстрирует продвинутые техники SQL-анализа для финтех-задач: выявление мошенничества, анализ оттока клиентов, RFM-сегментация и расчет метрик риска.

---

## 🎯 Цели проекта

1. **Fraud Detection** — поиск аномальных транзакций через статистические методы
2. **Churn Analysis** — выявление клиентов с признаками оттока
3. **Customer Segmentation** — RFM-сегментация базы клиентов
4. **Risk Metrics** — расчет Fraud Rate, Cost of Risk, MoM динамики

---

## 📁 Структура проекта

```
project-02-sql-fintech/
├── data/
│   └── fintech_transactions.db    # SQLite база (генерируется)
├── sql/
│   ├── schema.sql                 # Схема БД (таблицы, индексы)
│   ├── seed_data.sql              # Примеры тестовых данных
│   └── queries/
│       ├── 01_fraud_detection.sql # Поиск фрода (Z-score, скользящее среднее)
│       ├── 02_churn_analysis.sql  # Отток (LAG, интервалы)
│       ├── 03_customer_segmentation.sql # RFM (NTILE, RANK)
│       └── 04_risk_metrics.sql    # Метрики риска (Fraud Rate, MoM)
├── src/
│   └── init_db.py                 # Скрипт генерации данных
├── notebooks/
│   └── sql_analysis.ipynb         # Интерактивный анализ с графиками
├── output/                        # Результаты (игнорируется Git)
└── README.md                      # Этот файл
```

---

## 🚀 Быстрый старт

### Требования

- Python 3.8+
- Библиотеки: `pandas`, `matplotlib`, `seaborn`, `sqlite3` (встроенная)

### Установка зависимостей

```bash
pip install pandas matplotlib seaborn
```

Или из файла requirements.txt:
```bash
pip install -r requirements.txt
```

### Шаг 1: Создание базы данных

```bash
python src/init_db.py
```

Скрипт создаст SQLite базу в папке `data/` с:
- 100 клиентами
- ~600 транзакциями
- ~3% фрод-транзакций

**Пример вывода:**
```
✓ База данных создана: data/fintech_transactions.db
✓ Сгенерировано 100 клиентов
✓ Сгенерировано 603 транзакций
Общий объем: 7,024,272.88 RUB
Фрод-транзакции: 18 (2.99%)
```

### Шаг 2: Запуск анализа в Jupyter Notebook

```bash
jupyter notebook notebooks/sql_analysis.ipynb
```

Ноутбук выполнит все 4 запроса и построит визуализации.

### Шаг 3: Самостоятельное выполнение SQL запросов

Откройте любой SQL файл из папки `sql/queries/` и выполните его в:
- **DB Browser for SQLite** (GUI)
- **SQLite CLI**: `sqlite3 data/fintech_transactions.db < sql/queries/01_fraud_detection.sql`
- **Python**: через `sqlite3.connect()` и `pd.read_sql_query()`

---

## 📈 Описание запросов

### Query 01: Fraud Detection

**Оконные функции:**
- `AVG() OVER (ROWS BETWEEN)` — скользящее среднее за 5 транзакций
- `RANK() OVER` — ранжирование по сумме для клиента
- Z-score расчет для выявления выбросов

**Бизнес-логика:**
- Транзакция подозрительна, если Z-score > 2.5
- Или страна операции не RU (NG, US, CN, CY, GB)
- Или сумма превышает скользящее среднее в 3 раза

---

### Query 02: Churn Analysis

**Оконные функции:**
- `LAG(transaction_date)` — предыдущая дата транзакции
- `LAG(amount)` — предыдущая сумма
- `ROW_NUMBER()` — порядковый номер транзакции
- `AVG() OVER (PARTITION BY)` — средний интервал для клиента

**Бизнес-логика:**
- High Churn Risk: последняя активность >45 дней назад ИЛИ ≥2 больших разрыва (>30 дней)
- Medium Churn Risk: последняя активность >30 дней назад

---

### Query 03: Customer Segmentation (RFM)

**Оконные функции:**
- `NTILE(5)` — деление на квантили (5 групп)
- `RANK() OVER` — ранг по денежному объему
- `PERCENT_RANK()` — процентиль клиента

**Сегменты:**
| Сегмент | Критерии | Рекомендации |
|---------|----------|--------------|
| Champions | R≥4, F≥4, M≥4 | Loyalty rewards, early access |
| Loyal Customers | F≥4, R≥3 | Upsell higher value products |
| New Customers | R≥4, F≤2 | Onboarding campaigns |
| At Risk | R≤2, F≥3, M≥3 | Re-engagement campaigns |
| Lost | R≤2, F≤2 | Win-back или снижение контактов |

---

### Query 04: Risk Metrics

**Метрики:**
- **Fraud Rate** = Фрод объем / Общий объем × 100%
- **Cost of Risk** = Потери от фрода / Портфель
- **MoM Change** = (Текущий месяц - Предыдущий) / Предыдущий × 100%

**Оконные функции:**
- `LAG() OVER` — предыдущий месяц для MoM расчета
- Агрегаты с `CASE WHEN` — условное суммирование

---

## 🎓 Что это демонстрирует работодателю

### Технические навыки:
✅ Продвинутый SQL (CTE, оконные функции, агрегаты)  
✅ Работа с SQLite/PostgreSQL/SQL Server  
✅ Python + pandas для анализа данных  
✅ Визуализация (matplotlib, seaborn)  
✅ Генерация реалистичных тестовых данных  

### Предметные знания (финтех):
✅ Fraud Detection методы (Z-score, аномалии)  
✅ Churn Analysis (интервалы, LAG)  
✅ RFM-сегментация клиентов  
✅ Risk Metrics (Fraud Rate, Cost of Risk, NPL)  
✅ Понимание транзакционных данных  

---

## 💡 Советы для интервью

### Вопрос: "Как оптимизировать запрос с оконными функциями?"

**Ответ:**
1. **Индексы**: Добавить индекс на колонку в `PARTITION BY` и `ORDER BY`
   ```sql
   CREATE INDEX idx_transactions_customer_date ON transactions(customer_id, transaction_date);
   ```
2. **Избегать множественных окон**: Переиспользовать CTE вместо повторных `OVER()`
3. **Фильтрация до оконных функций**: Сначала `WHERE`, потом окна (если возможно)
4. **Анализ плана выполнения**: `EXPLAIN QUERY PLAN` в SQLite

### Вопрос: "Почему SQLite для этого проекта?"

**Ответ:**
- Легковесный, не требует сервера
- Идеален для прототипирования и портфолио
- Те же SQL запросы работают на PostgreSQL/SQL Server с минимальными правками
- В продакшене используем полноценные СУБД (PostgreSQL, ClickHouse, Snowflake)

---

## 🔧 Расширение проекта

### Идеи для улучшения:
1. **Добавить ML-модель** — классификация фрода через sklearn (Logistic Regression, Random Forest)
2. **Airflow DAG** — автоматический ежедневный пересчет метрик
3. **Power BI дашборд** — визуализация Fraud Rate, Churn Risk, RFM-сегментов
4. **Больше данных** — увеличить до 10K клиентов для тестов производительности

---

## 📚 Дополнительные ресурсы

- [SQLite Window Functions](https://www.sqlite.org/windowfunctions.html)
- [PostgreSQL Window Functions Tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [RFM Analysis Guide](https://www.clevertap.com/blog/rfm-analysis/)
- [Fraud Detection Best Practices](https://fraud.net/resources/fraud-detection-guide/)

---

## 👤 Автор

**Artur Minart**  
Data Analyst | FinTech Focus  
📧 iamartur1111@gmail.com  
🔗 [GitHub](https://github.com/MartinMinart/data-portfolio)  
📍 Москва

---

*Проект создан для портфолио Data Analyst. Все данные синтетические.*
