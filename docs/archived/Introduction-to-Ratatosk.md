One of the more confusing aspects of the Rodan client/server API interaction is the role of the [Ratatosk Framework](http://github.com/wireload/Ratatosk) in the Cappuccino client. This Framework handles the bulk of the client-server interaction, and so this page will attempt to clarify just how this interaction works.

Both the Rodan client and server are based on the Model-View-Controller design pattern. (Django calls itself "Model-Template-View" [but it's the same thing](https://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names)).

To illustrate the interaction between the client and server, consider the process of creating a new Project using the Rodan client application. When the user creates a new Project in the client application, a new Objective-J object is created (via `[[Project alloc] init]`). Since we want this project to persist on the server side as well, we need to have some way of synchronizing both the client and server, creating server-side instances of the project when a client-side model is created. This is the function of Ratatosk.

In the Rodan client, the `Project` model extends the `WLRemoteObject` class from Ratatosk. This is the base object for models. On this model we implement two methods, `+remoteProperties` and `-remotePath`. Respectively, these methods provide the mapping between the client-side object fields and the server-side object fields, and the path to the server where the client-side object can map itself. Let's look at this closer.

Suppose we have the following Project model:

```objective-j
@implementation Project : WLRemoteObject
{
    CPString   pk           @accessors;
    CPString   projectName  @accessors;
}

+ (CPArray)remoteProperties
{
    return [
        ['pk', 'url'],
        ['projectName', 'name']
    ];
}

- (CPString)remotePath
{
    if ([self pk])
        return [self pk];
    else
        return @"/projects/";
}

@end
```

This simplified model illustrates a number of features:

* The `@accessors` provides automatic getters/setters. (See: [Synthesizing Accessor Methods](http://www.cappuccino-project.org/blog/2008/10/synthesizing-accessor-methods.html)). This is crucial for the Key/Value Observing design pattern to work.
* `+remoteProperties` provides a class method that maps the class variable name (position 0) with the remote variable name (position 1).
* The `-remotePath` method can return two values. The Primary Key of this object is the unique remote URL (e.g., `http://localhost:8000/project/12345/`). Only the server can assign this value, since it contains the canonical identifier for all objects. If, however, this object has *not* synchronized itself with the server, the `pk` value will not be set. In this case, we return the URL where this object can go to create itself. (If this doesn't make sense, you should consult the documentation on the [Rodan Server API](Rodan-Server-API), specifically about the `POST` method on the endpoints).

There are a few other methods that are defined on the `WLRemoteObject` that are necessary to explain:

* `+objectsFromJson` and `-initWithJson`. The former takes a JSON array of project objects from the server and returns an array of Objective-J `Project` objects, initialized with the mapping specified in `+remoteProperties`. The latter returns a single object of the same (`objectsFromJson` actually just iterates a list, calling `initWithJson` for each object).
* `ensure(Created|Saved|Deleted)`. Calling `[projectObject ensureCreated]` will initate a `POST` request to the server, ensuring that the object is saved on the server side. The `Saved` and `Deleted` variants do similar things, sending `PATCH` and `DELETE` methods, respectively.

So far we've covered creating a new object and syncing it with the server. This, however, is pretty simple. The real magic of Ratatosk happens when you update an object on the client side, and want the changes to be reflected on the server side. Ratatosk will manage the state of each object and, when something changes on that object (say, for example, you change the project name in the client interface), Ratatosk will automatically "kick off" a `PATCH` request to the server, ensuring that it is notified of the changes. Since this is handled transparently, the developer does not need to manually manage the request/response cycle for each object -- it is handled internally by Ratatosk itself.

## Transformers

In the `+remoteProperties` method, the sub-arrays describing the mapping may take a number of other arguments.  Here's the documentation for this method:

```objective-j
/*
 Specify object properties by implementing this class method on subclasses. The format is:

    [
        [<local property name> [, remote property name [, property transformer[, load only?]]]]
    ]

    If no remote property name is specified, the local property name is used as the remote property
    name.
*/
```

A `property transformer` is a class that will automatically deal with both forward-and-reverse serializing the server-side objects to client-side objects. Take, for example, the following mapping:

```objective-j
['pages', 'pages', [WLForeignObjectsTransformer forObjectClass:Page]],
```

In this instance, the `WLForeignObjectsTransformer` will automatically convert all objects in the `pages` array to client-side `Page` objects.

In another example:

```objective-j
['created', 'created', [[WLDateTransformer alloc] init], true]
```

This will automatically convert a string representing a Date object into an actual JavaScript Date object.

You can write your own transformers, but Ratatosk comes with a number of them built-in, in the `WLRemoteTransformers.j` file.
