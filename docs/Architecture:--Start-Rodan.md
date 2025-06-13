Note: to make sure that the services have the latest configuration, you may want to restart them if they have already been running (`service xxxx restart`).

#### Rodan task queue

Make sure that `rabbitmq-server` is running with `rabbitmqctl status`. If not, run:

````
$> service rabbitmq-server start
````

Open the port for RabbitMQ (typically 5672).

#### Rodan database

Make sure that PostgreSQL and Redis are running. If not, run:

````
$> service postgresql start
$> service redis-server start
````

Open the port for PostgreSQL (typically 5432) and Redis (typically 6379).

#### Rodan resource file server

Make sure that the following NFS-related services are running:

````
$> service rpcbind start
$> service nfs-kernel-server start
````

Open the ports for NFS-related services (typically 111/udp and 2049/tcp).

#### Rodan workers

**1**. Mount NFS folder:
 
````
$> service rpcbind start
$> mount -t nfs -o proto=tcp,port=2049 $RESOURCE_FILE_SERVER_IP:/ $RESOURCE_FOLDER_MOUNT_POINT
````

Try if the mounted folder works fine.

**2**. Start supervisor:

````
$> service supervisor start
````

Check `supervisorctl` for Rodan status.

Then, Rodan worker should be available.

#### Rodan server

Start nginx:

````
$> service nginx start
````

Then follow the steps for "Rodan workers". After that, open port 80.