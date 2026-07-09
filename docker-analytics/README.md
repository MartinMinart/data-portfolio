# 🐳 Docker Analytics Stack

Полностью контейнеризованный аналитический стек с PostgreSQL, Metabase и PgAdmin.

---

## 📋 Компоненты

- **PostgreSQL 15** — реляционная БД для хранения данных
- **Metabase** — открытая BI платформа для визуализации
- **PgAdmin 4** — веб-интерфейс для управления PostgreSQL

---

## 🚀 Быстрый старт

### 1. Подготовка (.env файл)

Скопируйте `.env.example` в `.env` и обновите пароли:

```bash
cp .env.example .env

# Сгенерируйте безопасные пароли (macOS/Linux):
# openssl rand -base64 32

# Отредактируйте .env с новыми паролями
nano .env
```

**⚠️ ВАЖНО:** Никогда не коммитьте `.env` в git! Он должен быть в `.gitignore`.

### 2. Запуск стека

```bash
cd docker-analytics
./start.sh
```

Или вручную:

```bash
docker-compose up -d
```

Проверьте статус:

```bash
docker-compose ps
```

### 3. Доступ к сервисам

| Сервис | URL | Учетные данные |
|--------|-----|----------------|
| **Metabase** | http://localhost:3033 | admin@example.com / пароль из .env |
| **PgAdmin** | http://localhost:5051 | admin@analytics.com / пароль из .env |
| **PostgreSQL** | localhost:5435 | analyst / пароль из .env |

### 4. Остановка стека

```bash
./stop.sh
```

Или вручную:

```bash
docker-compose down
```

---

## 📊 Подключение данных

### Вариант 1: Через PgAdmin Web UI

1. Откройте http://localhost:5051
2. Логин: `admin@analytics.com` 
3. Пароль: из файла `.env`
4. Создайте новое подключение к базе
5. Host: `postgres-analytics`, Port: `5432`

### Вариант 2: Через SQL скрипты

Поместите SQL файлы в папку `init-scripts/` перед запуском:

```bash
# Создайте новый SQL файл
echo "CREATE TABLE my_data AS SELECT * FROM ..." > init-scripts/02-my-tables.sql

# Перезагрузитесь
docker-compose down -v
docker-compose up -d
```

### Вариант 3: Через Python скрипт

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5435,
    database="analytics",
    user="analyst",
    password="your_password_here"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE example (id INT, name VARCHAR(100))")
conn.commit()
cursor.close()
conn.close()
```

### Вариант 4: Через Metabase UI

1. Откройте http://localhost:3033
2. Войдите с учетными данными (первый запуск)
3. **Admin Panel** → **Databases** → **Add database**
4. Выберите PostgreSQL
5. Параметры подключения:
   - Host: `postgres-analytics`
   - Port: `5432`
   - Database: `analytics`
   - Username: `analyst`
   - Password: из файла `.env`

---

## 🗂️ Структура проекта

```
docker-analytics/
├── docker-compose.yml      # Конфигурация сервисов
├── .env.example            # Шаблон переменных окружения
├── .env                    # Локальные переменные (НЕ коммитить!)
├── start.sh                # Скрипт запуска
├── stop.sh                 # Скрипт остановки
├── init-scripts/
│   └── 01-init-database.sql  # SQL скрипты инициализации
└── README.md               # Этот файл
```

---

## 📝 Примеры использования

### Пример 1: Загрузка CSV в PostgreSQL

```bash
# 1. Поместите CSV в контейнер
docker cp data.csv data-portfolio-postgres:/tmp/

# 2. Подключитесь к БД
docker exec -it data-portfolio-postgres psql -U analyst -d analytics

# 3. Создайте таблицу и импортируйте
CREATE TABLE my_data (id INT, name VARCHAR(100), value DECIMAL);
\COPY my_data FROM '/tmp/data.csv' WITH (FORMAT csv, HEADER true);
SELECT COUNT(*) FROM my_data;
```

### Пример 2: Backup БД

```bash
# Создать backup
docker exec data-portfolio-postgres \
  pg_dump -U analyst analytics > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановить backup
cat backup_20260709_142300.sql | \
  docker exec -i data-portfolio-postgres \
    psql -U analyst -d analytics
```

### Пример 3: Просмотр логов

```bash
# PostgreSQL логи
docker-compose logs -f postgres-analytics

# Metabase логи
docker-compose logs -f metabase

# Все логи
docker-compose logs -f
```

---

## 🔧 Troubleshooting

### Проблема: "Port already in use"

```bash
# Проверьте занятые порты
lsof -i :5435  # PostgreSQL
lsof -i :3033  # Metabase
lsof -i :5051  # PgAdmin

# Или измените порты в .env
POSTGRES_PORT=5436
METABASE_PORT=3034
PGADMIN_PORT=5052
```

### Проблема: "Connection refused"

```bash
# Проверьте статус контейнеров
docker-compose ps

# Посмотрите логи
docker-compose logs postgres-analytics

# Перезагрузитесь
docker-compose down -v
docker-compose up -d
```

### Проблема: "Database does not exist"

```bash
# Подключитесь к postgres
docker exec -it data-portfolio-postgres psql -U analyst

# Создайте БД
CREATE DATABASE analytics;
```

---

## 💾 Управление данными

### Удаление всех данных (WARNING!)

```bash
docker-compose down -v
```

Флаг `-v` удалит все volumes, включая данные PostgreSQL.

### Сохранение данных

Volumes автоматически сохраняются в Docker:
- `postgres_data` — данные PostgreSQL
- `metabase_data` — конфигурация Metabase

---

## 🔐 Безопасность

### Best Practices:

1. **Никогда не коммитьте `.env`** — добавьте в `.gitignore`
2. **Используйте сильные пароли** — минимум 32 символа
3. **Меняйте пароли регулярно** — раз в 90 дней
4. **Не используйте в production** — добавьте SSL/TLS, firewall
5. **Ограничьте доступ** — используйте VPN или IP whitelist

### Для Production:

```yaml
# Добавьте в docker-compose.yml:
services:
  postgres-analytics:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U analyst"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## 📚 Полезные команды

```bash
# Запуск в фоне
docker-compose up -d

# Остановка без удаления
docker-compose stop

# Перезагрузка
docker-compose restart

# Просмотр статуса
docker-compose ps

# Просмотр логов (последние 100 строк)
docker-compose logs --tail=100

# Следение за логами в реальном времени
docker-compose logs -f

# Удаление контейнеров
docker-compose down

# Удаление контейнеров + данных
docker-compose down -v

# Масштабирование (если используется)
docker-compose up -d --scale postgres-analytics=2
```

---

## 🎓 Дополнительные ресурсы

- [PostgreSQL документация](https://www.postgresql.org/docs/)
- [Metabase документация](https://www.metabase.com/docs/)
- [PgAdmin документация](https://www.pgadmin.org/docs/)
- [Docker Compose справка](https://docs.docker.com/compose/compose-file/)

---

## 👤 Автор

**Artur Minart** — Data Analyst Portfolio  
📧 iamartur1111@gmail.com  
🔗 [GitHub](https://github.com/MartinMinart/data-portfolio)

---

*Последнее обновление: 2026-07-09*
