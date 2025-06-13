Rodan implements [token-based authentication](https://www.w3.org/2001/sw/Europe/events/foaf-galway/papers/fp/token_based_authentication/). A token is stored in the database in relation to every user account. To retrieve a user's token, you can send a request to the Rodan server with the username and password:

```shell
curl -v -XPOST -d username=$USERNAME -d password=$PASSWORD http://localhost:8000/auth/token/
```

This will respond with:

```shell
{"token": "655aff7dc865866fc9bd9e7fafb32bfeb484365a"}
```

This may then be used for requests to the Rodan server via the `Authorization` header. Most endpoints require this token as a proof of "logged-in". If the token is not provided, Rodan will return 401 (NOT AUTHENTICATED) as the status code.

```shell
curl -XGET -H "Authorization: Token 655aff7dc865866fc9bd9e7fafb32bfeb484365a" http://localhost:8000/projects/
```

Other authentication-related endpoints include:

* `/auth/me/`: display the current user information.
* `/auth/reset-token/`: log out the user (reset the user authentication token).
* `/auth/change-password/`: change password.
* `/auth/register/`: register.


Because the token is transferred as plain text in HTTP header, any Rodan deployment should use HTTPS protocol to encrypt the HTTP request.

#### HTTP Basic Authentication

This is the most basic and insecure way of authentication (example see [here](https://luckymarmot.com/paw/doc/auth/basic-auth)), and is **only** available in DEBUG mode for browsable API and admin. With `DEBUG=True`, your browser will ask for the username and password when Rodan returns 401. The session will be kept open unless the browser is restarted.
