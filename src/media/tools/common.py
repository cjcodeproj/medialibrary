#!/usr/bin/env python
'''Common routines for command line tools'''

import random
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


def random_sample_list(in_list, rand_limit):
    '''
    Take a large list, and turn it into a random sample.
    '''
    total = len(in_list)-1
    if rand_limit > len(in_list):
        rand_limit = len(in_list)
    slots = []
    out = []
    while len(slots) <= rand_limit-1:
        r_num = random.randint(0, total)
        if r_num not in slots:
            slots.append(r_num)
    for slot_i in slots:
        out.append(in_list[slot_i])
    return out
