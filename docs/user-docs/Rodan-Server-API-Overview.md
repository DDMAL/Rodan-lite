Rodan provides a set of RESTful API built upon [Django REST framework](http://www.django-rest-framework.org/). Most endpoints accept JSON as HTTP request body, and return JSON as HTTP response body. In debug mode (`DEBUG=True` in settings), a browsable API is available. The browsable API, powered by Django REST framework, loads the response JSON into the HTML page, wraps HTTP requests (GET, POST, etc.) using forms and buttons, and provides detailed documentation for each view, for example:

[[images/browsable_api_example.png]]

The endpoints are defined in [`urls.py`](https://github.com/DDMAL/Rodan/blob/develop/rodan/urls.py), and are categorized into:

* API root
* Authentication
* List API
* Detail API
* Task queue API
* Interactive RunJob API
* Admin
* Websocket API

#### RESTful API conventions:

* Errors are returned to the user in the form of HTTP Status Codes. **DO NOT** return an error message with a non-error code. (i.e., do not return an error with a status code of HTTP 200 OK.)
* For non-validation errors, the error message will be put in a JSON object formatted as `{"detail": error_message}`. (The status code is 4XX.) Validation errors are returned as a JSON object containing all erroneous fields (see [here](https://github.com/DDMAL/Rodan/wiki/List-API#validation-errors)).
* Content type and return type are negotiated via HTTP Headers (`Accept: application/json`) or query parameters (appending `?format=json` to the URL).
