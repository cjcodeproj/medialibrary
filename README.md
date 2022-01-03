# Media Schema Reader

Code library for reading XML files using to the vtmedia schema.

The vtmedia schema is an XML schema for recording data on physical copies of media like CDs, or 
DVDs, and their contents.

## Executables/Demos

Thre are five demonstration proof of concept executables in the library.

```
media.tools.movies.list
media.tools.movies.show
media.tools.movies.namelist
media.tools.movies.keywordlist
media.tools.movies.castlist
media.tools.movies.genrebreakdown
```

To run these tools use.

```
$ export MEDIAPATH=(path_to_xml_directory_structure)
$ python -m media.tools.movies.list
$ python -m media.tools.movies.show
$ python -m media.tools.movies.namelist
$ python -m media.tools.movies.keywordlist
$ python -m media.tools.movies.castlist
$ python -m media.tools.movies.genrebreakdown
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

The easiest way to test is to download a copy of the vtmedia-schema repo and use the examples there.

## Python Shell Interface (Beta)

Pulling data using the Python Shell.

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
python -m pip install --user medialibrary-0.1-py3-none-any.whl
```
