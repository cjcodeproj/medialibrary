# Media Schema Reader

Code library for reading XML files using to the vtmedia schema.

The vtmedia schema is an XML schema for recording data on physical copies of media like CDs, or 
DVDs, and their contents.

## Executables/Demos

Thre are two demonstration executables in the library.

```
media.tools.listmovies
media.tools.showmovies
```

To run these tools use.

```
$ export MEDIAPATH=(path_to_xml_directory_structure)
$ python -m media.tools.movies.list
$ python -m media.tools.movies.show
$ python -m media.tools.movies.namelist
```

```
$ python -m media.tools.movies.list
Title                                              Year Genre                                             
================================================== ==== ==================================================
2010                                               1984 [FICTION] Sci-Fi "Space Exploration Adventure"    
All The President's Men                            1976 [FICTION] Drama/Mystery "Newspaper Mystery"       
Contact                                            1997 [FICTION] Sci-Fi/Drama "Alien Contact"            
Death Proof                                        2017 [FICTION] Horror/Thriller "Car Action"            
...
```

```
$ python -m media.tools.movies.show
...
All The President's Men                                               (1976)
============================================================================
[FICTION] Drama/Mystery "Newspaper Mystery"
(based on a true story, based on a book)

Director: Alan Pakula
Cinemaphotographer: Gordon Willis
Cast: Dustin Hoffman, Robert Redford, Jack Warden, Martin Balsam, Hal
      Holbrook, Jason Robards, Jane Alexander

Plot
Two news reporters investigate the Watergate burglary and discover a
conspiracy leading all the way to the President Of The United States.

Keywords:
 Charles Colson, CIA, Clark McGregor, Department Of Justice, Donald
 Segretti, FBI, Hugh Sloan, investigative journalism, journalism, Ken
 Clawson, Library Of Congress, Mark Felt, newspaper, parking garage, Richard
 Nixon, Richard Nixon, scandal, taxi cabs, The Washington Post, Watergate
 Conspiracy, Watergate Hotel, White House

...
```

```
$ python -m media.tools.movies.namelist
Family Name          Given Name      Job Roles           
==================== =============== ====================
Abroms               Edward          Editor
Alberti              Maryse          Cinemaphotographer
Albertson            Sean            Editor
Alden Robinson       Phil            Director
Alexander            Jane            Cast
Apple                Cathering       Editor
Ashton               John            Cast
...
```

The easiest way to test is to download a copy of the vtmedia-schema repo and use the examples there.

## Building

Assuming a normal Python 3 environment with setuptools and build modules installed:

```
cd medialibrary
python -m build 
```

Command will generate a dist/ directory with a .tar.gz file and a .whl file.

## Installing

Assuming a normal Python 3 environment:

```
python -m install --user medialibrary-0.1-py3-none-any.whl
```
