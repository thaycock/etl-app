# syntax=docker/dockerfile:experimental
FROM python:3.12-slim

ENV LOGGING_PATH /tmp/logs/
ENV FLASK_APP=apihealth.src.health.api:app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV RUNTIME_ENVIRONMENT=DEV

RUN apt-get update \
    && apt-get -y install \
        gcc \
        python3-dev \
        libpcre3 \
        libpcre3-dev \
        libpq-dev \
        libgtk-3-dev \
        tox \
        postgresql-server-dev-all \
    && pip install -U --no-cache-dir pip poetry \
    && pip install lockfile \
    && pip install Flask \
    && pip install python-dotenv

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

RUN chmod +x /app/scripts/run-dev.sh

RUN mkdir -p /tmp/logs/ && \
    touch /tmp/logs/{info.log,errors.log,debug.log,critical.log,warn.log}

EXPOSE 5000
