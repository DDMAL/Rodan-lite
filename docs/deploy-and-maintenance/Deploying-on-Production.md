# Steps to deploy Rodan on Production with Healthy Git Workflow
1. _Create a new branch from develop, move to the branch, and rename it to `release-<version>`_. e.g. `release-v7.7.7`. This is to not block the development process. So during the process of preparing a new release, pull requests that are not in the release plan can still be merged into the development branch.
2. _Update text related to version everywhere._ On the release branch, update the `PROD_TAG` to the new version in Makefile and run 
```
old_tag=<the version prior to the new release> make update_prod_version_tag
```
This will update the version in `production.yml` and `rodan-main/code/rodan/__init__.py`. e.g. to move from `v7.7.6` to `v7.7.7`, do `old_tag=v7.7.6 make update_prod_version_tag`

3. _Make a new commit on changes made in step 2._ Put the commit message in this way:
```
Release v7.7.7

- <new feature one>
- <new feature two>
- ...
- <bug fix one>
- <bug fix two>
```
Be sure to include _**ALL changes**_ in this release.

4. _Add a git tag._ Use 
```
git tag -fa v7.7.7
``` 
to add a git tag to the new commit. You'll be requested to put messages on the tag you just added. Just copy-paste the commit messages you wrote in step 2.

5. _Push the commit _**AND THE TAG**_ to github._
6. _Setup a build rule on Docker Hub._ Go to the docker hub, and set up a build rule to build on the release branch. Put the release branch name (`release-v7.7.7`) in `Source` and `placeholder` in `Docker Tag` and click `Save and Build`. If you've tagged and named the release branch correctly, images are built and tagged as `v7.7.7`.
![Screen Shot 2023-06-02 at 1 05 16 PM](https://github.com/DDMAL/Rodan/assets/25975988/994dddcd-96c2-400e-b526-a1aa09312c71)


7. _Make pull requests to merge the release branch into `master` and `develop`._ After docker finishes building and pushing images, make pull requests to merge the release branch into the master _**and develop**_ branches.
8. _Pull the updated master branch on production server._ Once the pull request is approved and the release branch is in the master branch, go to production and do `git pull` on the master branch to keep updated with github.
9. _Deploy rodan on production server._ Do a series of makefile operations to deploy the new rodan on production server.
```
make stop
make clean
make pull_prod
make deploy_production
```
10. _Remove the release branch._ After the release branch is merged into _**BOTH**_ master and develop branches, delete the release branch. The release branch only exists when we're in the process of making a release. When a release is already on air, we remove the release branch.


