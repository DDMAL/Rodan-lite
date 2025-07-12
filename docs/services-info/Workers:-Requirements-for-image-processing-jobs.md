Rodan is designed to be modular. If you hope to use the image processing jobs, however, several additional dependencies are required.

### Install Gamera

Currently, Rodan comes configured with support for the [Gamera](http://gamera.informatik.hsnr.de) toolkit. You should download the source code and, ensuring you are still within your Rodan virtual environment, run the install.  (We assume that you downloaded the gamera source to `$HOME/gamera`.)

    (rodan_env)$> cd $HOME/gamera

If installing on Mac OSX Mavericks, you may have to do the following if you see a compile error:

    (rodan_env)$> export CFLAGS="-stdlib=libstdc++ -mmacosx-version-min=10.6"

Build then install.

    (rodan_env)$> python setup.py install --nowx

This command installs Gamera without the GUI, since we are only interested in the Gamera image processing modules. Once you have installed this, you can install a number of optional Gamera modules.

* [Musicstaves toolkit](http://gamera.informatik.hsnr.de/addons/musicstaves/) contains a number of functions for working with printed music scores.
* [Document Preprocessing Toolkits](http://github.com/DDMAL/document-preprocessing-toolkit) are four modules that offer some further document processing functionality.
* [Rodan plugins module](http://github.com/DDMAL/rodan_plugins) is a set of Gamera plugins that replace built-in Gamera modules to allow them to operate with input/output, rather than modifying an image in-place.

You will want to download these to your $HOME directory and install each individually. In the case of the [Document Preprocessing Toolkits](http://github.com/DDMAL/document-preprocessing-toolkit), there are four separate modules within the toolkit directory.  Install each individually, making sure to install the `lyric_extraction` toolkit LAST (as it depends on the other three modules), but ignore matlab completely.

Each module needs to know where the Gamera include files exist in order to build, so you will have to define an include path when installing.  For example, when installing the `rodan_plugins', you would do the following:

    (rodan_env)$> cd $HOME/rodan_plugins
    (rodan_env)$> CFLAGS="-I/$HOME/gamera/include" python setup.py install

If compilation fails on Mac OSX Mavericks, try using:

    (rodan_env)$> CFLAGS="-stdlib=libstdc++ -mmacosx-version-min=10.6 -I/$HOME/gamera/include" python setup.py install

which assumes that Gamera was installed in `$HOME/gamera/'.  The install line above should work with all modules.

### LibMEI

Check out the master branch of https://github.com/DDMAL/libmei to download the LibMEI suite.

Go to `$LIBMEI_SOURCE/tools` and execute:

    (rodan_env)$> python parseschema2.py -o src -l cpp $RODAN_HOME/helper_scripts/neumes_and_layout_compiled.xml
    (rodan_env)$> python parseschema2.py -o src -l python $RODAN_HOME/helper_scripts/neumes_and_layout_compiled.xml
    (rodan_env)$> rm -rf ../src/modules/*
    (rodan_env)$> rm -rf ../python/pymei/Modules/*
    (rodan_env)$> mv src/cpp/* ../src/modules/
    (rodan_env)$> mv src/python/* ../python/pymei/Modules/

Then, follow the instructions on https://github.com/DDMAL/libmei/wiki/Compiling-and-Installing to compile and install the customized LibMEI, and follow https://github.com/DDMAL/libmei/wiki/Installing-the-Python-bindings to install the Python bindings (remember to stay in rodan_env).

## xmllint

Neon.js job needs xmllint executable. If it is not installed in `$PATH`, modify `$RODAN_HOME/rodan/settings.py` as the path to xmllint executable.