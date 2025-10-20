#!/bin/bash

# Скрипт быстрого запуска бота High Focus

echo "🚀 Запуск High Focus Bot..."
echo ""

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "⚠️  Виртуальное окружение не найдено. Создаём..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверка зависимостей
if ! python -c "import aiogram" 2>/dev/null; then
    echo "📦 Установка зависимостей..."
    pip install -r requirements.txt
    echo "✅ Зависимости установлены"
fi

# Проверка файла .env
if [ ! -f ".env" ]; then
    echo ""
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env и добавьте в него:"
    echo "   BOT_TOKEN=your_token_here"
    echo ""
    exit 1
fi

# Запуск бота
echo ""
echo "✅ Всё готово! Запуск бота..."
echo "📌 Для остановки нажмите Ctrl+C"
echo ""
python bot.py

