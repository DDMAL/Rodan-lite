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
