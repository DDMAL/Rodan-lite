# Rodan lite (WIP)

A lighter version of Rodan, for a simpler dev's life

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

| Service/Component    | Category         | Uses         | Notes                 |
| -------------------- | ---------------- | ------------ | --------------------- |
| `frontend-nginx`     | Frontend         |              |                       |
| `frontend-client`    | Frontend         | `scripts`    |                       |
| `backend-django`     | Backend          |              | formerly `rodan-main` |
| `backend-iipsrv`     | Backend          |              |                       |
| `database-redis`     | Database         |              |                       |
| `database-postgres`  | Database         |              |                       |
| `taskqueue-rabbitmq` | Task queue       |              |                       |
| `worker-py3-celery`  | Workers (Celery) | `rodan-main` |                       |
| `worker-gpu-celery`  | Workers (Celery) | `rodan-main` |                       |
| `celery` (?)         | Workers (Celery) | `rodan-main` | unsure what this is   |

Note: for all `celery` jobs, the code are inside `rodan-main` folder.
