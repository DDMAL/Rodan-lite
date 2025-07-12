The Staging server is an environment that is intended to test the integration of our tools for Rodan, before deploying a new release for Production. This server is updated nightly with all files and users deleted.

### Deploy

After installing Docker, logging into Docker, and Git cloning Rodan, setting up SSH with GitHub, and setting the environment variables, run the following Makefile commands.

```shell
make stop
make deploy_staging
```

This will bring up the containers and start the necessary services in each of them. You may now need to [[configure SSL with Certbot|Set up SSL With Certbot]], if you haven't already.

If you need to pull the most recent images, run `make pull` before `make deploy_staging`.



