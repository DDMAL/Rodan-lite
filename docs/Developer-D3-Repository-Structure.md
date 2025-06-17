# Repository Folder Structure

- The `hooks` folder is specific to docker, and it holds settings for the automatic docker builds in the cloud.
- the `scripts` folder (/scripts) holds miscellaneous files and scripts, like the default environment variables file for Rodan and cronjobs scripts
- Each folder houses their own container needed to run the Rodan service (except: hooks, redis, scripts)

### Docker Container/Services Folder Structure

Each service has its own folder, and they all hold the same folder structure.

- The `code` folders (eg: rodan-main/code, rodan-client/code) are submodules for their respective repositories. 
- The `config` folders (eg: nginx/config, rodan-client/config) houses configuration files for the container.
- The `scripts` folder (eg: rodan-client/scripts) point to start scripts and docker entry points for their respective containers. These scripts exist to help you for that specific container. There can also be scripts to help build the service outside of the dockerfile.
- The `maintenance` folder (eg: postgres/maintenance) is a collection of database maintenance scripts. These are vital to backups, do not change them unless you know what you are doing.

# The Makefile

The Makefile is meant to make your life easier. Prepend each of the following commands with `make` to run them from the root of the project directory (e.g. `make run`).

#### Most useful commands

- `run` This command will bring up all docker containers for local development. This has an optional argument, `DOCKER_TAG`, that will pull specific docker images. See [Testing New Docker Images](https://github.com/DDMAL/Rodan/wiki/Testing-New-Docker-Images) for more information.
- `run_client` This command will bring up the Rodan-Client container to work on the frontend.
- `deploy_staging` This command will deploy Rodan Staging using the scalable docker swarm. The domain is already declared in the configuration for you.
- `deploy_production` This command will deploy Rodan Production using the scalable docker swarm.  The domain is already declared in the configuration for you.
- `update` This command will update the running docker swarm services with the latest image with the nightly tag. You can pull new images while the services are running. If you want to know how to update to another specific tag, look at where this command is written in the Makefile to understand the docker commands to do this on your own. All you need to do is replace nightly.
- `stop` This command will stop all docker containers and services without exception. (It will also stop non-Rodan docker services or containers running on your machine, if you are running any.)
- `build` This command will build all of Rodan in parallel (Rodan, Celery, Python2-Celery, Python3-Celery, Postgres with PL-Python, etc.) Rebuilding Rodan takes a very long time (on the order of several hours), and you should not need to use this often, if ever, unless you are debugging on the build process itself.
- `push` This will push all the locally built images of Rodan to replace the one on Docker Hub with the nightly tag.
- `pull` This will pull the latest nightly images from Docker Hub.
- `pull_docker_tag` This will pull a specific set of images from Docker Hub, by tag. Define the variable `tag` before running this command, e.g. `tag=v1.5.0rc0 make pull_docker_tag`.
- `push_docker_tag` This will push the locally built images of Rodan-docker to Docker Hub, and tag them with the given tag. Define the variable `tag` before running this command, e.g. `tag=v1.5.0rc0 make push_docker_tag`.
- `clean` This will delete all stopped services, images, and volumes **(dangerous!)**.
- `clean_git` This will git reset the current rodan-docker repository and pull the latest rodan-docker git changes
- `clean_swarm` This command will stop Rodan services, leave the swarm, and reinitialize a new empty docker swarm. It combines other commands.

Please see the section on ARM based CPUs if you're attempting to run Rodan locally on such a machine. 
