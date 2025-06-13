Rodan uses VIPS to process JPEG images for the Diva.js image viewer. VIPS is a Python image manipulation library that's fast and memory efficient, especially on large images.

In order to install the VIPS Python bindings on a Mac, follow these steps:
1. Install VIPS via homebrew: `brew install vips`.
2. Link the Python bindings from `brew`'s `site-packages` folder into your own Python virtualenv by running the following command:
```
echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> `python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"`/homebrew.pth
```
3. Verify that it's been installed by opening a Python session in your virtual environment and running `import vipsCC`.
