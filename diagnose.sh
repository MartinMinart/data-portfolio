#!/bin/bash

# ============================================
# Универсальный скрипт диагностики DATA-PORTFOLIO
# ============================================

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода заголовков
print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

# Функция для вывода секций
print_section() {
    echo -e "\n${GREEN}--- $1 ---${NC}\n"
}

# Очистка экрана и заголовок
clear
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════╗"
echo "║   DIAGNOSTIC REPORT - DATA-PORTFOLIO     ║"
echo "║   Generated: $(date '+%Y-%m-%d %H:%M:%S')            ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# 1. Текущая директория
print_section "Рабочая директория"
pwd
echo "User: $(whoami)"

# 2. Структура проекта
print_header "1. СТРУКТУРА ПРОЕКТА"
echo "Дерево файлов (макс. глубина 3):"
find . -maxdepth 3 -type f -not -path '*/\.*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' | head -30

echo -e "\n\nОсновные папки:"
ls -d */ 2>/dev/null | head -10

echo -e "\nКлючевые файлы:"
ls -lh docker-analytics/docker-compose.yml .env .env.example 2>/dev/null || echo "Некоторые файлы отсутствуют"

# 3. Проверка .env
print_header "2. ПРОВЕРКА .ENV"
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env существует${NC}"
    echo "Размер: $(wc -c < .env) bytes"
    echo -e "\nПеременные (без паролей):"
    grep -E "^[A-Z_]+=" .env | sed 's/=.*/=***/' | head -10
else
    echo -e "${RED}❌ .env не найден!${NC}"
    echo "Создайте .env из .env.example"
fi

