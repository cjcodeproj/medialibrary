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

from media.validation.core.tests import AbstractValidator
from media.validation.tests.media\
        .contents.generic.catalog import GenericCatalogValidator
from media.validation.tests.media\
        .contents.generic.story import GenericStoryValidator
from media.validation.tests.media\
        .contents.genericv.technical import GenericVisualTechnicalValidator
from media.validation.tests.media.\
        contents.movie.technical import MovieTechnicalValidator


class MovieValidator(AbstractValidator):
    '''
    Validation tests for a movie.
    '''
    def __init__(self):
        super().__init__()
        self.tests = []
        self.load_objects()

    def load_objects(self):
        '''
        Load test object classes.
        '''
        # self.tests.append(ValidateGenericCopyrightTests())
        self.tests.append(GenericCatalogValidator())
        # self.tests.append(ValidatePlotTests())
        self.tests.append(GenericStoryValidator())
        # self.tests.append(TechnicalTestsRunner())
        # self.tests.append(MovieTechnicalTestsRunner())
        self.tests.append(GenericVisualTechnicalValidator())
        self.tests.append(MovieTechnicalValidator())

    def run_standard_tests(self, in_movie_status, in_level=5):
        '''
        Run standard movie tests.
        '''
        for tst in self.tests:
            tst.run_standard_tests(in_movie_status, in_level)
