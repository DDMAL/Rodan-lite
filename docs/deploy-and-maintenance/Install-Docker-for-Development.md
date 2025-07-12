Download and install [Docker](https://www.docker.com/community-edition) for your platform. If Docker is not supported on your platform (e.g. macOS older than 10.10.3, Windows older than 10 Pro, or unsupported hardware), use [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_mac/) instead which will also require virtualbox. The installation with docker toolbox is slightly different, but the same images can be used without too much modification.

After Docker or Docker Toolbox is installed, run the following command:

```shell
docker login
```
Rodan-docker images are privately hosted on Docker Hub and you will not be able to get the latest version of the images without logging in to docker for access. Enter the DDMAL credentials for Docker Hub (contact the lab manager if you don't know them) to save the credentials in docker. You only need to do this once.

# Docker Toolbox

Docker Toolbox should not be necessary on relatively modern machines.

- You can get `Virtualbox` from: https://www.virtualbox.org/wiki/Downloads or from Homebrew.

```
brew cask install virtualbox
```

- You can get `Docker Toolbox` from: https://docs.docker.com/toolbox/ or from Homebrew.

```
brew cask install docker-toolbox
```

Docker Toolbox needs Virtual Box in order to virtualize some functionality on older hardware. Toolbox is considered legacy software right now and may eventually become deprecated.

Machines that are spun up with VirtualBox do not get resolved to localhost, you could write a line in the host file but note that Google Chrome and Microsoft Edge ignore the host file. The better solution is to fix the IP address in inside the docker container. Eg: If the output of `docker-machine ip default` is `192.168.99.100`, then the following IP will work.

```
docker compose exec nginx bash
sed -i "s/localhost/192.168.99.100/g" /var/www/default/dist/configuration.json
```

Now instead of accessing Rodan through localhost, the api is available at https://192.168.99.100 and the Rodan-Client is available at: https://192.168.99.100:9002
