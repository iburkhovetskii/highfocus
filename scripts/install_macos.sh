#!/bin/bash

# Скрипт установки launchd service для High Focus Bot (macOS)

set -e

echo "🍎 Установка High Focus Bot как macOS Launch Agent"
echo "================================================="
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

# Создаем временный файл plist
PLIST_NAME="com.highfocus.bot.plist"
PLIST_FILE="/tmp/$PLIST_NAME"
INSTALL_PATH="$HOME/Library/LaunchAgents"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.highfocus.bot</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/venv/bin/python</string>
        <string>$SCRIPT_DIR/bot.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/bot.log</string>
    
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/bot_error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>$SCRIPT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

echo "✅ Plist файл создан"
echo ""

# Создаем директорию LaunchAgents если её нет
mkdir -p "$INSTALL_PATH"

echo "📋 Для установки выполните следующие команды:"
echo ""
echo "cp $PLIST_FILE $INSTALL_PATH/"
echo "launchctl load $INSTALL_PATH/$PLIST_NAME"
echo ""
echo "Проверить статус:"
echo "launchctl list | grep highfocus"
echo ""
echo "Просмотр логов:"
echo "tail -f $SCRIPT_DIR/bot.log"
echo ""

read -p "Установить service сейчас? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Установка..."
    
    # Останавливаем если уже запущен
    launchctl unload "$INSTALL_PATH/$PLIST_NAME" 2>/dev/null || true
    
    # Копируем новый файл
    cp "$PLIST_FILE" "$INSTALL_PATH/"
    
    # Загружаем service
    launchctl load "$INSTALL_PATH/$PLIST_NAME"
    
    echo ""
    echo "✅ Service установлен и запущен!"
    echo ""
    echo "📊 Проверка:"
    sleep 2
    if launchctl list | grep -q "highfocus"; then
        echo "✓ Бот запущен!"
        launchctl list | grep highfocus
    else
        echo "⚠️  Бот не найден в списке процессов"
    fi
    echo ""
    echo "Полезные команды:"
    echo "  Остановить:     launchctl unload $INSTALL_PATH/$PLIST_NAME"
    echo "  Запустить:      launchctl load $INSTALL_PATH/$PLIST_NAME"
    echo "  Перезапустить:  launchctl unload $INSTALL_PATH/$PLIST_NAME && launchctl load $INSTALL_PATH/$PLIST_NAME"
    echo "  Посмотреть логи: tail -f $SCRIPT_DIR/bot.log"
    echo "  Удалить:        launchctl unload $INSTALL_PATH/$PLIST_NAME && rm $INSTALL_PATH/$PLIST_NAME"
else
    echo ""
    echo "ℹ️  Plist файл сохранен в: $PLIST_FILE"
    echo "   Установите его вручную командами выше."
fi

echo ""
echo "✨ Готово!"

