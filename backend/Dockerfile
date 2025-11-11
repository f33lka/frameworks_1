# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Системные зависимости (минимально необходимые для сборки зависимостей)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

# Копируем код приложения
COPY . /app

# Обеспечиваем каталог для SQLite и помечаем как том
RUN mkdir -p /app/instance
VOLUME ["/app/instance"]

# Значения по умолчанию (можно переопределить переменными окружения)
ENV FLASK_ENV=production \
    DATABASE_URL=sqlite:///instance/app.db

EXPOSE 5000

# Healthcheck через стандартную библиотеку Python
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=5 \
  CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:5000/api/health').getcode()==200 else sys.exit(1)" || exit 1

# Запуск через gunicorn c фабрикой приложения create_app() в app.py
CMD ["gunicorn","-b","0.0.0.0:5000","-w","2","app:create_app()"]
