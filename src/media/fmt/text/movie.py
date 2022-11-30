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
Standard text format reports for movies.
'''

from datetime import timedelta
from media.fmt.text.basics import hdr_list, hdr_list_np, hdr_text, hdr_block

# Note: The field limit for movie titles should probably be 45.


class List():
    '''Formatting a listing of movies, one per line.'''
    def __init__(self, in_movie):
        self.movie = in_movie
        self._prep_fields()
        self.output = self.mentry()

    @classmethod
    def list_header(cls):
        '''Generate a simple header'''
        out = f"{'Title':50s} {'Year':4s} {'Runtime':8s} {'Genre':50s}\n" + \
              cls.list_header_line()
        return out

    @classmethod
    def list_header_line(cls):
        """
        Generate a text line to separate headers vs rows.
        """
        return f"{'=' * 50} {'=' * 4} {'=' * 8} {'=' * 50}"

    def _prep_fields(self):
        self.title_key = self.movie.unique_key
        self.runtime = timedelta(seconds=0)
        if self.movie.technical:
            if self.movie.technical.runtime:
                self.runtime = self.movie.technical.runtime.overall

    def mentry(self):
        '''One line entry'''
        y_string = 0
        cat_string = ""
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                y_string = self.movie.catalog.copyright.year
        if self.movie.classification:
            cat_string = build_genre_classification(self.movie)
        out = f"{self.movie.title!s:50s} {y_string:4d} " +\
              f"{self.runtime!s:>8s} {cat_string:50s}"
        return out

    def __str__(self):
        return self.output


class MiniEntry():
    '''Oneliner mini-format'''
    def __init__(self, in_movie, in_indent=2):
        self.movie = in_movie
        self.indent = in_indent
        self._prep_fields()
        self.output = self._build_output()

    @classmethod
    def header_line(cls, in_indent=2):
        '''Generate a simple header'''
        out = f"{' ' * in_indent}{'Title':40s} {'Year':4s} {'Genre':20s}\n" + \
              cls.header_line_line()
        return out

    @classmethod
    def header_line_line(cls, in_indent=2):
        """
        Generate a line to separate headers vs rows.
        """
        return f"{' ' * in_indent}{'-' * 40} {'-' * 4} {'-' * 20}\n"

    def _prep_fields(self):
        self.title_key = self.movie.unique_key
        self.year = ''
        self.genre = ''
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                self.year = self.movie.catalog.copyright.year
        if self.movie.classification is not None:
            self.genre = build_genre_simple(self.movie)

    def _build_output(self):
        return f"{' ' * self.indent}{self.movie.title!s:40s} " + \
               f"{self.year:4d} {self.genre:20s}\n"

    def __str__(self):
        return self.output


class Brief():
    '''Formatting for a brief text record'''
    def __init__(self, in_movie):
        self.movie = in_movie
        self._prep_fields()
        self._build_output()

    def _prep_fields(self):
        self.title_key = self.movie.unique_key
        self.runtime = timedelta(seconds=0)
        if self.movie.technical:
            if self.movie.technical.runtime:
                self.runtime = self.movie.technical.runtime.overall

    def _build_output(self):
        '''
        The primary output coordinator
        '''
        self.output = self.entry_header()
        self.output += self.classification_info()
        self.output += self.technical_info()
        self.output += self.primary_crew()
        self.output += self.cast()
        self.output += self.plot()
        self.output += self.keywords() + "\n"

    def entry_header(self):
        '''Basic report header for a movie'''
        y_string = ""
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                y_string = self.movie.catalog.copyright.year
        if y_string:
            out = f"{self.movie.title!s:69s} ({y_string})\n"
        else:
            out = f"{self.movie.title}\n"
        out += "=" * 76
        out += "\n"
        return out

    def classification_info(self):
        '''Basic report on genre information'''
        o_string = ""
        if self.movie.classification:
            o_string = build_genre_classification(self.movie)
            o_string += "\n"
            if self.movie.classification.genres.subgenres:
                o_string += build_subgenre_classifications(self.movie)
            o_string += "\n"
        return o_string

    def technical_info(self):
        '''Basic technical information'''
        o_string = ""
        if self.runtime:
            o_string += f"Runtime: {self.runtime}\n\n"
        return o_string

    def primary_crew(self):
        '''Report on crew basics'''
        out = ""
        if self.movie.crew is not None:
            if self.movie.crew.directors:
                out += hdr_list("Director",
                                self.movie.crew.directors) + "\n"
            if self.movie.crew.cinemap:
                out += hdr_list("Cinemaphotographer",
                                self.movie.crew.cinemap) + "\n"
        return out

    def cast(self):
        '''Report on film cast'''
        out = ""
        names = []
        if self.movie.crew.cast is not None:
            for role_o in self.movie.crew.cast.cast:
                names.append(role_o.actor)
            out = hdr_list_np("Cast", names)
            out += "\n"
        return out

    def plot(self):
        '''Report on plot'''
        out = ""
        if self.movie.story is not None:
            if self.movie.story.plot and str(self.movie.story.plot) != "":
                out += hdr_text("Plot", str(self.movie.story.plot))
                out += "\n\n"
        return out

    def keywords(self):
        '''Report on keywords'''
        out = ""
        if self.movie.story is not None:
            if self.movie.story.keywords:
                if len(self.movie.story.keywords.all()) > 0:
                    out += hdr_block("Keyword",
                                     self.movie.story.keywords.all())
        return out

    def __str__(self):
        return self.output


def build_genre_simple(in_movie):
    '''
    Build a string for all genres.
    '''
    o_string = ''
    classification = in_movie.classification
    if classification.genres.primary:
        o_string = f"{classification.genres.primary}"
    if classification.genres.secondary:
        o_string += '/' + '/'.join(classification.genres.secondary)
    return o_string


def build_genre_classification(in_movie):
    '''
    Build a text classification string.
    '''
    o_string = ""
    classification = in_movie.classification
    if classification.category:
        o_string = "[" + str(classification.category) + "]"
    o_string += " " + build_genre_simple(in_movie)
    if classification.genres.specific:
        o_string += f" \"{classification.genres.specific}\""
    return o_string


def build_subgenre_classifications(in_movie):
    '''
    Build the subgenre list.
    '''
    s_string = ", ".join(sorted(in_movie.classification.genres.subgenres))
    return f"({s_string})\n"
