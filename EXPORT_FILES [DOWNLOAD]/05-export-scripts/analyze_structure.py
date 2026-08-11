#!/usr/bin/env python3
"""
Универсальный анализатор структуры проекта
Работает с любым Python проектом: data-portfolio, ML проекты, веб-приложения и т.д.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import subprocess

class UniversalProjectAnalyzer:
    def __init__(self, root_path="."):
        self.root = Path(root_path).resolve()
        self.config = self.load_config()
        
    def load_config(self):
        """Загружает конфигурацию анализатора"""
        return {
            "ignore_dirs": [".git", "__pycache__", "node_modules", ".venv", "venv", "env", ".conda", ".vscode", ".github"],
            "ignore_files": [".DS_Store", "*.pyc", "*.pyo", "*.so", "*.dll"],
            "max_depth": 4,
            "important_extensions": {
                ".py": "🐍 Python",
                ".ipynb": "📓 Jupyter",
                ".sql": "🗄️ SQL",
                ".md": "📝 Markdown",
                ".json": "🔧 JSON",
                ".yaml": "⚙️ YAML",
                ".yml": "⚙️ YAML",
                ".txt": "📄 Text",
                ".csv": "💾 CSV",
                ".xlsx": "📊 Excel",
                ".html": "🌐 HTML",
                ".css": "🎨 CSS",
                ".js": "📜 JavaScript",
                ".sh": "🐚 Shell",
                ".dockerfile": "🐳 Docker",
                ".toml": "🔧 TOML"
            }
        }
    
    def should_ignore(self, path):
        """Проверяет, нужно ли игнорировать файл/папку"""
        name = path.name
        if name in self.config["ignore_dirs"]:
            return True
        for pattern in self.config["ignore_files"]:
            if pattern.startswith("*."):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False
    
    def format_size(self, size_bytes):
        """Форматирует размер в человеко-читаемый формат"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        # Форматируем без десятичных для целых чисел
        if size_bytes == int(size_bytes):
            return f"{int(size_bytes)}{size_names[i]}"
        else:
            return f"{size_bytes:.1f}{size_names[i]}"
    
    def parse_size(self, size_str):
        """Парсит строку размера в байты (исправленная версия)"""
        try:
            # Если уже число, возвращаем как есть
            if isinstance(size_str, (int, float)):
                return float(size_str)
            
            size_str = str(size_str).strip().upper()
            
            # Извлекаем число и единицу измерения
            import re
            match = re.match(r'([\d.]+)\s*([KMGT]?B?)', size_str)
            if not match:
                return 0
            
            value = float(match.group(1))
            unit = match.group(2).replace('B', '')
            
            multipliers = {'': 1, 'K': 1024, 'M': 1048576, 'G': 1073741824, 'T': 1099511627776}
            multiplier = multipliers.get(unit, 1)
            
            return value * multiplier
        except:
            return 0
    
    def get_tree(self, path=None, prefix="", level=0, show_files=True):
        """Рекурсивно получает структуру папок"""
        if path is None:
            path = self.root
            
        if level > self.config["max_depth"]:
            return [f"{prefix}└── ... (глубина > {self.config['max_depth']})"]
        
        result = []
        try:
            items = []
            for item in sorted(path.iterdir()):
                if not self.should_ignore(item):
                    items.append(item)
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                
                if item.is_dir():
                    result.append(f"{prefix}{current_prefix}{item.name}/")
                    extension = "    " if is_last else "│   "
                    result.extend(self.get_tree(item, prefix + extension, level + 1, show_files))
                elif show_files:
                    size = self.format_size(item.stat().st_size)
                    result.append(f"{prefix}{current_prefix}{item.name} ({size})")
        except PermissionError:
            result.append(f"{prefix}├── [ДОСТУП ЗАПРЕЩЁН]")
        
        return result
    
    def analyze_project_type(self):
        """Определяет тип проекта"""
        project_indicators = {
            "data-portfolio": ["*.ipynb", "*.sql", "data/", "notebooks/"],
            "web-app": ["package.json", "requirements.txt", "app.py", "index.html"],
            "ml-project": ["*.ipynb", "model.pkl", "train.py", "data/"],
            "api-service": ["app.py", "main.py", "Dockerfile", "requirements.txt"],
            "cli-tool": ["setup.py", "cli.py", "main.py", "README.md"],
        }
        
        detected = []
        for proj_type, indicators in project_indicators.items():
            matches = 0
            for indicator in indicators:
                if indicator.endswith('/'):
                    if (self.root / indicator).exists():
                        matches += 1
                elif indicator.startswith('*.'):
                    ext = indicator[1:]
                    if any(self.root.rglob(f"*{ext}")):
                        matches += 1
                else:
                    if (self.root / indicator).exists():
                        matches += 1
            
            if matches >= 2:
                detected.append(proj_type)
        
        return detected if detected else ["unknown"]
    
    def get_git_info(self):
        """Получает информацию о Git репозитории"""
        try:
            # Проверяем, есть ли .git папка
            git_dir = self.root / ".git"
            if not git_dir.exists():
                return None
            
            # Получаем текущую ветку
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.root,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            # Получаем последний коммит
            commit = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=self.root,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            # Получаем количество коммитов
            commits = subprocess.check_output(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=self.root,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            return {
                "branch": branch,
                "last_commit": commit,
                "total_commits": int(commits)
            }
        except:
            return None
    
    def analyze_dependencies(self):
        """Анализирует зависимости проекта"""
        deps = {
            "python": None,
            "node": None,
            "docker": None
        }
        
        # Python зависимости
        req_file = self.root / "requirements.txt"
        if req_file.exists():
            try:
                content = req_file.read_text(encoding='utf-8', errors='ignore')
                deps["python"] = [line.strip() for line in content.split('\n') 
                                 if line.strip() and not line.startswith('#')]
            except:
                deps["python"] = ["[Ошибка чтения]"]
        
        # Проверяем pyproject.toml (Poetry)
        pyproject = self.root / "pyproject.toml"
        if pyproject.exists():
            deps["python_poetry"] = True
        
        # Node.js зависимости
        package_json = self.root / "package.json"
        if package_json.exists():
            try:
                import json as json_module
                data = json_module.loads(package_json.read_text(encoding='utf-8', errors='ignore'))
                deps["node"] = {
                    "dependencies": len(data.get("dependencies", {})),
                    "devDependencies": len(data.get("devDependencies", {}))
                }
            except:
                deps["node"] = {"error": "Cannot parse"}
        
        # Docker
        dockerfile = self.root / "Dockerfile"
        if dockerfile.exists():
            deps["docker"] = True
        
        return deps
    
    def find_issues(self):
        """Находит потенциальные проблемы в проекте"""
        issues = []
        
        # Проверяем SQL на STDDEV
        for sql_file in self.root.rglob("*.sql"):
            try:
                content = sql_file.read_text(encoding='utf-8', errors='ignore')
                if "STDDEV" in content.upper():
                    issues.append({
                        "type": "SQL Compatibility",
                        "file": str(sql_file.relative_to(self.root)),
                        "message": "Используется STDDEV (не работает в SQLite)"
                    })
            except:
                pass
        
        # Проверяем наличие README
        if not (self.root / "README.md").exists():
            issues.append({
                "type": "Documentation",
                "file": "README.md",
                "message": "Отсутствует README.md"
            })
        
        # Проверяем .gitignore
        if not (self.root / ".gitignore").exists():
            issues.append({
                "type": "Best Practice",
                "file": ".gitignore",
                "message": "Рекомендуется добавить .gitignore"
            })
        
        return issues
    
    def generate_report(self):
        """Генерирует полный отчет"""
        report = []
        report.append("=" * 90)
        report.append(f"📊 УНИВЕРСАЛЬНЫЙ АНАЛИЗ ПРОЕКТА")
        report.append(f"📍 Путь: {self.root}")
        report.append(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 90)
        
        # 1. Информация о проекте
        project_type = self.analyze_project_type()
        report.append(f"\n🏷️  Тип проекта: {', '.join(project_type)}")
        
        git_info = self.get_git_info()
        if git_info:
            report.append(f"🔀 Git ветка: {git_info['branch']}")
            report.append(f"💾 Коммитов: {git_info['total_commits']} (последний: {git_info['last_commit']})")
        
        # 2. Структура папок
        report.append("\n📁 СТРУКТУРА ПРОЕКТА:\n")
        report.extend(self.get_tree(show_files=True))
        
        # 3. Статистика файлов
        report.append("\n" + "=" * 90)
        report.append("📊 СТАТИСТИКА ФАЙЛОВ:\n")
        
        file_stats = defaultdict(lambda: {"count": 0, "size": 0})
        all_files = []
        
        for file_path in self.root.rglob("*"):
            if file_path.is_file() and not self.should_ignore(file_path):
                all_files.append(file_path)
                ext = file_path.suffix if file_path.suffix else "no_extension"
                size = file_path.stat().st_size
                file_stats[ext]["count"] += 1
                file_stats[ext]["size"] += size
        
        # Сортируем по количеству
        sorted_exts = sorted(file_stats.items(), key=lambda x: x[1]["count"], reverse=True)
        
        report.append(f"📄 Всего файлов: {len(all_files)}")
        report.append(f"💿 Общий размер: {self.format_size(sum(f.stat().st_size for f in all_files))}\n")
        
        for ext, stats in sorted_exts[:15]:  # Топ 15 расширений
            ext_name = self.config["important_extensions"].get(ext, ext)
            report.append(f"   {ext_name:<12} {stats['count']:>5} файлов  ({self.format_size(stats['size'])})")
        
        # 4. Зависимости
        report.append("\n" + "=" * 90)
        report.append("📦 ЗАВИСИМОСТИ:\n")
        
        deps = self.analyze_dependencies()
        if deps.get("python"):
            report.append(f"🐍 Python зависимости: {len(deps['python'])} пакетов")
            if len(deps['python']) <= 10:
                for dep in deps['python'][:10]:
                    report.append(f"   - {dep}")
            else:
                for dep in deps['python'][:5]:
                    report.append(f"   - {dep}")
                report.append(f"   ... и ещё {len(deps['python']) - 5}")
        
        if deps.get("node"):
            report.append(f"📦 Node.js: {deps['node'].get('dependencies', 0)} dependencies, {deps['node'].get('devDependencies', 0)} devDependencies")
        
        if deps.get("docker"):
            report.append(f"🐳 Docker: Dockerfile обнаружен")
        
        # 5. Проблемы
        issues = self.find_issues()
        if issues:
            report.append("\n" + "=" * 90)
            report.append("⚠️  ОБНАРУЖЕННЫЕ ПРОБЛЕМЫ:\n")
            for issue in issues:
                report.append(f"   🔴 [{issue['type']}] {issue['file']}")
                report.append(f"      💡 {issue['message']}")
        
        # 6. Рекомендации
        report.append("\n" + "=" * 90)
        report.append("💡 РЕКОМЕНДАЦИИ:\n")
        
        if "data-portfolio" in project_type:
            report.append("📊 Для Data Portfolio проекта:")
            report.append("   • Добавьте README.md с описанием каждого проекта")
            report.append("   • Убедитесь, что SQL запросы совместимы с SQLite")
            report.append("   • Добавьте requirements.txt для воспроизводимости")
        
        if not any("README.md" in str(f) for f in all_files):
            report.append("📝 Добавьте README.md с описанием проекта")
        
        if file_stats.get(".ipynb", {}).get("count", 0) > 0:
            report.append("📓 Очистите вывод Jupyter notebooks перед коммитом")
        
        # 7. Быстрые команды
        report.append("\n" + "=" * 90)
        report.append("🚀 БЫСТРЫЕ КОМАНДЫ:\n")
        report.append("   python analyze_structure.py --save    # Сохранить отчёт")
        report.append("   python analyze_structure.py --json    # Только JSON вывод")
        report.append("   python analyze_structure.py --tree    # Только дерево папок")
        
        report.append("\n" + "=" * 90)
        report.append("✅ Анализ завершён!")
        report.append("=" * 90)
        
        return "\n".join(report)
    
    def save_report(self, filename=None):
        """Сохраняет отчёт в файл"""
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report = self.generate_report()
        
        # Сохраняем текстовый отчёт
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Сохраняем JSON для машинной обработки
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.root),
            "project_type": self.analyze_project_type(),
            "git_info": self.get_git_info(),
            "stats": {
                "total_files": len(list(self.root.rglob("*"))),
                "extensions": dict(self.get_file_stats())
            },
            "issues": self.find_issues(),
            "dependencies": self.analyze_dependencies()
        }
        
        json_filename = filename.replace('.txt', '.json')
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        return filename, json_filename
    
    def get_file_stats(self):
        """Возвращает статистику по расширениям"""
        stats = defaultdict(lambda: {"count": 0, "size": 0})
        for file_path in self.root.rglob("*"):
            if file_path.is_file() and not self.should_ignore(file_path):
                ext = file_path.suffix if file_path.suffix else "no_extension"
                stats[ext]["count"] += 1
                stats[ext]["size"] += file_path.stat().st_size
        return stats

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Анализ структуры проекта')
    parser.add_argument('path', nargs='?', default='.', help='Путь к проекту')
    parser.add_argument('--save', '-s', action='store_true', help='Сохранить отчёт в файл')
    parser.add_argument('--json', '-j', action='store_true', help='Вывести только JSON')
    parser.add_argument('--tree', '-t', action='store_true', help='Показать только дерево папок')
    parser.add_argument('--depth', '-d', type=int, default=4, help='Глубина дерева папок')
    
    args = parser.parse_args()
    
    # Создаём анализатор
    analyzer = UniversalProjectAnalyzer(args.path)
    analyzer.config["max_depth"] = args.depth
    
    if args.json:
        # JSON вывод
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(analyzer.root),
            "project_type": analyzer.analyze_project_type(),
            "git_info": analyzer.get_git_info(),
            "stats": analyzer.get_file_stats(),
            "issues": analyzer.find_issues()
        }
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    elif args.tree:
        # Только дерево
        print("\n".join(analyzer.get_tree()))
    elif args.save:
        # Сохраняем отчёт
        txt_file, json_file = analyzer.save_report()
        print(f"✅ Отчёты сохранены:")
        print(f"   📄 Текстовый: {txt_file}")
        print(f"   📊 JSON: {json_file}")
    else:
        # Выводим в консоль
        print(analyzer.generate_report())

if __name__ == "__main__":
    main()