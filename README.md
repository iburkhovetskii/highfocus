# ⚡️ High Focus Telegram Bot

Telegram-бот для High Focus с интерактивным квизом для определения типа фокуса пользователя.

## 🚀 Быстрый старт

### ⚠️ Важно: Для 24/7 работы нужен удаленный сервер!

Бот на локальном Mac останавливается когда ноутбук выключен.  
**Рекомендуется:** Деплой на облачный сервис (см. [DEPLOY.md](DEPLOY.md))

### Локальный запуск (для тестирования)

**1. Получите токен у @BotFather**
```bash
# В Telegram отправьте /newbot боту @BotFather
```

**2. Создайте .env файл**
```bash
echo "BOT_TOKEN=ваш_токен_здесь" > .env
```

**3. Установите зависимости**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Запустите бота**
```bash
python bot.py
```

---

## 🌐 Деплой на продакшн (24/7)

### Вариант 1: Railway.app (Проще всего 🌟)
```bash
npm install -g @railway/cli
railway login
railway init
railway variables set BOT_TOKEN=your_token
railway up
```

### Вариант 2: Docker на VPS
```bash
# На сервере
docker-compose up -d
```

### Вариант 3: Fly.io
```bash
fly launch
fly secrets set BOT_TOKEN=your_token
fly deploy
```

**Подробнее:** [DEPLOY.md](DEPLOY.md) - полная инструкция по всем вариантам!

## 📊 Структура проекта

```
highfocus/
├── bot.py              # Основная логика бота
├── database.py         # Работа с SQLite
├── keyboards.py        # Inline-клавиатуры
├── states.py           # FSM состояния
├── config.py           # Конфигурация
├── db_viewer.py        # Утилита статистики
├── requirements.txt    # Зависимости
├── .env                # Токен бота (создать вручную!)
│
├── config/             # Конфигурационные файлы
│   ├── *.plist         # Launch Daemon для macOS
│   ├── *.service       # Systemd для Linux
│   └── env_example.txt # Пример .env
│
├── scripts/            # Скрипты запуска
│   ├── install_daemon.sh    # Установка для macOS (работает всегда)
│   ├── run_background.sh    # Фоновый режим
│   └── stop_bot.sh          # Остановка
│
├── docs/              # Документация и экспорты
└── logs/              # Логи (если нужны)
```

## 🎯 Возможности

- ✅ Квиз из 8 вопросов
- ✅ Определение типа фокуса (Креативный/Аналитический/Энергетический)
- ✅ Персональные рекомендации по вкусу напитка
- ✅ Сохранение полных текстов ответов в БД
- ✅ Утилита просмотра статистики
- ✅ Экспорт данных в CSV
- ✅ Автономная работа (даже при закрытом ноутбуке)

## 🎛️ Управление

### Проверить статус
```bash
# Если установлен как daemon (рекомендуется)
sudo launchctl list | grep highfocus

# Если запущен через scripts
ps aux | grep bot.py
```

### Просмотр логов
```bash
tail -f bot.log
```

### Остановить/Перезапустить
```bash
# Daemon
sudo launchctl unload /Library/LaunchDaemons/com.highfocus.bot.daemon.plist
sudo launchctl load /Library/LaunchDaemons/com.highfocus.bot.daemon.plist

# Background
./scripts/stop_bot.sh
```

## 📊 Статистика

```bash
python db_viewer.py
```

Показывает:
- Количество пользователей
- Распределение по типам фокуса
- Детальные ответы последних пользователей
- Предпочтения по вкусам
- Экспорт в CSV

## 🎓 Типы фокуса

| Тип | Вкус | Характеристика |
|-----|------|----------------|
| 💡 Креативный | 🍐 Груша-Пармезан | Идеи и вдохновение |
| 🧠 Аналитический | 🍫 Брауни | Концентрация и порядок |
| ⚡️ Энергетический | 🍯 Солёная карамель | Быстрое действие |

## 🛠️ Технологии

- Python 3.8+
- aiogram 3.13.1 (Telegram Bot)
- aiosqlite 0.20.0 (База данных)
- python-dotenv 1.0.1

## ⚠️ Важно

### Для работы при закрытом ноутбуке (macOS):
Используйте `sudo ./scripts/install_daemon.sh` вместо обычного запуска.

Launch Daemon работает на уровне системы и не зависит от состояния ноутбука.

### Безопасность:
- Токен хранится в `.env` (не в Git!)
- База данных локальная
- Запуск от непривилегированного пользователя

## 🆘 Решение проблем

**Бот не запускается:**
1. Проверьте `.env`: `cat .env`
2. Проверьте venv: `ls venv/`
3. Проверьте логи: `tail -f bot.log`

**Бот останавливается при закрытии ноутбука:**
```bash
sudo ./scripts/install_daemon.sh
```

**Посмотреть все процессы:**
```bash
ps aux | grep bot.py
sudo launchctl list | grep highfocus
```

---

**Создано с ⚡️ для High Focus**

*Держим ум в тонусе!*
# highfocus
