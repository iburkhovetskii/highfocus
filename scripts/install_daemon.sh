#!/bin/bash

# Установка Launch Daemon для работы бота в любом режиме (даже при закрытом ноутбуке)

echo "🔧 Установка High Focus Bot как Launch Daemon"
echo "Бот будет работать всегда, даже когда ноутбук закрыт"
echo ""

PLIST_FILE="/Users/iliaburkhovetskii/highfocus/com.highfocus.bot.daemon.plist"
INSTALL_PATH="/Library/LaunchDaemons/com.highfocus.bot.daemon.plist"

# Останавливаем старый сервис если есть
sudo launchctl unload "$INSTALL_PATH" 2>/dev/null || true

# Копируем новый файл
sudo cp "$PLIST_FILE" "$INSTALL_PATH"
sudo chown root:wheel "$INSTALL_PATH"
sudo chmod 644 "$INSTALL_PATH"

# Загружаем сервис
sudo launchctl load "$INSTALL_PATH"

echo ""
echo "✅ Launch Daemon установлен!"
echo ""
echo "Бот теперь будет работать:"
echo "  ✓ При закрытом ноутбуке"
echo "  ✓ В режиме сна"
echo "  ✓ При старте системы"
echo "  ✓ Автоматический перезапуск при сбое"
echo ""
echo "Управление:"
echo "  Статус:      sudo launchctl list | grep highfocus"
echo "  Остановить:  sudo launchctl unload $INSTALL_PATH"
echo "  Запустить:   sudo launchctl load $INSTALL_PATH"
echo "  Логи:        tail -f /Users/iliaburkhovetskii/highfocus/bot.log"

