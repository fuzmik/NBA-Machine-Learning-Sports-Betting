# syntax=docker/dockerfile:1

FROM arm64v8/ubuntu:22.04
#FROM debian:stretch-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

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
    apt install python3-pip build-essential python3-dev python3 python3-h5py libhdf5-dev -y

COPY . /app
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && \
    pip install -U pip && \
    rm -rf /root/.cache

USER appuser

COPY Flask /app/Flask

EXPOSE 5000

WORKDIR /app/Flask
CMD ["gunicorn", "-w", "2", "app:app", "--bind=0.0.0.0:5000"]
