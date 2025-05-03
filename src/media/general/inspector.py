#!/usr/bin/env python

#
# Copyright 2025 Chris Josephes
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

'''Code suitable for ad-hoc inspections of a media object.'''

import random
from media.data.media import Media
from media.data.media.contents.movie import Movie
from media.data.media.contents.audio.album import Album


class Inspector():
    '''
    A class to provide short details on a media object.
    '''
    def __init__(self):
        pass

    def inspect(self, in_media):
        '''
        Return information about a media object.
        '''
        out = ''
        if not issubclass(in_media.__class__, Media):
            return 'Not a media object.'
        out += "=" * 35 + "\n"
        out += "Media object confirmed.\n"
        out += f"Media Title: {in_media.title!s}\n"
        out += self._inspect_library(in_media)
        out += self._inspect_contents(in_media)
        out += "=" * 35 + "\n"
        return out

    def _inspect_library(self, in_media):
        out = ''
        if in_media.library:
            if len(in_media.library.instances) > 0:
                out += f"Instance count: {len(in_media.library.instances)}\n"
            else:
                out += "No instances.\n"
        return out

    def _inspect_contents(self, in_media):
        out = ''
        if len(in_media.contents) > 0:
            out += f"Total content objects: {len(in_media.contents)}\n"
            for con in in_media.contents:
                if issubclass(con.__class__, Movie):
                    out += self._inspect_con_movie(con)
                elif issubclass(con.__class__, Album):
                    out += self._inspect_con_album(con)
        return out

    def _inspect_con_movie(self, in_con):
        out = "\nMovie Object Found\n"
        if in_con.title:
            out += f"    Title: {in_con.title}\n"
        if in_con.crew:
            if in_con.crew.cast.cast:
                act_count = len(in_con.crew.cast.cast)
                out += f"    Actor Count: {act_count}\n"
                out += f"    First Actor: {in_con.crew.cast.cast[0].actor}\n"
        return out

    def _inspect_con_album(self, in_con):
        out = "Album Object Found\n"
        art_str = ""
        if in_con.title:
            out += f"    Title: {in_con.title}\n"
        if in_con.catalog:
            if in_con.catalog.artists:
                for art_i in in_con.catalog.artists:
                    art_str += str(art_i) + " "
        if art_str:
            out += f"    Artists: {art_str}\n"
        out += f"    Element Count: {len(in_con.elements)}\n"
        return out

    @classmethod
    def rand_media(cls, in_matches):
        '''
        Return a random media object from a small list.
        '''
        r_num = random.randint(0, len(in_matches)-1)
        return in_matches[r_num]

    def find_random_album(self, in_repo):
        '''
        Find a media object that contains at least
        one album.
        '''
        matches = []
        for media in in_repo.media:
            if len(media.contents) > 0:
                for medcon in media.contents:
                    if issubclass(medcon.__class__, Album):
                        matches.append(media)
                        break
        return Inspector.rand_media(matches)

    def find_random_movie(self, in_repo):
        '''
        Find a media object that contains at least
        one movie.
        '''
        matches = []
        for media in in_repo.media:
            if len(media.contents) > 0:
                for medcon in media.contents:
                    if issubclass(medcon.__class__, Movie):
                        matches.append(media)
                        break
        return Inspector.rand_media(matches)
