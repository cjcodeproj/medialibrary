#!/usr/bin/env python

#
# Copyright 2022 Chris Josephes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

'''
Module to report on all named within a movie
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


class NameJobTitleMap():
    '''Crewname object that lists every job role in every title.
    '''
    def __init__(self, in_name, in_job, in_title):
        self.name = in_name
        self.jobs = {}
        self.jobs[in_job] = [in_title]

    def add_job_title(self, in_job, in_title):
        '''
        Add a job role and movie title to the name.
        '''
        if in_job in self.jobs:
            self.jobs[in_job].append(in_title)
        else:
            self.jobs[in_job] = [in_title]

    @classmethod
    def header(cls):
        '''
        Output a simple header.
        '''
        out = f"{'Family Name':20s} {'Given Name':15s} " + \
              f"{'Job':20s} {'Title':25s}\n" + \
              f"{'=' * 20} {'=' * 15} {'=' * 20} {'=' * 25}"
        return out

    def __str__(self):
        out = ''
        name_l = 1
        for job_i in sorted(self.jobs):
            job_l = 1
            for title_i in sorted(self.jobs[job_i]):
                if name_l == 1:
                    out = f"{self.name.family:20s} {self.name.given:15s} " + \
                          f"{job_i:20s} {title_i!s:25s}\n"
                else:
                    if job_l == 1:
                        out += f"{' ':36s} {job_i:20s} {title_i!s:25s}\n"
                    else:
                        out += f"{' ':57s} {title_i!s:25s}\n"
                job_l += 1
                name_l += 1
        return out

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __eq__(self, other):
        return self.name == other.name


def extract_from_list(in_dict, in_crew_job, in_job_title, in_movie_title):
    '''
    Extract the name of a crew member from a job array.
    '''
    for name_i in in_crew_job:
        if name_i in in_dict:
            in_dict[name_i].add_job_title(in_job_title, in_movie_title)
        else:
            in_dict[name_i] = NameJobTitleMap(name_i, in_job_title,
                                              in_movie_title)


def extract_role_from_list(in_dict, in_crew_roles,
                           in_job_title, in_movie_title):
    '''
    Extract the name of the actor from a role object.
    '''
    for name_i in in_crew_roles:
        if name_i.actor in in_dict:
            in_dict[name_i.actor].add_job_title(in_job_title, in_movie_title)
        else:
            in_dict[name_i.actor] = NameJobTitleMap(name_i.actor,
                                                    in_job_title,
                                                    in_movie_title)


def grab_crew_names(movies):
    '''
    Extract name objects from the arrays specific to
    the job functions.
    '''
    nm_dict = {}
    for movie in movies:
        if movie.crew is not None:
            if movie.crew.directors:
                extract_from_list(nm_dict, movie.crew.directors,
                                  'Director', movie.title)
            if movie.crew.writers:
                extract_from_list(nm_dict, movie.crew.writers,
                                  'Writer', movie.title)
            if movie.crew.cinemap:
                extract_from_list(nm_dict, movie.crew.cinemap,
                                  'Cinemaphotographer', movie.title)
            if movie.crew.editors:
                extract_from_list(nm_dict, movie.crew.editors,
                                  'Editor', movie.title)
            if movie.crew.cast:
                extract_role_from_list(nm_dict, movie.crew.cast.cast,
                                       'Cast', movie.title)
    return list(nm_dict.values())


def list_names(in_names):
    '''
    Generate output from the list of passed names.
    '''
    print(NameJobTitleMap.header())
    for name_i in sorted(in_names):
        print(name_i, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='show X names')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    all_names = grab_crew_names(all_movies)
    if args.random:
        rand_limit = args.random
        list_names(random_sample_list(all_names, rand_limit))
    else:
        list_names(all_names)
