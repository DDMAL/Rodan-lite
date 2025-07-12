# Rodan API Overview

> Courtesy of ChatGPT
>
> I'm not sure if this document is still relevant (@notkaramel, 250617). I'm suspecting that this refers to the old "Rodan web server" where Rodan used to have an API layer for interactions.

## Root API

The root endpoint `/` returns a JSON object containing the following keys:

### `routes`

A dictionary listing all available API endpoints.

```json
"routes": {
    "connections": "http://localhost:8000/connections/",
    "resultspackages": "http://localhost:8000/resultspackages/",
    "resourcelists": "http://localhost:8000/resourcelists/",
    "workflowjobs": "http://localhost:8000/workflowjobs/",
    "auth-reset-token": "http://localhost:8000/auth/reset-token/",
    "taskqueue-status": "http://localhost:8000/taskqueue/status/",
    "auth-change-password": "http://localhost:8000/auth/change-password/",
    "workflowruns": "http://localhost:8000/workflowruns/"
    // ...
}
```

### `configuration`

Provides version information for Rodan job packages and other global settings, such as the pagination limit.

```json
"configuration": {
    "job_packages": {
        "rodan.jobs.conversion": "1.0.0-alpha",
        "rodan.jobs.gamera": "1.0.0-alpha",
        "rodan.jobs.pil": "1.0.0-alpha"
    },
    "page_length": 20
}
```

### `version`

Indicates the version of the Rodan core system.

```json
"version": "1.0.0-alpha"
```

---

## Taskqueue API

There are three `GET`-only endpoints for monitoring the Rodan workers:

- `/taskqueue/status/`: Shows configuration and usage statistics for all workers.
- `/taskqueue/scheduled/`: Lists scheduled tasks across all workers.
- `/taskqueue/active/`: Displays tasks currently being processed by workers.

**Note:** These endpoints are restricted to admin users and are intended for performance monitoring and diagnostics.

---

## Detail API

Detail API requires the specific UUID of the object, and its endpoint uses singular noun, such as `/job/7938a064-736a-491b-9c96-20fe49e3b6c6/`. We use UUID in order to reduce the possibility of collisions and avoid serial database keys.

Detail API supports the following HTTP verbs:

- `GET`: retrieves all the fields of the object.
- `PATCH`: updates selected fields of the object (if the object is editable). `PUT` method has similar functionalities but Rodan favours `PATCH` method as `PUT` requires all fields while `PATCH` simply requires the fields that need to be updated. (_Note: the browsable API only allows `PUT`, not `PATCH`._)
- `DELETE`: destroys the object (if the object is deletable). It returns 204 (NO CONTENT) if successful.

The `PATCH` request may return 400 (BAD REQUEST) if there are validation errors (see [[List API]]).

---
## List API
List API uses plural nouns such as `http://localhost:8000/projects/`, and support 3 HTTP verbs: `GET`, `POST`, and `OPTIONS`.

- `GET`: returns a page of objects. It supports ordering and filtering.
- `POST`: creates a new object. It is only enabled if the user has permission to create a new object in this category. It validates the provided fields, and it returns 201 (CREATED) if the validation passes, or 400 (BAD REQUEST) if the validation fails.
- `OPTIONS`: returns possible parameters for `GET` and `POST`.

#### Pagination

The `GET` request performs pagination by default, and results in following format:

```
{
    "count": [Integer],
    "next": [URL],
    "previous": [URL],
    "current_page": [Integer],
    "total_pages": [Integer],
    "results": [List of objects]
}
```

- `count`: the total number of objects.
- `next` and `previous`: the URL to the next or previous page. They could be `null` if current page is the first or last page.
- `current_page`: the current page number.
- `total_pages`: the number of pages in total.
- `results`: the actual objects. The number is in Rodan global settings and is provided in [[API root]].

#### Ordering and filtering

