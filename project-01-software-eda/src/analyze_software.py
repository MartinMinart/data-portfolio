"""
Software Analysis Module
Анализ установленного ПО: загрузка, очистка, визуализация и генерация отчетов.

Автор: Artur Minart
Дата: 2026-05-20
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime


def load_data(filepath: str) -> pd.DataFrame:
    """Загружает CSV файл с данными о ПО."""
    df = pd.read_csv(filepath)
    print(f"✅ Загружено {len(df)} записей о программном обеспечении")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Очищает данные: приводит типы, обрабатывает пропуски."""
    # Преобразование даты
    df['install_date'] = pd.to_datetime(df['install_date'])
    
    # Приведение типов числовых колонок
    df['size_mb'] = pd.to_numeric(df['size_mb'], errors='coerce')
    
    # Удаление дубликатов (если есть)
    initial_count = len(df)
    df = df.drop_duplicates(subset=['software_name', 'version'])
    if len(df) < initial_count:
        print(f"⚠️ Удалено {initial_count - len(df)} дубликатов")
    
    print("✅ Очистка данных завершена")
    return df


def perform_eda(df: pd.DataFrame) -> dict:
    """Выполняет разведочный анализ данных."""
    eda_report = {
        'total_software': len(df),
        'total_size_gb': round(df['size_mb'].sum() / 1024, 2),
        'categories': df['category'].value_counts().to_dict(),
        'top_vendors': df['vendor'].value_counts().head(5).to_dict(),
        'avg_size_mb': round(df['size_mb'].mean(), 2),
        'newest_install': df['install_date'].max().strftime('%Y-%m-%d'),
        'oldest_install': df['install_date'].min().strftime('%Y-%m-%d')
    }
    
    print("\n📊 Основные метрики:")
    print(f"   Всего программ: {eda_report['total_software']}")
    print(f"   Общий размер: {eda_report['total_size_gb']} ГБ")
    print(f"   Средний размер: {eda_report['avg_size_mb']} МБ")
    print(f"   Категорий: {len(eda_report['categories'])}")
    
    return eda_report


