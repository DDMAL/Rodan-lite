# Introduction

The production server only uses tagged versions of images created for Rodan staging. Since staging gets updated quite frequently, 
it's important to have a way of testing these tagged images in a thorough way. While they wouldn't be tagged in the first place unless
they worked on the staging server, extensive testing locally can never hurt. 

# The Process

Testing prod is quite similar to testing `nightly` builds. Make sure you have Docker Engine running, execute `make pull_prod` and then `make test_prod`. Even though `test_prod` will automatically run the pull command, it's good to first get the images in a separate command lest there be issues. 

Unlike `docker-compose.yml` for testing nightly builds and `arm-compose.yml` for ARM based machines, `test_prod` uses the `test-prod-compose.yml` file, where the tags can be seen for various images. Modifying these tags would allow you to test out different versions, assuming the `.yml` file would still be compatible. 

After `make test_prod` is executed, the same process as the normal `make run` command needs to be followed with various `docker compose exec` instances. More can be read [here](https://github.com/DDMAL/Rodan/wiki/Working-on-Rodan).