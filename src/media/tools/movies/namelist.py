#!/usr/bin/env python
'''
Module to report on all named within a movie
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import load_media_dev, compile_movies


class NameList():
    '''Build a structure of names and job roles'''
    def __init__(self):
        self.names = {}

    def add(self, name, job_role, title):
        '''Add a name, job role, and title to the list'''
        if name in self.names:
            if job_role in self.names[name]:
                self.names[name][job_role].append(title)
            else:
                self.names[name][job_role] = [title]
        else:
            self.names[name] = {}
            self.names[name][job_role] = [title]

    def output(self):
        '''Return the names, job roles, and titles'''
        print(f"{'Family Name':20s} {'Given Name':15s} " +
              f"{'Job Role':20s} {'Title'}")
        print(f"{'=' * 20} {'=' * 15} {'=' * 20} {'=' * 25}")
        for nam in sorted(self.names.keys()):
            for j_role in sorted(self.names[nam].keys()):
                t_count = 1
                for title in sorted(self.names[nam][j_role]):
                    if t_count == 1:
                        print(f"{nam.family:20s} {nam.given:15s} " +
                              f"{j_role:20s} {title!s}")
                    else:
                        print(f"{' ':20s} {' ':15s} {j_role:20s} {title!s}")
                    t_count += 1


def grab_crew_names(movies):
    '''Extract crew names from a movie'''
    name_list = NameList()
    for movie in movies:
        if movie.crew is not None:
            if movie.crew.directors:
                for dir_n in movie.crew.directors:
                    name_list.add(dir_n, "Director", movie.title)
            if movie.crew.writers:
                for writ_n in movie.crew.writers:
                    name_list.add(writ_n, "Writer", movie.title)
            if movie.crew.cinemap:
                for cinemap_n in movie.crew.cinemap:
                    name_list.add(cinemap_n, "Cinemaphotographer", movie.title)
            if movie.crew.editors:
                for editor_n in movie.crew.editors:
                    name_list.add(editor_n, "Editor", movie.title)
            if movie.crew.cast:
                for role in movie.crew.cast.cast:
                    name_list.add(role.actor, "Cast", movie.title)
    return name_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    names = grab_crew_names(all_movies)
    names.output()
