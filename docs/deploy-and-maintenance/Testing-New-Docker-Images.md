# Introduction

> Portals:
>
> - I request Docker Hub building new images using my feature branch! How do i do that? See [`<custom docker tag>`](#custom-docker-tag)
> - How to prepare docker tag when I want to move changes to production? See [`<git tag>`](#git-tag), which will leads you to [Deploying on Production](https://github.com/DDMAL/Rodan/wiki/Deploying-on-Production)
> - Too many texts going on :/ Just show me the concolusion thank you. See [Takeaway](#Takeaway)

This page describes how to build and test your own Rodan docker images without intervening with the nightly builds.

## How Docker Tag Works on Rodan

We have four kinds of tags going on on Docker Hub: `nightly`/`this`/`<custom docker tag>`/`git tag`

### `nightly`

The nightly tag is only used on develop branch. It should not be intervened by feature branches. To pull images with nightly tag, follow instructions in [Working on Rodan](https://github.com/DDMAL/Rodan/wiki/Working-on-Rodan) or [Running Rodan on ARM](https://github.com/DDMAL/Rodan/wiki/Running-Rodan-on-ARM)

### `this`

`this` tag is specifically used when a pull request is made to merge a feature branch into develop branch. `ddmal/rodan-python3-celery`, `ddmal/rodan-main`, and `ddmal/rodan-client` are built using the codebase on the feature branch and pushed to Docker Hub using the special `this` tag. We do so since `rodan-main` is built using `rodan-python3-celery`, and `nginx` is built using `ddmal/rodan-main` and `ddmal/rodan-client`.

### `<custom docker tag>`

Read this section if **you want to work on your feature branch, build images on Docker Hub that has your changes in it, and pull those images to your workstation to test them**. To do so without intervening with the `nightly` tag, set up a build rule on Docker Hub and add a custom tag to it. Here're the steps to do so:

1. Go do the rodan repo on Docker Hub and click the builds tab.
2. Click Configure Automated Builds.
   ![configure-automated-builds](https://github.com/DDMAL/Rodan/assets/25975988/c2127494-5de5-4ec6-9ed3-f5db46ed57c3)
3. Click the plus beside Build Rules.
   ![build-rules](https://github.com/DDMAL/Rodan/assets/25975988/90f1175b-05ac-42e9-8c90-332e47f45ded)
4. Put the branch name in `Source`. e.g. My feature branch is called `add-docker-tag`, so I put `add-docker-tag` in Source.
5. Put the tag you want (e.g. `my-tag`) in `Docker Tag`. You have to follow the naming rule of docker tag.
6. Click the `Save and Build` button.
   ![build-rule](https://github.com/DDMAL/Rodan/assets/25975988/be649bc3-55a4-4721-9da5-5721204eb8ad)
7. Docker images will be tagged using the tag you specified.
8. After Docker Hub finishes building your feature branch, `make run DOCKER_TAG=<docker tag>` or `make run_arm DOCKER_TAG=<docker tag>` to pull images tagged with `<docker tag>` and start rodan. e.g., `make run DOCKER_TAG=my-tag` to pull these images:

```
ddmal/nginx:my-tag
ddmal/rodan-main:my-tag
ddmal/celery:my-tag
ddmal/rodan-python3-celery:my-tag
ddmal/rodan-gpu-celery:my-tag
ddmal/postgres-plpython:my-tag
```

and start containers using using those images.

### `<git tag>`

Docker Hub will use git tags as the docker tag when it is building images from a release branch. A release branch should follow rules:

1. It is named as `release-<version>`.
2. It should always have a git tag attached to its `HEAD`.

See [Deploying on Production](https://github.com/DDMAL/Rodan/wiki/Deploying-on-Production) to learn how to prepare a release branch and make a new release.

### Takeaway

- If you're not interested in asking Docker Hub to build images using your changes and pull those special images, do `make run/make run_arm` and start making changes.
- The `nightly` tag is only used on develop branch, don't try to play around with it.
- Forget everything about `this` tag. It's just how Docker Hub works.
- To ask for Docker Hub building images using your feature branch, you need to go to Docker Hub and set up a build rule.
- For release branches, add a git tag on release branches. You still need to set up a build rule, but Docker Hub doesn't use the Docker Tag but tags images with the git tag.

---

## The following are deprecated

For testing your docker images the following files will need to be edited: `hooks\build`, `hooks\push`, `rodan-main\dockerfile`, `nginx\dockerfile` (and `nginx\dockerfile.arm` for an M1 machine) and `docker-compose.yml` (`arm-compose.yml` if necessary as well). In each of these files replace all `nightly` tags with a new tag (i.e. `build_fix`) **except for the iipsrv nightly tags**.

In the build and push files the tag variables set at the top of the file will need to be edited to correspond to the new tag. For example, if the testing tag was `build_fix`, lines 13-16 in the build file would be changed to:

```
RODAN_TAG=build_fix
#`cd rodan-main/code && git describe --tags --always`
RODAN_CLIENT_TAG=build_fix
#`cd rodan-client/code && git describe --tags --always`
RODAN_DOCKER_TAG=build_fix
#`git describe --tags --always`
BUILD_HASH=build_fix
#`git rev-parse --verify HEAD`
```

While it is possible to not edit these two files in this way by pushing a new git tag, this method is simpler and avoids conflict if there is a new production release.

#### Changing the Dockerhub Build Rules

The new branch and tag will be needed to be added to the [rodan repository on dockerhub](https://hub.docker.com/repository/registry-1.docker.io/ddmal/rodan/builds). This can be done by selecting 'Configure Automated Builds', adding your branch as the source and your tag as the docker tag.
Now every time changes are pushed to the new branch, new images will be built that can be pulled by simply running `make run`.

_**Before merging to develop it is necessary that all the changes documented in this page are reverted to ensure that develop's images are not affected.**_
