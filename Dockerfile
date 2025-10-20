# High Focus Bot Dockerfile
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY bot.py database.py keyboards.py states.py config.py db_viewer.py ./

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем бота
CMD ["python", "bot.py"]

