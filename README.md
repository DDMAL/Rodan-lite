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

- Build the project from starch (going to be a separate compose file):
```sh
docker compose -f docker-compose.yml build
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
