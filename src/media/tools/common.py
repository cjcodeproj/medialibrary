#!/usr/bin/env python
'''Common routines for command line tools'''

import media.fileops.scanner
import media.fileops.loader
import media.fileops.repo
from media.fileops.filenames import FilenameMatches

# Walker module walks the filesystem
# Loader module reads in the discovered files


def load_media_dev(in_path):
    '''Identify suitable files and load them up'''
    repo = media.fileops.repo.Repo(in_path)
    repo.scan()
    loader = media.fileops.loader.Loader()
    m_devices = loader.load_media(repo, FilenameMatches.Movie_Media)
    return m_devices


def compile_movies(media_devices):
    '''Extract movies from devices'''
    movies = []
    for m_dev in media_devices:
        for movie in m_dev.contents:
            if movie not in movies:
                movies.append(movie)
    return movies
