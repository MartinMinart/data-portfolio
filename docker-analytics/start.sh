#!/bin/bash
echo "🚀 Запуск аналитического стека..."

# Запускаем контейнеры
docker compose up -d

# Ждём запуска PostgreSQL
echo "⏳ Ожидание запуска PostgreSQL..."
sleep 10

# Импортируем данные
./import-data.sh

echo ""
echo "✅ Аналитический стек запущен!"
echo ""
echo "📌 Доступные сервисы:"
echo "   Metabase:  http://localhost:3033"
echo "   PgAdmin:   http://localhost:5051"
echo "   PostgreSQL: localhost:5435"
echo ""
echo "🔐 Данные для входа:"
echo "   Metabase: Создай аккаунт при первом входе"
echo "   PostgreSQL: user=analyst, password=analyst123, db=analytics"
echo "   PgAdmin: admin@analytics.com / admin123"
