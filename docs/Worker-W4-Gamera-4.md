## Background

[Gamera-4](https://github.com/hsnr-gamera/gamera-4) is a framework for building document analysis applications. Rodan uses Gamera for multiple document analyses, such as binarization jobs, connected components analysis, image conversion jobs, and staff finding jobs.

Before Summer 2022, Rodan used [Gamera 3](https://github.com/hsnr-gamera/gamera-3) from our own [fork](https://github.com/DDMAL/gamera_rodan) which only supported Python2 and has been deprecated. Since the migration in July 2022, we have moved to Gamera 4 for Python3, which contained several bugs and issues that were specific to our jobs.

We then decided to fix and install Gamera-4 from our own fork [ddmal/gamera4-rodan](https://github.com/DDMAL/gamera4-rodan). For more information on the differences between our fork and the official Gamera-4 repository, visit this [page](https://github.com/DDMAL/gamera4-rodan/wiki/Differences-with-the-official-package)

## Installation on Rodan

`Rodan/python3-celery/Dockerfile` specifies the Gamera image used (see [here](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/python3-celery/Dockerfile#L29)). For more information on how to build and manage the image and tags, refer to this [page](https://github.com/DDMAL/gamera4-rodan/wiki/Docker-builds).

## MusicStaves Toolkit

The [MusicStaves Toolkit](https://gamera.informatik.hsnr.de/addons/musicstaves/index.html) is one of Gamera's additional packages for document analysis problems that are too specific to be included in the core distribution.
Rodan specifically uses MusicStaves for [Heuristic Pitch Finding](https://github.com/DDMAL/Rodan/blob/master/rodan-main/code/rodan/jobs/heuristic_pitch_finding/StaffFinding.py), [Miyao Staff Finder and Roach-Tatem Remove Staff Lines](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/toolkits/music_staves) jobs.

As of August 2023, there is no official support for Gamera-4 with the MusicStaves toolkit (i.e. MusicStaves is still in Python2). Since then we have made small fixes (mostly integers-floats-bytes type conversion) on [gamera4-rodan/musicstaves](https://github.com/DDMAL/gamera4-rodan/tree/main/musicstaves) in order to keep using the package with Gamera4 in Python3.

MusicStaves Toolkit is built and installed [here](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/python3-celery/Dockerfile#L70C1-L74C1).

## Resource Types

Gamera introduces 2 resource types that are handled in Rodan: `application/gamera-polygons+txt` and `application/gamera+xml`.
