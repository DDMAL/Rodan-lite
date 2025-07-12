Rodan supports "export to JSON" and "import from JSON" for Workflows. The APIs are:

````
GET  /workflow/{ID}/?export=true&format=json   for exporting
POST /workflows/   with {'project': PROJ_ID, 'serialized': JSON_data} for importing
````

The JSON workflow should follow a defined schema [here](https://github.com/DDMAL/Rodan/blob/1.0.0-beta/rodan/serializers/workflow.py#L226). 