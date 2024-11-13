FROM python:3.12-slim

ENV DATABASE_PATH=/data/db.sqlite3
ENV PYTHONUNBUFFERED=1
ENV DOCKER=True

WORKDIR /app

RUN pip install --no-cache-dir setuptools

COPY Backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /data && chmod 777 /data

COPY Backend/ .

VOLUME ["/data"]

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]