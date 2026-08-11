#!/bin/bash

# ============================================================
# 📦 ЭКСПОРТ И ДИАГНОСТИКА DATA-PORTFOLIO
# ============================================================
# Запуск: bash DOWNLOAD.md
# Результат: папка EXPORT_FILES [DOWNLOAD] со всеми файлами
# ============================================================

PROJECT="data-portfolio"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🚀 Запуск экспорта для $PROJECT..."
echo ""

# === СОЗДАНИЕ ПАПОК ===
mkdir -p "EXPORT_FILES [DOWNLOAD]"/{01-core,02-export-readme,03-export-docker,04-export-cheatsheets,05-export-scripts,06-diagnostics}

echo "✅ Папки созданы:"
echo "   EXPORT_FILES [DOWNLOAD]/"
echo "   ├── 01-core/              - Основные файлы проекта"
echo "   ├── 02-export-readme/     - Все README файлы"
echo "   ├── 03-export-docker/     - Docker-compose файлы"
echo "   ├── 04-export-cheatsheets/- Памятки и справочники"
echo "   ├── 05-export-scripts/    - Диагностические скрипты"
echo "   └── 06-diagnostics/       - Отчёты диагностики"
echo ""

# === КОПИРОВАНИЕ ФАЙЛОВ ===

echo "📄 Копирование README файлов..."
cp README.md "EXPORT_FILES [DOWNLOAD]/01-core/" 2>/dev/null
cp docker-analytics/README.md "EXPORT_FILES [DOWNLOAD]/02-export-readme/README_docker-analytics.md" 2>/dev/null
cp project-01-software-eda/README.md "EXPORT_FILES [DOWNLOAD]/02-export-readme/README_software-eda.md" 2>/dev/null
cp project-02-sql-fintech/README.md "EXPORT_FILES [DOWNLOAD]/02-export-readme/README_sql-fintech.md" 2>/dev/null
cp airflow-dag/README.md "EXPORT_FILES [DOWNLOAD]/02-export-readme/README_airflow-dag.md" 2>/dev/null

echo "🐳 Копирование Docker-compose..."
cp docker-analytics/docker-compose.yml "EXPORT_FILES [DOWNLOAD]/03-export-docker/docker-compose_data-portfolio.yml" 2>/dev/null

echo "📚 Копирование памяток..."
cp Памятка_data-portfolio.md "EXPORT_FILES [DOWNLOAD]/04-export-cheatsheets/" 2>/dev/null
cp bashrc_reference.md "EXPORT_FILES [DOWNLOAD]/04-export-cheatsheets/" 2>/dev/null

echo "🔧 Копирование скриптов..."
cp diagnose.sh "EXPORT_FILES [DOWNLOAD]/05-export-scripts/" 2>/dev/null
cp analyze_structure.py "EXPORT_FILES [DOWNLOAD]/05-export-scripts/" 2>/dev/null
cp commit-all.sh "EXPORT_FILES [DOWNLOAD]/05-export-scripts/" 2>/dev/null
cp docker-diag "EXPORT_FILES [DOWNLOAD]/05-export-scripts/" 2>/dev/null

echo ""
echo "=== ЗАПУСК ДИАГНОСТИКИ ==="

pa > "EXPORT_FILES [DOWNLOAD]/06-diagnostics/analysis_${DATE}.txt" 2>&1
docker-diag > "EXPORT_FILES [DOWNLOAD]/06-diagnostics/docker_diag_${DATE}.txt" 2>&1
./diagnose.sh > "EXPORT_FILES [DOWNLOAD]/06-diagnostics/full_diagnose_${DATE}.txt" 2>&1
dps > "EXPORT_FILES [DOWNLOAD]/06-diagnostics/containers_status_${DATE}.txt" 2>&1

echo ""
echo "✅ ДИАГНОСТИКА ЗАВЕРШЕНА!"
echo ""
echo "📁 Структура экспорта:"
echo "   EXPORT_FILES [DOWNLOAD]/"
echo "   ├── 01-core/              - Основные файлы проекта"
echo "   ├── 02-export-readme/     - Все README файлы"
echo "   ├── 03-export-docker/     - Docker-compose файлы"
echo "   ├── 04-export-cheatsheets/- Памятки и справочники"
echo "   ├── 05-export-scripts/    - Диагностические скрипты"
echo "   └── 06-diagnostics/       - Отчёты диагностики"
echo ""
echo "📄 Отчёты диагностики:"
echo "   - analysis_${DATE}.txt"
echo "   - docker_diag_${DATE}.txt"
echo "   - full_diagnose_${DATE}.txt"
echo "   - containers_status_${DATE}.txt"