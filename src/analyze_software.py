
---

### ✅ Код для EDA и визуализации


```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def load_data(filepath):
    """Загрузка данных из CSV"""
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        print(f"✅ Загружено {len(df)} записей")
        return df
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return None

def analyze_categories(df):
    """Анализ по категориям"""
    if 'Category' in df.columns:
        category_counts = df['Category'].value_counts()
        print("\n📊 Топ категорий ПО:")
        print(category_counts.head(10))
        return category_counts
    else:
        print("⚠️ Колонка 'Category' не найдена")
        return None

def visualize_data(df, output_dir):
    """Создание визуализаций"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # График 1: Топ категорий
    if 'Category' in df.columns:
        plt.figure()
        df['Category'].value_counts().head(10).plot(kind='barh', color='steelblue')
        plt.title('Топ-10 категорий программного обеспечения')
        plt.xlabel('Количество программ')
        plt.tight_layout()
        plt.savefig(output_path / 'categories_top10.png', dpi=300)
        print(f"💾 Сохранен график: {output_path / 'categories_top10.png'}")
    
    # График 2: Распределение по производителям
    if 'Publisher' in df.columns:
        plt.figure()
        df['Publisher'].value_counts().head(10).plot(kind='bar', color='coral')
        plt.title('Топ-10 производителей ПО')
        plt.xlabel('Производитель')
        plt.ylabel('Количество программ')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_path / 'publishers_top10.png', dpi=300)
        print(f"💾 Сохранен график: {output_path / 'publishers_top10.png'}")
    
    plt.close('all')

def generate_report(df, output_dir):
    """Генерация отчета"""
    output_path = Path(output_dir)
    
    report = f"""# Отчет по анализу ПО

## Общая статистика
- Всего программ: {len(df)}
- Уникальных категорий: {df['Category'].nunique() if 'Category' in df.columns else 'N/A'}
- Уникальных производителей: {df['Publisher'].nunique() if 'Publisher' in df.columns else 'N/A'}

## Топ-10 категорий
"""
    
    if 'Category' in df.columns:
        for cat, count in df['Category'].value_counts().head(10).items():
            report += f"- {cat}: {count}\n"
    
    with open(output_path / 'report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"💾 Сохранен отчет: {output_path / 'report.md'}")

def main():
    """Основная функция"""
    print("🚀 Запуск анализа ПО...\n")
    
    # Пути
    data_path = Path('data/installed_software.csv')
    output_dir = 'output'
    
    # Проверка файла
    if not data_path.exists():
        # Пробуем найти файл в корневой папке
        root_path = Path('../installed_software.csv')
        if root_path.exists():
            data_path = root_path
        else:
            print(f"❌ Файл {data_path} не найден!")
            return
    
    # Загрузка данных
    df = load_data(data_path)
    if df is None:
        return
    
    # Показываем первые строки
    print("\n📋 Первые 5 записей:")
    print(df.head())
    
    # Анализ
    print("\n📈 Анализ данных...")
    analyze_categories(df)
    
    # Визуализация
    print("\n🎨 Создание визуализаций...")
    visualize_data(df, output_dir)
    
    # Отчет
    print("\n📝 Генерация отчета...")
    generate_report(df, output_dir)
    
    print("\n✅ Анализ завершен!")

if __name__ == "__main__":
    main()