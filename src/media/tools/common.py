#!/usr/bin/env python
'''Common routines for command line tools'''

import media.fileops.scanner
import media.fileops.loader
from media.fileops.filenames import FilenameMatches

# Walker module walks the filesystem
# Loader module reads in the discovered files


def load_media_dev(in_path):
    '''Identify suitable files and load them up'''
    walker = media.fileops.scanner.Walker([in_path])
    walker.filename_match(FilenameMatches.Movie_Media)
    walker.scan()
    mload = media.fileops.loader.Loader(walker)
    mload.load_media()
    media_devices = mload.medialist
    return media_devices


def compile_movies(media_devices):
    '''Extract movies from devices'''
    movies = []
    for m_dev in media_devices:
        for movie in m_dev.contents:
            if movie not in movies:
                movies.append(movie)
    return movies
