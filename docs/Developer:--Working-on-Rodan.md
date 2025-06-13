# Introduction 

This page describes how to run Rodan locally on your own computer

# Starting up Rodan

If this is the first time you install Rodan on your local machine, you need a few extra steps to build some modules.

First, make sure you have installed the following packages with the exact versions as listed below.

```
node: v12.22.12
yarn: 1.22.22
npm: 8.10.0
```
You can consult ChatGPT to find commands for package installation.

Next, you need to do `make remote_jobs`.

Then, you need to modify some files before you can run rodan locally. 
Within the Rodan directory run: 

```shell
cp rodan-client/local-dev/COPYconfiguration rodan-client/config/configuration.json
```

and 

```shell
cp rodan-client/local-dev/CPCONFIGFILE rodan-client/code/src/js/Configuration.js
```

Then

In `Rodan/rodan-main/code/rodan/settings.py` change, `SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "https")` to `SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "http")`

***Always revert these changes before pushing**

The following command will start up all the containers for each service.

```shell
make run
```

Once all the containers are launched, which should take less than a minute, you can start actually launching the services within each of these containers.

The following commands will run scripts that are non-finishing and must be running for Rodan to work. Run each of these commands in different shells. I would recommend using tmux or iTerm2 to create multiple panes. 

You may need to run `make remote_jobs` to ensure all jobs are on your local machine before moving onto the next steps.

To start the Rodan API, run the following two commands in a tab, making sure you start in the same folder where you cloned the repository:

```shell
docker compose exec rodan-main /run/start
```

If you point your browser to `http://localhost/api`, you should be able to see the Rodan API.

Next you need to start the celery workers. These are all started in a very similar way, and you should do each of them in a new Terminal/Powershell window or tab.

For Rodan core tasks (uploading/creating resources, creating diva, creating master tasks to distribute to the other celery queues, etc.)
```shell
docker compose exec celery /run/start-celery
```

For Python3 jobs:
```shell
docker compose exec py3-celery /run/start-celery
```

For GPU jobs:
```shell
docker compose exec gpu-celery /run/start-celery
```

You don't have to run all three of these if you only want to work on a single job (for example, only a job that uses the Python3 queue). Make sure the correct queue is running for the job(s) you wish to work on _and_ make sure the first (Rodan core) celery is running), otherwise the Rodan job will never complete. Which queue a job runs in is declared in the jobs setting dictionary, for example: https://github.com/DDMAL/pil-rodan/blob/a29a183a9815dd54450b6876e3a3a037b76cd93c/to_png.py#L9-L11.

- Once the `/run/start` and all the `/run/start-celery` for the queues you need have been started, you can point your browser to http://localhost to view the Rodan-Client web interface. 
- Once you make a change to a job's code locally, you do not need to restart the entire process to see the changes reflected in Rodan - you can keep the containers running and just restart Rodan itself in the tab where you ran `docker compose exec rodan bash` (use `Ctrl+C` to stop Rodan, and then run `/run/start` again). Do the same for each of the Celery queues you have running.
- To view the Rodan RestfulAPI, visit http://localhost/api. The default username is `rodan` with the password `rodan`. If needed, you may observe the log output of the Rodan containers in the terminal window where `make run` is running. When you are finished, quit using `Ctrl+C`.
- You can also get a basic shell into the containers instead of running the start scripts by running, for example, `docker compose exec rodan-main bash` 


### Note for Docker Toolbox Users

Because docker toolbox needs to run virtualbox to virtualize some hardware, Rodan will not be available on http://localhost. Read more about it in [Install Docker for Development](https://github.com/DDMAL/rodan-docker/wiki/Install-Docker-for-Development) if this is your situation.

## Installing and Enabling Jobs

By default not all of the Rodan jobs are installed, but all dependencies for all rodan jobs are. Most jobs only need to be `git clone`d in the `/rodan-main/code/rodan/jobs` folder and uncommented in `/rodan-main/code/rodan/settings.py` under section `1.c`.

For more information on how jobs work in Rodan, please see [[Job Queues|Job-queues]].

## Sending Emails

Rodan sends email notifications using Amazon SES via SMTP. By default, emails are printed to the console. If you wish to test out this feature locally, you will need to set the following variables in the `local.env` file using the credentials found on the [resource page](https://wiki.internal.simssa.ca/wiki/Resources#AWS_Email) in the Wiki. Make sure not to commit these credentials to the repository!

```
###############################################################################
# SMTP Configuration
###############################################################################

EMAIL_HOST=<host>
EMAIL_PORT=<port>
EMAIL_HOST_USER=<username>
EMAIL_HOST_PASSWORD=<password>
```

## Create other accounts locally

1. Run rodan locally
2. Ssh into the rodan-main container by using the command `docker exec -it [rodan-main container ID]` /bin/bash 
> You can get the container ID by using the `docker ps` command and copy and pasting it 
3. cd into the rodan directory, `cd /code/Rodan`
4. Run the manage.py shell, `python3 manage.py shell`
3. Create a testworker, test_worker = User.objects.create_user(username="test_worker", email="test@rodan2.simssa.ca", password="password") 