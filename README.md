# Media Library Reader

The `medialibrary` module is a Python module for reading files containing entertainment media
data adhering to the vtmedia schema; which is an XML schema that records details on movies
and other works of art.

```
$ python -m media.tools.movies.list --sort runtime --random 5 --stats --mediapath ~/xml/movies
Title                                              Year Runtime  Genre                                             
================================================== ==== ======== ==================================================
Total Excess: How Carolco Changed Hollywood        2020  0:59:00 [NONFICTION] Documentary "Hollywood Tell-All"     
The Big Easy                                       1986  1:40:29 [FICTION] Drama/Comedy/Crime "Murder Investigation"
Klute                                              1971  1:54:10 [FICTION] Mystery/Thriller "Witness Protection"   
Air Force One                                      1997  2:04:36 [FICTION] Action/Thriller "President Plane Thriller"
The Hot Spot                                       1990  2:10:21 [FICTION] Drama/Thriller/Romance "Con Artist Scheming"
================================================== ==== ======== ==================================================
  Movie count :   545
  Sample size :     5  ( 0.92%)
```

The following repositories contain the XMLSchema definition and a sample dataset for testing the
code.


| Repository | Purpose |
| --- | --- |
| [vtmedia-schema](https://github.com/cjcodeproj/vtmedia-schema) | Schema and XML validation for media data |
| [mediadata](https://github.com/cjcodeproj/mediadata) | A large dataset of sample media/movie data |


Neither of these are required for module operation, but they both contain sample data and documentation on
how to build your own files.


## Package Distribution

[![PyPi version](https://img.shields.io/pypi/v/medialibrary)](https://pypi.org/project/medialibrary/)

## Installing

Installaiton of the module wheel file.

```
$ python -m pip install --user medialibrary
```

### Quick Start

Once you have the software installed, and you have a repository (either your own, or something you downloaded), you can
immediately start using the software.

```
$ export MEDIAPATH=~/xml/mediafiles
$ python -m media.tools.movies.list
```


## Building

See the BUILDING.md file in the source code distribution.
