=======================
media.tools.movies.show
=======================

NAME
----

media.tools.movies.show - list movies in a repository

SYNOPSIS
--------

::

  $ python -m media.tools.movies.show [-h] [--mediapath MEDIAPATH] [--random RANDOM]
           [--group none|alphabetical|decade|genre]
           [--sort title|year|runtime]
           [--pagebreaks]

DESCRIPTION
-----------

Provides a summary of movies in a repository, with details on the story, keywords, the cast and crew involved.

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

``--pagebreaks``
    Add a simple ASCII page break after every entry.


EXAMPLES
--------

Example 1: Print a random sample of movies in full detail::

  $ python -m media.tools.movies.show --random 3

  Red Rock West                                                         (1992)
  ============================================================================
  [FICTION] Thriller/Drama "Mistaken Identity Thriller"
  (noir)

  Director: John Dahl
  Cinemaphotographer: Marc Reshovsky
  Cast: Nicholas Cage, J. T. Walsh, Lara Flynn Boyle, Dennis Hopper, Timothy
        Carhart, Dan Shor, Dwight Yoakam

  Plot
  A down on his luck oil field worker lookjing for a job is mistaken for a
  hired killer in a small town bar. Desperate for cash, he plays along until
  his conscious gets the better of him and he warns off the intended target.

  Keywords:
   bar, bar, Buick Riviera, buried money, Cadillac, cemetary, delivery truck,
   deputy, desert, Ford Bronco, gun, hospital, hotel, leg injury, murder for
   hire, rifle, sheriff, train, Wyoming, bank robbery, Marines, oil fields,
   ranch hand, Texas, western suit

  Rising Sun                                                            (1993)
  ============================================================================
  [FICTION] Action/Crime/Drama "Murder Investigation"
  (based on a book)

  Director: Philip Kaufman
  Cinemaphotographer: Michael Chapman
  Composer: Tôru Takemitsu

  Cast: Sean Connery, Wesley Snipes, Harvey Keitel, Cary-Hiroyuki Tagawa,
        Kebin Anderson, Mako, Ray Wise, Stan Egi, Stan Shaw, Tia Carrere, Seve
        Buscemi, Tatjana Patitz, Peter Crombie, Sam Lloyd, Daniel von Bargen,
        Lauren Robinson, Amy Hill, Tom Dahlgren, Clyde Kusatsu

  Plot
  Two Los Angeles cops must investigate the murder of a call girl in a
  Japanese high rise building, while navigating a twisty road of digital
  evidence, business deals, political corruption, and outside investigators
  tring to protect their own interests.

  Keywords:
   liason officer, Los Angeles (California), Los Angeles Police Department,
   police detective

  Witness                                                               (1985)
  ============================================================================
  [FICTION] Thriller/Drama/Romance "Undercover Cop"

  Director: Peter Weir
  Cinemaphotographer: John Seale
  Composer: Maurice Jarre

  Cast: Harrison Ford, Kelly McGillis, Josef Sommer, Lukas Hass, Jan Rubes,
        Alexander Godunov, Danny Glover, Brent Jennings, Patti LuPone, Angus
        MacInnes, Frederick Rolf, Viggo Mortensen

  Plot
  An amish boy witnesses an execution, and finds himself in the middle of a
  police coruption scandle. The lead detective must do everything to protect
  the boy and his mother from corrupt cops, including hiding out on an amish
  farm.

  Keywords:
   ambush, amish, Amtrack, barn raising, corrupt cops, cows, farm, grain silo,
   gun, knife, Lancaster (Pennsylvania), milking, pacifism, Philadelphia
   (Pennsylvania), police detective, protective custody, shotgun, suffocation,
   train station, witness protection



ENVIRONMENT VARIABLES
---------------------

``MEDIAPATH``
    The default path to the media repository if it isn't defined on the command line.

SEE ALSO
--------

media.tools.movies.list, media.tools.media.list