if [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example существует${NC}"
else
    echo -e "${YELLOW}⚠️ .env.example отсутствует${NC}"
fi

# 4. Статус Docker контейнеров
print_header "3. DOCKER CONTAINERS STATUS"
if command -v docker &> /dev/null; then
    echo "Docker version: $(docker --version)"
    echo -e "\nЗапущенные контейнеры:"
    
    if [ -f "docker-analytics/docker-compose.yml" ]; then
        cd docker-analytics && docker compose ps 2>/dev/null && cd ..
    else
        docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null
    fi
    
    echo -e "\nИспользование ресурсов:"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" 2>/dev/null || echo "Stats unavailable"
else
    echo -e "${RED}Docker не установлен${NC}"
fi

# 5. Порты и сеть
print_header "4. PORTS & NETWORK"
echo "Проверка портов data-portfolio стека:"
for port in 5435 3033 5051; do
    if nc -z localhost $port 2>/dev/null; then
        echo "  Port $port: ✅ OPEN"
    else
        echo "  Port $port: ❌ CLOSED"
    fi
done

echo -e "\nDocker сети:"
docker network ls 2>/dev/null | grep -E "analytics-net|data-portfolio" || echo "Сети не найдены"

# 6. Проверка docker-analytics
print_header "5. DOCKER-ANALYTICS STACK"
if [ -f "docker-analytics/docker-compose.yml" ]; then
    echo -e "${GREEN}✅ docker-compose.yml существует${NC}"
    echo "Размер: $(wc -c < docker-analytics/docker-compose.yml) bytes"
    
    echo -e "\nСервисы в docker-compose:"
    grep -E "^  [a-z-]+:" docker-analytics/docker-compose.yml | sed 's/://g' | sed 's/^  //' | head -10
else
    echo -e "${RED}❌ docker-analytics/docker-compose.yml не найден!${NC}"
fi

# 7. Проверка PostgreSQL
print_header "6. POSTGRESQL"
if docker ps --format "{{.Names}}" | grep -q "data-portfolio-postgres"; then
    echo -e "${GREEN}✅ PostgreSQL контейнер запущен${NC}"
    
    # Проверка пользователя
    echo -e "\nПроверка пользователя analyst:"
    docker exec data-portfolio-postgres psql -U analyst -d analytics -c "SELECT version();" 2>/dev/null && echo -e "${GREEN}✅ Пользователь analyst существует${NC}" || echo -e "${RED}❌ Пользователь analyst не найден${NC}"
    
    # Проверка таблиц
    echo -e "\nТаблицы в базе analytics:"
    docker exec data-portfolio-postgres psql -U analyst -d analytics -c "\dt" 2>/dev/null || echo "Нет таблиц или ошибка доступа"
else
    echo -e "${RED}❌ PostgreSQL контейнер не запущен${NC}"
fi

# 8. Проверка Metabase
print_header "7. METABASE"
if docker ps --format "{{.Names}}" | grep -q "data-portfolio-metabase"; then
    echo -e "${GREEN}✅ Metabase контейнер запущен${NC}"
    echo -e "\nПроверка health endpoint:"
    curl -s http://localhost:3033/api/health 2>/dev/null | head -5 || echo "Metabase не отвечает"
else
    echo -e "${RED}❌ Metabase контейнер не запущен${NC}"
fi

# 9. Проверка PgAdmin
print_header "8. PGADMIN"
if docker ps --format "{{.Names}}" | grep -q "data-portfolio-pgadmin"; then
    echo -e "${GREEN}✅ PgAdmin контейнер запущен${NC}"
    echo -e "\nПроверка доступности:"
    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:5051 2>/dev/null || echo "PgAdmin не отвечает"
else
    echo -e "${RED}❌ PgAdmin контейнер не запущен${NC}"
fi

# 10. Проверка проектов
print_header "9. ПРОЕКТЫ ПОРТФОЛИО"
echo "Структура проектов:"

for project in project-01-software-eda project-02-sql-fintech airflow-dag; do
    if [ -d "$project" ]; then
        echo -e "\n${GREEN}✅ $project${NC}"
        if [ -f "$project/README.md" ]; then
            echo "  ✅ README.md"
        fi
        if [ -d "$project/src" ]; then
            echo "  ✅ src/ (файлов: $(find $project/src -name '*.py' 2>/dev/null | wc -l))"
        fi
        if [ -f "$project/requirements.txt" ]; then
            echo "  ✅ requirements.txt"
        fi
    else
        echo -e "\n${YELLOW}⚠️ $project не найден${NC}"
    fi
done

# 11. Проверка логов
print_header "10. ЛОГИ"
echo "Последние строки логов контейнеров:"

if [ -f "docker-analytics/docker-compose.yml" ]; then
    cd docker-analytics && docker compose logs --tail=10 2>/dev/null | tail -15 && cd ..
else
    echo "Логи недоступны"
fi

# 12. Проверка Volumes
print_header "11. DOCKER VOLUMES"
docker volume ls 2>/dev/null | grep -E "postgres|metabase|pgadmin" | head -10 || echo "Volumes не найдены"

# 13. Проверка .gitignore
print_header "12. .GITIGNORE"
if [ -f ".gitignore" ]; then
    echo -e "${GREEN}✅ .gitignore существует${NC}"
    echo -e "\nПравила защиты .env:"
    grep -E "\.env" .gitignore 2>/dev/null || echo "⚠️ .env не защищен в .gitignore!"
else
    echo -e "${RED}❌ .gitignore не найден!${NC}"
fi

# 14. Проблемы и рекомендации
print_header "13. ISSUES & RECOMMENDATIONS"
issues=0

# Проверка контейнеров
running_containers=$(docker ps -q 2>/dev/null | wc -l)
if [ "$running_containers" -gt 0 ]; then
    echo -e "${GREEN}✅ Запущено контейнеров: $running_containers${NC}"
else
    echo -e "${RED}❌ Нет запущенных контейнеров${NC}"
    ((issues++))
fi

# Проверка PostgreSQL
if docker ps --format "{{.Names}}" 2>/dev/null | grep -q "data-portfolio-postgres"; then
    echo -e "${GREEN}✅ PostgreSQL работает${NC}"
else
    echo -e "${RED}❌ PostgreSQL не запущен${NC}"
    ((issues++))
fi

# Проверка .env
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env отсутствует${NC}"
    ((issues++))
fi

# Проверка .gitignore
if grep -q "\.env" .gitignore 2>/dev/null; then
    echo -e "${GREEN}✅ .env защищен в .gitignore${NC}"
else
    echo -e "${YELLOW}⚠️ .env не защищен в .gitignore${NC}"
    ((issues++))
fi

# Итог
print_header "14. SUMMARY"
echo "Total issues found: $issues"
if [ $issues -eq 0 ]; then
    echo -e "${GREEN}🎉 Все системы работают нормально!${NC}"
else
    echo -e "${YELLOW}🔧 Требуется внимание к $issues проблемам${NC}"
fi

echo -e "\n${BLUE}============================================${NC}"
echo -e "${BLUE}END OF DIAGNOSTIC REPORT${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "\n📋 Скопируйте этот вывод и отправьте в чат для получения помощи"
echo "💡 Или выполните: ./diagnose.sh > diagnosis_$(date +%Y%m%d_%H%M%S).txt"
