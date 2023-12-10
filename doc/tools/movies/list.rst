=======================
media.tools.movies.list
=======================

NAME
----

media.tools.movies.list - list movies in a repository

SYNOPSIS
--------

::

  python -m media.tools.movies.list.py [-h] [--mediapath MEDIAPATH] [--random RANDOM]
         [--group none|alphabetical|decade|genre]
         [--sort title|year|runtime]
         [--stats | --no-stats]

DESCRIPTION
-----------

Provides a list of all movies in a repository, one movie per line, along with the year the movie was created,
the runtime of the movie, the primary and secondary genres, and the specific description if it exists.

OPTIONS
-------

``--mediapath``
    Path to scan for media files

``--random [integer]``
    Instead of full output, present a random subset of data

``--group (none, alphabetical, decade, genre)``
    Divide all the output into groups, either alphabetically by title, by the decade the movie was created,
    or by the primary genre of the movie.

``--sort (title, year, runtime)``
    Sort all movies by the title, the year it was created, or the runtime.

``--stats/--no-stats``
    Print statistics covering the total number of movie in the repository


EXAMPLES
--------

Example 1: Print a sample list of movies, but also identify the size of the repository::

  $ python -m media.tools.movies.list --random 10 --stats

  Title                                              Year Runtime  Genre
  ================================================== ==== ======== ==================================================
  Christine                                          1983 1:50:01  [FICTION] Horror/Thriller
  Clerks III                                         2022 1:40:01  [FICTION] Comedy "Working Class Comedy"
  Foul Play                                          1978 1:55:58  [FICTION] Comedy/Romance/Mystery/Thriller "Mismatched Lovers Solve Mystery"
  Gone Baby Gone                                     2007 1:53:55  [FICTION] Mystery/Drama/Crime "Privaate Investigators"
  Inherit The Viper                                  2019 1:24:08  [FICTION] Drama/Thriller/Crime "Appalachia Dealers"
  The Man With The Golden Gun                        1974 2:05:13  [FICTION] Action/Adventure
  Missing                                            2023 1:50:42  [FICTION] Mystery/Thriller "Missing Mother"
  Murder By Death                                    1976 1:34:39  [FICTION] Comedy/Mystery
  Runaway                                            1984 1:39:59  [FICTION] Action/Sci-Fi "Malfunctioning Robot Hunter"
  Tower Of Terror                                    1997 1:29:01  [FICTION] Adventure/Comedy "Haunted Hotel Investigation"
  ================================================== ==== ======== ==================================================
    Movie count :   795
    Sample size :    10  ( 1.26%)



ENVIRONMENT VARIABLES
---------------------

``MEDIAPATH``
    The default path to the media repository if it isn't defined on the command line.

SEE ALSO
--------

media.tools.movies.show, media.tools.media.list
