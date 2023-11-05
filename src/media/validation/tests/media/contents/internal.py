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
generic validation module media/content/movie
'''

from media.validation.tests.media.contents.movie import MovieValidator
from media.data.media.contents.movie import Movie


class ValidateContentTests():
    '''
    Class to add content testing to the test lists.
    '''
    def __init__(self):
        self.tests = []
        self.setup()

    def setup(self):
        '''
        Set up content validation objects for testing.
        '''
        self.tests.append(MovieValidator())

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run the standard tests by identifying the media type.
        '''
        for con in in_dish.status.contents:
            obj = con.item
            if issubclass(obj.__class__, Movie):
                movie_v = MovieValidator()
                movie_v.run_standard_tests(con, in_level)
