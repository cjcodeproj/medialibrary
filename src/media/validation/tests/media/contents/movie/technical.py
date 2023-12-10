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
generic validation module
'''

# pylint: disable=R0801
# pylint: disable=W0613

from datetime import timedelta
from media.validation.core.faults import Fault, FaultLevel
from media.validation.core.status import StatusCode, TestResult
from media.validation.core.tests import AbstractValidator

DEFMAXSCORE = 5


class MovieTechnicalValidator(AbstractValidator):
    '''
    Technical validation block for all movies.
    '''
    def __init__(self):
        super().__init__()
        self.load_objects()

    def load_objects(self):
        '''
        Load additional class objects with validation tests.
        '''
        self.objects.append(MovieRuntimeValidator())

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run the standard test suite.
        '''
        for tobj in self.objects:
            tobj.run_standard_tests(in_dish, in_level)


class MovieRuntimeValidator(AbstractValidator):
    '''
    Tests against the runtime value of all A/V
    content objects.
    '''

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run the standard tests for movie runtime values.
        '''
        self.test_runtime_value(in_dish)

    def test_runtime_value(self, in_dish):
        '''
        Test that the overall runtime value makes sense.
        '''
        f_text = 'Movie runtimes are typically more than 45 minutes'
        test_r = TestResult('movie.technical.runtime.value', DEFMAXSCORE)
        technical = in_dish.item.technical
        if technical is not None:
            runtime = technical.runtime
            if runtime:
                runtime_value = runtime.overall or timedelta(0)
                movie_minimum = timedelta(minutes=45)
                if runtime_value <= movie_minimum:
                    fault = Fault(FaultLevel.NOTICE, f_text)
                    test_r.result(3, StatusCode.FAIL, fault)
                else:
                    test_r.autopass()
            else:
                test_r.skip()
        else:
            test_r.skip()
        in_dish.add_result(test_r)
