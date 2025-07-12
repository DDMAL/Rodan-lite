If you are using [Diva.js](https://github.com/DDMAL/diva.js) for viewing images, Rodan needs Graphics Magick and Kakadu to convert images in background, and IIP Server to serve images.

### Graphics Magick

On ubuntu:

    $> sudo apt-get install graphicsmagick-imagemagick-compat

You should check out `convert` command, which should be from graphicsmagick, not imagemagick.

On Mac:

    $> brew install graphicsmagick

After `brew install`, open `rodan/settings.py`, modify

    BIN_CONVERT = None

to

    BIN_CONVERT = "/path/to/gm convert"

### Kakadu

If you have purchased Kakadu code, normally it should be good to follow `Compiling_Instructions.txt` to build the executables.

A special note for DDMAL's virtual machines: [[Compiler options for Kakadu v7.5]].

### vips

On ubuntu: `apt-get install libvips-tools`. On Mac, follow this page: [[Install VIPS on Mac OS X]].

### IIP Server

Follow the following instructions to install IIP server, with Kakadu support: https://github.com/ruven/iipsrv *Important: please always compile IIP server from source to link Kakadu libraries to it.*

To check installation, point the browser to `http://SERVER_NAME/fcgi-bin/iipsrv.fcgi`.