#!/bin/bash

# Скрипт установки systemd service для High Focus Bot

set -e

echo "🤖 Установка High Focus Bot как systemd service"
echo "================================================"
echo ""

# Получаем текущий путь
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURRENT_USER=$(whoami)

echo "📁 Директория проекта: $SCRIPT_DIR"
echo "👤 Пользователь: $CURRENT_USER"
echo ""

# Проверяем наличие виртуального окружения
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Запустите сначала: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Проверяем наличие .env файла
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "⚠️  Файл .env не найден!"
    echo "Создайте файл .env с токеном бота перед установкой service."
    exit 1
fi

# Создаем временный файл service
SERVICE_FILE="/tmp/highfocus-bot.service"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=High Focus Telegram Bot
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$SCRIPT_DIR
Environment="PATH=$SCRIPT_DIR/venv/bin"
ExecStart=$SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/bot.py
Restart=always
RestartSec=10

# Логирование
StandardOutput=journal
StandardError=journal
SyslogIdentifier=highfocus-bot

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service файл создан"
echo ""
echo "📋 Для установки выполните следующие команды:"
echo ""
echo "sudo cp $SERVICE_FILE /etc/systemd/system/"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable highfocus-bot"
echo "sudo systemctl start highfocus-bot"
echo ""
echo "Проверить статус:"
echo "sudo systemctl status highfocus-bot"
echo ""
echo "Просмотр логов:"
echo "sudo journalctl -u highfocus-bot -f"
echo ""

read -p "Установить service сейчас? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Установка..."
    sudo cp "$SERVICE_FILE" /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable highfocus-bot
    sudo systemctl start highfocus-bot
    
    echo ""
    echo "✅ Service установлен и запущен!"
    echo ""
    echo "📊 Статус:"
    sudo systemctl status highfocus-bot --no-pager
    echo ""
    echo "Полезные команды:"
    echo "  Остановить:     sudo systemctl stop highfocus-bot"
    echo "  Перезапустить:  sudo systemctl restart highfocus-bot"
    echo "  Посмотреть логи: sudo journalctl -u highfocus-bot -f"
else
    echo ""
    echo "ℹ️  Service файл сохранен в: $SERVICE_FILE"
    echo "   Установите его вручную командами выше."
fi

echo ""
echo "✨ Готово!"

