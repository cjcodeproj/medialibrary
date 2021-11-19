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
```

To run these tools use.

```
$ export MEDIAPATH=(path_to_xml_directory_structure)
$ python -m media.tools.movies.list
$ python -m media.tools.movies.show
$ python -m media.tools.movies.namelist
$ python -m media.tools.movies.keywordlist
# python -m media.tools.movies.castlist
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
python -m pip install --user medialibrary-0.1-py3-none-any.whl
```
