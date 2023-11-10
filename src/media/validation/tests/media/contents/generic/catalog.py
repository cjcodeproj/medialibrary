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
generic catalog validation module
'''

from media.validation.core.faults import Fault, FaultLevel
from media.validation.core.status import StatusCode, TestResult
from media.validation.core.tests import AbstractValidator


class GenericCatalogValidator(AbstractValidator):
    '''
    Catalog data validator.
    '''
    def __init__(self):
        super().__init__()
        self.load_objects()

    def load_objects(self):
        '''
        Load additional test pbjects.
        '''
        self.objects.append(GenericCatalogCopyrightValidator())

    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run all tests related to the catalog element.
        '''
        self.local_tests = [self.test_catalog_present,
                            self.test_copyright_present]
        for ltst in self.local_tests:
            ltst(in_dish)
        for tst in self.objects:
            tst.run_standard_tests(in_dish, in_level)

    def test_catalog_present(self, in_dish):
        '''
        Test that the catalog element was present.
        '''
        test_r = TestResult('generic.catalog', 5)
        cata = in_dish.item.catalog
        if cata is not None:
            test_r.autopass()
        else:
            fault = Fault(FaultLevel.WARNING, 'No catalog element')
            test_r.result(0, StatusCode.FAIL, fault)
        in_dish.add_result(test_r)

    def test_copyright_present(self, in_dish):
        '''
        Test that the copyright element was present.
        '''
        test_r = TestResult('generic.catalog.copyright', 5)
        cata = in_dish.item.catalog
        if cata.copyright is not None:
            test_r.autopass()
        else:
            fault = Fault(FaultLevel.WARNING, 'No copyright element')
            test_r.result(0, StatusCode.FAIL, fault)
        in_dish.add_result(test_r)


class GenericCatalogCopyrightValidator(AbstractValidator):
    '''
    Copyright data validator.
    '''
    def run_standard_tests(self, in_dish, in_level=5):
        '''
        Run all tests related to copyright.
        '''
        self.test_copyright_year(in_dish)
        if in_level <= 4:
            self.test_copyright_holders(in_dish)

    def test_copyright_year(self, in_dish):
        '''
        Test copyright year value.
        '''
        test_r = TestResult('generic.catalog.copyright.year', 5)
        cpy = in_dish.item.catalog.copyright
        if cpy is not None:
            if cpy.year > 0:
                test_r.autopass()
            else:
                fault = Fault(FaultLevel.WARNING, 'No copyright year value')
                test_r.result(0, StatusCode.FAIL, fault)
        else:
            test_r.skip()
        in_dish.add_result(test_r)

    def test_copyright_holders(self, in_dish):
        '''
        Test copyright holder values.
        '''
        test_r = TestResult('generic.catalog.copyright.holders', 5)
        cpy = in_dish.item.catalog.copyright
        if cpy is not None:
            if len(cpy.holders) > 0:
                test_r.autopass()
            else:
                fault = Fault(FaultLevel.NOTICE, 'No copyright holders')
                test_r.result(0, StatusCode.FAIL, fault)
        else:
            test_r.skip()
        in_dish.add_result(test_r)
