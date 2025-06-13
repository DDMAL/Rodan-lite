The API Root `/` returns a JSON object that contains:

* `routes`: lists the URLs to all the endpoints.

````
    "routes": {
        "connections": "http://localhost:8000/connections/",
        "resultspackages": "http://localhost:8000/resultspackages/",
        "resourcelists": "http://localhost:8000/resourcelists/",
        "workflowjobs": "http://localhost:8000/workflowjobs/",
        "auth-reset-token": "http://localhost:8000/auth/reset-token/",
        "taskqueue-status": "http://localhost:8000/taskqueue/status/",
        "auth-change-password": "http://localhost:8000/auth/change-password/",
        "workflowruns": "http://localhost:8000/workflowruns/",
        ...
````

* `configuration`: provides the versions of Rodan job packages, and other global configurations such as the number of objects in every page.

````
    "configuration": {
        "job_packages": {
            "rodan.jobs.conversion": "1.0.0-alpha",
            "rodan.jobs.gamera": "1.0.0-alpha",
            "rodan.jobs.pil": "1.0.0-alpha"
        },
        "page_length": 20
    }
````

* `version`: provides the version of Rodan core system.

````
    "version": "1.0.0-alpha"
````