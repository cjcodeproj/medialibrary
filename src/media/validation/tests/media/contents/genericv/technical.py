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


class GenericVisualTechnicalValidator(AbstractValidator):
    '''
    Generic test for the technical element
    on all visual content (movies, television)

    Specific tests for movies or television
    should go in their respective classes.
    '''
    def __init__(self):
        super().__init__()
        self.load_objects()

    def load_objects(self):
        '''
        Load additional test classes.
        '''
        self.objects.append(GenericVisualRuntimeValidator())

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run all tests.
        '''
        self.local_tests = [self.test_runtime_presence]
        for ltst in self.local_tests:
            ltst(in_dish)
        for tobj in self.objects:
            tobj.run_standard_tests(in_dish, in_level)

    def test_runtime_presence(self, in_dish):
        '''
        Test for the presence of the runtime element data.
        '''
        name = 'genericv.technical.runtime'
        test_r = TestResult(name, DEFMAXSCORE)
        technical = in_dish.item.technical
        if technical is not None:
            runtime = technical.runtime
            if runtime:
                test_r.autopass()
            else:
                fault = Fault(FaultLevel.NOTICE,
                              'Technical block should have runtime element')
                test_r.result(0, StatusCode.FAIL, fault)
        else:
            test_r.skip()
        in_dish.add_result(test_r)


class GenericVisualRuntimeValidator(AbstractValidator):
    '''
    Tests against the runtime value of all A/V
    content objects.
    '''

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run the all test methods.
        '''
        self.test_runtime_value(in_dish)

    def test_runtime_value(self, in_dish):
        '''
        Test runtime value to see if it has been
        properly set.
        '''
        name = 'genericv.technical.runtime.value'
        test_r = TestResult(name, DEFMAXSCORE)
        technical = in_dish.item.technical
        if technical is not None:
            runtime = technical.runtime
            if runtime:
                runtime_value = runtime.overall or timedelta(0)
                template_value = timedelta(seconds=1, minutes=1, hours=1)
                if runtime_value == template_value:
                    fault = Fault(FaultLevel.NOTICE,
                                  'Suspicious runtime value (1h1m1s)')
                    test_r.result(3, StatusCode.FAIL, fault)
                else:
                    test_r.autopass()
            else:
                test_r.skip()
        else:
            test_r.skip()
        in_dish.add_result(test_r)
