# Python3 Celery

## Jobs

This Docker image contains the following jobs:

| Job             | Link/Info                                  |
| --------------- | ------------------------------------------ |
| `pixel_wrapper` | https://github.com/DDMAL/pixel_wrapper.git |
| `neon_wrapper`  | https://github.com/DDMAL/neon_wrapper      |
| `gamera`        | Pre-built Docker Image ddmal/gamera4:2.0.0 |

# Working directory

The container uses `celery` to spin up multiple **workers** that process **jobs**. Each **job** is executed when a **worker** becomes available and a task is present in the RabbitMQ broker queue.
