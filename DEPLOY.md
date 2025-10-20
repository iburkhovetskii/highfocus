# 🚀 Деплой High Focus Bot

## 🎯 Варианты деплоя

### ❌ Локальный Mac (НЕ рекомендуется)
**Проблема:** Бот останавливается когда ноутбук выключен/спит.

### ✅ Рекомендуемые варианты:

---

## 1. 🐳 Docker на VPS (Лучший вариант)

### Преимущества:
- ✅ Работает 24/7
- ✅ Изолированное окружение
- ✅ Легко обновлять
- ✅ Автоматический перезапуск

### Шаг 1: Выберите VPS

**Бесплатные/Дешевые опции:**
- **Oracle Cloud** - бесплатно навсегда (Free Tier)
- **Google Cloud** - $300 кредитов на 3 месяца
- **AWS** - 1 год бесплатно (EC2 t2.micro)
- **DigitalOcean** - $200 кредитов на 60 дней
- **Hetzner** - от €4.15/мес (дешево)
- **Contabo** - от €4/мес

### Шаг 2: Установите Docker на сервере

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose

# Проверка
docker --version
docker-compose --version
```

### Шаг 3: Загрузите проект на сервер

```bash
# На вашем Mac
cd /Users/iliaburkhovetskii/highfocus
tar -czf highfocus.tar.gz bot.py database.py keyboards.py states.py config.py \
    db_viewer.py requirements.txt Dockerfile docker-compose.yml .env

# Загрузите на сервер
scp highfocus.tar.gz user@your-server-ip:/home/user/

# На сервере
ssh user@your-server-ip
tar -xzf highfocus.tar.gz
cd highfocus
```

### Шаг 4: Запустите через Docker

```bash
# Запуск
docker-compose up -d

# Проверка логов
docker-compose logs -f

# Статус
docker-compose ps

# Остановка
docker-compose down

# Перезапуск
docker-compose restart
```

---

## 2. ☁️ Бесплатные облачные платформы

### A. Railway.app (Рекомендуется 🌟)

**Преимущества:**
- Бесплатный тариф ($5 кредитов/месяц)
- Автодеплой из GitHub
- Простой интерфейс

**Установка:**
```bash
# 1. Установите Railway CLI
npm install -g @railway/cli

# или
brew install railway

# 2. Логин
railway login

# 3. Инициализация
cd /Users/iliaburkhovetskii/highfocus
railway init

# 4. Добавьте переменные окружения
railway variables set BOT_TOKEN=your_token_here

# 5. Деплой
railway up
```

### B. Fly.io

**Преимущества:**
- Бесплатно (3 маленьких VM)
- Работает 24/7
- Легко масштабировать

**Установка:**
```bash
# 1. Установите Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Логин
fly auth login

# 3. Создайте приложение
cd /Users/iliaburkhovetskii/highfocus
fly launch

# 4. Установите токен
fly secrets set BOT_TOKEN=your_token_here

# 5. Деплой
fly deploy
```

### C. Render.com

**Преимущества:**
- Бесплатный тариф
- Автодеплой из GitHub
- База данных в подарок

**Установка:**
1. Загрузите код на GitHub
2. Зайдите на render.com
3. New → Background Worker
4. Подключите GitHub репозиторий
5. Добавьте переменную окружения `BOT_TOKEN`
6. Deploy!

---

## 3. 🖥️ Классический VPS с systemd

### Oracle Cloud (Бесплатно навсегда)

1. Создайте аккаунт на oracle.com/cloud/free
2. Создайте VM (Ubuntu)
3. Подключитесь по SSH
4. Установите Python и зависимости
5. Скопируйте код бота
6. Создайте systemd service

```bash
# На сервере
sudo nano /etc/systemd/system/highfocus.service
```

```ini
[Unit]
Description=High Focus Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/highfocus
Environment="PATH=/home/ubuntu/highfocus/venv/bin"
ExecStart=/home/ubuntu/highfocus/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable highfocus
sudo systemctl start highfocus
sudo systemctl status highfocus
```

---

## 📊 Сравнение вариантов

| Вариант | Стоимость | Сложность | Uptime | Рекомендация |
|---------|-----------|-----------|--------|--------------|
| **Railway.app** | Бесплатно* | ⭐ Легко | 99.9% | 🌟 Лучше для начала |
| **Fly.io** | Бесплатно | ⭐⭐ Средне | 99.9% | 🌟 Отлично |
| **Docker на VPS** | $4-20/мес | ⭐⭐⭐ Средне | 99.9% | 🌟 Лучше для продакшена |
| **Oracle Cloud** | Бесплатно | ⭐⭐⭐ Сложно | 99.95% | ✅ Если нужна мощность |
| **Render.com** | Бесплатно* | ⭐ Легко | 99% | ✅ Простой вариант |

*Ограничения на бесплатном тарифе

---

## 🎯 Моя рекомендация для вас:

### Вариант 1: Railway.app (Проще всего)
```bash
npm install -g @railway/cli
cd /Users/iliaburkhovetskii/highfocus
railway login
railway init
railway variables set BOT_TOKEN=your_token
railway up
```
**Готово за 5 минут!**

### Вариант 2: Docker на Hetzner (Дешево и надежно)
- €4.15/мес за VPS
- Полный контроль
- Отличная производительность

---

## 📝 Что сделать сейчас:

1. **Выберите платформу** (рекомендую Railway или Fly.io)
2. **Создайте аккаунт**
3. **Следуйте инструкциям выше**
4. **Бот будет работать 24/7!**

---

## 🆘 Нужна помощь?

Напишите какую платформу выбрали, и я помогу с настройкой!

---

**P.S.** Docker-файлы уже созданы и готовы к использованию! 🐳

