1. delete images with docker desktop and pull with make pull
2. replace `./rodan-client/Dockerfile.old`  with this one:
```
FROM debian
EXPOSE 9002

# Install OS packages.
RUN apt-get -qq update \
  && apt-get -qq install -y \
    git \
    gnupg2 \
    libgif-dev \
    curl \
    build-essential
# Add node
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - \
  && apt-get install -yq \
    nodejs=12.22.*
# Add yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt -qq update \
  && apt -qq install -y \
    yarn

RUN rm -rf /var/lib/apt/lists/*

# Install node project.
COPY code/ /code/
RUN set -x \
  && cd /code \
  # && npm install
  && yarn install

# On some machines, the webpack dev server on the container won't accept connections from the host on localhost.
# Make the development server listen on 0.0.0.0 instead to accept connections from all addresses.
ENV RODAN_CLIENT_DEVELOP_HOST 0.0.0.0
WORKDIR /code/node_modules/.bin

COPY ./config/configuration.json /code/configuration.json

# Template start script, in case the startup gets longer.
COPY ./scripts/start /run/
RUN sed -i 's/\r//' /run/start
RUN chmod +x /run/start
```
3. in rodan’s directory, run `cd rodan-client && docker build -t ddmal/rodan-client:dev -f Dockerfile.old .`
4. replace `docker-compose.yml`  with this:
```
version: "3.4"
services:
  nginx:
    image: "ddmal/nginx:${DOCKER_TAG}"
    command: /run/start
    depends_on:
      - celery
      - postgres
      - rabbitmq
      - redis
      - rodan-main
    environment:
      TZ: America/Toronto
      SERVER_HOST: localhost
    ports:
      - "80:80"
      - "443:443"
      - "9002:9002"
    volumes:
      - "resources:/rodan/data"

  rodan-main:
    image: "ddmal/rodan-main:${DOCKER_TAG}"
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "/usr/bin/curl -H 'User-Agent: docker-healthcheck' http://localhost:8000/api/?format=json || exit 1"
        ]
      interval: "10s"
      timeout: "5s"
      retries: 2
      start_period: "2m"
    command: bash -c "tail -f /dev/null"
    environment:
      TZ: America/Toronto
      SERVER_HOST: localhost
      CELERY_JOB_QUEUE: None
    depends_on:
      - postgres
      - rabbitmq
      - redis
      - iipsrv
    env_file:
      - ./scripts/local.env
    volumes:
      - "resources:/rodan/data"
      - "./rodan-main/code:/code/Rodan"
    ports:
      - "8000:8000"

  rodan-client:
    image: "ddmal/rodan-client:${DOCKER_TAG}"
    volumes:
      - "./rodan-client/code:/code"
      - "./rodan-client/config/configuration.json:/client/configuration.json"

  iipsrv:
    image: "ddmal/iipsrv:${DOCKER_TAG}"
    volumes:
      - "resources:/rodan/data"

  celery:
    image: "ddmal/rodan-main:${DOCKER_TAG}"
    command: bash -c "tail -f /dev/null"
    environment:
      TZ: America/Toronto
      SERVER_HOST: localhost
      CELERY_JOB_QUEUE: celery
    healthcheck:
      test:
        [
          "CMD",
          "celery",
          "inspect",
          "ping",
          "-A",
          "rodan",
          "--workdir",
          "/code/Rodan",
          "-d",
          "celery@celery"
        ]
      interval: "30s"
      timeout: "3s"
      start_period: "1m"
      retries: 3
    depends_on:
      - postgres
      - rodan-main
      - rabbitmq
      - redis
    env_file:
      - ./scripts/local.env
    volumes:
      - "resources:/rodan/data"
      - "./rodan-main/code:/code/Rodan"

  py3-celery:
    image: "ddmal/rodan-python3-celery:${DOCKER_TAG}"
    command: bash -c "tail -f /dev/null"
    environment:
      TZ: America/Toronto
      SERVER_HOST: localhost
      CELERY_JOB_QUEUE: Python3
    depends_on:
      - postgres
      - rodan-main
      - rabbitmq
      - redis
      - celery
    env_file:
      - ./scripts/local.env
    volumes:
      - "resources:/rodan/data"
      - "./rodan-main/code:/code/Rodan"

  gpu-celery:
    image: "ddmal/rodan-gpu-celery:${DOCKER_TAG}"
    command: bash -c "tail -f /dev/null"
    environment:
      TZ: America/Toronto
      SERVER_HOST: localhost
      CELERY_JOB_QUEUE: GPU
    depends_on:
      - postgres
      - rodan-main
      - rabbitmq
      - redis
      - celery
    env_file:
      - ./scripts/local.env
    volumes:
      - "resources:/rodan/data"
      - "./rodan-main/code:/code/Rodan"

  redis:
    image: "redis:alpine"
    healthcheck:
      test: [ "CMD", "redis-cli", "ping" ]
      interval: 10s
      timeout: 5s
      retries: 5
    depends_on:
      - postgres

  postgres:
    image: "ddmal/postgres-plpython:${DOCKER_TAG}"
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready", "-U", "postgres" ]
      interval: 10s
      timeout: 5s
      retries: 5
    env_file:
      - ./scripts/local.env

  rabbitmq:
    image: "rabbitmq:alpine"
    healthcheck:
      test: [ "CMD", "rabbitmq-diagnostics", "-q", "ping" ]
      interval: "30s"
      timeout: "3s"
      retries: 3
    depends_on:
      - redis
    env_file:
      - ./scripts/local.env

  dev-rodan-client:
    image: "ddmal/rodan-client:dev"
    entrypoint: tail -f /dev/null
    ports:
      - "8080:9002"
    volumes:
      - "./rodan-client/code:/code"

volumes:
  resources:
```
5. start rodan with instructions (https://github.com/DDMAL/Rodan/wiki/Working-on-Rodan#starting-up-rodan)
6. 
```
cd rodan-client && cp local-dev/COPYconfiguration code/configuration.json
```
7. 
```
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh "-c" "cd /code && yarn install && cd /code/node_modules/.bin && yarn global add gulp"
```
8. 
```
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh "-c" "cd /code/node_modules/.bin && gulp"
```

See changes at `localhost:8080`.

To update UIs, make changes to `rodan-client` and redo step 8.