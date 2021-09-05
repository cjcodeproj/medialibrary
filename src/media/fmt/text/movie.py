#!/usr/bin/env python
'''
Standard text format reports for movies.
'''

from media.fmt.text.basics import hdr_list, hdr_text, hdr_block


class List():
    '''Formatting a listing of movies, one per line.'''
    def __init__(self, in_movie):
        self.movie = in_movie
        self.output = ""
        self.output += self.mentry()

    @classmethod
    def list_header(cls):
        '''Generate a simple header'''
        out = "{0:50s} {1:4s}\n".format("Title", "Year")
        out += "{0} {1}".format('=' * 50, '=' * 4)
        return out

    def mentry(self):
        '''One line entry'''
        y_string = ""
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                y_string = self.movie.catalog.copyright.year
        out = "{0:50s} {1:4}".format(self.movie.title, y_string)
        return out

    def __str__(self):
        return self.output


class Brief():
    '''Formatting for a brief text record'''
    def __init__(self, in_movie):
        self.movie = in_movie
        self.output = ""
        # prep the header
        self.output = self.header()
        self.output += self.primary_crew()
        self.output += self.plot()
        self.output += self.keywords()
        self.output += "\n"
        # report on directors
        # plot/keywords

    def header(self):
        '''Basic report header for a movie'''
        y_string = ""
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                y_string = self.movie.catalog.copyright.year
        if y_string:
            out = "{0:69} ({1})\n".format(self.movie.title, y_string)
        else:
            out = "{0}\n".format(self.movie.title)
        out += "=" * 76
        out += "\n"
        return out

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

    def plot(self):
        '''Report on plot'''
        out = ""
        if self.movie.story is not None:
            if self.movie.story.plot and str(self.movie.story.plot) != "":
                out += "\n"
                out += hdr_text("Plot", str(self.movie.story.plot))
                out += "\n\n"
        return out

    def keywords(self):
        '''Report on keywords'''
        out = ""
        if self.movie.story is not None:
            if self.movie.story.keywords:
                out += hdr_block("Keyword", self.movie.story.keywords.all())
        return out

    def __str__(self):
        return self.output
