Rodan-Docker images are rebuilt every night at `2am` on the staging server `132.206.14.133`. This could be done on a raspberry pi, as long as the cron job is on a machine somewhere. The nightly script is defined in the repository <a href="https://github.com/DDMAL/rodan-docker/blob/0204a0f7fc87d3685c24b212ce6578c734f45e34/scripts/nightly#L1">here</a>, at `rodan-docker/scripts/nightly`.

#### You must have done the following:

- Install `Docker-CE`, `Docker-Compose`
- Login `docker login` with the ddmal/docker credentials
- Create SSH-Keys for `GitHub` on the `DDMAL-Lab Manager` account.
  - [[Set up SSH with GitHub]]
  - Check your configuration with `ssh git@github.com`
- Added `2 0 * * 1-5 /srv/webapps/Rodan/scripts/nightly` in `crontab -e`
