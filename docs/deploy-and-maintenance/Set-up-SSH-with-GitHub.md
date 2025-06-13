### Setup an SSH key to pull the latest Rodan-Docker changes on a deployed server

There are some very good instructions on how to create an ssh key <a href="https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-linux">Here</a> from GitHub. There are just a few things to consider, **do not install `xclip`** it is not useful for our purposes because we have SSH-ed in our staging environment anyway. **Use `copy and paste` functions instead.**

```bash
ssh-keygen -t rsa -b 4096 -C "yourname"
```

- Add the Public key (e.g., id_rsa.pub) to the deploy keys in the settings for Rodan-Docker. **Do not check the "allow editing" checkbox.** Put the name of the server and your name also.
- Create an ssh config under your account with the following, make sure the IdentityFile directive points to the location of the private ssh key we just made.
  ```
  Host github.com
    User git
    HostName github.com
    IdentityFile ~/.ssh/id_rsa
  ```

### Clone the repository

**Important:** There are two major branches for Rodan. Major releases are in Production, while the `develop` branch with the nightly builds is the one on the Staging server.

```bash
cd /srv/webapps/
git clone --single-branch -b develop git@github.com:DDMAL/Rodan.git
```