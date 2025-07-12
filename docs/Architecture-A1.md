# Rodan Architectural Design

To help with understand of the architecture, please make sure you are clear of the following terminologies:

- Docker, Dockerfile
- Docker compose

## Layers and Components

### Layer 1: Frontend

- [Optional] `rodan-client` - web viewer, for developing the Rodan-Client front end

### Layer 2: Backend

- `celery` - the Rodan asynchronous task runner. There are different celery services for each queue (Python3, GPU, and a master Celery that handles basic Rodan tasks like uploading resources and saving workflows)

### Layer 3: Task Queue & Database

- `postgres-plpython` - the PostgreSQL database used by the Rodan server, with the Python extensions installed and custom backup functions.
- `redis` - a key-value database used by the Rodan server to manage websocket connections. It is used to auto-refresh results on the web interface.
- `rabbitmq` - a message queue to track jobs for `celery`, a Python library used by Rodan for job management.

### Layer 4: Workers

- `nginx` - a reverse proxy server. It also serves the minified version of the web viewer when not working on the frontend.
- `rodan-main` - the Rodan server providing a REST API.

[[images/installation_1.png]]

## Starting Rodan: `docker compose` orchestration

In order:

- [[Quick setup: automated script]]
- Manual setup
  - [[Rodan task queue]]
  - [[Rodan database]]
  - [[Rodan resource file server]]
  - [[Rodan worker]]
    - [[Requirements for image processing jobs]]
  - [[Rodan web server]]
    - [[Diva.js image viewer support]]
- [[Start Rodan]]

Note: to make sure that the services have the latest configuration, you may want to restart them if they have already been running (`service xxxx restart`).

#### Rodan task queue

Make sure that `rabbitmq-server` is running with `rabbitmqctl status`. If not, run:

```
$> service rabbitmq-server start
```

Open the port for RabbitMQ (typically 5672).

#### Rodan database

Make sure that PostgreSQL and Redis are running. If not, run:

```
$> service postgresql start
$> service redis-server start
```

Open the port for PostgreSQL (typically 5432) and Redis (typically 6379).

#### Rodan resource file server

Make sure that the following NFS-related services are running:

```
$> service rpcbind start
$> service nfs-kernel-server start
```

Open the ports for NFS-related services (typically 111/udp and 2049/tcp).

#### Rodan workers

**1**. Mount NFS folder:

```
$> service rpcbind start
$> mount -t nfs -o proto=tcp,port=2049 $RESOURCE_FILE_SERVER_IP:/ $RESOURCE_FOLDER_MOUNT_POINT
```

Try if the mounted folder works fine.

**2**. Start supervisor:

```
$> service supervisor start
```

Check `supervisorctl` for Rodan status.

Then, Rodan worker should be available.

#### Rodan server

Start nginx:

```
$> service nginx start
```

Then follow the steps for "Rodan workers". After that, open port 80.
