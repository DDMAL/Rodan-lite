# Steps to run Run locally
_This is for M1/ARM/Mac with Apple Chip users. If you're using Intel chips, you're in the wrong place :(_

Is this your first time setting up Rodan? If yes, go [here](#First-time-setting-up-environment). No? [this](#This-is-not-my-first-time-running-Rodan) is for you. Looking for troubleshooting? [Here](#Troubleshooting) you go.

## First time setting up environment
1. `git clone https://github.com/DDMAL/Rodan.git`
2. `cd Rodan`
3. `git fetch origin; git checkout develop`
4. `make build_arm`, before running this step ensure that the Docker application is installed, open, and running.
5. `make remote_jobs`
6. Open `./rodan-main/code/rodan/settings.py`, comment out jobs inside `RODAN_GPU_JOBS`. You do something like this:
```python
RODAN_GPU_JOBS = [
    # "rodan.jobs.Calvo_classifier",
    # "rodan.jobs.text_alignment",
    # "rodan.jobs.Paco_classifier",
    # "rodan.jobs.background_removal",
    # "rodan.jobs.SAE_binarization"
]
```
7. Open `./rodan-main/code/rodan/jobs/register_all_jobs.py`, comment out register_gpu() in register_all(). 
```python
def register_all():
    # Register all jobs
    register_base()
    register_py3()
    # register_gpu()
```
8. `make run_arm`
9. Open a new tab, navigate to Rodan, `docker compose -f arm-compose.yml exec rodan-main /run/start`
10. Open a new tab, navigate to Rodan, `docker compose -f arm-compose.yml exec celery /run/start-celery`
11. Open a new tab, navigate to Rodan, `docker compose -f arm-compose.yml exec py3-celery /run/start-celery`

## This is not my first time running Rodan
Do this if you already have `nginx-local:latest` on your machine, you've run remote_job so environments for `pixel_wrapper` and `neon_wrapper` are good to go, and you've already commented out jobs related to GPU.
1. `make run_arm`
2. Open a new tab, navigate to Rodan, `docker compose -f arm-compose.yml exec rodan-main /run/start`
3. Open a new tab, navigate to Rodan, `docker compose -f arm-compose.yml exec celery /run/start-celery`
4. Open a new tab, navigate to Rodan, `docker compose -f arm-compose.yml exec py3-celery /run/start-celery`

## Troubleshooting
### HELP I don't know I have `nginx-local:latest` or not. What should I do?
* Open your favorite terminal
* Make sure docker desktop is running
* Enter this: `docker image ls nginx-local:latest`
* If you already have it, here's what you'll see:
```
REPOSITORY    TAG       IMAGE ID       CREATED       SIZE
nginx-local   latest    6b9697b940bd   13 days ago   214MB
```
* If you do NOT have it, you'll get this:
```
REPOSITORY    TAG       IMAGE ID       CREATED       SIZE
```

### Okey I don't have `nginx-local:latest`, what should I do?
Run `make build_arm`

# Introduction

The primary difference between "default" Rodan and the version that runs on ARM based CPUs (such as the Apple M1 series) is the lack of TensorFlow and other GPU/specific architecture dependent solution support. Alongside disabling the gpu-celery container and GPU dependent jobs, this also limits our ability to use HPC RabbitMQ, causing us to fallback on the non-HPC version. 

## Preparing the Repository 

There are several files that need to be changed for the ARM commands to work. While it would be possible to separate these into another branch, we don't want to split the developers this way -- functionality on all else remains the same. 

First, go to `/rodan-main/code/rodan/settings.py` and comment out all jobs classified under RODAN_GPU_JOBS. You may have to further comment out other jobs depending on the state of the `develop` branch. 

Secondly, go to `/rodan-main/code/rodan/jobs/register_all_jobs.py` and comment out the `register_gpu()` function call inside the `register_all()` function.  

## Getting the Images and Running Them

Contrary to the default version, ARM uses the `arm-compose.yml` file for image specifications. While most images specified there will be pulled automatically once you run `docker compose` with that specific `.yml` file, we need to build the NGINX container to remove HPC-RabbitMQ. 

Rest of the images will automatically be downloaded from Docker Hub once you run `make run_arm` -- they are the same between both versions. You should be able to run the rest of Rodan (except the gpu-celery container) following the instructions in [Working on Rodan](https://github.com/DDMAL/Rodan/wiki/Working-on-Rodan) page. 