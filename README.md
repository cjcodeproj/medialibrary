# Media Library Reader

The `medialibrary` module is a Python module for reading XML files containing entertainment media
data adhering to the vtmedia schema.


| Repository | Purpose |
| --- | --- |
| [vtmedia-schema](https://github.com/cjcodeproj/vtmedia-schema) | Schema and XML validation for media data |
| [mediadata](https://github.com/cjcodeproj/mediadata) | A large dataset of sample media/movie data |


Neither of the repositories are required for operation of this module, but they provide a
good source of sample data.

## Building

Assuming a normal Python 3 environment with setuptools and build modules installed:

```
cd medialibrary
python -m build 
```

The build will generate a dist/ directory with a .tar.gz file and a .whl file, suitable
for installing.

## Installing

Installaiton of the module wheel file.

```
python -m pip install --user medialibrary-0.1-py3-none-any.whl
```


## Unit Tests

Unit tests can be run as follows:
```
cd medialibrary
PYTHONPATH=src/ python -m unittest
```


## Code Cleanliness

### Source Module

All code is checked with pycodestyle and pylint before committed.

```
cd medialibrary/src
pycodestyle media
pylint media
```

### Unit Tests
```
cd medialibrary
pycodestyle test
PYTHONPATH=src/ pylint test
```
