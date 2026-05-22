import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Настройка стиля графиков
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def load_data(filepath):
    """Загрузка данных из CSV"""
    print(f"Загрузка данных из {filepath}...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Загружено {len(df)} записей.")
    print(f"Колонки: {list(df.columns)}")
    return df


def find_data_file(base_dir, filename='installed_software.csv'):
    """Попытаться найти файл данных в нескольких стандартных местах и вернуть путь.
    Ищем в: <base_dir>/data, <base_dir>/src, <base_dir> (корень проекта), текущая рабочая директория.
    """
    candidates = [
        os.path.join(base_dir, 'data', filename),
        os.path.join(base_dir, 'src', filename),
        os.path.join(base_dir, filename),
        os.path.join(os.getcwd(), filename),
    ]

    for p in candidates:
        if os.path.exists(p):
            print(f"Найден файл данных: {p}")
            return p

    # Не нашли — поднимем информативную ошибку с перечислением проверенных путей
    raise FileNotFoundError(
        "Файл данных не найден. Проверенные пути:\n" + "\n".join(candidates)
    )

def eda_report(df):
    """Разведочный анализ данных"""
    report = []
    report.append("=== Отчет по установленному ПО ===\n")
    report.append(f"Всего программ: {len(df)}")
    report.append(f"Всего уникальных вендоров: {df['Publisher'].nunique()}")
    
    # Проверка наличия колонки InstallDate
    if 'InstallDate' in df.columns:
        dates = pd.to_datetime(df['InstallDate'], errors='coerce')
        installed_recent = dates[dates > '2024-01-01'].count()
        report.append(f"Установлено после 2024-01-01: {installed_recent}")
    
    report.append("\nТоп-10 вендоров по количеству ПО:")
    top_vendors = df['Publisher'].value_counts().head(10)
    for vendor, count in top_vendors.items():
        report.append(f"  - {vendor}: {count}")
    
    report.append("\nТоп-10 программ:")
    top_programs = df['DisplayName'].value_counts().head(10)
    for program, count in top_programs.items():
        report.append(f"  - {program}: {count}")
    
    return "\n".join(report)

def plot_top_vendors(df, output_path):
    """График топ вендоров"""
    plt.figure(figsize=(12, 8))
    vendor_counts = df['Publisher'].value_counts().head(10)
    sns.barplot(x=vendor_counts.values, y=vendor_counts.index, hue=vendor_counts.index, palette='viridis', legend=False)
    plt.title('Топ-10 вендоров по количеству установленного ПО')
    plt.xlabel('Количество программ')
    plt.ylabel('Вендор')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"График сохранен: {output_path}")

def plot_install_timeline(df, output_path):
    """Временная шкала установки"""
    if 'InstallDate' not in df.columns:
        print("Колонка InstallDate не найдена, пропускаем график")
        return
    
    plt.figure(figsize=(12, 6))
    dates = pd.to_datetime(df['InstallDate'], errors='coerce')
    dates = dates.dropna()
    
    # Группировка по месяцам
    monthly = dates.dt.to_period('M').value_counts().sort_index()
    
    plt.plot(monthly.index.astype(str), monthly.values, marker='o')
    plt.title('Количество установленных программ по месяцам')
    plt.xlabel('Месяц')
    plt.ylabel('Количество')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"График сохранен: {output_path}")

def main():
    # Пути
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # пытаемся найти CSV в стандартных местах
    data_path = find_data_file(base_dir, 'installed_software.csv')
    charts_dir = os.path.join(base_dir, 'output', 'charts')
    reports_dir = os.path.join(base_dir, 'output', 'reports')
    
    # Убедимся, что папки существуют
    os.makedirs(charts_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # Загрузка
    df = load_data(data_path)
    
    # Покажем первые строки
    print("\nПервые 5 записей:")
    print(df.head())

    # Генерация отчета
    report_text = eda_report(df)
    report_filename = f"software_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = os.path.join(reports_dir, report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\nТекстовый отчет сохранен: {report_path}")

    # Графики
    plot_top_vendors(df, os.path.join(charts_dir, 'top_vendors.png'))
    plot_install_timeline(df, os.path.join(charts_dir, 'install_timeline.png'))


    print("\n" + "="*50)
    print("Анализ завершен успешно!")
    print("="*50)
    print(report_text)

if __name__ == "__main__":
    main()