## 📚 **ПАМЯТКА ПО .BASHRC И АЛИАСАМ**

### 📍 **Где находится .bashrc**

Файл `.bashrc` находится в **домашней директории** пользователя:

```bash
# Полный путь
/home/codespace/.bashrc

# Или сокращённо
~/.bashrc
```

---

### 🔍 **Что такое .bashrc?**

**`.bashrc`** — это скрытый файл конфигурации оболочки **Bash** (Bourne Again SHell). Он автоматически выполняется при каждом запуске интерактивной сессии Bash (например, при открытии нового терминала). Этот файл используется для настройки окружения пользователя: задания переменных, создания алиасов (сокращённых команд), настройки внешнего вида командной строки и загрузки дополнительных функций.

**Простыми словами:** `.bashrc` — это ваш личный "набор настроек" для терминала, который загружается при каждом его открытии, чтобы вы сразу могли пользоваться удобными командами.

---

### 💡 **Что такое алиас (alias)?**

**Алиас (alias)** — это пользовательское сокращение для командной строки. Он позволяет заменить длинную или сложную команду на короткое и запоминающееся имя.

**Пример:**
```bash
# Вместо длинной команды:
cd /workspaces/data-portfolio/docker-analytics && docker-compose logs --tail=50

# Используем алиас:
dpl
```

**Синтаксис создания алиаса:**
```bash
alias короткое_имя='длинная_команда'
```

---

### 📂 **Как посмотреть все алиасы**

```bash
# Вывести все текущие алиасы
alias

# Найти алиасы по ключевому слову (например, для data-portfolio)
alias | grep "dp"

# Найти Git алиасы
alias | grep -E "st|ga|gc|gp|gl"

# Найти Docker алиасы
alias | grep -E "dpu|dpd|dpl|dps"
```

---

### 🛠️ **Как редактировать .bashrc**

```bash
# Открыть в редакторе nano
nano ~/.bashrc

# Открыть в VS Code
code ~/.bashrc

# Открыть в Sublime Text (если установлен)
subl ~/.bashrc
```

**После добавления новых алиасов нужно применить изменения:**
```bash
source ~/.bashrc
# или
. ~/.bashrc
```

---

### 📝 **Структура пользовательских настроек в .bashrc**

```bash
# ============================================================
# 🚀 ПОЛЬЗОВАТЕЛЬСКИЕ НАСТРОЙКИ
# ============================================================

# ============ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ============
export DATA_PORTFOLIO="/workspaces/data-portfolio"   # Путь к проекту

# ============ ПЕРЕМЕЩЕНИЕ ============
alias dp="cd $DATA_PORTFOLIO"                        # В корень проекта
alias dpa="cd $DATA_PORTFOLIO/docker-analytics"      # В папку Docker стека
alias dpsql="cd $DATA_PORTFOLIO/project-02-sql-fintech"  # В SQL проект

# ============ DOCKER ============
alias dpu="cd $DATA_PORTFOLIO/docker-analytics && docker-compose up -d"  # Запустить стек
alias dpd="cd $DATA_PORTFOLIO/docker-analytics && docker-compose down"   # Остановить стек
alias dpl="cd $DATA_PORTFOLIO/docker-analytics && docker-compose logs --tail=50"  # Логи
alias dps="docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"  # Статус контейнеров

# ============ GIT ============
alias st="git status"          # Статус
alias ga="git add ."           # Добавить все изменения
alias gc="git commit -m"       # Создать коммит
alias gp="git push"            # Отправить в GitHub
alias gl="git pull"            # Получить изменения

# ============ АНАЛИЗ ============
alias pa="python $DATA_PORTFOLIO/analyze_structure.py"  # Анализ структуры проекта
alias docker-diag="bash $DATA_PORTFOLIO/diagnose.sh"    # Диагностика Docker
```

---

### 🧪 **Как проверить, что алиасы работают**

```bash
# 1. Проверить, что алиас существует
type dpu

# 2. Проверить все алиасы для data-portfolio
alias | grep -E "dp|dpa|dpu|dpd|dpl|dps"

# 3. Проверить Git алиасы
alias | grep -E "st|ga|gc|gp|gl"

# 4. Выполнить тестовую команду
dp && pwd  # Должно показать /workspaces/data-portfolio
```

