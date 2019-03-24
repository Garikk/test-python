# build container
FROM python:3.7-alpine as build
WORKDIR /pip-packages
RUN apk update && pip install --upgrade pip && apk add postgresql-libs \
    && apk add libffi-dev && apk add postgresql-libs \
    && apk add --virtual .build-deps gcc musl-dev postgresql-dev redis

# run container
FROM python:3.7-alpine

WORKDIR /app

RUN apk update && pip install --upgrade pip && apk add postgresql-libs \
    && apk add libffi-dev && apk add postgresql-libs \
    && apk add --virtual .build-deps gcc musl-dev postgresql-dev redis \
    && pip install gunicorn

ENV FLASK_ENV=production

ENV GUNICORN_PORT=5000
ENV GUNICORN_MODULE=app
ENV GUNICORN_CALLABLE=app

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
