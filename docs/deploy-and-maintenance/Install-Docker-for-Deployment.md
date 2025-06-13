This page details the procedure for preparing an Ubuntu 18.0.4 virtual machine to deploy rodan-docker on production or staging.

### Update

Before installing anything, it is a good idea to have all the packages on the machine as up-to-date as possible. This command (below), over the regular `apt-get upgrade`, will smartly handle changing dependencies with new versions. Not to worry, `apt-get` has a _fairly_ good (not perfect) conflict resolution system, but it is important to note that it is not perfect. Our app is isolated from this process, but it may break other tools outside the containers (for SSL certificate regeneration, etc.)

```
sudo -i
apt-get dist-upgrade -y
```

### Auto-Update

Once you have your machine up to date, it is recommended that you setup unattended-upgrades.

- `apt-get install unattended-upgrades`
- Edit the contents of `/etc/apt/apt.conf.d/50unattended-upgrades` with, keeping the comments for reference.

  ```conf.d
  Unattended-Upgrade::Allowed-Origins {
          "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    // Extended Security Maintenance; doesn't necessarily exist for
    // every release and this system may not have it installed, but if
    // available, the policy for updates is such that unattended-upgrades
    // should also install from here by default.
    "${distro_id}ESM:${distro_codename}";
    "${distro_id}:${distro_codename}-updates";
  };
  ```

- Updates to nginx, **IF INSTALLED**, should be performed manually

  ```conf.d
  // List of packages to not update (regexp are supported)
  Unattended-Upgrade::Package-Blacklist {
    nginx;
  };
  ```

- Send email on failure (could be to the root user)

  ```conf.d
  // Send email to this address for problems or packages upgrades
  // If empty or unset then no email is sent, make sure that you
  // have a working mail setup on your system. A package that provides
  // 'mailx' must be installed. E.g. "user@example.com"
  Unattended-Upgrade::Mail "rodan.simssa@gmail.com";

  // Set this value to "true" to get emails only on errors. Default
  // is to always send a mail if Unattended-Upgrade::Mail is set
  Unattended-Upgrade::MailOnlyOnError "true";
  ```

- Don't let old kernels or dependencies take up space

  ```conf.d
  // Remove unused automatically installed kernel-related packages
  // (kernel images, kernel headers and kernel version locked tools).
  Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";

  // Do automatic removal of new unused dependencies after the upgrade
  // (equivalent to apt-get autoremove)
  Unattended-Upgrade::Remove-Unused-Dependencies "true";

  // Automatically reboot *WITHOUT CONFIRMATION*
  //  if the file /var/run/reboot-required is found after the upgrade
  Unattended-Upgrade::Automatic-Reboot "true";

  // If automatic reboot is enabled and needed, reboot at the specific
  // time instead of immediately
  //  Default: "now"
  Unattended-Upgrade::Automatic-Reboot-Time "02:00";

  ```

- Optionally install all updates only on shutdown

  ```conf.d
  // Install all unattended-upgrades when the machine is shutting down
  // instead of doing it in the background while the machine is running
  // This will (obviously) make shutdown slower
  //Unattended-Upgrade::InstallOnShutdown "true";
  ```

- Make sure `unattended-upgrades` is working
  - `service --status-all` should have `[ + ] unattended-upgrades` in the output
  - `unattended-upgrades --dry-run --debug` should return
    ```bash
    Fetched 0 B in 0s (0 B/s)
    fetch.run() result: 0
    blacklist: ['nginx']
    whitelist: []
    No packages found that can be upgraded unattended and no pending auto-removals
    ```

# Installation

If you are installing rodan-docker for local development, and  Docker is not supported on your platform (e.g. macOS older than 10.10.3, Windows older than 10 Pro, or unsupported hardware), use [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_mac/) instead. The installation with docker toolbox is slightly different, look at the [docker-toolbox](https://github.com/DDMAL/rodan-docker/wiki/Docker-Toolbox) page for more information.

For installing on ubuntu for production, install `docker` and `docker compose` on ubuntu with a convenient script as a regular user that will instantiate docker. We could use the script provided by docker by using `curl -fsSL https://get.docker.com -o get-docker.sh` but we do not control what goes in or out of that script.

```bash
curl -fsSL https://gist.githubusercontent.com/deepio/297c3e79f3c02f6e49166297eac8020c/raw/81aaca1edbf4795fb3648194b8040f2083664cda/Install%2520Docker-CE%2520Ubuntu | bash
```

- Logout and login to allow the current user to have access to docker
- Create a private key pair
  - `ssh-keygen -t rsa -b 4096 -C "rodan.simssa@gmail.com"
  - In this example, we named it rodan-docker
- Enter the public key in the github repo's deploy keys with a name associated to the server you setup
  - `https://github.com/DDMAL/rodan-docker/settings`
  - `Deploy Key`
  - `Add deploy key`
  - Add a name in the name box
  - Copy the contents of `~/.ssh/rodan-docker.pub` into the key box
  - **Make sure `Allow write access` is off**
- Create a config file in the ssh folder `~/.ssh/`

  ```
  Host github.com
    HostName github.com
    User git
    IdentityFile ~/.
  ```

- Test the ssh config with `ssh github.com`, should return

  ```
  PTY allocation request failed on channel 0
  Hi DDMAL/rodan-docker! You've successfully authenticated, but GitHub does not provide shell access.
  Connection to github.com closed.
  ```

# Updating NVidia and CUDA

By following these steps, you will first delete any existing NVidia drivers on the system, then install version 460 of the driver and the container runtime.

As of 2022-06-01, we are running CUDA 11.4 and NVidia driver 460 in production.

```bash
sudo apt-get purge "*nvidia*"
sudo apt install nvidia-driver-460
sudo apt install nvidia-container-runtime
```

You can check which version of NVidia and CUDA by running `nvidia-smi`.

# Log in to Docker

After Docker or Docker Toolbox is installed, clone this repository on your computer and run the following command:

```shell
docker login
```

Enter the DDMAL credentials for Docker Hub, the credentials are on the DDMAL Wiki (contact the lab manager if you don't know them.) Save the credentials to your computer; you only need to do this once but it is a good idea to keep the password in a password manager also.

That's it! You now have the minimum installation needed to run Rodan locally.