Ordering and filtering are applied by appending query parameters in `GET` request. Passing in `ordering=$FIELD_NAME` will apply an ascending order to all the results, and `ordering=-$FIELD_NAME` a descending order. For filtering, passing in `$FIELD_NAME__$FIELD_LOOKUP_TYPE=$VALUE` will apply the functionality that resembles [Django queryset filtering](https://docs.djangoproject.com/en/1.8/ref/models/querysets/#field-lookups), for example, `/jobs/?name__icontains=grayscale`.

Not all fields can be ordered or filtered against, and not all field lookup types are supported for filterable fields. The supported ones are retrievable through `OPTIONS` request. An example result could be:

```
{
    "filter_fields": {
        "updated": [
            "lt",
            "gt"
        ],
        "name": [
            "exact",
            "icontains"
        ],
        ...
    },
    "ordering_fields": [
        "updated",
        "group",
        "name",
        ...
    ],
    ...
}
```

#### Validation Errors

If the `POST` request does not pass the validation, Rodan will return an object that contains all validation errors that are assigned into corresponding field names, such as:

```
{
    'workflow': ['This field is required.'],
    'status': ['Can only create a WorkflowRun that requests processing.']
}
```

Note: the validation errors are always quoted in a list. It allows multiple errors on one field.

For complex objects, for example, the POSTed object of the WorkflowRun creation view:

```
{
    'workflow': 'http://testserver/workflow/00000000-1111-2222-3333-444444444444/',
    'resource_assignments': {
        'http://testserver/inputport/00000000-0000-0000-0000-000000000000/': [
            'http://testserver/resource/00000000-0000-0000-0000-000000000000/',
            'http://testserver/resource/00000000-0000-0000-0000-000000000001/',
            'http://testserver/resource/00000000-0000-0000-0000-000000000002/',
            'http://testserver/resource/00000000-0000-0000-0000-000000000003/'
        ],
        'http://testserver/inputport/11111111-0000-0000-0000-000000000000/': [
            'http://testserver/resource/11111111-0000-0000-0000-000000000000/',
            'http://testserver/resource/11111111-0000-0000-0000-000000000001/'
        ],
        'http://localhost:8000/inputport/22222222-0000-0000-0000-000000000000/': [
            'http://testserver/resource/22222222-0000-0000-0000-000000000000/',
            'http://testserver/resource/22222222-0000-0000-0000-000000000001/',
            'http://testserver/resource/22222222-0000-0000-0000-000000000002/'
        ]
    }
}
```

The validation errors are positioned by nested objects and array indices. For example:

```
{
    'resource_assignments': {
        'http://testserver/inputport/00000000-0000-0000-0000-000000000000/': {
            1: ['Resource is not in the project of Workflow']
        }
    }
}
```

... indicates an error with `'http://testserver/resource/00000000-0000-0000-0000-000000000001/'`.

---
## Interactive RunJob API
The interactive RunJob API provides an interface for user to work with Rodan. There are two APIs for this functionality:

````
/interactive/RunJob_UUID/acquire/
/interactive/RunJob_UUID/Token/(sub URL)
````

The idea behind is that the user has to acquire a "lock" before they start working on an interactive RunJob. This is done through the first API (`acquire`). The acquisition, if successful, only ensures a certain seconds of the user's lock, and thus the Rodan client has to extend the lock before the previous one expires. The `acquire` API, if successful, returns a token and expiry time.

Using the token, the user then accesses the second API to retrieve the interactive interface. Rodan supports sub-URLs for sub interfaces and Ajax purposes. At last, the user sends a POST to store the result of the interactive RunJob.

A recommended client UX design is to load the interactive interface as an `<iframe>` while keeping `POSTing` the `acquire` API in the background.

[[images/client_interactive_runjob_interface.png]]

You may also be interested in the following class, written by Andrew Fogarty for the Interactive Classifier (https://github.com/DDMAL/Interactive-Classifier). Please note that it requires jQuery and is written in ECMAScript 6.

```
import $ from "jquery";

/**
 * This class maintains a `runjob.working_user_expiry` Rodan token throughout its lifetime.
 *
 * For more information, see {@link https://github.com/DDMAL/Interactive-Classifier/wiki/Token-Authentication}.
 */
export default class Authenticator {

    /**
     * Grabs the authentication URL from the page URL and sets the timeout
     * to 5000 miliseconds.
     */
    constructor()
    {
        // This will be the URL that we hit to authenticate.
        this._authUrl = Authenticator.getAuthUrl();
        // Authenticate every few seconds
        this._time = 5000;
    }

    /**
     * Start authenticating on an interval.
     */
    startTimedAuthentication()
    {
        var that = this;
        this._timer = setInterval(function ()
        {
            that.authenticate();
        }, this._time);
    }

    /**
     * Authenticate with the server then save the working POST url for when
     * we will submit to the server later.
     */
    authenticate()
    {
        var that = this;
        $.ajax({
            url: this._authUrl,
            type: 'POST',
            headers: {
                Accept: "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8"
            },
            complete: function (response)
            {
                var responseData = JSON.parse(response.responseText);
                // Save the working url
                that._workingUrl = responseData["working_url"];
            }
        });
    }

    /**
     * Get the working POST url for the Interactive Job.  This is the URL that
     * we make a post request to when we want to complete the interactive
     * portion of the interactive job.
     *
     * @returns {string} - The "working" URL on the server for the job.
     */
    getWorkingUrl()
    {
        return this._workingUrl;
    }

    /**
     * Get the authentication url.
     *
     * @returns {string} - The authentication URL.
     */
    static getAuthUrl()
    {
        return window.location.href.split("/").slice(0, -2).join("/") + "/acquire/";
    }
}
```

---
## asdf
