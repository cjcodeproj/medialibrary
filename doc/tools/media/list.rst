======================
media.tools.media.list
======================

NAME
----

media.tools.media.list - list physical media in a repository

SYNOPSIS
--------

::

  python -m media.tools.media.list [-h] [--mediapath MEDIAPATH] [--random RANDOM]
         [--group none|alphabetical|decade|genre]
         [--sort title|year|runtime]
         [--stats | --no-stats]

DESCRIPTION
-----------

Provides a list of all physical media in repository, including the title, the format of the media, and the
acquisition date, if any.

OPTIONS
-------

``--mediapath``
    Path to scan for media files

``--random [integer]``
    Instead of full output, present a random subset of data


EXAMPLES
--------

Example 1: Print a sample list of physical media.::

  $ python -m media.tools.media.list --random 10


  Title                                         Media Type Copies Date
  --------------------------------------------- ---------- ------ -------------------
  The Big Chill                                 Blu-Ray         1
  Fall                                          Blu-Ray         1
  Happy, Texas                                  DVD             1
  Jagged Edge                                   Blu-Ray         1
  Presumed Innocent / Frantic                   Blu-Ray         1
  Red Dawn                                      DVD             1
  Sonic The Hedgehog 2                          Ultra HD        1
  The Sting                                     Ultra HD        1
  Streets Of Fire                               Ultra HD        1
  Top Gun                                       Ultra HD        1


ENVIRONMENT VARIABLES
---------------------

``MEDIAPATH``
    The default path to the media repository if it isn't defined on the command line.

SEE ALSO
--------

media.tools.media.validate
