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


import re
from media.validation.core.faults import Fault, FaultLevel
from media.validation.core.status import StatusCode, TestResult
from media.validation.core.tests import AbstractValidator


class GenericStoryValidator(AbstractValidator):
    '''
    Generic tests that apply to every story object.
    '''
    def __init__(self):
        super().__init__()
        self.load_objects()

    def load_objects(self):
        '''
        Load additional test objects that should be run.
        '''
        self.objects.append(GenericPlotValidator())

    def run_standard_tests(self, in_dish, in_level):
        '''
        Run all story element related tests.
        '''
        self.local_tests = [self.test_plot_presence]
        for l_tst in self.local_tests:
            l_tst(in_dish)
        for tst in self.objects:
            tst.run_standard_tests(in_dish, in_level)

    def test_plot_presence(self, in_dish):
        '''
        Confirm that a plot element is present.
        '''
        test_r = TestResult('generic.story.plot', 5)
        sty = in_dish.item.story
        if sty is not None:
            if sty.plot is not None:
                test_r.autopass()
            else:
                fault = Fault(FaultLevel.WARNING, 'No plot defined.')
                test_r.result(0, StatusCode.FAIL, fault)
        else:
            test_r.skip()
        in_dish.add_result(test_r)


class GenericPlotValidator(AbstractValidator):
    '''
    Generic tests that apply to every plot object.
    '''

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run all plot related tests.
        '''
        if in_level <= 4:
            self.test_plot_whitespace(in_dish)
            self.test_plot_length(in_dish)

    def test_plot_whitespace(self, in_dish):
        '''
        Test plot object for leading or trailing
        whitespace.

        Technically, this test should never return a fault
        because the XML loader code does this
        automatically, since the Plot is expected to
        be a multi-line element.
        '''
        test_r = TestResult('generic.story.plot.whitesapce', 5)
        plt = in_dish.item.story.plot
        if plt is not None:
            faults = []
            p_str = str(plt)
            l_pad = re.search(r"^\s+", p_str)
            r_pad = re.search(r"\s+$", p_str)
            if l_pad is not None:
                fault = Fault(FaultLevel.WARNING, 'Leading whitespace')
                faults.append(fault)
            if r_pad is not None:
                fault = Fault(FaultLevel.WARNING, 'Trailing whitespace')
                faults.append(fault)
            if len(faults) > 0:
                test_r.result(0, StatusCode.FAIL)
                test_r.add_faults(faults)
            else:
                test_r.autopass()
        else:
            test_r.skip()
        in_dish.add_result(test_r)

    def test_plot_length(self, in_dish):
        '''
        Test the number of words in the plot description.
        It should be at least 20.
        '''
        test_r = TestResult('generic.story.plot.length', 5)
        sty = in_dish.item.story
        if sty is not None:
            if sty.plot is not None:
                p_str = str(sty.plot).strip()
                p_words = p_str.split()
                if len(p_words) < 20:
                    fault = Fault(FaultLevel.NOTICE,
                                  'Plot has less than 20 words')
                    test_r.result(3, StatusCode.FAIL, fault)
                else:
                    test_r.autopass()
            else:
                test_r.skip()
        else:
            test_r.skip()
        in_dish.add_result(test_r)
