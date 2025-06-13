First, follow all steps for [[Rodan worker]], **but before "Configure Rodan source", follow the steps in [[Diva.js image viewer support]], and set configuration parameters as follows**:

```
$> ./configure --enable-debug=no --enable-diva MODE="server" \
       RODAN_VENV_DIR=/myapps/Rodan/rodan_env/ \
       RODAN_DATA_DIR=/myapps/Rodan/data \
       AMQP_HOST="localhost" AMQP_PORT="5672" AMQP_VHOST="rodan" \
       AMQP_USER="rodan" AMQP_PASSWORD="12345" \
       DB_HOST="localhost" DB_PORT="5432" \
       DB_NAME="rodan" DB_USER="rodan" DB_PASSWORD="12345" \
       DB_USER_TEST="rodan" DB_PASSWORD_TEST="123456" \
       DB_REDIS_PORT="6379" DB_REDIS_DBNUMBER=0 \
       WWW_USER="www-data" WWW_GROUP="www-data" \
       DOMAIN_NAME="rodan.simssa.ca" \
       CLIENT_MAX_BODY_SIZE="200M" \
       SSL_CERT=/mycerts/server.crt \
       SSL_CERT_KEY=/mycerts/server.key \
       IIPSRV_FCGI=/srv/fcgi-bin/iipsrv.fcgi \                 # not required if --disable-diva
       --with-graphicsmagick-search-path="/myhome/bin/" \      # not required if --disable-diva
       --with-kdu_compress-search-path="/myhome/bin/" \        # not required if --disable-diva
       --with-xmllint-search-path="/myhome/bin/" \             # not required if --disable-diva
       --with-vips-search-path="/myhome/bin/"                  # not required if --disable-diva
```

#### Install and configure nginx

```
$> apt-get install nginx
$> rm /etc/nginx/sites-enabled/rodan
$> cp $RODAN_HOME/etc/nginx/sites-available/rodan /etc/nginx/sites-available
$> ln -s /etc/nginx/sites-available/rodan /etc/nginx/sites-enabled/rodan
```

#### Initialize database

Start PostgreSQL and Redis server (on Rodan database).

Activate virtual environment.

Then synchronize database and create superuser. The `migrate` command will prompt for a PostgreSQL superuser access: select `1`, and enter `$DB_SU_USER` and `$DB_SU_PASSWORD`.

`$DB_SU_USER` and `$DB_SU_PASSWORD` have to be created before hand in the PostgreSQL instance:

```
postgres=# create user `$DB_SU_USER` with password `$DB_SU_PASSWORD`;
postgres=# alter user `$DB_SU_USER` with superuser;
```

```
(rodan_env)$> python manage.py migrate
(rodan_env)$> python manage.py createsuperuser
```

#### Additional configuration for CORS (optional)

CORS functionality allows communication between Rodan and clients that are hosted on other domains. Configuring CORS support on the Rodan server involves configuring Django and your web server.

The configuration variable for `django_cors_headers` must be uncommented in `settings_production.py`. Only one of these requires changing - `CORS_ORIGIN_WHITELIST`. The others should be fine with the values in the set in the `settings_production.py.example`.

###### `CORS_ORIGIN_ALLOW_ALL`

Setting this to `True` will add `*` to the response header `Access-Control-Allow-Origin`. You should probably keep this as `False` and specify allowed origins in `CORS_ORIGIN_WHITELIST`.

###### `CORS_ORIGIN_WHITELIST`

This is a whitelist of origin IPs and/or domains that Django will allow access to. It is recommended to add entries here instead of setting `CORS_ORIGIN_ALLOW_ALL` to `True`.

###### `CORS_ALLOW_CREDENTIALS`

This tells Django whether to allow credential headers. Keep this set to `True`.

###### `CORS_EXPOSE_HEADERS`

This tells Django what headers to expose in responses. The headers `Set-Cookie` and `Vary` are all that is required.

###### CORS on nginx

The serving of Resources to the client/user is currently facilitated through nginx and not Django. Therefore, nginx needs to whitelist those client requests for Resource files that originate from different domains.

The following configuration should be placed in the `location /uploads` block of the nginx config. Note that this example allows all domains access; you will probably not want to do that (unsafe).

This was taken from https://michielkalkman.com/snippets/nginx-cors-open-configuration/.

```
     if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' '*';
        #
        # Om nom nom cookies
        #
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        #
        # Custom headers and headers various browsers *should* be OK with but aren't
        #
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        #
        # Tell client that this pre-flight info is valid for 20 days
        #
        add_header 'Access-Control-Max-Age' 1728000;
        add_header 'Content-Type' 'text/plain charset=UTF-8';
        add_header 'Content-Length' 0;
        return 204;
     }
     if ($request_method = 'POST') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
     }
     if ($request_method = 'GET') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
     }
```

#### Enable REST framework browsable API in debug mode (optional)

If you are using REST framework browsable API in production environment, you need to manually symlink static files:

    $> cd $RODAN_HOME/rodan/static/
    $> ln -s ../../rodan_env/lib/python2.7/site-packages/rest_framework/static/rest_framework/ rest_framework

#### Start Rodan in development mode (optional)

_Note: it is not recommended to run Rodan without any deployment servers in a production environment. You can skip this section if you have followed the deployment section._

1. Make sure rabbitmq-server is running with <code>rabbitmqctl status</code>; if it's not, running <code>rabbitmq-server</code> will start it.

2. And start Celery first because it will populate the initial Rodan jobs into the database:

   `(rodan_env)$> ./celery_start.sh`

3. Finally, start the server:

   `(rodan_env)$> python manage.py runserver`

   Note: you may use `runserver_plus` instead of `runserver`. This enables the Werkzeug debugger which is very powerful, but
   it conflicts with ws4redis, and may sometimes cause a blank screen to be displayed in rodan-client.

4. Open your browser and open `http://localhost:8000` to test your install.
