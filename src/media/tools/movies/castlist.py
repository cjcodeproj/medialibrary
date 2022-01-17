#!/usr/bin/env python
'''
Module to report on all named within a movie
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


class ActorRoleMap():
    '''
    Align an actor with all of their roles
    '''
    def __init__(self, in_role, in_title):
        self.name = in_role.actor
        self.titles = {}
        self.titles[in_title] = in_role.portrays

    def add_title(self, in_role, in_title):
        '''
        Add title and role data to the entry.
        '''
        if in_title in self.titles:
            self.titles[in_title].extend(in_role.portrays)
        else:
            self.titles[in_title] = in_role.portrays

    @classmethod
    def header(cls):
        '''
        Generate a report header/
        '''
        out = f"{'Actor Name':30s} {'Title':30s} {'Portrays':30s}\n" + \
              f"{'=' * 30} {'=' * 30} {'=' * 30}\n"
        return out

    def __str__(self):
        out = ''
        name_c = 1
        for title in sorted(self.titles):
            title_c = 1
            for portrays in self.titles[title]:
                if name_c == 1:
                    out += f"{self.name!s:30s} {title!s:30s} " + \
                           f"{portrays.formal!s:30s}\n"
                else:
                    if title_c == 1:
                        out += f"{' ':30s} {title!s:30s} " + \
                               f"{portrays.formal!s:30s}\n"
                    else:
                        out += f"{' ':30s} {' ':30s} {portrays.formal!s:30s}\n"
                name_c += 1
                title_c += 1
        return out

    def __lt__(self, other):
        return self.name < other.name

    def __rt__(self, other):
        return self.name > other.name

    def __eq__(self, other):
        return self.name == other.name


def grab_cast_names(in_movies):
    '''
    Extract cast names from movies.
    '''
    ca_dict = {}
    for movie in in_movies:
        if movie.crew is not None:
            if movie.crew.cast:
                for role in movie.crew.cast.cast:
                    if role.actor in ca_dict:
                        ca_dict[role.actor].add_title(role, movie.title)
                    else:
                        ca_dict[role.actor] = ActorRoleMap(role, movie.title)
    return list(ca_dict.values())


def list_names(in_names):
    '''
    Output all of the passed names.
    '''
    print(ActorRoleMap.header(), end='')
    for nm_i in sorted(in_names):
        print(nm_i, end='')


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
    names = grab_cast_names(all_movies)
    if args.random:
        rand_limit = args.random
        list_names(random_sample_list(names, rand_limit))
    else:
        list_names(names)
