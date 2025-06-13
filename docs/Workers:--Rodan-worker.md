If you are planning on creating a Rodan web server, make sure you visit that page first. This will set up Rodan worker. First, check out Rodan source, either by `git` (make sure to do a recursive clone for populating all submodules):

```
$> git clone --recursive https://github.com/DDMAL/Rodan.git
```

Following instructions will use `$RODAN_HOME` as the absolute path where you have checked out the Rodan source code.

#### Set up Python environment

Rodan is based on Python 2.7.x. Python 3 does not work with Rodan.

We recommend that all Python packages (see [requirements.txt](https://github.com/DDMAL/Rodan/blob/develop/requirements.txt)) should be installed inside a dedicated [virtual environment](http://virtualenv.readthedocs.org/en/latest/) for Rodan, because a virtual environment allows you to have multiple Python "environments" on the same machine:

```
$> sudo pip install virtualenv
$> cd $RODAN_HOME
$> virtualenv --no-site-packages rodan_env
```

(Note: from now on, we assume that we are in $RODAN_HOME.)

Then activate virtual environment:

```
$> source rodan_env/bin/activate
```

Note that your prompt looks like the following:

```
(rodan_env)$>
```

Whatever Python modules are installed from now on will only be available while in this virtual environment. (To exit your virtual environment, simply use the command `deactivate`.)

Then we install all Python packages. You may need system libraries before compiling some of them. On Ubuntu, perform:

```
(rodan_env)$> sudo apt-get install libpython-dev lib32ncurses5-dev:i386 libxml2-dev libxslt1-dev zlib1g-dev lib32z1-dev libjpeg-dev libpq-dev
```

If lib32z1-dev fails, you can download it from here [packages.ubuntu.com](https://packages.ubuntu.com/trusty/i386/libbz2-dev/download)

If it's still giving you trouble, install aptitude and double click the deb file.

```
sudo apt-get install aptitude
sudo apt-get -f install
sudo apt-get install aptitude
```

For other Linux distributions, please find corresponding names.

Install Python packages:

```
(rodan_env)$> pip install -r requirements.txt
(rodan_env)$> pip install Werkzeug
```

Mac users: if you get an error about not having a c compiler, try running:

```
export CC=gcc
```

The `readline` package is deprecated, try installing the `gnureadline` package (https://pypi.python.org/pypi/gnureadline)

If you get "error: use of undeclared identifier 'SOL_TCP'", go into requirements.txt and change the line
uWSGI==2.0.11.1 to uWSGI==2.0.15

Now, exit virtual environment by executing:

    (rodan_env)$> deactivate

#### Install NFS client (if NFS is configured. Skip if Mac user)

```
(rodan_env)$> apt-get install nfs-common inotify-tools
```

Create a folder for mounting NFS folder as `$RESOURCE_FOLDER_MOUNT_POINT`.

#### Configure Rodan source

For running the configuration, a SECRET_KEY is needed. To generate your SECRET_KEY, you can either use the code below or you can use any random combination of ascii characters:

```
import random, string
print 'SECRET_KEY={0}'.format(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(40)))
```

Install `autoconf` (Ubuntu: use `apt-get`, Mac: use `brew`). Change directory to Rodan source code directory, and run following commands (make sure the paths and names are correct for your setup):

```
$> autoconf
$> ./configure --enable-debug=no --enable-diva MODE="worker" \
       RODAN_VENV_DIR=/myapps/Rodan/rodan_env/ \
       RODAN_DATA_DIR=/myapps/Rodan/data \
       AMQP_HOST="localhost" AMQP_PORT="5672" AMQP_VHOST="rodan" \
       AMQP_USER="rodan" AMQP_PASSWORD="12345" \
       DB_HOST="localhost" DB_PORT="5432" \
       DB_NAME="rodan" DB_USER="rodan" DB_PASSWORD="12345" \
       DB_REDIS_PORT="6379" DB_REDIS_DBNUMBER=0 \
       WWW_USER="www-data" WWW_GROUP="www-data" \
       SECRET_KEY=@SECRET_KEY \                                # use the random SECRET_KEY from above
       --with-graphicsmagick-search-path="/myhome/bin/" \      # not required if not using some of native jobs
       --with-kdu_compress-search-path="/myhome/bin/" \        # not required if not using some of native jobs
       --with-xmllint-search-path="/myhome/bin/" \             # not required if not using some of native jobs
       --with-vips-search-path="/myhome/bin/"                  # not required if not using some of native jobs
```

`$WWW_USER` and `$WWW_GROUP` are the user and group that actually run the Rodan code. In a production environment, it is highly recommended to set up the dedicated account for limiting the permission of the application.

The configure script will output the command for altering the user and group for Rodan application and data directories, like follows:

```
$> sudo chgrp -R $WWW_GROUP $RODAN_HOME/*
$> sudo chown $WWW_USER:$WWW_GROUP $RESOURCE_FOLDER_MOUNT_POINT
```

In the settings.py file, replace the variables "@EMAIL_USERNAME@" and "@EMAIL_PASSWORD@" by either an email and password or an empty string. Replace the variable @MAX_PAGINATE_BY@ by 100. (This is to avoid getting a syntax error).

#### Next, follow the steps from Rodan Web Server, skipping the first configure step. Afterwards install Rodan Client to get the interface.

#### Install and configure supervisor (Optional)

We use [supervisor](http://supervisord.org/) to register Rodan as system services.

Install supervisor:

```
$> sudo apt-get install supervisor
```

Mac users:

```
brew install supervisor
```

Copy generated supervisor configurations:

```
$> cp $RODAN_HOME/etc/supervisor/conf.d/rodan.conf /etc/supervisor/conf.d/
```

#### Set up [[requirements for image processing jobs]] (optional if you do not intend to use Rodan for optical music recognition)
