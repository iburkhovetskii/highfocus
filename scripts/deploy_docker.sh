#!/bin/bash

# Скрипт для быстрого деплоя через Docker

echo "🐳 Деплой High Focus Bot через Docker"
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Установите: https://docs.docker.com/get-docker/"
    exit 1
fi

# Проверка .env
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте: echo 'BOT_TOKEN=your_token' > .env"
    exit 1
fi

# Остановка старых контейнеров
echo "🛑 Остановка старых контейнеров..."
docker-compose down 2>/dev/null

# Сборка
echo "🔨 Сборка Docker образа..."
docker-compose build

# Запуск
echo "🚀 Запуск бота..."
docker-compose up -d

# Проверка
echo ""
echo "✅ Бот запущен!"
echo ""
echo "Команды:"
echo "  Логи:        docker-compose logs -f"
echo "  Статус:      docker-compose ps"
echo "  Остановить:  docker-compose down"
echo "  Перезапуск:  docker-compose restart"
