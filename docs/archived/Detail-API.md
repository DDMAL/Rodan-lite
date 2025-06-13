Detail API requires the specific UUID of the object, and its endpoint uses singular noun, such as `/job/7938a064-736a-491b-9c96-20fe49e3b6c6/`. We use UUID in order to reduce the possibility of collisions and avoid serial database keys.

Detail API supports the following HTTP verbs:

* `GET`: retrieves all the fields of the object.
* `PATCH`: updates selected fields of the object (if the object is editable). `PUT` method has similar functionalities but Rodan favours `PATCH` method as `PUT` requires all fields while `PATCH` simply requires the fields that need to be updated. (*Note: the browsable API only allows `PUT`, not `PATCH`.*)
* `DELETE`: destroys the object (if the object is deletable). It returns 204 (NO CONTENT) if successful.

The `PATCH` request may return 400 (BAD REQUEST) if there are validation errors (see [[List API]]).

