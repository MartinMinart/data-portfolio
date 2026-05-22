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
