# Unused grok-builder stage kept for reference — not consumed by main-django.
FROM ubuntu:latest AS grok-builder
RUN apt-get update && \
  apt-get install -y \
  make cmake git \
  libopenjp2-7 \
  libopenjp2-7-dev \
  libopenjp2-tools
WORKDIR /
RUN git clone https://github.com/GrokImageCompression/grok
WORKDIR /grok
RUN git checkout 4932d86b19d9008a28ae898035cfa43340e636e6 && mkdir build
WORKDIR /grok/build
RUN cmake -DBUILD_THIRDPARTY=ON .. && make -j3

FROM python:3.7.16-slim-buster AS main-django

# Copy run scripts
COPY scripts/start /run/
COPY scripts/start-celery /run/
COPY scripts/wait-for-app /run/
RUN chmod +x /run/start /run/start-celery /run/wait-for-app

# Buster is EOL — redirect apt to the archive mirror
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
    && sed -i '/buster-updates/d' /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends \
       git libpq-dev build-essential libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Build the directory layout that start/start-celery expect:
#   /code/Rodan/manage.py
#   /code/Rodan/rodan/   ← the Django app, importable as 'rodan'
RUN mkdir -p /code/Rodan
COPY backend/django/manage.py /code/Rodan/manage.py
COPY backend/django/requirements.txt /code/Rodan/requirements.txt
COPY backend/django/code /code/Rodan/rodan/

WORKDIR /code/Rodan
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["/run/start"]
