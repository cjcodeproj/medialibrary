==========================
media.tools.media.validate
==========================

NAME
----

media.tools.media.validate - examine records in a repository for completeness

SYNOPSIS
--------

::

  python -m media.tools.media.validate [-h] [--mediapath MEDIAPATH]
          [--level 1|2|3|4|5 ]
          [--filter passing|failed|none]
          [--random RANDOM]
          [--list/--no-list]
          [--details/--no-details]
          [--stats]

DESCRIPTION
-----------

Examines all of the data in a given repository for completeness, accuracy, or possible inconsistencies by running
a series of tests, based on what kind of media it is.

OPTIONS
-------

``-h|--help``
    Print command usage information.

``--mediapath``
    Path to scan for media files.

``--level [integer 1-5]``
    All diagnostic tests are divided into five levels, based on the intensity of the testing.

    The default test level is 5, which is considered the bare minimum tests required to ensure the
    data is usable.  Every level from 4 down to 1 is designed to be a more detailed test that ensures
    the data is complete, but it also adds time to the testing run.

``--filter passing|failed|none``
    Filters output to either show only records that have passed with a perfect score, or records that have failed
    at least one test.  The ``none`` argument is the default and allows either record to be output.

``--random [integer]``
    Outputs only a random sampling of records.

``--list/--no-list``
    Provide output as a list, with one piece of media per line.

``--details/--no-details``
    Provide a detailed output record for each piece of media, listing every score, and faults detected.

``--stats``
    Show output statistics at the end of the program run, including total scores, and program runtime.

EXAMPLES
--------

Example 1: Show a quick overview of all media.::

  $ python -m media.tools.media.validate --stats

  Media                                    Type       Score      Run/Skip Pass/Fail Faults
  ---------------------------------------- ---------- ---------- -------- --------- ------
  Zootopia                                 Ultra HD    10.0/10.0  14    3   14    0      0
  Spider-Man: No Way Home                  Ultra HD    10.0/10.0  14    3   14    0      0
  The Killer Elite                         Ultra HD     9.7/10.0  14    3   13    1      1
  Urban Cowboy (40th Anniversary Edition)  Blu-Ray      9.3/10.0  15    2   14    1      1
  Vertigo                                  Blu-Ray     10.0/10.0  14    3   14    0      0

                       Entire Set Sample Set
                       ---------- ----------
  Total Media:                781          5
  Passed:                     294          3
  Failed:                     487          2

  Overall Percentage:      37.64%     60.00%

   Program Start Time : 2023-12-10 10:58:58.624746
     Program End Time : 2023-12-10 10:59:00.240080
           Duration   : 0:00:01.615334



Example 2: Show the full details of all validation testing against two pieces of media.::

  $ python -m media.tools.media.validate --level 4 --details --random 2

  Media                                    Type       Score      Run/Skip Pass/Fail Faults
  ---------------------------------------- ---------- ---------- -------- --------- ------
  Explorers (Collector's Edition)          Blu-Ray      9.2/10.0  17    0   15    2      2
  White Sands                              DVD         10.0/10.0  14    3   14    0      0

  ========================================================================
  Explorers (Collector's Edition)                                  Blu-Ray
  ========================================================================

                             Score : 9.2/10.0
                         Tests Run : 17
                     Tests Skipped : 0
                            Passed : 15
                            Failed : 2


  No   Test                                     Result  Score Max   Faults
  ---- ---------------------------------------- ------- ----- ----- ------
     1 media.title                              Pass        5     5      0
     2 media.title.main                         Pass        5     5      0
     3 media.title.main.value                   Pass        5     5      0
     4 media.title.edition                      Pass        5     5      0
     5 media.title.edition.value                Pass        5     5      0
     6 media.title.main.whitespace              Pass        5     5      0
     7 media.title.edition.whitespace           Pass        5     5      0

  Content: Explorers                                               (Movie)
  ------------------------------------------------------------------------

  No   Test                                     Result  Score Max   Faults
  ---- ---------------------------------------- ------- ----- ----- ------
     1 generic.catalog                          Pass        5     5      0
     2 generic.catalog.copyright                Pass        5     5      0
     3 generic.catalog.copyright.year           Pass        5     5      0
     4 generic.catalog.copyright.holders        Fail        0     5      1
     5 generic.story.plot                       Pass        5     5      0
     6 generic.story.plot.whitesapce            Pass        5     5      0
     7 generic.story.plot.length                Pass        5     5      0
     8 genericv.technical.runtime               Pass        5     5      0
     9 genericv.technical.runtime.value         Fail        3     5      1
    10 movie.technical.runtime.value            Pass        5     5      0

                           <<< FAULTS >>>

  Test                                     Level      Message
  ---------------------------------------- ---------- --------------------
  generic.catalog.copyright.holders        NOTICE     No copyright holders
  genericv.technical.runtime.value         NOTICE     Suspicious runtime value (1h1m1s)


  ========================================================================
  White Sands                                                          DVD
  ========================================================================

                             Score : 10.0/10.0
                         Tests Run : 14
                     Tests Skipped : 3
                            Passed : 14
                            Failed : 0


  No   Test                                     Result  Score Max   Faults
  ---- ---------------------------------------- ------- ----- ----- ------
     1 media.title                              Pass        5     5      0
     2 media.title.main                         Pass        5     5      0
     3 media.title.main.value                   Pass        5     5      0
     4 media.title.edition                      Skipped     -     -      -
     5 media.title.edition.value                Skipped     -     -      -
     6 media.title.main.whitespace              Pass        5     5      0
     7 media.title.edition.whitespace           Skipped     -     -      -

  Content: White Sands                                             (Movie)
  ------------------------------------------------------------------------

  No   Test                                     Result  Score Max   Faults
  ---- ---------------------------------------- ------- ----- ----- ------
     1 generic.catalog                          Pass        5     5      0
     2 generic.catalog.copyright                Pass        5     5      0
     3 generic.catalog.copyright.year           Pass        5     5      0
     4 generic.catalog.copyright.holders        Pass        5     5      0
     5 generic.story.plot                       Pass        5     5      0
     6 generic.story.plot.whitesapce            Pass        5     5      0
     7 generic.story.plot.length                Pass        5     5      0
     8 genericv.technical.runtime               Pass        5     5      0
     9 genericv.technical.runtime.value         Pass        5     5      0
    10 movie.technical.runtime.value            Pass        5     5      0


ENVIRONMENT VARIABLES
---------------------

``MEDIAPATH``
    The default path to the media repository if it isn't defined on the command line.
