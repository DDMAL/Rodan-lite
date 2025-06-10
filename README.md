# Rodan lite (WIP)

A lighter version of Rodan, for a simpler dev's life

# Commands

- Building the project:

```sh
docker compose build
```

- Run Rodan:

```sh
docker compose up
```

# Components

| Category         | Component                   | Notes |
| ---------------- | --------------------------- | ----- |
| Frontend         | `nginx`                     |       |
| Frontend         | `rodan-client`              |       |
| Backend          | `rodan-main`/`rodan-django` |       |
| Backend          | `iipsrv`                    |       |
| Database         | `redis`                     |       |
| Database         | `postgres`                  |       |
| Task queue       | `rabbitmq`                  |       |
| Workers (Celery) | `python3-celery`            |       |
| Workers (Celery) | `gpu-celery`                |       |
| Workers (Celery) | `celery`                    |       |

Note: for all `celery` jobs, the code are inside `rodan-main`/`rodan-django` folder.
