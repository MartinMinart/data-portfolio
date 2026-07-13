# 📊 Data Portfolio | Artur Minart

> Data Analyst • SQL / Python / BI  
> 📧 iamartur1111@gmail.com | 📱 +7 982 216-78-48  
> 🔗 GitHub: https://github.com/MartinMinart/data-portfolio

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20PostgreSQL-4479A1) ![Airflow](https://img.shields.io/badge/Apache%20Airflow-ETL-017CEE) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED) ![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-FFB900)

---

## 🧭 Оглавление

- [Обо мне](#-обо-мне)
- [Технический стек](#-технический-стек)
- [Проекты](#-проекты)
- [Как запустить проекты локально](#-как-запустить-проекты-локально)
- [Секреты и .env](#-секреты-и-env)
- [Опыт работы](#-опыт-работы)
- [Образование и курсы](#-образование-и-курсы)
- [Контакты](#-контакты)

---

## 👨‍💻 Обо мне

Я — аналитик данных, который любит превращать сырьё в понятные инсайты, SQL-запросы, отчёты и автоматизированные пайплайны. В этом репозитории собраны проекты по Python, SQL, ETL/ELT, Airflow, Docker и BI.

Ключевые направления:
- SQL-анализ и оконные функции
- Python для EDA, очистки данных и отчётности
- ETL/ELT-процессы и оркестрация задач
- BI и визуализация данных
- Локальный запуск аналитических стеков через Docker

---

## 🛠️ Технический стек

| Категория | Инструменты |
|---|---|
| Языки | Python, SQL, Bash |
| Аналитика и обработка данных | pandas, numpy, matplotlib, seaborn, Jupyter |
| Базы данных | SQLite, PostgreSQL |
| Оркестрация и инфраструктура | Apache Airflow, Docker, Docker Compose |
| BI и визуализация | Power BI, DAX |
| Контроль версий | Git, GitHub |

---

## 📂 Проекты

Ниже — краткая карта того, что реально находится в каждом каталоге репозитория и какие технологии там используются.

### 1. 📈 project-01-software-eda
- Файлы: [project-01-software-eda/data/installed_software.csv](project-01-software-eda/data/installed_software.csv), [project-01-software-eda/src/analyze_software.py](project-01-software-eda/src/analyze_software.py), [project-01-software-eda/notebooks/software_eda.ipynb](project-01-software-eda/notebooks/software_eda.ipynb), [project-01-software-eda/requirements.txt](project-01-software-eda/requirements.txt)
- Задача: разведочный анализ установленного ПО, распределение по категориям и вендорам, анализ динамики установок.
- Технологии: Python, pandas, matplotlib, seaborn, Jupyter, CSV.

### 2. 🏦 project-02-sql-fintech
- Файлы: [project-02-sql-fintech/sql/schema.sql](project-02-sql-fintech/sql/schema.sql), [project-02-sql-fintech/sql/seed_data.sql](project-02-sql-fintech/sql/seed_data.sql), [project-02-sql-fintech/sql/queries](project-02-sql-fintech/sql/queries), [project-02-sql-fintech/src/init_db.py](project-02-sql-fintech/src/init_db.py), [project-02-sql-fintech/notebooks/sql_analysis.ipynb](project-02-sql-fintech/notebooks/sql_analysis.ipynb)
- Задача: финтех-аналитика на SQL с фродом, churn, RFM и метриками риска.
- Технологии: SQL, SQLite, Python, pandas, matplotlib, seaborn, Jupyter.

### 3. 🐳 docker-analytics
- Файлы: [docker-analytics/docker-compose.yml](docker-analytics/docker-compose.yml), [docker-analytics/start.sh](docker-analytics/start.sh), [docker-analytics/stop.sh](docker-analytics/stop.sh), [docker-analytics/import-data.sh](docker-analytics/import-data.sh), [docker-analytics/init-scripts/01-init-database.sql](docker-analytics/init-scripts/01-init-database.sql)
- Задача: локальный аналитический стек с PostgreSQL, Metabase и PgAdmin.
- Технологии: Docker Compose, PostgreSQL, Metabase, PgAdmin, Bash, SQL.

### 4. ⚙️ airflow-dag
- Файлы: [airflow-dag/ecommerce_dag.py](airflow-dag/ecommerce_dag.py), [airflow-dag/README.md](airflow-dag/README.md)
- Задача: демонстрация ETL-пайплайна в Apache Airflow для данных о продажах.
- Технологии: Apache Airflow, Python, pandas, Bash, PythonOperator, BashOperator.

### 5. 🧪 archive-01-airflow-ecommerce
- Файлы: [archive-01-airflow-ecommerce/ecommerce_dag.py](archive-01-airflow-ecommerce/ecommerce_dag.py), [archive-01-airflow-ecommerce/README.md](archive-01-airflow-ecommerce/README.md)
- Задача: архивная версия Airflow DAG для e-commerce ETL.
- Технологии: Apache Airflow, Python, pandas, Bash.

### 6. 🧾 archive-02-sql-ecommerce
- Файлы: [archive-02-sql-ecommerce/query.sql](archive-02-sql-ecommerce/query.sql), [archive-02-sql-ecommerce/README.md](archive-02-sql-ecommerce/README.md)
- Задача: подборка SQL-запросов с оконными функциями на примере продаж.
- Технологии: SQL, оконные функции, CTE, аналитические запросы.

### 7. 📊 archive-03-powerbi-ecommerce
- Файлы: [archive-03-powerbi-ecommerce/README.md](archive-03-powerbi-ecommerce/README.md)
- Задача: концепт Power BI-дэшборда для e-commerce с KPI, slicers и DAX-метриками.
- Технологии: Power BI, DAX, SQL.

### 8. 📈 powerbi-dashboard
- Файлы: [powerbi-dashboard/README.md](powerbi-dashboard/README.md)
- Задача: отдельная папка для описания BI-дашбордов и визуализаций.
- Технологии: Power BI, BI-архитектура, DAX.

### 9. 📚 sql-window-functions
- Файлы: [sql-window-functions/query.sql](sql-window-functions/query.sql), [sql-window-functions/README.md](sql-window-functions/README.md)
- Задача: практика по оконным функциям SQL в компактном формате.
- Технологии: SQL, window functions, аналитические запросы.

### 10. 📝 my reference books
- Файлы: [my reference books/A_B test.ipynb](my%20reference%20books/A_B%20test.ipynb), [my reference books/Python справочник.ipynb](my%20reference%20books/Python%20справочник.ipynb), [my reference books/Cправочник по SQL.ipynb](my%20reference%20books/Cправочник%20по%20SQL.ipynb) и другие ноутбуки
- Задача: рабочая подборка заметок, шпаргалок и примеров по SQL, Python, временным рядам и A/B-тестам.
- Технологии: Jupyter Notebook, Python, SQL, pandas, визуализации, аналитические заметки.

---

## ▶️ Как запустить проекты локально

### 1. Проект по анализу установленного ПО

```bash
cd project-01-software-eda
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze_software.py
```

### 2. Финтех-проект по SQL

```bash
cd project-02-sql-fintech
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/init_db.py
jupyter notebook notebooks/sql_analysis.ipynb
```

### 3. Локальный аналитический стек через Docker

```bash
cd docker-analytics
./start.sh
```

Остановить стек можно так:

```bash
cd docker-analytics
./stop.sh
```

---

## 🔐 Секреты и .env

Чтобы не хранить пароли и секреты в коде и README:

- В корне репозитория добавлены шаблоны `.env.example` и `.env` (файлы содержат только плейсхолдеры).  
- Файл `.env` должен содержать локальные значения и никогда не коммититься — в `.gitignore` уже добавлена соответствующая запись.
- docker-analytics и скрипты читают креды из `.env` (через `env_file` в docker-compose или via `source` в bash-скриптах).
- Рекомендуется:
  1. Скопировать `.env.example` → `.env` и заполнить реальные значения локально.
  2. Не коммитить `.env`.
  3. Заменить в скриптах жёстко закодированные пароли на чтение переменных окружения (если остались).

---

### 4. Архивные проекты

Для [archive-01-airflow-ecommerce](archive-01-airflow-ecommerce) и [archive-02-sql-ecommerce](archive-02-sql-ecommerce) достаточно открыть соответствующие файлы и воспроизвести примеры локально. Для [archive-03-powerbi-ecommerce](archive-03-powerbi-ecommerce) это скорее концепт и описание, чем готовый дашборд.

---

## 💼 Опыт работы

Портфолио отражает мой путь в области аналитики данных и BI: от SQL-запросов и EDA к ETL-пайплайнам, контейнерам и локальным аналитическим стеком. В проектах уделяю внимание практической полезности, читаемости кода и понятной визуализации результатов.

---

## 🎓 Образование и курсы

- MBA, маркетинг-менеджмент — МИРБИС
- Бухгалтерский учёт, анализ и аудит — Славянский государственный педагогический университет
- Инженер-механик — ХГТУСА
- Курсы: Data Science & ML (Python, NumPy, Pandas), продюсер онлайн-курсов

---

## 📬 Контакты

Готов к диалогу по аналитике данных, BI, SQL и автоматизации отчётности.

- Email: iamartur1111@gmail.com
- Телефон: +7 982 216-78-48
- GitHub: https://github.com/MartinMinart/data-portfolio

---

*Последнее обновление: 2026-08-11*
