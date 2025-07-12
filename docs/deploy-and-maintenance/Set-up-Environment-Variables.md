When deploying Rodan for staging or production, it is necessary to change certain values from their defaults in some of the configuration files for security and to ensure that the app can be accessed by a URL of your choosing. 

**Make sure to change the environment variables before bringing up the containers!** It is very important! A root user is created with these environment variables and we **do not** want people to guess these simple passwords.

### Django Environment Variables

In the `/scripts` folder you will find files containing environment variables. Edit one of `production.sample` or `staging.sample` and rename it to `production.env` or `staging.env`. (The `local.env` file is already set up properly for local development, so you should not ever have to touch it.) You can find examples of these on the actual staging and production servers. 

The things you will need to change are under `Django Configuration` and `SMTP Configuration`:

`Django Configuration`:
* `ADMIN_USER`: Set to the corresponding entry from the Accounts page on the DDMAL wiki.
* `ADMIN_EMAIL`: Set to the corresponding entry from the Accounts page on the DDMAL wiki.
* `ADMIN_PASSWORD`: Set to the corresponding entry from the Accounts page on the DDMAL wiki.
* `DJANGO_SECRET_KEY`: Set to the corresponding entry from the Accounts page on the DDMAL wiki.
* `IIPSRV_URL`: Needs to be modified to match the URL from which you will access this Rodan App. For example, if you have reserved the URL `https://rodan-test.simssa.ca` then this should be set to `http://rodan-test.simssa.ca/fcgi-bin/iipsrv.fcgi/`.

`SMTP Configuration`:
* `EMAIL_HOST`: Set to the corresponding entry from the AWS Email section of the Resources page on the DDMAL wiki.
* `EMAIL_PORT`: Set to the corresponding entry from the AWS Email section of the Resources page on the DDMAL wiki.
* `EMAIL_HOST_USER`: Set to the corresponding entry from the AWS Email section of the Resources page on the DDMAL wiki.
* `EMAIL_HOST_PASSWORD`: Set to the corresponding entry from the AWS Email section of the Resources page on the DDMAL wiki.

## Edit .yml Files

You will also need to change one of two `.yml` files in the root directory of the repository: `production.yml` or `staging.yml`. Change the `SERVER_HOST` entry in all places that it appears to be the URL that you have reserved for this deployment of Rodan.