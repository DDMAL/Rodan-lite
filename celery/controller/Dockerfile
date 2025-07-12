FROM python:3.7.16-slim-buster

RUN apt-get update && \
    apt-get install -y build-essential git libpq-dev

WORKDIR /
RUN git clone https://github.com/DDMAL/Rodan-lite

WORKDIR /Rodan-lite/backend/django
RUN pip install -r requirements.txt
