#!/usr/bin/env python

#
# Copyright 2023 Chris Josephes
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
Comparison classes that check two movies against each other.
'''

# pylint: disable=too-few-public-methods


from media.data.media.contents.generic.keywords import ProperNounKeyword


class MovieComparator():
    '''
    Loads all films, and creates individual comparison
    operation objects for each film, allowing each
    film to maintain a separate object for scoring
    data and comparison operations.
    '''
    def __init__(self):
        self.data = []
        self.results = []

    def load_data(self, in_list):
        '''
        Load all films into the object array.
        '''
        self.data.extend(in_list)

    def compare(self):
        '''
        Build the comparator objects, and then
        have very object run the comparison
        operation against all of the films.
        '''
        for film in self.data:
            self.results.append(MovieComparison(film))
        for film_compare in self.results:
            for film in self.data:
                film_compare.compare_against(film)

    def report(self):
        '''
        Generate output reports for a given film.
        '''
        for result in self.results:
            result.report()


class MovieComparison():
    '''
    Object class for running comparison operations of
    any film against an internally stored film.
    '''
    def __init__(self, in_film):
        self.film = in_film
        self.matches = {}

    def compare_against(self, in_film):
        '''
        Compare the passed film against the film stored in the object.

        Do not run if the film passed is identical to the interal film.

        All comparison operations are literally just tests between
        'self' and 'other', similar to object comparator methods.
        '''
        if in_film == self.film:
            return
        self.compare_director(in_film)
        self.compare_writer(in_film)
        self.compare_cinemaphotographer(in_film)
        self.compare_editor(in_film)
        self.compare_cast(in_film)
        self.compare_keywords(in_film)

    def add_match(self, in_film, in_trait):
        '''
        If a match is identified, add it to the internal data structure.
        '''
        other_f = in_film
        if other_f not in self.matches:
            self.matches[other_f] = MovieMatch(other_f, in_trait)
        else:
            self.matches[other_f].add_trait(in_trait)

    def compare_director(self, in_film):
        '''
        See if the other film has identical directors.
        '''
        for director in in_film.crew.directors:
            if director in self.film.crew.directors:
                self.add_match(in_film, MatchTrait('Director', director, 10))

    def compare_writer(self, in_film):
        '''
        See if the other film has identical writers.
        '''
        for writer in in_film.crew.writers:
            if writer in self.film.crew.writers:
                self.add_match(in_film, MatchTrait('Writer', writer, 8))

    def compare_cinemaphotographer(self, in_film):
        '''
        See if the other film has identical cinemaphotographers.
        '''
        for cinema in in_film.crew.cinemap:
            if cinema in self.film.crew.cinemap:
                trait = MatchTrait('Cinemaphotographer', cinema, 7)
                self.add_match(in_film, trait)

    def compare_editor(self, in_film):
        '''
        See if the other film has similar directors.
        '''
        for editor in in_film.crew.editors:
            if editor in self.film.crew.editors:
                self.add_match(in_film, MatchTrait('Editor', editor, 6))

    def compare_cast(self, in_film):
        '''
        See if the other filn has similar actors.
        '''
        in_cast = in_film.crew.cast
        my_cast = self.film.crew.cast
        if in_cast and my_cast:
            for role in in_cast.cast:
                other_actor = role.actor
                for mrole in my_cast.cast:
                    m_actor = mrole.actor
                    if other_actor == m_actor:
                        self.add_match(in_film, MatchTrait('Cast', m_actor, 5))

    def compare_keywords(self, in_film):
        '''
        See if the other film has identical keywords.
        '''
        other_keywords = in_film.story.keywords
        keywords = self.film.story.keywords
        if other_keywords and keywords:
            for keyword in other_keywords.all():
                if keyword in keywords.all():
                    if isinstance(keyword, ProperNounKeyword):
                        kw_score = 5 + keyword.relevance
                    else:
                        kw_score = 2 + keyword.relevance
                    trait = MatchTrait('Keyword', keyword, kw_score)
                    self.add_match(in_film, trait)

    def header(self):
        '''
        Report header.
        '''
        out = f"\nSource Movie: {self.film.catalog_title()}\n" +\
              f"{'='*89}\n" +\
              f"{'Movie':35s} {'Matches':7s} " +\
              f"{'Score':5s} {'Trait':18s} {'Value':s}\n" +\
              f"{'-'*35} {'-'*7} {'-'*5} {'-'*18} {'-'*20}\n"
        return out

    def report(self):
        '''
        Generate output of comparison results.
        '''
        print(self.header(), end='')
        for other_f in sorted(self.matches,
                              key=lambda x: self.matches[x].points,
                              reverse=True):
            print(str(self.matches[other_f]), end='')


class MovieMatch():
    '''
    Object to keep track of identified matches for a given film.
    Keeps a copy of the data that matches, and a passed scoring
    value identifying the quality of the match.
    '''
    def __init__(self, in_film, in_trait):
        self.film = in_film
        self.traits = [in_trait]
        self.points = in_trait.score

    def add_trait(self, in_trait):
        '''
        If another match has been identified for the same film,
        then record it.
        '''
        self.traits.append(in_trait)
        self.points += in_trait.score

    def __str__(self):
        out = ""
        count = 1
        trait_count = len(self.traits)
        for trt in self.traits:
            if count == 1:
                out += f"{self.film.catalog_title():34.34s}  " +\
                       f"{trait_count:7d} {self.points:5d} " +\
                       f"{trt}\n"
            else:
                out += f"{' '*49} {trt}\n"
            count += 1
        return out


class MatchTrait():
    '''
    Simple data structure containing a film, the
    matching data, and the score value.
    '''
    def __init__(self, in_title, in_data, in_score=1):
        self.title = in_title
        self.data = in_data
        self.score = in_score

    def __str__(self):
        return f"{self.title:18s} {str(self.data)}"
