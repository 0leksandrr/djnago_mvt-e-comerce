FROM python:3.12.1-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

ADD pyproject.toml /backend/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . /backend/
