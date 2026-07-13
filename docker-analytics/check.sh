#!/bin/bash

echo "========================================="
echo "    ДИАГНОСТИКА DOCKER-СТЕКА"
echo "========================================="

# Переменные
PG_CONTAINER="data-portfolio-postgres"
PG_PORT="5435"
PG_USER="postgres"
PG_PASSWORD="postgres"

# 1. Проверка текущей директории
echo ""
echo "📍 Текущая директория: $(pwd)"

# 2. Проверка запущенных контейнеров
echo ""
echo "📦 Запущенные контейнеры:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 3. Проверка PostgreSQL (правильное имя контейнера)
echo ""
echo "🐘 Проверка PostgreSQL (контейнер: $PG_CONTAINER):"
docker exec $PG_CONTAINER psql -U $PG_USER -c "\l" 2>/dev/null || echo "❌ PostgreSQL не доступен"

# 4. Создание базы данных для Metabase
echo ""
echo "📊 Создание базы данных metabase:"
docker exec $PG_CONTAINER psql -U $PG_USER -c "CREATE DATABASE metabase;" 2>/dev/null && echo "✅ База metabase создана" || echo "⚠️ База metabase уже существует или ошибка"

# 5. Создание базы данных credit_risk_db
echo ""
echo "📊 Создание базы данных credit_risk_db:"
docker exec $PG_CONTAINER psql -U $PG_USER -c "CREATE DATABASE credit_risk_db;" 2>/dev/null && echo "✅ База credit_risk_db создана" || echo "⚠️ База credit_risk_db уже существует или ошибка"

# 6. Проверка размеров баз данных
echo ""
echo "📊 Размеры баз данных:"
docker exec $PG_CONTAINER psql -U $PG_USER -c "
SELECT datname, pg_size_pretty(pg_database_size(datname)) 
FROM pg_database 
WHERE datistemplate = false 
ORDER BY pg_database_size(datname) DESC;"

# 7. Проверка credit_risk_db
echo ""
echo "📋 Проверка credit_risk_db:"
docker exec $PG_CONTAINER psql -U $PG_USER -d credit_risk_db -c "\dt" 2>/dev/null || echo "ℹ️ В базе credit_risk_db пока нет таблиц"

# 8. Проверка логов Metabase
echo ""
echo "📋 Логи Metabase (последние 5 строк):"
docker logs data-portfolio-metabase --tail=5 2>&1

# 9. Перезапуск Metabase
echo ""
echo "🔄 Перезапуск Metabase..."
docker restart data-portfolio-metabase
sleep 5

# 10. Проверка статуса
echo ""
echo "📦 Статус после перезапуска:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "========================================="
echo "✅ Диагностика завершена"
echo ""chmod +x check.sh
./check.sh
echo "🔗 Доступные сервисы:"
echo "  - PostgreSQL: localhost:5435 (user: postgres, password: postgres)"
echo "  - Metabase: http://localhost:3033"
echo "  - PgAdmin: http://localhost:5051 (email: admin@admin.com, password: admin)"
echo "========================================="