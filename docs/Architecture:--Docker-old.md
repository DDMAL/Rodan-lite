A [Docker container image](https://www.docker.com/what-container) is a lightweight, stand-alone, executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings. You can think of containers as similar to Virtual Machines, but containers are more lightweight and portable because they virtualize the operating system instead of hardware. Docker services and containers are just **namespaces** and **cgroups**; there is no hardware virtualization.

**Rodan's Docker setup is comprised of 9 services:**

- `nginx` - a reverse proxy server. It also serves the minified version of the web viewer when not working on the frontend.
- `rodan-main` - the Rodan server providing a REST API.
- `celery` - the Rodan asynchronous task runner. There are different celery services for each queue (Python3, GPU, and a master Celery that handles basic Rodan tasks like uploading resources and saving workflows)
- `postgres-plpython` - the PostgreSQL database used by the Rodan server, with the Python extensions installed and custom backup functions.
- `redis` - a key-value database used by the Rodan server to manage websocket connections. It is used to auto-refresh results on the web interface.
- `rabbitmq` - a message queue to track jobs for `celery`, a Python library used by Rodan for job management.
- [Optional] `rodan-client` - web viewer, for developing the Rodan-Client front end

`nginx`, `rodan`, `rodan-client` and `postgres-plpython` each have a `Dockerfile` in this repository. Dockerfiles are basically lists of commands that define how to set up a Docker image (which can then be launched as a Docker container). For `redis` and `rabbitmq` we use existing public images from Docker Hub maintained by the organizations that maintain those software projects. The `docker-compose.yml` file specifies the dependencies between the container images - which ones need to be running so that other ones run properly - and combines them to define a complete Rodan installation.