---

### ⚠️ **Частые ошибки и их решение**

| Проблема | Решение |
|----------|---------|
| `bash: alias: not found` | Проверьте синтаксис: `alias имя='команда'` (без пробелов вокруг `=`) |
| Алиас не работает после добавления | Выполните `source ~/.bashrc` |
| `Permission denied` при редактировании | Используйте `sudo nano ~/.bashrc` |
| Дублирующиеся алиасы | Ничего страшного, работают оба варианта |
| Алиас переопределён | Последний в файле имеет приоритет |

---

### 📋 **Полезные команды для работы с алиасами**

```bash
# Удалить алиас
unalias имя_алиаса

# Удалить все алиасы (осторожно!)
unalias -a

# Посмотреть, что делает алиас
type имя_алиаса

# Временно отключить алиас для одной команды
\имя_алиаса  # Например: \ls вместо ls
```

---

### 📚 **Дополнительные ресурсы**

- [Официальная документация Bash](https://www.gnu.org/software/bash/manual/)
- [Bash Aliases Guide](https://linuxize.com/post/bash-aliases/)
- [Bashrc как настроить окружение](https://www.digitalocean.com/community/tutorials/bash-alias)

---

### 💡 **Советы по использованию**

1. **Создавайте алиасы для часто используемых команд** — это экономит время и упрощает работу
2. **Группируйте алиасы по категориям** — так проще поддерживать порядок в `.bashrc`
3. **Используйте понятные имена** — чтобы через месяц не забыть, что делает алиас
4. **Комментируйте алиасы** — объясняйте, для чего они нужны
5. **Храните `.bashrc` в Git** — удобно переносить настройки между машинами

---

### 📁 **Полный путь к .bashrc**

```bash
# Домашняя директория пользователя
/home/codespace/.bashrc

# Проверить существование
ls -la ~/.bashrc

# Просмотреть содержимое
cat ~/.bashrc

# Открыть для редактирования
nano ~/.bashrc
```


## 📊 **ПОЛНЫЙ СПИСОК АЛИАСОВ ДЛЯ DATA-PORTFOLIO**

### 🚀 **Навигация**

### 📂 **Docker-experiments (быстрый доступ)**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `de` | `cd /workspaces/docker-experiments` | Переход в проект docker-experiments |
| `de-stack` | `cd /workspaces/docker-experiments/ai-stack` | Переход в папку AI-стек |

---

### 📂 **data-portfolio (быстрый доступ)**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `de` | `cd /workspaces/data-portfolio` | Переход в проект docker-experiments |
| `de-stack` | `cd /workspaces/data-portfolio/docker-analytics` | Переход в папку AI-стек |

---

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `dp` | `cd /workspaces/data-portfolio` | Переход в корень проекта data-portfolio |
| `dpa` | `cd /workspaces/data-portfolio/docker-analytics` | Переход в папку Docker стека |
| `dpsql` | `cd /workspaces/data-portfolio/project-02-sql-fintech` | Переход в SQL проект |
| `peda` | `cd /workspaces/data-portfolio/project-01-software-eda` | Переход в EDA проект |
| `de` | `cd /workspaces/docker-experiments` | Переход в проект docker-experiments |
| `de-stack` | `cd /workspaces/docker-experiments/ai-stack` | Переход в AI-стек docker-experiments |

---

### 🐳 **Docker (data-portfolio)**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `dpu` | `cd ~/data-portfolio/docker-analytics && docker-compose up -d` | Запустить Docker стек в фоне |
| `dpd` | `cd ~/data-portfolio/docker-analytics && docker-compose down` | Остановить Docker стек |
| `dpl` | `cd ~/data-portfolio/docker-analytics && docker-compose logs --tail=50` | Показать последние 50 строк логов |
| `dplf` | `cd ~/data-portfolio/docker-analytics && docker-compose logs -f` | Следить за логами в реальном времени |
| `dps` | `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` | Показать статус всех контейнеров |
| `dpa-ps` | `cd ~/data-portfolio/docker-analytics && docker-compose ps` | Показать статус контейнеров стека |
| `dpa-config` | `cd ~/data-portfolio/docker-analytics && docker-compose config` | Показать обработанную конфигурацию |
| `dp-up` | `cd ~/data-portfolio/docker-analytics && docker-compose up -d` | Запустить стек (синоним dpu) |
| `dp-down` | `cd ~/data-portfolio/docker-analytics && docker-compose down` | Остановить стек (синоним dpd) |
| `dp-logs` | `cd ~/data-portfolio/docker-analytics && docker-compose logs --tail=50` | Логи (синоним dpl) |
| `dp-ps` | `cd ~/data-portfolio/docker-analytics && docker-compose ps` | Статус стека (синоним dpa-ps) |
| `dp-check` | `./diagnose.sh` | Запустить диагностику проекта |

---

### 📊 **Анализ и диагностика**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `pa` | `python /workspaces/data-portfolio/analyze_structure.py` | Проанализировать структуру проекта |
| `docker-diag` | `bash /workspaces/data-portfolio/diagnose.sh` | Запустить диагностику Docker |
| `dp-check` | `./diagnose.sh` | Запустить диагностику (синоним) |

---

### 📝 **Git**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `st` | `git status` | Показать статус Git |
| `gst` | `git status` | Показать статус (синоним) |
| `ga` | `git add .` | Добавить все изменения в Git |
| `gc` | `git commit -m` | Создать коммит (нужно передать сообщение) |
| `gp` | `git push` | Отправить изменения в GitHub |
| `gl` | `git pull` | Получить изменения из GitHub |
| `gco` | `git checkout` | Переключить ветку |
| `gb` | `git branch` | Показать список веток |
| `gd` | `git diff` | Показать различия в файлах |
| `glog` | `git log --oneline --graph --all` | Показать историю коммитов в виде графа |

---

### 🚀 **Быстрые коммиты**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `commit` | `cd ~/data-portfolio && ./commit-all.sh` | Быстрый коммит (add + commit + push) |

---

### 🛠️ **Системные**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `cls` | `clear` | Очистить экран терминала |
| `..` | `cd ..` | Перейти на уровень выше |
| `...` | `cd ../..` | Перейти на два уровня выше |
| `....` | `cd ../../..` | Перейти на три уровня выше |
| `h` | `history` | Показать историю команд |
| `ll` | `ls -alF` | Показать все файлы с деталями |
| `la` | `ls -A` | Показать все файлы (включая скрытые) |
| `l` | `ls -CF` | Показать файлы в столбик |
| `help-dp` | `echo "справка..."` | Показать справку по алиасам |

---

## 📋 **Быстрая памятка**

```bash
# Самые полезные команды:

dp          # В корень проекта
dpa         # В docker-analytics
dpu         # Запустить стек
dpd         # Остановить стек
dpl         # Посмотреть логи
st          # Статус Git
ga          # Добавить все изменения
gc "текст"  # Создать коммит
gp          # Отправить в GitHub
pa          # Анализ проекта
docker-diag # Диагностика Docker
```

---

## 🔧 **Как посмотреть все алиасы**

```bash
# Все алиасы
alias

# Только алиасы для data-portfolio
alias | grep -E "dp|dpa|dpu|dpd|dpl|dps"

# Только Git алиасы
alias | grep -E "st|ga|gc|gp|gl"

# Только Docker алиасы
alias | grep -E "dpu|dpd|dpl|dps|docker"
```

---

## 💡 **Как добавить новый алиас**

```bash
# Временно (только для текущей сессии)
alias новое_имя='команда'

# Навсегда (добавить в .bashrc)
echo 'alias новое_имя="команда"' >> ~/.bashrc
source ~/.bashrc
```
## 🎉 **Отлично! Памятка получилась отличная!**

Вы хорошо структурировали информацию. Вот что можно добавить для полноты:

---

## 📝 **Добавить в bashrc_reference.md**

### 🔄 **Раздел: Переключение между проектами**

```bash
# ============ ПЕРЕКЛЮЧЕНИЕ МЕЖДУ ПРОЕКТАМИ ============
alias dp="cd /workspaces/data-portfolio"              # В data-portfolio
alias de="cd /workspaces/docker-experiments"          # В docker-experiments
alias dpa="cd /workspaces/data-portfolio/docker-analytics"
alias de-stack="cd /workspaces/docker-experiments/ai-stack"
```

---

### 🧪 **Раздел: Быстрая диагностика**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `dps` | `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` | Статус всех контейнеров |
| `docker-diag` | `bash ~/data-portfolio/diagnose.sh` | Полная диагностика Docker |
| `pa` | `python ~/data-portfolio/analyze_structure.py` | Анализ структуры проекта |

---

### 📝 **Раздел: Полезные команды для работы с .bashrc**

```bash
# ============ РАБОТА С .BASHRC ============
alias bashrc="nano ~/.bashrc"           # Открыть .bashrc для редактирования
alias bashrc-reload="source ~/.bashrc"  # Перезагрузить .bashrc
alias bashrc-show="cat ~/.bashrc"       # Показать содержимое .bashrc
alias bashrc-backup="cp ~/.bashrc ~/.bashrc.backup"  # Создать бэкап
```

**Добавить в таблицу:**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `bashrc` | `nano ~/.bashrc` | Открыть .bashrc для редактирования |
| `bashrc-reload` | `source ~/.bashrc` | Перезагрузить .bashrc (применить изменения) |
| `bashrc-show` | `cat ~/.bashrc` | Показать содержимое .bashrc |
| `bashrc-backup` | `cp ~/.bashrc ~/.bashrc.backup` | Создать резервную копию .bashrc |

---

### 🚀 **Раздел: Быстрый коммит**

```bash
# ============ БЫСТРЫЙ КОММИТ ============
alias commit="cd /workspaces/data-portfolio && ./commit-all.sh"
```

**Добавить в таблицу:**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `commit` | `cd ~/data-portfolio && ./commit-all.sh` | Быстрый коммит (add + commit + push) |

---

### 🛠️ **Раздел: Системные алиасы**

```bash
# ============ СИСТЕМНЫЕ ============
alias cls="clear"           # Очистить экран
alias ..="cd .."            # На уровень выше
alias ...="cd ../.."        # На два уровня выше
alias ....="cd ../../.."    # На три уровня выше
alias h="history"           # История команд
```

---

### 📋 **Итоговая структура добавлений**

Добавьте в конец файла `bashrc_reference.md`:

```markdown
---

## 🚀 **ДОПОЛНИТЕЛЬНЫЕ АЛИАСЫ**

### 📝 **Работа с .bashrc**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `bashrc` | `nano ~/.bashrc` | Открыть .bashrc для редактирования |
| `bashrc-reload` | `source ~/.bashrc` | Перезагрузить .bashrc (применить изменения) |
| `bashrc-show` | `cat ~/.bashrc` | Показать содержимое .bashrc |
| `bashrc-backup` | `cp ~/.bashrc ~/.bashrc.backup` | Создать резервную копию .bashrc |

### 🚀 **Быстрый коммит**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `commit` | `cd ~/data-portfolio && ./commit-all.sh` | Быстрый коммит (add + commit + push) |

### 📁 **Переключение между проектами**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `dp` | `cd /workspaces/data-portfolio` | В корень data-portfolio |
| `de` | `cd /workspaces/docker-experiments` | В корень docker-experiments |
| `dpa` | `cd /workspaces/data-portfolio/docker-analytics` | В Docker стек data-portfolio |
| `de-stack` | `cd /workspaces/docker-experiments/ai-stack` | В AI-стек docker-experiments |

### 🧪 **Быстрая диагностика**

| Алиас | Команда | Что делает |
|-------|---------|------------|
| `dps` | `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` | Статус всех контейнеров |
| `docker-diag` | `bash ~/data-portfolio/diagnose.sh` | Полная диагностика Docker |
| `pa` | `python ~/data-portfolio/analyze_structure.py` | Анализ структуры проекта |

---

## 💡 **Самые полезные команды (шпаргалка)**

```bash
# ⭐ ТОП-10 команд для ежедневной работы

dp          # В корень проекта data-portfolio
dpa         # В папку docker-analytics
dpu         # Запустить Docker стек
dpd         # Остановить Docker стек
dpl         # Посмотреть логи
st          # Статус Git
ga          # Добавить все изменения в Git
gc "текст"  # Создать коммит
gp          # Отправить в GitHub
pa          # Анализ структуры проекта
docker-diag # Диагностика Docker
```


