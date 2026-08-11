# 📚 ПАМЯТКА ПО РАБОТЕ С DATA-PORTFOLIO

## 📁 СТРУКТУРА ПРОЕКТА
data-portfolio/
├── docker-analytics/ # Docker стек (PostgreSQL + Metabase + PgAdmin)
│ ├── docker-compose.yml # Конфигурация сервисов
│ ├── .env # Переменные окружения (НЕ КОММИТИТЬ!)
│ ├── init-scripts/ # SQL скрипты инициализации
│ ├── start.sh # Запуск стека
│ ├── stop.sh # Остановка стека
│ └── README.md # Документация
├── project-01-software-eda/ # Анализ установленного ПО
├── project-02-sql-fintech/ # Финтех-аналитика на SQL
├── airflow-dag/ # ETL-пайплайн в Airflow
├── archive-*/ # Архивные проекты
├── .env # Глобальные переменные (НЕ КОММИТИТЬ!)
├── .env.example # Шаблон переменных
├── .gitignore # Игнорируемые файлы
├── diagnose.sh # Диагностика проекта
└── README.md # Главный README

---

## 🚀 БЫСТРЫЕ КОМАНДЫ

### Перемещение по проекту
```bash
cd /workspaces/data-portfolio          # В корень проекта
cd docker-analytics                    # В папку Docker стека
cd project-01-software-eda             # В проект EDA
cd project-02-sql-fintech              # В SQL проект
Docker стек
bash
cd docker-analytics
docker-compose up -d                   # Запустить все сервисы
docker-compose down                    # Остановить все сервисы
docker-compose ps                      # Статус контейнеров
docker-compose logs --tail=50          # Последние логи
docker-compose logs -f                 # Логи в реальном времени
```
Проверка сервисов
```bash
# PostgreSQL
docker exec data-portfolio-postgres psql -U analyst -d analytics -c "SELECT version();"

# Metabase
curl http://localhost:3033/api/health

# PgAdmin
curl -s -o /dev/null -w "%{http_code}" http://localhost:5051
```

Диагностика
```bash
./diagnose.sh                          # Полная диагностика проекта
./diagnose.sh > diagnosis_$(date +%Y%m%d_%H%M%S).txt  # Сохранить отчёт
```

🔗 ДОСТУП К СЕРВИСАМ
Сервис	URL	Логин	Пароль
Metabase	http://localhost:3033	(при первом запуске)	(задайте сами)
PgAdmin	http://localhost:5051	admin@analytics.com	из .env
PostgreSQL	localhost:5435	analyst	из .env


## 🔐 БЕЗОПАСНОСТЬ
Никогда не коммитьте!
```bash
.env          # Реальные пароли
.env.local    # Локальные переменные
*.log         # Логи
__pycache__/  # Кэш Python
Создание .env из шаблона
bash
cp .env.example .env
nano .env  # Заполните реальными паролями
```

## 🛠️ ПОЛЕЗНЫЕ КОМАНДЫ
Работа с Git
```bash
git status                           # Статус изменений
git add .                            # Добавить все изменения
git commit -m "сообщение"            # Создать коммит
git push                             # Отправить в GitHub
git pull                             # Получить изменения
git checkout -b new-branch           # Создать новую ветку
```
Работа с Python
```bash
python -m venv .venv                 # Создать виртуальное окружение
source .venv/bin/activate            # Активировать (Linux/Mac)
pip install -r requirements.txt      # Установить зависимости
python src/analyze_software.py       # Запустить скрипт
```
Работа с Docker
```bash
docker ps                            # Список запущенных контейнеров
docker ps -a                         # Все контейнеры
docker images                        # Список образов
docker volume ls                     # Список томов
docker system df                     # Использование диска
docker system prune -f               # Очистка (осторожно!)
```

## ⚙️ НАСТРОЙКА АЛИАСОВ (сокращений)
Добавьте в ~/.bashrc или ~/.zshrc:

