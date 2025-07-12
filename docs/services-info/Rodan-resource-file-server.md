The Rodan resource file server is unnecessary if the web server and all workers are on the same machine (they can access the same path for resource files). If they are on different machines, however, it is necessary to set up the resource file server. NFS is not available on Mac.

The resource file server is based on NFS (Network File System) protocol. The server needs to enable following kernel modules:

````
$> modprobe nfs
$> modprobe nfsd
````

If there is any error reported, please consult your Linux distribution for the installation of these kernel modules.

Install NFS packages:

````
$> apt-get install nfs-common inotify-tools nfs-kernel-server runit
````

Create a local folder for storing Rodan resource files as `$RESOURCE_FILE_SERVER_LOCAL_FOLDER`. Then set up exported folder by adding following line to `/etc/exports` with replacing **each** of the subnets of Rodan server and workers:

````
$RESOURCE_FILE_SERVER_LOCAL_FOLDER $SUBNET_1(rw,sync,fsid=0,no_subtree_check,no_root_squash) $SUBNET_2(rw,sync,fsid=0,no_subtree_check,no_root_squash) ... $SUBNET_n(rw,sync,fsid=0,no_subtree_check,no_root_squash)
````

(Re)start NFS services:

````
$> service rpcbind start && service nfs-kernel-server start
````
