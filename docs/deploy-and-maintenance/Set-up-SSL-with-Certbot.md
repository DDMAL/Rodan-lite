In order to configure the Rodan app for access over HTTPS, you will need to set up certificates with [Certbot](https://certbot.eff.org/docs/using.html). 

# How Certbot Works

Certbot works by making your server complete a "challenge," the steps of which are detailed [here](https://certbot.eff.org/docs/using.html#webroot). In brief, it will ask you for the domain name of your website; let's say it's `yourwebsite.com`. It will then create a file named `[a long, random string of characters]` containing a string of data on your server, and make a request to `http://yourwebsite.com/.wellknown/acme_challenge/[a long, random string of characters]` and try to retrieve that string of data. If the data it retrieves is the same as the data it placed in your server, then the challenge is successful, and you will be granted certificates that let you run your web app over HTTPS.

These certificates will be stored in a volume named `certbot`, which is managed by docker and located on the VM at `/var/lib/docker/volumes/rodan_certbot`. This directory is mounted as a volume into the `nginx` container so that it can access the certificates, and also so that the certificates persist as long as the VM exists even if docker is down. 

Certbot is installed by default in the `nginx` container, which mediates all HTTP requests between Rodan and the outside world. The straightforward thing you might think to do here would be to just deploy with `make deploy_staging` or `make deploy_production`, get a bash shell into the nginx container with the following command:

```
sudo docker exec -it $(sudo docker ps -q -f name=rodan_nginx) bash
```

And run certbot to get your certificates. Unfortunately, **this process will not work unless you already have certificates from a previous run of certbot.** If you are installing rodan-docker from scratch (that is, without having certificates already) and run `make deploy_staging`, the nginx container will crash shortly after booting up, and restart, and crash, and restart forever. (If you run it with `make deploy_production`, it will just crash and stay down.)

So, you can't load up the `nginx` container to run certbot unless... you've already run certbot. Which you can't do, because the container is crashing. What's going on here?

# The Nginx Container

This is a lot of detail, but it is useful to know exactly what is going on so that you can debug if/when things go wrong.

Here is the entry for the `nginx` service in the `staging.yml` file in the main directory of the `rodan-docker` repository, with added comments.

``` yaml
  # Define a service called "nginx".
  nginx:
    # Define this service to start from the ddmal/nginx:v1.3.1 image
    image: "ddmal/nginx:v1.3.1"
    deploy:
      replicas: 1
      # Define the docker container running this service to reserve less than one CPU and one GB of memory on the VM.
      resources:
        reservations:
          cpus: "0.5"
          memory: 1G
        limits:
          cpus: "0.5"
          memory: 1G
      # Force this service to restart whenever it crashes, no matter what.
      restart_policy:
        condition: any
        delay: 5s
        window: 30s
    # Define a 'healthcheck' which checks periodically that the correct processes are running in the container and logs it if they are not.
    healthcheck:
      test: ["CMD", "/usr/sbin/service", "nginx", "status"]
      interval: "10s"
      timeout: "5s"
      retries: 2
      start_period: "5m"
    # Point to the script that will be run automatically when the container boots up. If this script ends or crashes, the container will shut down.
    command: /run/start-production
    # Define environment variables that will be available inside the container.
    environment:
      TZ: America/Toronto
      SERVER_HOST: rodan2.simssa.ca
      TLS: 1
    # Define the ports for which docker will open traffic into this container.
    ports:
      - "80:80"
      - "443:443"
      - "5671:5671"
      - "9002:9002"
    # Define the location of volumes that will allow this service to access the filesystem of its host machine.
    volumes:
      - "resources:/rodan/data"
      - "certbot:/etc/letsencrypt"
```

This file defines the behavior and configuration of each service in rodan-docker when deployed with `make deploy_staging`. Note this line in particular:

```
    # Point to the script that will be run automatically when the container boots up. If this script ends or crashes, the container will shut down.
    command: /run/start-production
```

This `/run/start-production` file is a script that runs some basic setup procedures and ends with running the command `nginx`, which starts up the `nginx` reverse proxy inside the container. However, if the certificates are not present, then nginx will exit immediately with an error, the `/run/start-production` script will end, and the container will dutifully take itself down. Then, because we have defined a `restart-policy` of `any` a few lines higher up, it will attempt to go up again, and repeat. (The `production.yml` file does not include a `restart-policy`, so it will just crash.)

So, here is what we need to accomplish:

1. Start up the `nginx` container in a way that does not crash immediately.
2. Start up the Nginx reverse proxy inside the `nginx` container such that it is accepting connections on port 80 (so that certbot can complete the challenge) but does not look for (and fail to find) the certificates.
3. Run certbot and get the certificates, which will be placed in the `/etc/letsencrypt` folder inside the `nginx` container (which are mounted into a docker volume, so they will persist even if the container goes down).
4. Shut all running containers down and start it back up like normal, so the Nginx reverse proxy in the container finds the certificates and accepts HTTPS traffic.

Complicating this is the fact that we cannot run the `nginx` service by itself; the Nginx reverse proxy is configured to only work if the other containers of rodan-docker are up.

### One way to do it

You can edit the `staging.yml` file so that the command line from above reads:

```
    # Point to the script that will be run automatically when the container boots up. If this script ends or crashes, the container will shut down.
    command: tail -f /dev/null
```

If we then run `make deploy_staging`, the `nginx` container will simply run a command that lasts forever and does nothing, never crashing. Then, you can get a bash shell into that container with

```
sudo docker exec -it $(sudo docker ps -q -f name=rodan_nginx) bash
```

And poke around inside the container. There is a script at `/run/start` that is similar to the `/run/start-production` script, but configures Nginx slightly differently so that it does not use TLS and does not look for the certificates (this is actually the script that is executed when you run rodan-docker for local development). Run this script in one terminal and open up another bash shell into the container (as above) to run certbot.

To test that Nginx is working properly, you can emulate what certbot is about to do: navigate to `/var/www/letsencrypt/.well-known/acme-challenge`, and make a file named `test.txt` containing some text. (for example, run `echo "Hello World" > test.txt`). Then, in a browser, navigate to `http://rodan.simssa.ca/.well-known/acme-challenge/test.txt` (substituting in whatever domain you're setting rodan up for), and you should see the text in `test.txt`.

If successful, run certbot (at last!) with

```
certbot certonly --dry-run --webroot
```

It will ask you for the domain name you're trying to get a certificate for (input `rodan.simssa.ca` or `rodan-staging.simssa.ca` or whatever domain you're setting up) and the webroot of your server (input `/var/www/letsencrypt/`). If all goes well, it will tell you all challenges succeeded. It is important that you make sure this works with the `--dry-run` flag first! We are limited to a certain number of attempts per week.

Run again without the `--dry-run` flag to run it for real. If there is a problem, it's not a bad idea to run in [Manual mode](https://certbot.eff.org/docs/using.html#manual) first (add the `--manual` flag to the above command) so you can see exactly in which folders certbot is "looking" for.

Finally, check that the certificates are in the right place in the VM (check `/var/lib/docker/volumes/rodan_certbot/data_/live` outside the docker container). If they're there, you can shut everything down with `make stop`, **edit the `staging.yml` file back to its original state,** and deploy again. The Nginx reverse proxy in the `nginx` container should find the certificates and not crash, which you can confirm with `docker ps`.
