# Project 01: Software EDA (Exploratory Data Analysis)

## Описание
Проект демонстрирует навыки сбора, очистки и визуального анализа данных о программном обеспечении на рабочем месте аналитика.

## Структура
- `data/`: Исходные данные (CSV)
- `src/`: Python скрипт для автоматического анализа
- `notebooks/`: Jupyter Notebook для интерактивного исследования
- `output/`: Сгенерированные графики и текстовые отчеты

## Как запустить

### Вариант 1: Python скрипт (Windows PowerShell)

```powershell
# Активируйте среду
conda activate data-work

# Перейдите в папку проекта
cd C:\Users\MI\Documents\GitHub\data-portfolio\project-01-software-eda

# Запустите скрипт
python src\analyze_software.py
```

### Вариант 2: Jupyter Notebook
В VS Code:
- Откройте notebooks/software_eda.ipynb
- Выберите kernel: Python 3.10 #Ваше ядро
- Нажмите "Run All" (▶▶)

В браузере:
```powershell
conda activate data-work
cd project-01-software-eda\notebooks
jupyter notebook
```

### Вариант 3: Git Bash (Linux/Mac)
```bash
conda activate data-work
cd ~/Documents/GitHub/data-portfolio/project-01-software-eda
python src/analyze_software.py
```

## Результаты
- После запуска в папке output/ появятся:
- Графики (output/charts/):
- - top_vendors.png — Топ-10 вендоров
- - install_timeline.png — Временная шкала установки
- Отчёты (output/reports/):
- - software_report_YYYYMMDD_HHMMSS.txt — Текстовый отчёт