```bash
# Для data-portfolio
alias dp='cd /workspaces/data-portfolio'
alias dpa='cd /workspaces/data-portfolio/docker-analytics'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dpl='cd /workspaces/data-portfolio/docker-analytics && docker-compose logs --tail=50'
alias dpu='cd /workspaces/data-portfolio/docker-analytics && docker-compose up -d'
alias dpd='cd /workspaces/data-portfolio/docker-analytics && docker-compose down'

# Общие алиасы
alias pa='python /workspaces/data-portfolio/analyze_structure.py'
alias docker-diag='bash /workspaces/data-portfolio/diagnose.sh'
alias st='git status'
alias gst='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
```

Применить изменения:

```bash
source ~/.bashrc   # или source ~/.zshrc
```


## 🔧 **Добавляем алиасы в .bashrc - пример**

```bash
echo '
# ============ GIT ALIASES ============
alias st="git status"
alias gst="git status"
alias ga="git add ."
alias gc="git commit -m"
alias gp="git push"
alias gl="git pull"
alias gco="git checkout"
alias gb="git branch"
alias gd="git diff"
' >> ~/.bashrc

# Применить изменения
source ~/.bashrc

## 🎯 ПОСЛЕДОВАТЕЛЬНОСТЬ РАБОТЫ
1. Начать работу
```bash
cd /workspaces/data-portfolio
st                    # Проверить статус Git
./diagnose.sh         # Проверить состояние проекта
cd docker-analytics
docker-compose ps     # Проверить контейнеры
```

2. Внести изменения
```bash
# Отредактировать файлы
nano docker-analytics/docker-compose.yml

# Проверить
docker-compose config  # Проверить YAML синтаксис

# Перезапустить
docker-compose down && docker-compose up -d
```

3.cd /workspaces/data-portfolio

# Добавить новые файлы
git add commit-all.sh Памятка_data-portfolio.md

# Создать коммит
git commit -m "feat: add commit-all.sh script and update cheat sheet

- Add commit-all.sh for quick commits (like in docker-experiments)
- Update cheat sheet with Git commands and aliases
- Add Git aliases to .bashrc (st, ga, gc, gp, gl, etc.)"

# Отправить
git push Закоммитить
```bash
git add .
git commit -m "описание изменений"
git push
```

## 🧾 ШПАРГАЛКА ПО GIT И КОММИТАМ

### Быстрый цикл работы
```bash
cd /workspaces/data-portfolio
git status
git add .
git commit -m "описание изменений"
git push
```

### Быстрый вариант для всех изменений
```bash
./commit-all.sh "обновил папки и файлы"
Полезные алиасы (по аналогии с другими проектами)
bash
alias st='git status'
alias gst='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
```

#### Создание Pull Request
```bash
# Через GitHub CLI
gh pr create --title "название PR" --body "описание PR"

# Или вручную через браузер
# https://github.com/MartinMinart/data-portfolio/pull/new/chore/env-and-audit
```

## ❓ ЧАСТЫЕ ПРОБЛЕМЫ
"Port already in use"
```bash
# Найти процесс на порту
lsof -i :5435
# или
netstat -tulpn | grep 5435

# Изменить порт в .env
POSTGRES_PORT=5436
"Permission denied"
bash
chmod +x diagnose.sh
chmod +x docker-analytics/start.sh
"No such file or directory"
bash
# Проверить, где вы находитесь
pwd
# Перейти в нужную директорию
cd /workspaces/data-portfolio
```

## 📚 ПОЛЕЗНЫЕ ССЫЛКИ
- PostgreSQL документация (https://www.postgresql.org/docs/)
- Metabase документация (https://www.metabase.com/docs/latest/)
- Docker документация (https://docs.docker.com/)
- Apache Airflow документация (https://airflow.apache.org/docs/)



## 📅 ПОСЛЕДНЕЕ ОБНОВЛЕНИЕ
Дата: 2026-08-11
Автор: Artur Minart

Эта памятка создана для быстрой работы с проектом data-portfolio
