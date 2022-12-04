FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y curl vim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install -U pip && pip install poetry

RUN poetry install --no-root