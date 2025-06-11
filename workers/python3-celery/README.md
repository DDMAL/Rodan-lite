# Python3 Celery

## Jobs

This Docker image contains the following jobs:

| Job             | Link/Info                                  |
| --------------- | ------------------------------------------ |
| `pixel_wrapper` | https://github.com/DDMAL/pixel_wrapper.git |
| `neon_wrapper`  | https://github.com/DDMAL/neon_wrapper      |
| `gamera`        | Pre-built Docker Image ddmal/gamera4:2.0.0 |

The container uses `celery` to spin up multiple **workers** that process **jobs**. Each **job** is executed when a **worker** becomes available and a task is present in the RabbitMQ broker queue.

## Dockerfile Build Steps 🐳

> Courtesy of ChatGPT

| Step | Stage       | Description                                                                                                           |
| ---- | ----------- | --------------------------------------------------------------------------------------------------------------------- |
| 1    | Builder     | Create a `builder` image based on Alpine and install: `bash`, `git`, `npm`, `python3`, `yarn`.                        |
| 2    | Pixel Build | Clone `pixel_wrapper` (tag `v2.0.2`) with submodules. Run activation script, install dependencies, build with `Gulp`. |
| 3    | Neon Build  | Clone `neon_wrapper` (`develop` branch) with submodules. Install dependencies and build using Yarn.                   |
| 4    | Get Gamera  | Use `ddmal/gamera4:2.0.0` image to get Gamera-related files.                                                          |
| 5    | Final Image | Base image: `python:3.7-slim` (Debian 11 "Bullseye").                                                                 |
| 6    | -           | Copy `start-celery` and `wait-for-app` scripts to `/run/` and make them executable.                                   |
| 7    | -           | Copy Rodan backend, Pixel/Neon wrappers, and Gamera files into the image.                                             |
| 8    | -           | Install system dependencies (tools, Python, DB, and OpenCV libraries).                                                |
| 9    | -           | Install Python dependencies using `pip`, with fixed `setuptools==58`.                                                 |
| 10   | -           | Build and install Gamera and Musicstaves from source (`setup.py`).                                                    |
| 11   | -           | Install OpenCV workaround version: `opencv-python==4.6.0.66`.                                                         |
| 12   | -           | Adjust Celery concurrency setting in startup script.                                                                  |
| 13   | -           | Set container entrypoint to `/run/start-celery`.                                                                      |

Note: Pixel Build and Neon Build stages are run simultaneously by `docker compose`

# Working directory

```
/
├── run/
│   ├── start-celery
│   └── wait-for-app
├── code/
│   └── Rodan/
│       ├── rodan/
│       │   ├── jobs/
│       │   │   ├── pixel_wrapper/       # From pixel-builder
│       │   │   └── neon_wrapper/        # From neon-builder
│       │   └── ... (other Rodan files)
│       └── ... (other Django project files)
├── gamera4-rodan/
│   ├── gamera-4/
│   │   └── ... (Gamera source files)
│   └── musicstaves/
│       └── ... (Musicstaves source files)
└── ...
```
