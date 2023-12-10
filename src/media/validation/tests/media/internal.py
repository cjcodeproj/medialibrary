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
Primary media validator tests.
'''

# pylint: disable=R0801


import re
from media.validation.core.faults import FaultLevel, Fault
from media.validation.core.status import StatusCode, TestResult
from media.validation.core.tests import AbstractValidator
from media.validation.tests.media.contents import ValidateContentTests


class MediaValidator(AbstractValidator):
    '''
    Main validator object for media.
    '''
    def __init__(self):
        super().__init__()
        self.load_objects()

    def load_objects(self):
        '''
        Load all related testing objects.
        '''
        # self.objects.append(MediaTitleTests())
        self.objects.append(MediaTitleValidator())
        self.objects.append(ValidateContentTests())

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run standard media tests.
        '''
        self.local_tests = [self.test_title_present]
        for l_test in self.local_tests:
            l_test(in_dish)
        for tst in self.objects:
            tst.run_standard_tests(in_dish, in_level)

    def test_title_present(self, in_dish):
        '''
        Test the presence of the title element.
        '''
        test_r = TestResult('media.title', 5)
        title_o = in_dish.media.title
        if title_o:
            test_r.autopass()
        else:
            fault = Fault(FaultLevel.CRITICAL, 'No title element')
            test_r.result(0, StatusCode.FAIL, fault)
        in_dish.status.add_result(test_r)


class MediaTitleValidator(AbstractValidator):
    '''
    Validation tests for the media title.
    '''

    def run_standard_tests(self, in_dish, in_level):
        '''
        Run all title related tests.
        '''
        self.test_title_main(in_dish)
        self.test_title_main_value(in_dish)
        self.test_title_edition(in_dish)
        self.test_title_edition_value(in_dish)
        if in_level <= 4:
            self.test_title_main_whitespace(in_dish)
            self.test_title_edition_whitespace(in_dish)

    def test_title_main(self, in_dish):
        '''
        Test the presence of the main title.
        '''
        test_r = TestResult('media.title.main', 5)
        tobj = in_dish.media.title
        if tobj:
            if tobj.title:
                test_r.autopass()
            else:
                fault = Fault(FaultLevel.WARNING, 'No main title')
                test_r.result(0, StatusCode.FAIL, fault)
        else:
            test_r.skip()
        in_dish.status.add_result(test_r)

    def test_title_main_value(self, in_dish):
        '''
        Test the value of the main title.
        '''
        test_r = TestResult('media.title.main.value', 5)
        tobj = in_dish.media.title
        if tobj:
            if tobj.title:
                t_str = tobj.title.strip()
                if t_str == '':
                    fault = Fault(FaultLevel.WARNING, 'Main title empty')
                    test_r.result(0, StatusCode.FAIL, fault)
                else:
                    test_r.autopass()
            else:
                test_r.skip()
        else:
            test_r.skip()
        in_dish.status.add_result(test_r)

    def test_title_main_whitespace(self, in_dish):
        '''
        Test for whitespace in the main title.
        '''
        test_r = TestResult('media.title.main.whitespace', 5)
        tobj = in_dish.media.title.title
        if tobj:
            faults = self._whitespace_test(str(tobj))
            if len(faults) > 0:
                test_r.result(0, StatusCode.FAIL)
                test_r.add_faults(faults)
            else:
                test_r.autopass()
        else:
            test_r.skip()
        in_dish.status.add_result(test_r)

    def test_title_edition(self, in_dish):
        '''
        Test the presence of an edition element.
        '''
        test_r = TestResult('media.title.edition', 5)
        tobj = in_dish.media.title
        if tobj:
            if tobj.edition:
                test_r.autopass()
            else:
                test_r.skip()
        else:
            test_r.skip()
        in_dish.status.add_result(test_r)

    def test_title_edition_value(self, in_dish):
        '''
        Validate the edition value of a piece of media.
        '''
        test_r = TestResult('media.title.edition.value', 5)
        tobj = in_dish.media.title
        if tobj:
            if tobj.edition:
                e_str = tobj.edition.strip()
                if e_str == '':
                    fault = Fault(FaultLevel.WARNING, 'Edition title empty')
                    test_r.result(0, StatusCode.FAIL, fault)
                else:
                    test_r.autopass()
            else:
                test_r.skip()
        else:
            test_r.skip()
        in_dish.status.add_result(test_r)

    def test_title_edition_whitespace(self, in_dish):
        '''
        Test for whitespace in the edition title.
        '''
        test_r = TestResult('media.title.edition.whitespace', 5)
        tobj = in_dish.media.title.edition
        if tobj:
            faults = self._whitespace_test(str(tobj))
            if len(faults) > 0:
                test_r.result(0, StatusCode.FAIL)
                test_r.add_faults(faults)
            else:
                test_r.autopass()
        else:
            test_r.skip()
        in_dish.status.add_result(test_r)

    def _whitespace_test(self, in_str):
        faults = []
        l_pad = re.search(r"^\s+", in_str)
        r_pad = re.search(r"\s+$", in_str)
        if l_pad:
            fault = Fault(FaultLevel.WARNING, 'Leading whitespace')
            faults.append(fault)
        if r_pad:
            fault = Fault(FaultLevel.WARNING, 'Trailing whitespace')
            faults.append(fault)
        return faults
