#!/usr/bin/env python
'''
Module to report on all named within a movie
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import load_media_dev, compile_movies


class RTP():
    '''
    Simple pairing between a role object and a movie title object
    '''
    def __init__(self, role, title):
        self.role = role
        self.title = title

    def __lt__(self, other):
        return self.title < other.title

    def __rt__(self, other):
        return self.title > other.title

    def __eq__(self, other):
        return self.title == other.title


class RoleList():
    '''Build a structure of names and job roles'''
    def __init__(self):
        self.names = {}

    def add(self, role, title):
        '''Add a name, job role, and title to the list'''
        actor = role.actor
        if actor in self.names:
            self.names[actor].append(RTP(role, title))
        else:
            self.names[actor] = [RTP(role, title)]

    def output(self):
        '''Return the names, job roles, and titles'''
        print(f"{'Actor Name':30s} {'Movie Title':30s} " +
              f"{'Character Name':30s}")
        print(f"{'=' * 30} {'=' * 25} {'=' * 30}")
        for nam in sorted(self.names.keys()):
            n_count = 1
            for role in sorted(self.names[nam]):
                p_count = 1
                for portrays in role.role.portrays:
                    if n_count == 1:
                        print(f"{nam!s:30s} {role.title!s:30s} " +
                              f"{portrays.formal!s:s}")
                    else:
                        if p_count == 1:
                            print(f"{' ':30s} {role.title!s:30s} " +
                                  f"{portrays.formal!s:s}")
                        else:
                            print(f"{' ':30s} {' ':30s} {portrays.formal!s:s}")
                    p_count += 1
                    n_count += 1


def grab_cast_names(movies):
    '''Extract crew names from a movie'''
    role_list = RoleList()
    for movie in movies:
        if movie.crew is not None:
            if movie.crew.cast:
                for role in movie.crew.cast.cast:
                    role_list.add(role, movie.title)
    return role_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    names = grab_cast_names(all_movies)
    names.output()
