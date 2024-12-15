# syntax=docker/dockerfile:1

#Testing this image
#FROM arm64v8/python:3.11.6-alpine3.17 as base
#FROM debian:stretch-slim
#line after this works
FROM python:3.11.6-slim-bookworm as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
VOLUME ["/app"]

ARG UID=1000
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apt update && \
    apt install pkg-config libhdf5-dev build-essential -y

COPY requirements.txt /tmp/
RUN pip --no-cache-dir install -r /tmp/requirements.txt && \
    pip install -U pip && \
    pip uninstall -y flask gunicorn && \
    pip install -U flask gunicorn && \
    rm -rf /root/.cache

USER appuser

EXPOSE 8800

WORKDIR /app/Flask
CMD ["gunicorn", "-w", "2", "app:app", "--bind=0.0.0.0:8800"]
