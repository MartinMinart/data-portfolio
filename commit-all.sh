#!/usr/bin/env bash
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "📝 Usage: $0 <commit-message>"
  echo "📌 Example: $0 'update files'"
  exit 1
fi

message="$*"

echo "📂 Добавляем все изменения..."
git add -A

echo "💾 Создаём коммит: $message"
git commit -m "$message"

echo "🚀 Отправляем в GitHub..."
git push

echo "✅ Готово! Коммит отправлен: $message"
