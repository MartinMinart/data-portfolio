# Airflow DAG: E-commerce Data Pipeline

## 📌 Описание проекта
Простой, но реалистичный DAG для Apache Airflow, реализующий ETL-пайплайн обработки данных о продажах.

## 🎯 Архитектура пайплайна

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   EXTRACT   │ -> │  TRANSFORM   │ -> │    LOAD     │ -> │   NOTIFY     │
│  (Извлечение)│    │(Трансформация)│    │  (Загрузка) │    │(Уведомление) │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

## 📁 Файлы
- `ecommerce_dag.py` — основной файл DAG
- `requirements.txt` — зависимости Python

## 🚀 Задачи в DAG

### 1. `extract_sales_data` (PythonOperator)
- Симуляция извлечения данных из источника
- Создание тестового DataFrame
- Сохранение в промежуточный CSV

### 2. `transform_sales_data` (PythonOperator)
- Фильтрация по статусу заказа
- Удаление дубликатов
- Добавление вычисляемых полей (месяц, категория суммы)
- Агрегация по категориям и месяцам

### 3. `load_sales_data` (PythonOperator)
- Загрузка данных в целевую систему
- Симуляция INSERT в базу данных
- Возврат метрики успешности

### 4. `notify_completion` (BashOperator)
- Уведомление о завершении пайплайна
- Логирование времени окончания

## 🛠️ Установка и запуск

### Шаг 1: Установка зависимостей
```bash
pip install apache-airflow pandas
```

### Шаг 2: Инициализация Airflow
```bash
# Инициализация базы данных
airflow db init

# Создание пользователя
airflow users create \
    --username admin \
    --password admin \
    --firstname Martin \
    --lastname Minart \
    --role Admin \
    --email martin@example.com
```

### Шаг 3: Запуск сервисов
```bash
# Терминал 1: Веб-сервер
airflow webserver --port 8080

# Терминал 2: Планировщик
airflow scheduler
```

### Шаг 4: Размещение DAG
```bash
# Скопируйте файл в папку DAGs
cp ecommerce_dag.py ~/airflow/dags/
```

### Шаг 5: Проверка и запуск
```bash
# Список всех DAG
airflow dags list

# Список задач в DAG
airflow tasks list ecommerce_sales_pipeline

# Запуск вручную
airflow dags trigger ecommerce_sales_pipeline

# Выполнение конкретной задачи
airflow tasks run ecommerce_sales_pipeline extract_sales_data 2024-01-01
```

## 📊 Мониторинг

Откройте веб-интерфейс: **http://localhost:8080**

Что можно увидеть:
- ✅ Статус выполнения задач (зелёный — успех, красный — ошибка)
- ⏱️ Время выполнения каждой задачи
- 📈 График зависимостей между задачами
- 📝 Логи выполнения (кнопка "Log" у каждой задачи)

## 🔧 Best Practices, реализованные в DAG

1. **Идемпотентность** — повторный запуск не создаёт дубликатов
2. **XCom** — передача данных между задачами через `xcom_pull`/`xcom_push`
3. **Обработка ошибок** — параметр `retries` для автоматических повторных попыток
4. **Модульность** — каждая задача выполняет одну функцию
5. **Документирование** — подробные docstring у функций
6. **Теги** — организация DAG по категориям (`data-engineering`, `etl`, `sales`)

## 📝 Что показать работодателю

1. Понимание архитектуры Airflow
2. Умение создавать DAG с зависимостями
3. Работа с разными типами операторов (Python, Bash)
4. Знание best practices оркестрации
5. Умение документировать код

## 🔗 Расширение функционала

В реальном проекте можно добавить:
- Подключение к реальной БД через `PostgresOperator` или `MySqlOperator`
- Загрузку в облако (S3, GCS) через `S3Hook`, `GCSHook`
- Отправку уведомлений в Slack/Telegram через `SlackWebhookOperator`
- Ветвление логики через `BranchPythonOperator`
- Динамическое создание задач через `TaskGroup`

## 🔗 Автор
Martin Minart  
GitHub: https://github.com/MartinMinart/data-portfolio
