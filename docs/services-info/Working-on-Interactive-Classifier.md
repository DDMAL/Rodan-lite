The code for Interactive Classifier is contained in `rodan-main/code/rodan/jobs/interactive_classifier`.

To set up Interactive Classifier, you will need to be running Node v7 and have Python 2.7 installed.

### To use Node v7:

1. Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) if not yet installed
2. Run `nvm install 7` or `nvm use 7` if already installed

### To use Python 2.7:

1. Install [pyenv](https://github.com/pyenv/pyenv#installation) if not yet installed
2. Run `pyenv install 2.7`
3. Run `pyenv shell 2.7`

### Making Changes

Whenever you make changes to Interactive Classifier source code, the static files need to be recompiled.

1. `cd rodan-main/code/rodan/jobs/interactive_classifier/ic_frontend`
2. `npm install --python=python2.7`
3. `gulp`

### Merging Changes

Running `gulp` will generate documentation in `docs/` and output compiled `.js`, `.js.map`, and `.css` files in `static/`.

Make sure to rebase before merging changes so that changes are merged in the static files. When rebasing, resolve all merge conflicts in the source code, then run gulp to regenerate the static files.

There should be a better way to do this (see issue [#913](https://github.com/DDMAL/Rodan/issues/913)).
