This repository uses the Git submodules mechanism to include all the libraries needed to set up Rodan. Git submodules are essentially pointers to other Git repositories, and are specified in the `.gitmodules` file.

Clone this repository into a convenient spot on your local machine, if you are setting up for local development, or into the `/srv/webapps/` folder if you are setting up on a VM for remote deployment. If you are setting up for deployment, you should follow the [[instructions to set up SSH with GitHub|Set up SSH with GitHub]] so that you do not have to log into your personal account to do this.

```shell
git clone https://github.com/DDMAL/rodan-docker.git
```

Cloning the submodules is necessary if you wish to build the Docker images or develop Rodan locally. When using graphical Git clients such as GitHub Desktop or SourceTree, the submodules are usually automatically cloned for you. When cloning on the command line, run the following command after `git clone` to clone the submodules as well:

```shell
git submodule update --init
```

Make sure that you are logged in to docker:

```shell
docker login
```

Rodan-docker images are privately hosted on Docker Hub and you will not be able to get the latest version of the images without logging in to docker for access. Enter the DDMAL credentials for Docker Hub (contact the lab manager if you don't know them) to save the credentials in docker. You only need to do this once.

To pull the latest nightly images from Docker Hub, navigate into the `rodan-docker` folder and use the following command inside the Makefile

```shell
make pull
```

Docker will begin pulling the latest nightly images for each service from Docker Hub (these are pretty big so it will take a while).

The method of spinning up the containers and starting Rodan differs depending on if you're doing this for [[local development|Working-on-Rodan]] or [[deploying for staging/production|Deployment]]. See the relevant pages in the sidebar.