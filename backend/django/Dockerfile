# FROM ddmal/rodan-python3-celery:nightly
FROM ubuntu:latest AS grok-builder
RUN apt-get update && \
  apt-get install -y \
  make cmake git \
  # OpenJPEG dependencies
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
WORKDIR /
COPY ../../scripts/start /run/
RUN chmod +x /run/start \
&& chown www-data /run/start

COPY . /rodan-django/
WORKDIR /rodan-django

RUN pip install --upgrade pip && pip install -r requirements.txt


# This script gets the gpu jobs into celery
# COPY ../../scripts/install_gpu_rodan_jobs /opt/install_gpu_rodan_jobs
# RUN set -e \
  # && chmod +x /opt/install_gpu_rodan_jobs \
  # && chown www-data /opt/install_gpu_rodan_jobs \
  # This script starts Rodan
# RUN /opt/install_gpu_rodan_jobs


# Substitute the build hash for our actual build hash
# RUN sed -i "s/__build_hash__ = \"local\"/__build_hash__ = \"${BUILD_HASH}\"/" /code/Rodan/rodan/__init__.py

# Change the concurrency
# RUN sed -i "s/concurrency=10/concurrency=6/g" /run/start-celery
# RUN sed -i "s/max-tasks-per-child=1/max-tasks-per-child=5/g" /run/start-celery