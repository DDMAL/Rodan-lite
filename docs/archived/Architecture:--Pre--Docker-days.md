N.B. This is old documentation, from before Rodan was Dockerized. It is included here for the sake of completeness, and in case it is useful in future.

# Non-Docker Installation Instructions

Rodan runs on Linux distributions (Mac OS X and Windows are not tested). It can be deployed distributedly as Rodan web server, Rodan database, Rodan task queue, Rodan resource file server, and Rodan workers. The system architecture is shown below.

[[images/installation_1.png]]

There are separate installation instructions for each of these parts. Please note that it is not necessary to install them on separate machines - it is possible to combine two or more parts, and all the parts can even be installed on a single machine. 

* [[Quick setup: automated script]]
* Manual setup
  * [[Rodan task queue]]
  * [[Rodan database]]
  * [[Rodan resource file server]]
  * [[Rodan worker]]
    * [[Requirements for image processing jobs]]
  * [[Rodan web server]]
    * [[Diva.js image viewer support]]
* [[Start Rodan]]
