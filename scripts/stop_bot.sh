#!/bin/bash

# Скрипт остановки бота

echo "🛑 Остановка High Focus Bot..."

if pgrep -f "python.*bot.py" > /dev/null; then
    pkill -f "python.*bot.py"
    echo "✅ Бот остановлен"
else
    echo "ℹ️  Бот не запущен"
fi

