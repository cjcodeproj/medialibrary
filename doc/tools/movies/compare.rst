=======================
media.tools.movies.compare
=======================

NAME
----

media.tools.movies.compare - compare movies in a repository against each other

SYNOPSIS
--------

::

  $ python -m media.tools.movies.compare [-h] [--mediapath MEDIAPATH]

DESCRIPTION
-----------

Provides a summary of movies in a repository, with details on the story, keywords, the cast and crew involved.

OPTIONS
-------

``--mediapath``
    Path to scan for media files

EXAMPLES
--------

Example 1: Comparison operation::

  $ python -m media.tools.movies.compare

  ...
  Source Movie: White Sands (1992)
  =========================================================================================
  Movie                               Matches Score Trait              Value
  ----------------------------------- ------- ----- ------------------ --------------------
  A Time To Kill (1996)                     3    17 Cinemaphotographer Peter Menzies Jr.
                                                    Cast               Samuel L. Jackson
                                                    Cast               Beth Grant
  The Dark Wind (1991)                      2    13 Keyword            desert
                                                    Keyword            New Mexico
  Iron Man 2 (2010)                         2    10 Cast               Mickey Rourke
                                                    Cast               Samuel L. Jackson
  Pat Garrett & Billy The Kid (1973)        1     8 Keyword            New Mexico
  The Guilt Trip (2012)                     1     8 Keyword            New Mexico
  The Sum Of All Fears (2002)               1     8 Writer             Daniel Pyne
  Shooter (2007)                            1     7 Cinemaphotographer Peter Menzies Jr.
  Hard Rain (1998)                          1     7 Cinemaphotographer Peter Menzies Jr.
  Outrageous Fortune (1987)                 1     5 Keyword            desert
  Electra Glide In Blue (1973)              1     5 Keyword            desert
  8 Seconds (1994)                          1     5 Cast               James Rebhorn
  2 Guns (2013)                             1     5 Keyword            undercover
  Harper Valley P.T.A. (1978)               1     5 Cast               Royce D. Applegate
  Body Heat (1981)                          1     5 Cast               Mickey Rourke
  Burglar (1987)                            1     5 Keyword            briefcase
  Blood Simple (1983)                       1     5 Cast               M. Emmet Walsh
  Breakdown (1997)                          1     5 Keyword            desert
  Far From Home (1989)                      1     5 Keyword            desert
  Fool For Love (1985)                      1     5 Keyword            desert
  The Last Ride (2004)                      1     5 Keyword            undercover
  The Last Ride (1994)                      1     5 Cast               Mickey Rourke
  Lost Highway (1996)                       1     5 Cast               Jack Kehler
  Red Rock West (1992)                      1     5 Keyword            desert
  Raw Courage (1984)                        1     5 Cast               M. Emmet Walsh
  The Rainmaker (1997)                      1     5 Cast               Mickey Rourke
  Another Stakeout (1993)                   1     5 Keyword            undercover
  The Adventures Of Priscilla, Queen        1     5 Keyword            desert
  The Kill Room (2023)                      1     5 Cast               Samuel L. Jackson
  Knives Out (2019)                         1     5 Cast               M. Emmet Walsh
  Consenting Adults (1992)                  1     5 Cast               Mary Elizabeth Mastrantonio
  Carlito's Way (1993)                      1     5 Cast               James Rebhorn
  Inglorious Basterds (2009)                1     5 Cast               Samuel L. Jackson
  The Wizard (1989)                         1     5 Cast               Beth Grant
  Waterworld (1995)                         1     5 Cast               Jack Kehler
  The Wraith (1986)                         1     5 Keyword            desert
  Pulp Fiction (1994)                       1     5 Keyword            briefcase
  The Professionals (1966)                  1     5 Keyword            desert
  True Romance (1993)                       1     5 Cast               Samuel L. Jackson
  Goldstone (2016)                          1     5 Keyword            desert
  The Game (1997)                           1     5 Cast               James Rebhorn
  Grandview, U.S.A. (1984)                  1     5 Cast               M. Emmet Walsh
  Scarface (1983)                           1     5 Cast               Mary Elizabeth Mastrantonio
  Speed (1994)                              1     5 Cast               Beth Grant
  Steel Dawn (1987)                         1     5 Keyword            desert
  Stakeout (1987)                           1     5 Keyword            undercover
  Sunset (1988)                             1     5 Cast               M. Emmet Walsh
  Incredibles 2 (2018)                      1     5 Cast               Samuel L. Jackson
  Dune (2021)                               1     5 Keyword            desert
  Tremors (1990)                            1     5 Keyword            desert
  John Wick: Chapter 3 - Parabellum         1     5 Keyword            desert
  Avengers: Endgame (2019)                  1     5 Cast               Samuel L. Jackson
  Captain America: The First Avenger        1     5 Cast               Samuel L. Jackson
  The Avengers (2012)                       1     5 Cast               Samuel L. Jackson
  ...



ENVIRONMENT VARIABLES
---------------------

``MEDIAPATH``
    The default path to the media repository if it isn't defined on the command line.

SEE ALSO
--------

media.tools.movies.list
