**Rodan is a web-based workflow engine**, developed under [the Single Interface for Music Score Searching and Analysis (SIMSSA) project](https://simssa.ca/). It natively provides a suite of software modules for optical music recognition (OMR) and supports custom modules for other tasks.

Rodan is powered by [Python](https://www.python.org/), using [Django](https://www.djangoproject.com/) as its web server, [Celery](http://www.celeryproject.org/) as its distributed task queue, and other supporting software packages. It features:

* Pluggable job packages
* Human-assisted workflow processing
* Distributed workflow processing
* Multi-user design
* RESTful API
* WebSocket messaging
* [Diva.js viewer](https://ddmal.github.io/diva.js/) for high-resolution images

Rodan is set up with [Docker](https://docs.docker.com/get-docker/) to run as a set of containers (though instructions on how to run it as a standalone, uncontainerized app remain).  Rodan itself is a fairly large stack that includes a Django application, two different databases, a distributed processing system, a reverse proxy, and a client for accessing the API. Each of these elements are contained inside docker containers for easier scaling and load distribution. This wiki details both Rodan's core functionality and how the Docker setup works.

** Rodan-lite Wiki TOC **
- Rodan Docker Setup and Deployment
    - Rodan Roadmap
    - Install Docker for Deployment
    - Install Docker for Development
    - How Rodan-Docker Works

- Developing
    - Repository Structure
    - Working on Rodan
    - Testing Production Locally
    - Working on Interactive Classifier
    - Job Queues
    - Testing New Docker Images

- Deployment
    - Set up Environment Variables
    - Set up SSL with Certbot
    - Set up SSH with GitHub
    - Deploying on Staging
    - Deploying on Production
    - Import Previous Data

- Miscellaneous
    - Maintenance
    - Continuous Integration (Nightly Builds)

- Rodan Core

- Rodan Job Package System
    - List of Rodan Jobs
    - Write a Rodan Job Package
    - Register Rodan Jobs through migration
    - Note on Gamera-4 Package

- Rodan Workflow Model
    - Workflow ERD  
    - [Examples](https://github.com/DDMAL/Rodan/wiki/New-Workflow-Model-Examples)
    - Workflow Validation
    - Workflow Execution
    - Subworkflow
    - Workflow ⇔ JSON

- Rodan Server API Overview
    - API Root
    - Authentication
    - List API
    - Detail API
    - Task Queue API
    - Interactive RunJob API
    - Admin
    - Websocket API

- Rodan Permission System
- Unit Test
- Run Unit Tests Locally
- Installation without Docker
- Miscellaneous


**For tutorials, please visit the following:**

For beginner USERS: https://github.com/DDMAL/e2e-omr-resources/wiki, 

For more advanced USERS and DEVELOPERS: https://ddmal.ca/e2e-omr-documentation/tutorial/getting-started.html