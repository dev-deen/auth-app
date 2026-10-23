FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /auth_app

ENV PORT=8000

CMD exec uvicorn auth_app.main:app --host 0.0.0.0 --port $PORT
