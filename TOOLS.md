# Command Line Tools


The medialibrary module includes the following proof of concept tools which can 
be called directly from the command line.


```
media.tools.media.list
media.tools.media.show
media.tools.movies.list
media.tools.movies.show
media.tools.movies.namelist
media.tools.movies.keywordlist
media.tools.movies.castlist
media.tools.movies.genrebreakdown
media.tools.movies.timebuckets
media.tools.movies.debuglist
media.tools.movies.validate
```

Every program will scan a directory full of XML files containing media and movie
data.  Every identified file matching the correct naming convention will 
be read, and turned into a Python object structure.

## Invocation

Any of the above tools can be run with the following invocation.

```
$ export MEDIAPATH=(path_to_xml_directory_structure)
$ python -m media.tools.media.list
```

or 

```
$ python -m media.tools.media.list --mediapath (path_to_xml_directory_structure)
```

Every tool uses Python argparse for argument parsing, and provides a help option.


## Media Tools

```
media.tools.media.list
media.tools.media.show
```

The media tools report on data related to physical media.

### Media List

```
python -m media.tools.media.list \[--random (int)\] \[--mediapath (path)\]
```

Provides a list of physical media.

```
$ python -m media.tools.media.list --random 5
Title                                         Media Type Copies Date               
--------------------------------------------- ---------- ------ -------------------
3 Days Of The Condor                          Blu-Ray         1 2010-01-01 -> P3Y
Contact                                       Blu-Ray         1 2020-01-01 -> P1Y
Enron: The Smartest Guys In The Room          Blu-Ray         1 2021-01-11
Road House 2: Last Call                       DVD             1 
Unstoppable                                   Blu-Ray         2 2020-01-01
```

### Media Show

```
python -m media.tools.media.show \[--random (int)\] \[--mediapath (path)\]
```

Provides detailed descriptions of physical media.

```
$ python -m media.tools.media.show
48 Hrs.                                                       Blu-Ray
=====================================================================
Library > Instances

  ID Label Acquisition                    Date               
  -------- ------------------------------ -------------------
  UNDEF    Purchase 0.99                  2010-01-01 -> P2Y  

Product Id > Codes

   Barcode: 883929301737 (upc)

Product Specs > Inventory

  Case > Blu-Ray
  
Contents > Movies

  Title                                    Year Genre               
  ---------------------------------------- ---- --------------------
  48 Hrs.                                  1982 Action/Comedy       

```

## Movie Tools

```
media.tools.movies.list
media.tools.movies.show
media.tools.movies.namelist
media.tools.movies.keywordlist
media.tools.movies.castlist
media.tools.movies.genrebreakdown
media.tools.movies.timebuckets
media.tools.movies.debuglist
media.tools.movies.validate
```

### Movie List

```
python -m media.tools.movies.list \[--random (int)\] \[--mediapath (path)\] \[--sort (runtime|length)\]
```

Provide a list of movies found in the repository.

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

### Movie Show

```
python -m media.tools.movies.show \[--random (int)\] \[--mediapath (path)\] \[--sort (runtime|length)\]
```

Provides detailed descriptions of movies.

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

### Movie Namelist

```
python -m media.tools.movies.namelist \[--random (int)\] \[--mediapath (path)\]
```

Lists all crew and cast names associated with the movies.

```
python -m media.tools.movies.namelist
Family Name          Given Name      Job Role             Title
==================== =============== ==================== =========================
Abroms               Edward          Editor               The Sugarland Express
Alberti              Maryse          Cinemaphotographer   Enron: The Smartest Guys In The Room
Albertson            Sean            Editor               Killing Season
Alden Robinson       Phil            Director             Sneakers
Alden Robinson       Phil            Writer               Sneakers
Alexander            Jane            Cast                 All The President's Men
Apple                Cathering       Editor               Onward
Ashton               John            Cast                 Midnight Run
...
```

### Movie Keywords

```
python -m media.tools.movies.keywords \[--random (int)\] \[--mediapath (path)\]
```

List all keywords found in movies.

```
$ python -m media.tools.movies.keywordlist
Keyword                                       Title
============================================= =========================
properNoun/place/7-Eleven                     Wargames
generic/accountant                            Midnight Run
generic/affair                                Blood Simple
generic/air duct                              The Great Escape
properNoun/entity/Air Force                   Wargames
generic/alcohol                               Death Proof
generic/alien contact                         Contact
generic/alien invasion                        The Last Starfighter
generic/aliens                                The Last Starfighter
properNoun/thing/Allure                       Death Proof
properNoun/place/Amarillo (Texas)             Midnight Run
properNoun/entity/Amtrack                     Midnight Run
generic/anagram                               Sneakers
generic/answering machine                     Sneakers
...
```

### Movie Casts

```
python -m media.tools.movies.castlist \[--random (int)\] \[--mediapath (path)\]
```

List all actors found in movies.

```
$ python -m media.tools.movies.castlist --mediapath ~/xml/m/vtmedia-schema/examples/
Actor Name                     Movie Title                    Character Name                
============================== ========================= ==============================
Jane Alexander                 All The President's Men        'The Bookeeper'
John Ashton                    Midnight Run                   Marvin Dorfler
William Atherton               The Sugarland Express          Clovis
Richard Attenborough           The Great Escape               Squadron Leader Roger Bartlett 'The Big X'
Dan Aykroyd                    Sneakers                       Darryl 'Mother' Roscow
Martin Balsam                  All The President's Men        Howard Simons
Zöe Bell                       Death Proof                    Zöe Bell
Steve Bisley                   Mad Max                        Jim Goose
Kyle Bornheimer                Onward                         Wilden Lightfoot
Matthew Broderick              Wargames                       David
Charles Bronson                The Great Escape               Flight Lieutenant Danny Welinski 'Tunnel King'
Jake Busey                     Road House 2: Last Call        'Wild' Bill
Michael Chiklis                Parker                         Melander
James Coburn                   The Great Escape               Flying Officer Sedgwick 'The Manufacturer'
Dabney Coleman                 Wargames                       McKittrick
Barry Corbin                   Wargames                       General Beringer
Peter Coyote                   Enron: The Smartest Guys In The Room Narrator
Rosario Dawson                 Death Proof                    Abernathy
                               Unstoppable                    Connie
Robert De Niro                 Killing Season                 Benjamin Ford
                               Midnight Run                   Jack Walsh
...
```

