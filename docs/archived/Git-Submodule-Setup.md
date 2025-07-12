This repository uses the Git submodules mechanism to include all the libraries needed to set up Rodan. Git submodules are essentially pointers to other Git repositories, and are specified in the `.gitmodules` file.

Cloning the submodules is necessary only if you wish to rebuild the Docker images. When using graphical Git clients such as GitHub Desktop or SourceTree, the submodules are usually automatically cloned for you. When cloning on the command line, run the following command after `git clone` to clone the submodules as well:

```shell
git submodule update --init
```
You may need to run `git submodule update --remote` to get the latest commit. 

When you update an upstream repository, e.g. `Rodan` or `rodan-client`, the changes will not be reflected in this repository (and hence, in the Docker images) until you pull the changes in. In order to pull a new version of Rodan, for example, run the following commands:

```shell
# Pull the submodule changes. The branch name must be specified explicitly.
cd rodan/code
git pull origin master
# Commit and push the changes to the parent repository (docker-rodan).
cd ../..
git add rodan/code
git commit -m "Update the rodan submodule"
git push
```
