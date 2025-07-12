# Rodan lite (WIP)

A lighter version of Rodan, for a simpler dev's life

Host machine pre-requisite:

- `docker`, (obviously)
- `nvidia-container-toolkit` for GPU Celery jobs

# Commands

- Build & then run Rodan:

```sh
docker compose build
docker compose up
```

- Build the project from starch (going to be a separate compose file):

```sh
docker compose -f docker-compose.yml build
```

- Run on production (goal)

```sh
docker compose pull
docker compose up -d
```

# Components

| READY | Service/Component       | Group/Node       | Uses codes in    | Notes                   |
| ----- | ----------------------- | ---------------- | ---------------- | ----------------------- |
| [x]   | `frontend-nginx`        | Frontend         |                  |                         |
| [x]   | `frontend-client`       | Frontend         | `scripts`        |                         |
| [ ]   | `backend-django`        | Backend          |                  | formerly `rodan-main`   |
| [x]   | `backend-iipsrv`        | Backend          |                  |                         |
| [x]   | `database-redis`        | Database         |                  |                         |
| [x]   | `database-postgres`     | Database         |                  |                         |
| [x]   | `taskqueue-rabbitmq`    | Task queue       |                  |                         |
| [ ]   | `celery-controller`     | Workers (Celery) | `backend/django` | Core jobs               |
| [ ]   | `celery-python-workers` | Workers (Celery) | `backend/django` | Workers for Python jobs |
| [ ]   | `celery-gpu-workers`    | Workers (Celery) | `backend/django` | Workers for GPU jobs    |

Note: for all `celery` jobs, the code are inside `backend/django` (previously `backend/rodan-main`) folder.
