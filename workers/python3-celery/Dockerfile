# --------- BUILDER IMAGE for Pixel and Neon ---------
FROM alpine:3.16 AS builder
RUN apk update
RUN apk add \
  bash \
  git \
  npm \
  python3 \
  yarn

# Build Pixel
FROM builder AS pixel-builder
RUN git clone --recurse-submodules -b v2.0.2 https://github.com/DDMAL/pixel_wrapper
WORKDIR /pixel_wrapper/
RUN python3 activate_wrapper.py
RUN npm install
RUN ./node_modules/.bin/gulp develop:rodan

# Build Neon, this might take a while
FROM builder AS neon-builder
RUN git clone --recurse-submodules -b develop https://github.com/DDMAL/neon_wrapper
WORKDIR /neon_wrapper
RUN yarn install
RUN yarn build

# --------- Get GAMERA files ---------
FROM ddmal/gamera4:2.0.0 AS gamera

# =========== MAIN / FINAL IMAGE ===========
# This release is based on Debian 11 "Bullseye"
FROM python:3.7-slim AS final-image

# Copy various scripts and make them executable.
COPY ../../scripts/start-celery /run/
COPY ../../scripts/wait-for-app /run/
RUN chmod +x /run/start-celery
RUN chmod +x /run/wait-for-app

# Copy external dependencies into main container.
# rodan-main is not pulled from builder-pixel-neon (to ease local development)
COPY ../../backend/rodan-main /code/Rodan
COPY --from=pixel-builder /pixel_wrapper /code/Rodan/rodan/jobs/pixel_wrapper
COPY --from=neon-builder /neon_wrapper /code/Rodan/rodan/jobs/neon_wrapper
# Gamera and Musicstaves will be installed later in this script.
COPY --from=gamera /gamera4-rodan /gamera4-rodan

# Install dependencies.
RUN apt-get update
RUN apt-get install -y \
  bash \
  curl \
  g++ \
  git \
  # python-magic dependency
  libmagic1 \
  # Psycopg2 dependency
  libpq-dev \
  # OpenCV dependencies
  libsm6 libxext6 libxrender-dev libglib2.0-data \
  python3-opencv \
  wget \
  vim

# https://stackoverflow.com/questions/69100275/error-while-downloading-the-requirements-using-pip-install-setup-command-use-2
RUN pip3 install setuptools==58
RUN pip3 install -r /code/Rodan/requirements.txt

# Install Gamera. Note: `--nowx` is a valid option for `gamera`
# https://github.com/DDMAL/Gamera/blob/e0bd310eb649645d941092a32b42acab8138675a/setup.py#L75-L77
WORKDIR /gamera4-rodan/gamera-4
RUN python3 setup.py --nowx install

# Install Musicstaves
WORKDIR /gamera4-rodan/musicstaves
RUN python3 setup.py install

# Temporary fix for OpenCV until https://github.com/DDMAL/Rodan/issues/639 is resolved.
RUN pip install opencv-python==4.6.0.66

# Change the concurency for python3 jobs
RUN sed -i "s/concurrency=10/concurrency=3/g" /run/start-celery

ENTRYPOINT ["/run/start-celery"]
