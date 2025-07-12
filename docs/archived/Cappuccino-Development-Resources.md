The Cappuccino client application is a "first-class" citizen of the Rodan Server API and currently serves as the reference implementation.

Cappuccino is based on Cocoa, and is written in Objective-J, a strict superset of JavaScript. Objective-J is based on Objective-C, itself designed around Smalltalk-style object-oriented paradigms. (As opposed to the Simula-style used by C++, Python, Java, and other popular OO languages).

Cappuccino follows Cocoa quite closely; so much so that the documentation for Cocoa is often identical or similar to the same methods in Cappuccino. The following is a list of required and recommended reading on Objective-J, Cappuccino, and Cocoa Design patterns.

* [On Objective-J and Leaky Abstractions](http://www.cappuccino-project.org/blog/2008/12/on-leaky-abstractions-and-objective-j.html)
* [Cocoa Fundamentals](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CocoaFundamentals/Introduction/Introduction.html)
* [Cocoa to Cappuccino Fundamentals](http://www.slevenbits.com/blog/2012/10/cocoa-to-cappuccino.html)
* [Learning Objective-J](http://www.cappuccino-project.org/learn/objective-j.html)

This video demonstrates a specific upload framework, but it is also a great introduction to XCodeCapp.

* [Cup - Upload Framework](http://vimeo.com/66123997)

The Rodan client (as with most Cocoa/Cappuccino projects) makes extensive use of both the _Delegate_ and _Key-Value Observing_ patterns.

* [Cocoa Design Patterns](https://developer.apple.com/library/mac/#documentation/cocoa/conceptual/CocoaFundamentals/CocoaDesignPatterns/CocoaDesignPatterns.html)

There is a substantial implementation of many patterns for Cappuccino in the "Kitchen Sink" application:

* [Cappuccino Kitchen Sink](https://github.com/ahankinson/Cappuccino-Kitchen-Sink)

And a comprehensive tutorial illustrating many of the concepts used in Rodan:

* [Tutorial: A RESTful Table View](http://coltrane.music.mcgill.ca/tutorials/capptutorial1/)
