#!/usr/bin/env python

#
# Copyright 2024 Chris Josephes
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
Standard text format reports for audio albums.
'''

from datetime import timedelta


class OneLiner():
    '''
    Format for a single line summary of an album.
    '''
    def __init__(self, in_album):
        self.album = in_album
        self.output = ""
        self.build()

    def build(self):
        """
        Construct a one-line summary of an album.
        """
        y_string = build_copyright_year(self.album)
        runtime = build_runtime(self.album)
        genre = build_genre_classification(self.album)
        artist = build_artist_string(self.album)
        self.output = f"{self.album.title!s:40s} " + \
                      f"{y_string:4s} " + \
                      f"{artist:20s} " + \
                      f"{runtime:8s} " + \
                      f"{genre:s}\n"

    def __str__(self):
        return self.output

    @classmethod
    def header_fields(cls):
        """
        Return header titles for column output.
        """
        out = f"{'Title':40s} " + \
              f"{'Year':4s} " + \
              f"{'Artist':20s} " + \
              f"{'Runtime':8s} " + \
              f"{'Genre':20s}\n" + \
              cls.header_line()
        return out

    @classmethod
    def header_line(cls):
        """
        Return a simple line to go under the header fields.
        """
        return f"{'=' * 40} {'=' * 4} {'=' * 20} {'=' * 8} {'=' * 20}\n"


def build_artist_string(in_album):
    '''
    Build a string of artist names.
    '''
    o_string = ''
    for art_o in in_album.catalog.artists:
        art_s = str(art_o)
        o_string += art_s + ", "
    o_string = o_string[:-2]
    return o_string


def build_genre_classification(in_album):
    '''
    Build a text classification string.
    '''
    o_string = ''
    classification = in_album.classification
    if classification.genres:
        if classification.genres.primary:
            o_string = f"{classification.genres.primary}"
            if classification.genres.secondary:
                o_string += '/' + '/'.join(classification.genres.secondary)
    if classification.soundtrack:
        if not o_string:
            o_string = 'Soundtrack'
    return o_string


def build_runtime(in_album):
    '''
    Construct a presentable version of the runtime value.

    The string hack to remove the microseconds came from a
    SO posting.
    '''
    runtime = timedelta(seconds=0)
    if in_album.technical.runtime:
        runtime = in_album.technical.runtime
    return str(runtime).split('.', maxsplit=1)[0]


def build_copyright_year(in_album):
    '''
    Construct a printable version of the copyright year.
    '''
    year_s = "0000"
    if in_album.catalog:
        if in_album.catalog.copyright:
            year_s = f"{in_album.catalog.copyright.year:4d}"
    return year_s
