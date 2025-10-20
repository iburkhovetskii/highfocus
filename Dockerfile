FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py database.py keyboards.py states.py config.py db_viewer.py ./

# Создаём директорию для БД (будет смонтирован Volume)
RUN mkdir -p /data && chmod 777 /data

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]

