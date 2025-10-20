FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py database.py keyboards.py states.py config.py db_viewer.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]

