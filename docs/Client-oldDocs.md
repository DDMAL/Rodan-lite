# 🛠️ Rodan Development Setup (Linux)

This guide walks you through setting up the Rodan development environment using Docker on a Linux machine.

---

## ✅ Prerequisites

- Docker & Docker Compose installed.
- Rodan project cloned locally.

---

## 1. 🧹 Clean Docker Images

Delete existing images and pull the latest ones:

```sh
docker image prune -a
make pull
```

---

## 2. 📝 Replace `rodan-client/Dockerfile.old`

Replace the contents of `./rodan-client/Dockerfile.old` with:

```Dockerfile
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
  && apt -qq install -y yarn

RUN rm -rf /var/lib/apt/lists/*

# Install node project
COPY code/ /code/
RUN set -x \
  && cd /code \
  && yarn install

# Make development server accessible
ENV RODAN_CLIENT_DEVELOP_HOST 0.0.0.0
WORKDIR /code/node_modules/.bin

COPY ./config/configuration.json /code/configuration.json

# Template start script
COPY ./scripts/start /run/
RUN sed -i 's/\r//' /run/start
RUN chmod +x /run/start
```

---

## 3. 🛠️ Build `rodan-client` Docker Image

Run:

```sh
cd rodan-client
docker build -t ddmal/rodan-client:dev -f Dockerfile.old .
```

---

## 4. 🔄 Replace `docker-compose.yml`

Replace the root `docker-compose.yml` with [this full content](#), or use the file provided in the repo.

---

## 5. 🚀 Start Rodan

Follow the official startup instructions:
👉 [Rodan Startup Guide](https://github.com/DDMAL/Rodan/wiki/Working-on-Rodan#starting-up-rodan)

---

## 6. 🧾 Copy Configuration

Run:

```sh
cd rodan-client
cp local-dev/COPYconfiguration code/configuration.json
```

---

## 7. 📦 Install Client Dependencies Inside Container

Run:

```sh
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh -c "cd /code && yarn install && cd /code/node_modules/.bin && yarn global add gulp"
```

---

## 8. 🧪 Build the Frontend

Run:

```sh
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh -c "cd /code/node_modules/.bin && gulp"
```

---

## 🖥️ View Rodan Client

Visit:

```
http://localhost:8080
```

---

## 🔁 Update the UI

Make changes in `rodan-client` source, then re-run:

```sh
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh -c "cd /code/node_modules/.bin && gulp"
```

---

# 🛠️ Rodan Development Setup (Linux)

This guide walks you through setting up the Rodan development environment using Docker on a Linux machine.

---

## ✅ Prerequisites

- Docker & Docker Compose installed.
- Rodan project cloned locally.

---

## 1. 🧹 Clean Docker Images

Delete existing images and pull the latest ones:

```sh
docker image prune -a
make pull
```

---

## 2. 📝 Replace `rodan-client/Dockerfile.old`

Replace the contents of `./rodan-client/Dockerfile.old` with:

```Dockerfile
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
  && apt -qq install -y yarn

RUN rm -rf /var/lib/apt/lists/*

# Install node project
COPY code/ /code/
RUN set -x \
  && cd /code \
  && yarn install

# Make development server accessible
ENV RODAN_CLIENT_DEVELOP_HOST 0.0.0.0
WORKDIR /code/node_modules/.bin

COPY ./config/configuration.json /code/configuration.json

# Template start script
COPY ./scripts/start /run/
RUN sed -i 's/\r//' /run/start
RUN chmod +x /run/start
```

---

## 3. 🛠️ Build `rodan-client` Docker Image

Run:

```sh
cd rodan-client
docker build -t ddmal/rodan-client:dev -f Dockerfile.old .
```

---

## 4. 🔄 Replace `docker-compose.yml`

Replace the root `docker-compose.yml` with [this full content](#), or use the file provided in the repo.

---

## 5. 🚀 Start Rodan

Follow the official startup instructions:
👉 [Rodan Startup Guide](https://github.com/DDMAL/Rodan/wiki/Working-on-Rodan#starting-up-rodan)

---

## 6. 🧾 Copy Configuration

Run:

```sh
cd rodan-client
cp local-dev/COPYconfiguration code/configuration.json
```

---

## 7. 📦 Install Client Dependencies Inside Container

Run:

```sh
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh -c "cd /code && yarn install && cd /code/node_modules/.bin && yarn global add gulp"
```

---

## 8. 🧪 Build the Frontend

Run:

```sh
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh -c "cd /code/node_modules/.bin && gulp"
```

---

## 🖥️ View Rodan Client

Visit:

```
http://localhost:8080
```

---

## 🔁 Update the UI

Make changes in `rodan-client` source, then re-run:

```sh
DOCKER_TAG=nightly docker compose exec dev-rodan-client sh -c "cd /code/node_modules/.bin && gulp"
```

---