### Movie Genres

```
python -m media.tools.movies.genrebreakdown \[--mediapath (path)\]
```

Provides a breakdown of every movie based their primary and secondary genres.

```
$ python -m media.tools.movies.genrebreakdown
...
                                                        <<< Primary Genres >>>

Primary Genre   Count Perc   Ratio                                              Sample Title
---------------  ----- ------ -------------------------------------------------- ---------------------------------------------
Action               8  34.8% -----------------                                  48 Hrs.
Adventure            3  13.0% ------                                             The Great Escape
Documentary          1   4.3% --                                                 Enron: The Smartest Guys In The Room
Drama                2   8.7% ----                                               All The President's Men
Horror               1   4.3% --                                                 Death Proof
Mystery              1   4.3% --                                                 Red Lights
Sci-Fi               3  13.0% ------                                             Contact
Thriller             4  17.4% --------                                           3 Days Of The Condor
---------------  ----- ------ -------------------------------------------------- ---------------------------------------------
Total movie count 23

                                                       <<< Secondary Genres >>>

Primary Genre: Action  (8 / 23)

Secondary Genre Count Perc   Ratio                                              Sample Title
--------------- ----- ------ -------------------------------------------------- ---------------------------------------------
Comedy              3  33.3% ----------------                                   48 Hrs.
Crime               2  22.2% -----------                                        Road House 2: Last Call
Drama               1  11.1% -----                                              Killing Season
Sci-Fi              1  11.1% -----                                              Mad Max
Thriller            2  22.2% -----------                                        Unstoppable
--------------- ----- ------ -------------------------------------------------- ---------------------------------------------
...
```

### Movie Runlengths

```
python -m media.tools.movies.timebuckets \[--mediapath (path)\]
```

Sumarize the runtime of every movie.

```
$ python -m media.tools.movies.timebuckets --buckets 5
Random Title                                       From     To       Count Perc   Ratio
-------------------------------------------------- -------- -------- ----- ------ --------------------------------------------------
Mad Max                                             1:26:01  1:43:28    10  43.5% ---------------------
Death Proof                                         1:43:28  2:00:55     8  34.8% -----------------
All The President's Men                             2:00:55  2:18:22     3  13.0% ------
Contact                                             2:18:22  2:35:49     1   4.3% --
The Great Escape                                    2:35:49  2:53:16     1   4.3% --
-------------------------------------------------- -------- -------- ----- ------ --------------------------------------------------
         Movie count : 23
Average film runtime : 1:51:49
 Median film runtime : 1:49:59  (The Sugarland Express)
     Interval Length : 0:17:27
        Bucket Count : 5
```

### Movie Debuglist 

```
python -m media.tools.movies.debuglist \[--mediapath (path)\]
```

Provides output useful for debugging the creation Python movie objects.  Internal tool.  Unsupported.

```
$ python -m media.tools.movies.debuglist
Title                               Year Sort Title                          Hash                 Object Address    
=================================== ==== ==================== ==================
All The President's Men             1976 all_the_presidents_men              -3106834757112910740 0xfffffc7fee37df60
Another 48 Hrs.                     1990 another_48_hrs                       6387184263348089960 0xfffffc7fee502fe0
Blood Simple                        1984 blood_simple                         1046538065311436375 0xfffffc7fee3e9b40
Chaos                               2005 chaos                                4753699084516088770 0xfffffc7fee5356f0

```

### Movie Validate

```
python -m media.tools.movies.validate \[--mediapath (path)\]
```

Examines movies and identifies missing or incomplete data.  Internal tool.  Unsupported.

```
$ python -m media.tools.movies.validate
Movie Title                                        Faults
-------------------------------------------------- -------------------------
Blood Simple                                       Plot has less than 20 words
Chaos                                              Plot missing
                                                   No copyright holder info
Enron: The Smartest Guys In The Room               Plot has less than 20 words
The Great Escape                                   Plot missing
```

## Python Shell Interface (Beta)

Pulling data using the Python Shell.

In this example, a repository object is created, which identifies every suitable XML file, and a
loader object, which is responsible for reading every suitable file and creating Media objects.

The objects are returned as an array, which can be accessed directly.

```
$ python
Python 3.9.7 (default, Sep  3 2021, 12:15:38) 
[GCC 10.2.0] on sunos5
Type "help", "copyright", "credits" or "license" for more information.
>>> import media.fileops.loader
>>> import media.fileops.repo
>>> r=media.fileops.repo.Repo('/home/user/xml/vtmedia-schema/examples/movies')
>>> r.scan()
>>> loader = media.fileops.loader.Loader()
>>> dev_list = loader.load_media(r)
>>> print(dev_list[0].contents[0].title)
Killing Season
>>> print(dev_list[0].contents[1].title)
Red Lights
>>> print(dev_list[1].contents[0].title)
All The President's Men
>>> print(dev_list[2].contents[0].title)
Unstoppable
>>> print(dev_list[3].contents[0].title)
Road House 2: Last Call
>>> print(dev_list[4].contents[0].title)
The Last Starfighter
>>> 
```
