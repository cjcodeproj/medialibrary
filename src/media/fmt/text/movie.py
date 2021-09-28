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
        out = f"{'Title':50s} {'Year':4s}\n"
        out += f"{'=' * 50} {'=' * 4}"
        return out

    def mentry(self):
        '''One line entry'''
        y_string = ""
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                y_string = self.movie.catalog.copyright.year
        out = f"{self.movie.title!s:50s} {y_string:4d}"
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
        self.output += self.classification_info()
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
            classification = self.movie.classification
            if classification.category:
                o_string = "[" + str(classification.category) + "]"
            if classification.genres.primary:
                o_string += f" {classification.genres.primary}"
            if classification.genres.secondary:
                o_string += "/" + "/".join(classification.genres.secondary)
            if classification.genres.specific:
                o_string += f" \"{classification.genres.specific}\""
            o_string += "\n"
            if classification.genres.subgenres:
                s_string = ", ".join(classification.genres.subgenres)
                o_string += f"({s_string})\n"
            o_string += "\n"
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
