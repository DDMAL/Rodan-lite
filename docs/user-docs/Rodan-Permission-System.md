Rodan has project-level permission controls. Regarding a project, the users are categorized into four groups:

1. Project creator
2. Project admins
3. Project workers
4. Outsiders

All **creator**, **admins**, **workers** have full access to the objects belonging to this project, including `Workflow`, `WorkflowRun`, `Resource`, `WorkflowJob`, `InputPort`, `OutputPort`, `WorkflowJobCoordinateSet`, `Connection`, `RunJob`, `ResultsPackage`, `Input`, `Output`.

**Creator** can add/remove **admins** and **workers**. **Admins** can add/remove **workers**. **Creator** and **admins** can change the project name and description.

**Outsiders** of a project cannot access the project.

The implementation is based on [django-guardian](https://github.com/django-guardian/django-guardian). Upon creation of every project, two user `Group`s are created for **admins** and **workers**.

Object permissions are categorized into "view", "add", "change", and "delete", and are properly granted to these two Groups. For example, admin group has "view_project" and "change_project" permissions on its project, and worker group only has "view_project" permission. These permissions are assigned in `post_save` signals of Django models.

According to the definition of REST framework, if a user has no "view" permission, trying to retrieve its detail view will get 404 error (NOT FOUND), indicating that the object does not exist in the user's catalog. If the user has "view" permission but not others, the POST/PUT/DELETE/PATCH will return 403 (FORBIDDEN).

The REST generic views verify the permission by adding `rodan.permissions.CustomObjectPermissions` to permission classes. For list views, `rest_framework.filters.DjangoObjectPermissionsFilter` is added to filter classes by default in `settings.py`, so that a user can only retrieve the list of objects that the user has access to.

**Admins**/**workers** add/remove operation is implemented in two new views under `project-detail`:

````
/project/UUID/admins/
/project/UUID/workers/
````

### Caveat

The permission system has not yet prevented the creation of objects that link to non-accessible ones.
For example, if any authenticated user knows the UUID of a project, the user can send a POST request to create a workflow in that project. The POST request actually creates the object, but returns 404 indicating no permission. The user can neither retrieve the newly-created object in any way, but the object will appear for creator/admins/workers.
But this is fine in most cases as the user cannot guess the UUIDs, unless the user was one of admins/workers and was removed from a project.