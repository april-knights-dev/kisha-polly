FROM python:3.9
ENV PYTHONUNBUFFERED True

COPY ./app/ /app/
COPY requirements.txt app/
WORKDIR /app

RUN pip install -r requirements.txt
CMD exec gunicorn --bind :8080 --workers 1 --threads 1 --timeout 0 app:flask_app