## Overview

As of July 2024, Compute Canada suggests that we migrate to vGPU instances and old hardware for GPU instances will come to the end of service soon. This page will include all the steps to set up (or reproduce) the current Rodan production server(s).
Here is a summary of what we have now for [rodan2.simssa.ca](rodan2.simssa.ca). Some reasoning behind this choice can be found in issue [#1184](https://github.com/DDMAL/Rodan/issues/1184).

1. A manager instance on Ubuntu 20.04 with Docker version 24.0.2, build cb74dfc, with 8 vCPUs and 1 vGPU (driver 550, 16GiB GPU RAM) and 40 GiB instance RAM.
2. A worker instance on Ubuntu 20.04 with Docker version 24.0.2, build cb74dfc, with 16 vCPUs and 16 GiB instance RAM.
3. A data instance on Ubuntu 18.04 with Docker version 24.0.2, build cb74dfc, with 4 vCPUs and 8 GiB instance RAM.
   **Note: do not upgrade Docker to any newer versions unless we are sure later Docker Engine does not lead to DNS resolution issues on Ubuntu.**

We distribute containers on the manager and worker instances as follows using Docker swarm, and we store all our data on the data instance. This avoids problems such as system incompatibility after upgrade and large data migration. From now on, the separation of data storage and computation allows us more flexible and more stable data handling with smaller instances.

On manager instance:

- rodan_rodan-main
- rodan_celery
- rodan_gpu-celery
- rodan_nginx
- rodan_postgres
- rodan_py3-celery
- rodan_redis

On worker instance:

- rodan_rabbitmq
- rodan_iipsrv
- rodan_rodan-client

Ideally, we want to put `py3-celery` on the worker instance at least. Although it is possible (and tested) with Debian 11 and 12, with Ubuntu 20.04, we have to put all those on the same instance to avoid `redis` timeout issue. Given the current limit of 8 vCPUs on the manager instance, the performance will be improved greatly if we can fix this and move those containers to the worker instance.

At this point, our manager instance is boot from the old `prod_Rodan2_GPU` disk with all the user data and resources, and therefore it is best practice to put `postgres` on this manager instance as well. Two instances share the data via NFS.

Also, upon testing, the `p` instance type (the worker instance) can easily be resized while retaining the same IP and Docker network.

## Prepare Instances

### Important notes on 26/08/2024

We experienced a major server crash: the GPU driver mysteriously disappeared, and the Docker service consumed so much memory that it could neither be launched nor modified. Despite trying everything we could to rescue the server, nothing worked, and the instance continued to report out-of-memory kills for any process we attempted to run. In the end, we realized that the only solution was to deploy a new server.

However, new problems arose: while we could accomplish everything with Debian 11, we couldn't run PACO training using the GPU. On the other hand, when using Ubuntu 20.04, we were unable to deploy the Docker service.

Later, we discovered the root of the problem preventing us from launching a full Docker Swarm. When launching a new Arbutus instance with Ubuntu 20.04, the default Linux kernel is a KVM version (which you can verify by running `uname -r`). This kernel is compact and optimized for virtual machines, but it does not include IPVS, which is necessary for virtual IP services. To use IPVS, a generic Linux kernel is required or we have to compile our own kernel.

While it is possible to directly install a new kernel and boot into it (with some complicated steps), doing so would cause another issue— the inability to properly use the NVIDIA GPU driver that comes with the vGPU instance.

To resolve this, the best approach is to start with the old Rodan volume that uses the old generic Linux kernel (or create a volume from a snapshot), boot it in another cloud environment (such as a persistent `p`-flavor instance), upgrade to the desired Ubuntu version (currently 20.04), then delete the instance and reboot it as a vGPU instance. Now, if you SSH into this new instance and check the kernel, it will be the desired generic version. Installing the vGPU driver at this point will also install the necessary KVM kernel, thereby avoiding compatibility issues between the generic kernel and the vGPU driver, while keeping the default kernel as the generic version that includes IPVS.

Since this process is quite complex, we've saved multiple snapshots at each step for backup purposes.

### Original documentation

Go to [Arbutus openstack page](https://arbutus.cloud.computecanada.ca/project/instances/), and click `Launch Instance`. Here is the information to fill out the form.

- Details: Any reasonable name and description. Make sure `Availability Zone` is `Any`.
- Source: For manager, it is boot from volume (and therefore the OS depends on the volume). For worker, it is boot from image and we pick the same OS (Ubuntu 20.04 in this case) and create a volume (1500 or 2000 GiB is fine). Make sure `Delete Volume on Instance Delete` is `False` for both worker and manager.
- Flavor: As of July 2024 we use `g1-16gb-c8-40gb` for manager and `p16-16gb` for worker.
- Networks: Select `rpp-ichiro-network`.
- Security Groups: Deselect `default` and select `prod-internal`.
- Configuration: Upload [cloud.init](https://github.com/DDMAL/Operations/blob/main/cloud-init.yml) from the ansible repo.
- Metadata: Add "rodan" label so that the new instance can be automatically added to `os_service_rodan` group managed by ansible. (This can also be done later.)
  Don't do anything else.

After this, run ansible `useradd` and `adminadd` to be able to ssh to the new instance.

## Set up vGPU drivers (on vGPU instance only)

1. Remove any existing Nvidia drivers.

```
sudo apt-get purge "*nvidia*"
```

2. Follow the official guide from Compute Canada [here](https://docs.alliancecan.ca/wiki/Using_cloud_vGPUs#Preparation_of_a_VM_running_Ubuntu20) according to the OS version.
3. Install `nvidia-container-toolkit`. (Official website[here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html))

```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

4. Install container runtime.

```
sudo apt install nvidia-container-runtime
```

## Install Docker (on both instances)

1. Make sure to follow the [Docker Guide](https://docs.docker.com/engine/install/ubuntu/) for specific OS and install the exact version we want.
2. Set up nvidia runtime for docker following [guide here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#configuring-docker). Prereq: (1) NVIDIA Container Toolkit; (2) Docker.

Steps:

a. `sudo nvidia-ctk runtime configure --runtime=docker --set-as-default`

b. `sudo systemctl restart docker`

c. run `docker info` and verify docker runtime has nvidia

```
Runtimes: io.containerd.runc.v2 nvidia runc
Default Runtime: nvidia
```

**Warning: steps from here are based on practice as there's no related official guide.**

d. in `/etc/docker/daemon.json` make sure it has full path like

```
{
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "args": []
        }
    },
    "default-runtime": "nvidia"
}
```

e. restart daemon and docker

```
systemctl daemon-reload
systemctl restart docker
```

## Set up GitHub (on both instances)

1. Generate the key pair.

```
ssh-keygen -t rsa -b 4096 -C "[rodan.simssa@gmail.com](mailto:rodan.simssa@gmail.com)"
```

We can name it `rodan-docker`.

2. Enter the public key (`~/.ssh/rodan-docker.pub`)in the github repo [settings](https://github.com/DDMAL/Rodan/settings) deploy keys with a name associated to the server.
   Make sure Allow write access is off.
3. Create a config file in the ssh folder `~/.ssh/`.

```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/rodan-docker
```

4. Test ssh.

```
ssh github.com
```

It should return

```
PTY allocation request failed on channel 0
Hi DDMAL/rodan-docker! You've successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed.
```

5. Clone the Rodan repo.

```
cd /srv/webapps/
git clone --single-branch -b master git@github.com:DDMAL/Rodan.git
```

Make sure to double check the branch.

## Set up Rodan

1. Modify `scripts/production.env` to have all the credentials.
2. Modify `rodan-client/config/configuration.json` to have 443 port `True`:

```
 "SERVER_HOST": "rodan2.simssa.ca",
    "SERVER_PORT": "443",
    "SERVER_HTTPS": true,
```

3. Make a copy of `production.sample` and rename it as `production.yml`. Then adjust `production.yml` and make sure we have reasonable resource allocation for each container.

## Set up NFS

Currently, our NFS sharing is achieved directly with docker. Please refer to `production.sample` in the repo. Just note the data server IP address and modify it accordingly in `production.yml`.
Some notes regarding this practice:

1. As of early 2025, we did not find official documentation regarding docker volume NFS. We put up things based on several related posts on docker user forum and it appeared to work quite well.
2. We also tried another approach, which was setting up NFS manually across instances, meaning that the docker volume directories on manager and worker instances were manually mounted using NFS. However, this leads to huge memory usage, even though we cannot conclude that it was this practice that caused this memory shortage and eventually malfunction of the distributed system. The history page should show the steps for the previous work.
3. Under this new setting, whenever docker swarm is not on, the docker volume will not be shared since the NFS is running only when docker swarm is working. This is normal.

## Set up Nginx

This is usually done by ansible `/playbooks/nginxconf.yml` after the current manager (or the instance running `Nginx`) IP has been updated in `/playbooks/vars/simssa.ca.yml` under `rodan2` block.

## Deploy Docker Swarm

(with `sudo -i` on both instances)

1. On manager

```
docker swarm init
```

and you will see a command for worker join token.
If swarm is already running, then run `docker swarm join-token worker`.

2. On worker, run the command generated in the previous step.

3. On manager, verify there are two nodes by `docker node ls`.

4. Start Rodan.

```
make pull_prod
make deploy_production
```

5. Verify Rodan service is correctly running by `docker service ls` on manager and `docker ps -a` on both instances.
   Sometimes `rodan_main` will fail when the stack is just launched but docker swarm will successfully reproduce it later when other containers are ready.

6. Some debugging commands that might be helpful:

```
docker info
docker service logs [service id]
docker service ps [service id] --no-trunc
docker logs [container id]
docker exec -it [container id] [bash or sh]
```

7. Some useful commands to run from `/srv/webapps/Rodan` on instance what runs the corresponding container, which can be found in [Makefile](https://github.com/DDMAL/Rodan/blob/master/Makefile):

```
make gpu-celery_log
make py3-celery_log
make celery_log
make rodan-main_log
```

## Future work

We might consider hosting data on a separate instance so that we do not have to stick with Ubuntu 20.04 and fit all big containers in the manager instance.

Also, to upgrade OS, if the nova cloud (for all GPU related instances) repo does not provide upgrade option, it is possible to delete the instance, boot the same volume as a regular `p` instance and do the OS upgrade in the persistent cloud. After the volume has been upgraded to the desired the newer OS version, we can delete the instance and boot a new vGPU instance from the same volume.

Be sure to search old issues and PRs for more notes.

We have not implemented the auto upgrade but instructions are [here](https://github.com/DDMAL/Rodan/wiki/Install-Docker-for-Deployment#auto-update).

Additionally, we still want to move `py3-celery` to the worker instance. Before having a separate data instance, we were not able to because `py3-celery` needs to access the docker volume hosted on the manager instance, and manual NFS sharing (not via docker) appears to cost too much memory. Now that we solved this problem with an additional data instance, it is possible that we can try to move `py3-celery` out from the manager instance to free up more vCPUs for other containers that need a lot of computational resources.
