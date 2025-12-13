FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py database_postgres.py keyboards.py states.py config.py db_viewer.py consent_text.py "Политика_обработки_персональных_данных.docx" ./

# Промокоды
COPY promo_codes.csv ./

# Картинки (типы фокуса и вкусы)
COPY Frame*.png ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
