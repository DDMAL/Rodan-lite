Both Rodan server and worker enforces all Jobs and ResourceTypes to be registered precisely in the database. Thus, upon startup, if Rodan finds a conflict between the code and the database of any Jobs or ResourceTypes, Rodan will throw a `ImproperlyConfigured` error indicating the problem and refuse to start. This is to ensure that all Rodan server and workers in a cluster have the same job packages.

A database migration is required at the server side whenever a Job or ResourceType is updated/added/deleted. It extends Django migration of models by adding a `post_migrate` signal in [`models/__init__.py`](https://github.com/DDMAL/Rodan/blob/develop/rodan/models/__init__.py#L36). In migration mode, Rodan sets a private flag (`settings._update_rodan_jobs == True`) and it tries to update the database whenever it finds a conflict. The migration trigger is `python manage.py migrate` in command-line.

The update and deletion (not addition) of Jobs and ResourceTypes always requires the confirmation of the server maintainer. For example, it would prompt:

````
The field `minimum` of Input Port Type `Feature Selection` of Job `gamera.custom.classification` seems to be updated: 
1
  -->
0

Confirm (y/N)? 
````

For the deletion of Jobs or ResourceTypes, Rodan may encounter problems because there are currently Resources, ResourceLists, or WorkflowJobs linked to them. Rodan will try deleting the foreign key-related instances after prompting the user.

