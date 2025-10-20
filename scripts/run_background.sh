#!/bin/bash

# Скрипт запуска бота в фоновом режиме (простой способ без systemd)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🤖 Запуск High Focus Bot в фоновом режиме..."

# Проверяем, не запущен ли уже бот
if pgrep -f "python.*bot.py" > /dev/null; then
    echo "⚠️  Бот уже запущен!"
    echo ""
    echo "PID процесса:"
    pgrep -f "python.*bot.py"
    echo ""
    echo "Для остановки используйте:"
    echo "  pkill -f 'python.*bot.py'"
    exit 1
fi

# Активируем виртуальное окружение и запускаем
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Запустите: ./start.sh"
    exit 1
fi

source venv/bin/activate

# Запускаем в фоновом режиме с nohup
nohup python bot.py > bot.log 2>&1 &

PID=$!

echo "✅ Бот запущен в фоновом режиме!"
echo "📋 PID: $PID"
echo "📄 Логи: $SCRIPT_DIR/bot.log"
echo ""
echo "Полезные команды:"
echo "  Просмотр логов:  tail -f bot.log"
echo "  Остановить бота: kill $PID"
echo "  или:             pkill -f 'python.*bot.py'"
echo "  Список процессов: ps aux | grep bot.py"
echo ""

