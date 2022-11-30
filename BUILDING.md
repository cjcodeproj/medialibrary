# Media Library Reader -- Build Instructions

Instructions for working with the medialibrary source code.

## Download Source Code

```
$ cd code
$ git clone https://github.com/cjcodeproj/medialibrary.git
```

## Building

Assuming a normal Python 3 environment with setuptools and build modules installed:

```
$ cd medialibrary
$ python -m build 
```

The build will generate a dist/ directory with a .tar.gz file and a .whl file, suitable
for installing.  When ready to install, just use the PIP command as documented in the
README.md file.


## Unit Tests

Unit tests can be run as follows:
```
$ cd medialibrary
$ PYTHONPATH=src/ python -m unittest
```


## Code Cleanliness

### Source Module

All code is checked with pycodestyle and pylint before committed.

```
$ cd medialibrary/src
$ pycodestyle media
$ pylint media
```

### Unit Tests
```
$ cd medialibrary
$ pycodestyle test
$ PYTHONPATH=src/ pylint test
```
