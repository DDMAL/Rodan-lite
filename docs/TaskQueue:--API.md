3 `GET`-only endpoints are provided for retrieving the information concerning Rodan workers:

* `/taskqueue/status/`: configuration and usage of all workers
* `/taskqueue/scheduled/`: scheduled tasks on all workers.
* `/taskqueue/active/`: the tasks being processed on all workers. 

These endpoints are only available to admin users, and are for monitoring the load and performance of Rodan workers.