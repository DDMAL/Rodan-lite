# Rodan WebSocket API
> Courtesy of ChatGPT


## What Are WebSockets?

WebSockets enable **bi-directional, real-time communication** between a browser and server. Unlike traditional polling, WebSockets allow the **server to push updates** to the client as they happen.

---

## 🔧 How It Works

### Dependencies & Installation

#### 1. Redis
A fast, in-memory key-value store used as a message broker with Django.

- Install:
  ```bash
  sudo apt-get install redis-server
  ```

- Start Redis:
  ```bash
  src/redis-server
  ```

- Test connection:
  ```bash
  redis-cli
  127.0.0.1:6379> PING
  127.0.0.1:6379> PONG
  ```

#### 2. ws4redis
WebSocket support for Redis-backed Django apps.

- Install:
  ```bash
  pip install django-websocket-redis
  ```

- Add heartbeat in `settings.py`:
  ```python
  WS4REDIS_HEARTBEAT = '--heartbeat--'
  ```

#### 3. psycopg2
PostgreSQL adapter for Python.

- Install:
  ```bash
  pip install psycopg2
  ```

#### 4. WebSocket Settings (`settings.py`)
```python
WEBSOCKET_URL = '/ws/'
WSGI_APPLICATION = 'ws4redis.django_runserver.application'
WS4REDIS_EXPIRE = 3600
WS4REDIS_HEARTBEAT = '--heartbeat--'
WS4REDIS_PREFIX = 'rodan'
WS4REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
```

#### 5. Run Migrations
Run as the Postgres superuser to set up WebSocket-related database triggers:

```bash
(rodan-env)$ python manage.py migrate
```

---

## 🖥️ Server-Side Operations

### 1. Post-Update Triggers (PostgreSQL)
Triggers are added to Rodan model tables to push update notifications. They are auto-generated on migration.  
See: [`rodan/models/__init__.py`](https://github.com/DDMAL/Rodan/blob/develop/rodan/models/__init__.py)

### 2. Redis Message Broadcasts
Broadcast messages when updates occur:

```python
r = redis.StrictRedis(REDIS_HOST, REDIS_PORT, DB)
r.publish('rodan:broadcast:rodan', 'message_string')
```

`REDIS_HOST`, `REDIS_PORT`, and `DB` are defined in `settings_production.py`.

### 3. Post-Migrate Signal
Triggers are reset after running:

```bash
(rodan-env)$ python manage.py migrate
```

---

## 🚀 Stress Testing

### Dependencies

Install [Thor](https://www.npmjs.com/package/thor) using Node.js:

```bash
npm install -g thor
```

### Running Tests

Run the stress test script:

```bash
~/Rodan/rodan/test/test_load.sh -a[connections] -n[messages] -s[server]
```

Example (displays help menu):

```bash
~/Rodan/rodan/test/test_load.sh -h
```

#### Script Options

| Option | Description |
|--------|-------------|
| `-a`   | Number of connections (default: 10,000) |
| `-n`   | Number of messages per connection |
| `-s`   | Server address (default: `localhost`) |
| `-h`   | Show help instructions |

**Logs saved to:** `~/Rodan/rodan/test/test_log`

---
