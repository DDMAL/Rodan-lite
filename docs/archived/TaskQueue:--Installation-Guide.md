# RabbitMQ Task Queue Installation Guide

## 1. Install RabbitMQ

- Download from [RabbitMQ website](https://www.rabbitmq.com/download.html)
- On macOS:
  ```bash
  brew install rabbitmq
  ```

* Start server:

  ```bash
  sudo rabbitmq-server
  ```

* **macOS only:** If it fails, update your PATH:

  ```bash
  echo 'export PATH=$PATH:/usr/local/sbin' >> ~/.bash_profile
  source ~/.bash_profile
  ```

---

## 2. Create User & Virtual Host

Set variables: `$USERNAME`, `$PASSWORD`, `$VHOST`

```bash
sudo rabbitmqctl add_user $USERNAME $PASSWORD
sudo rabbitmqctl add_vhost $VHOST
sudo rabbitmqctl set_permissions -p $VHOST $USERNAME ".*" ".*" ".*"
```

- **macOS:** If `.erlang.cookie` error occurs:

  ```bash
  sudo chown _yourusername ~/.erlang.cookie
  ```

---

## 3. Start RabbitMQ App

```bash
sudo rabbitmqctl start_app
```

---

## 4. Test AMQP Connection

Replace credentials in the script below:

```python
from kombu import Connection
url = 'amqp://root:root@localhost:5672/rodan'

with Connection(url) as c:
    try:
        c.connect()
        print("Eurika! It works!")
    except Exception as e:
        raise ValueError("Connection failed:", e)
```

---

## 🔑 Defaults

| Variable | Value       |
| -------- | ----------- |
| `$HOST`  | `localhost` |
| `$PORT`  | `5672`      |

```

Would you like me to save this into a `.md` file for download?
```

```

```