def create_visualizations(df: pd.DataFrame, output_dir: Path) -> list:
    """Создает и сохраняет графики анализа."""
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_files = []
    
    # Настройка стиля
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    
    # График 1: Распределение по категориям
    fig, ax = plt.subplots()
    category_counts = df['category'].value_counts()
    colors = plt.cm.Set3(range(len(category_counts)))
    ax.bar(category_counts.index, category_counts.values, color=colors)
    ax.set_title('Распределение ПО по категориям', fontsize=14, fontweight='bold')
    ax.set_xlabel('Категория')
    ax.set_ylabel('Количество')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    chart1_path = output_dir / '01_categories_distribution.png'
    plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
    plt.close()
    saved_files.append(str(chart1_path))
    print(f"✅ Сохранен график: {chart1_path.name}")
    
    # График 2: Топ вендоров
    fig, ax = plt.subplots()
    top_vendors = df['vendor'].value_counts().head(8)
    colors = plt.cm.Blues_r(range(len(top_vendors)))
    ax.barh(top_vendors.index, top_vendors.values, color=colors)
    ax.set_title('Топ-8 вендоров по количеству ПО', fontsize=14, fontweight='bold')
    ax.set_xlabel('Количество программ')
    ax.invert_yaxis()
    plt.tight_layout()
    
    chart2_path = output_dir / '02_top_vendors.png'
    plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
    plt.close()
    saved_files.append(str(chart2_path))
    print(f"✅ Сохранен график: {chart2_path.name}")
    
    # График 3: Размер по категориям
    fig, ax = plt.subplots()
    size_by_category = df.groupby('category')['size_mb'].sum().sort_values(ascending=False)
    colors = plt.cm.Oranges(range(len(size_by_category)))
    ax.bar(size_by_category.index, size_by_category.values / 1024, color=colors)  # в ГБ
    ax.set_title('Общий размер ПО по категориям (ГБ)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Категория')
    ax.set_ylabel('Размер (ГБ)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    chart3_path = output_dir / '03_size_by_category.png'
    plt.savefig(chart3_path, dpi=150, bbox_inches='tight')
    plt.close()
    saved_files.append(str(chart3_path))
    print(f"✅ Сохранен график: {chart3_path.name}")
    
    # График 4: Установки по времени (линейный график)
    fig, ax = plt.subplots()
    installs_by_month = df.set_index('install_date').resample('M')['software_name'].count()
    ax.plot(installs_by_month.index, installs_by_month.values, marker='o', linewidth=2, markersize=6)
    ax.set_title('Динамика установки ПО по месяцам', fontsize=14, fontweight='bold')
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Количество установок')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    chart4_path = output_dir / '04_install_timeline.png'
    plt.savefig(chart4_path, dpi=150, bbox_inches='tight')
    plt.close()
    saved_files.append(str(chart4_path))
    print(f"✅ Сохранен график: {chart4_path.name}")
    
    return saved_files


def generate_report(eda_results: dict, charts: list, output_dir: Path) -> str:
    """Генерирует текстовый отчет по анализу."""
    report_path = output_dir / 'analysis_report.txt'
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("ОТЧЕТ ПО АНАЛИЗУ УСТАНОВЛЕННОГО ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ\n")
        f.write("=" * 60 + "\n")
        f.write(f"Дата генерации: {timestamp}\n\n")
        
        f.write("📊 ОСНОВНЫЕ МЕТРИКИ\n")
        f.write("-" * 40 + "\n")
        f.write(f"Всего программ: {eda_results['total_software']}\n")
        f.write(f"Общий размер: {eda_results['total_size_gb']} ГБ\n")
        f.write(f"Средний размер программы: {eda_results['avg_size_mb']} МБ\n")
        f.write(f"Период установок: {eda_results['oldest_install']} — {eda_results['newest_install']}\n\n")
        
        f.write("📁 РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ\n")
        f.write("-" * 40 + "\n")
        for category, count in sorted(eda_results['categories'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"{category}: {count} шт.\n")
        f.write("\n")
        
        f.write("🏆 ТОП ВЕНДОРОВ\n")
        f.write("-" * 40 + "\n")
        for vendor, count in eda_results['top_vendors'].items():
            f.write(f"{vendor}: {count} шт.\n")
        f.write("\n")
        
        f.write("📈 СОЗДАННЫЕ ВИЗУАЛИЗАЦИИ\n")
        f.write("-" * 40 + "\n")
        for chart in charts:
            f.write(f"- {Path(chart).name}\n")
        f.write("\n")
        
        f.write("=" * 60 + "\n")
        f.write("Аналитик: Artur Minart | Data Analyst Portfolio\n")
        f.write("=" * 60 + "\n")
    
    print(f"✅ Отчет сохранен: {report_path.name}")
    return str(report_path)


def main():
    """Основная функция запуска анализа."""
    print("🚀 Запуск анализа программного обеспечения...\n")
    
    # Определение путей
    base_dir = Path(__file__).parent.parent
    data_path = base_dir / 'data' / 'installed_software.csv'
    output_dir = base_dir / 'output' / 'charts'
    reports_dir = base_dir / 'output' / 'reports'
    
    # Проверка существования файла
    if not data_path.exists():
        print(f"❌ Файл не найден: {data_path}")
        return
    
    # Загрузка данных
    df = load_data(str(data_path))
    
    # Очистка данных
    df = clean_data(df)
    
    # EDA
    eda_results = perform_eda(df)
    
    # Визуализация
    print("\n🎨 Создание визуализаций...")
    charts = create_visualizations(df, output_dir)
    
    # Генерация отчета
    print("\n📝 Генерация отчета...")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = generate_report(eda_results, charts, reports_dir)
    
    print("\n" + "=" * 50)
    print("✅ Анализ завершен успешно!")
    print(f"Графики: {len(charts)} файлов в {output_dir}")
    print(f"Отчет: {report_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
