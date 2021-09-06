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
$ python -m media.tools.listmovies
$ python -m media.tools.showmovies
```

The easiest way to test is to download a copy of the vtmedia-schema repo and use the examples there.
