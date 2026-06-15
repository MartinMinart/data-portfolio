"""
Airflow DAG: E-commerce Data Pipeline
Автор: Martin Minart
Описание: Простой DAG для извлечения, трансформации и загрузки данных о продажах
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
import csv
from pathlib import Path

# Конфигурация DAG
default_args = {
    'owner': 'Martin Minart',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecommerce_sales_pipeline',
    default_args=default_args,
    description='Пайплайн обработки данных о продажах',
    schedule_interval='@daily',  # Запуск каждый день
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['data-engineering', 'etl', 'sales'],
)


# -----------------------------------------------------------------------------
# Шаг 1: Извлечение данных (Extract)
# -----------------------------------------------------------------------------

def extract_sales_data(**context):
    """
    Симуляция извлечения данных из источника (CSV/API/БД)
    В реальности здесь будет подключение к реальной БД или API
    """
    print("📥 Начало извлечения данных...")
    
    # Создаём тестовые данные (в реальности — запрос к БД)
    data = {
        'order_id': [1, 2, 3, 4, 5],
        'customer_id': [101, 102, 101, 103, 102],
        'order_date': ['2024-01-15', '2024-01-16', '2024-01-20', '2024-01-22', '2024-02-01'],
        'amount': [1500.00, 800.00, 2200.00, 450.00, 1200.00],
        'category': ['Electronics', 'Clothing', 'Electronics', 'Home', 'Clothing'],
        'status': ['completed', 'completed', 'pending', 'completed', 'completed']
    }
    
    df = pd.DataFrame(data)
    
    # Сохраняем в промежуточный файл
    output_path = Path('/tmp/raw_sales_data.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Данные извлечены и сохранены в {output_path}")
    print(df.to_string())
    
    return str(output_path)


extract_task = PythonOperator(
    task_id='extract_sales_data',
    python_callable=extract_sales_data,
    dag=dag,
)


# -----------------------------------------------------------------------------
# Шаг 2: Трансформация данных (Transform)
# -----------------------------------------------------------------------------

def transform_sales_data(**context):
    """
    Очистка и трансформация данных:
    - Удаление дубликатов
    - Фильтрация по статусу
    - Добавление вычисляемых полей
    """
    print("🔄 Начало трансформации данных...")
    
    # Читаем сырые данные
    input_path = context['ti'].xcom_pull(task_ids='extract_sales_data')
    df = pd.read_csv(input_path)
    
    print(f"📊 До трансформации: {len(df)} записей")
    
    # Трансформация 1: Фильтруем только завершённые заказы
    df = df[df['status'] == 'completed'].copy()
    print(f"📊 После фильтрации по статусу: {len(df)} записей")
    
    # Трансформация 2: Удаляем дубликаты (если есть)
    df = df.drop_duplicates(subset=['order_id'])
    
    # Трансформация 3: Добавляем вычисляемые поля
    df['order_month'] = pd.to_datetime(df['order_date']).dt.to_period('M').astype(str)
    df['amount_category'] = df['amount'].apply(
        lambda x: 'high' if x > 1000 else ('medium' if x > 500 else 'low')
    )
    
    # Трансформация 4: Агрегация по категориям
    summary = df.groupby(['category', 'order_month']).agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    summary.columns = ['total_amount', 'avg_amount', 'order_count']
    summary = summary.reset_index()
    
    # Сохраняем transformed данные
    output_path = Path('/tmp/transformed_sales_data.csv')
    df.to_csv(output_path, index=False)
    
    # Сохраняем агрегированные данные
    summary_path = Path('/tmp/sales_summary.csv')
    summary.to_csv(summary_path, index=False)
    
    print(f"✅ Трансформация завершена")
    print(f"📄 Детальные данные: {output_path}")
    print(f"📄 Агрегированные данные: {summary_path}")
    print("\nАгрегированная статистика:")
    print(summary.to_string())
    
    return str(summary_path)


transform_task = PythonOperator(
    task_id='transform_sales_data',
    python_callable=transform_sales_data,
    dag=dag,
)


# -----------------------------------------------------------------------------
# Шаг 3: Загрузка данных (Load)
# -----------------------------------------------------------------------------

def load_sales_data(**context):
    """
    Загрузка данных в целевую систему (БД/хранилище)
    В реальности — INSERT в базу данных или загрузка в облачное хранилище
    """
    print("💾 Начало загрузки данных...")
    
    # Читаем transformed данные
    input_path = context['ti'].xcom_pull(task_ids='transform_sales_data')
    df = pd.read_csv(input_path)
    
    # Симуляция загрузки в БД
    print("📤 Загрузка данных в целевую систему...")
    for idx, row in df.iterrows():
        print(f"  Запись {idx + 1}/{len(df)}: {row['category']} - {row['total_amount']}")
    
    # В реальности здесь будет:
    # - Подключение к PostgreSQL/MySQL через SQLAlchemy
    # - df.to_sql('sales_summary', engine, if_exists='replace')
    # - Или загрузка в S3/GCS через boto3/gcsfs
    
    print("✅ Данные успешно загружены!")
    
    return {'records_loaded': len(df), 'status': 'success'}


load_task = PythonOperator(
    task_id='load_sales_data',
    python_callable=load_sales_data,
    dag=dag,
)


# -----------------------------------------------------------------------------
# Шаг 4: Уведомление о завершении
# -----------------------------------------------------------------------------

notify_task = BashOperator(
    task_id='notify_completion',
    bash_command='echo "✅ Пайплайн успешно завершён! $(date)"',
    dag=dag,
)


# -----------------------------------------------------------------------------
# Определение зависимостей между задачами
# -----------------------------------------------------------------------------

extract_task >> transform_task >> load_task >> notify_task


# -----------------------------------------------------------------------------
# Инструкция по запуску
# -----------------------------------------------------------------------------
"""
Установка Airflow (если не установлен):
pip install apache-airflow pandas

Инициализация БД Airflow:
airflow db init

Создание пользователя:
airflow users create \
    --username admin \
    --password admin \
    --firstname Martin \
    --lastname Minart \
    --role Admin \
    --email martin@example.com

Запуск веб-сервера:
airflow webserver --port 8080

Запуск планировщика (в отдельном терминале):
airflow scheduler

Копирование этого файла в папку DAGs:
cp ecommerce_dag.py ~/airflow/dags/

Проверка DAG:
airflow dags list
airflow tasks list ecommerce_sales_pipeline

Запуск вручную:
airflow dags trigger ecommerce_sales_pipeline

Мониторинг:
Откройте http://localhost:8080 и следите за выполнением DAG
"""
