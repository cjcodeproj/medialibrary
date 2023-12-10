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

'''Unit tests for validation testresult class.'''

# pylint: disable=R0801

import unittest
from media.validation.core.status import StatusCode, TestResult


class TestTestResult(unittest.TestCase):
    '''
    Basic tests for TestResult classes.
    '''
    def setUp(self):
        self.test_r = TestResult('test.sample1', 5)

    def test_test_result_object(self):
        '''
        Verify TestResult object is created.
        '''
        self.assertIsInstance(self.test_r, TestResult)

    def test_test_result_name(self):
        '''
        Verify TestResult object name value is correct.
        '''
        self.assertEqual(self.test_r.name, 'test.sample1')

    def test_test_result_max_score(self):
        '''
        Verify TestResult highest score value is set.
        '''
        self.assertEqual(self.test_r.possible, 5)

    def test_test_result_def_skipped_value(self):
        '''
        Verify TestResult default skipped value is set.
        '''
        self.assertFalse(self.test_r.skipped)

    def test_rest_result_def_status_code_value(self):
        '''
        Verify TestResult default status code value is set.
        '''
        self.assertEqual(self.test_r.status_code, StatusCode.FAIL)


class TestTestResultSkipped(unittest.TestCase):
    '''
    Tests for TestResult class when a test is skipped.
    '''
    def setUp(self):
        self.test_r = TestResult('test.sample2', 5)
        self.test_r.skip()

    def test_test_result_skipped(self):
        '''
        Confirm the skipped test value is true.
        '''
        self.assertTrue(self.test_r.skipped)

    def test_test_max_score_when_skipped(self):
        '''
        Confirm the skipped max score is 0.
        '''
        self.assertEqual(self.test_r.possible, 0)

    def test_test_real_score_when_skipped(self):
        '''
        Confirm the skipped possible score is 0.
        '''
        self.assertEqual(self.test_r.score, 0)


class TestTestResultSet(unittest.TestCase):
    '''
    Test for TestResult class when a test is set.
    '''
    def setUp(self):
        self.test_r = TestResult('test.sample3', 5)
        self.test_r.result(2, StatusCode.FAIL)

    def test_test_result_status_code(self):
        '''
        Confirm the status code is properly set.
        '''
        self.assertEqual(self.test_r.status_code, StatusCode.FAIL)

    def test_test_result_score(self):
        '''
        Confirm the score has been properly set.
        '''
        self.assertEqual(self.test_r.score, 2)


class TestTestResultSetError(unittest.TestCase):
    '''
    Test the error handling of TestResult.
    '''
    def setUp(self):
        self.test_r = TestResult('test.sample4', 5)

    def test_test_result_score_exception(self):
        '''
        Confirm exception is raised.
        '''
        with self.assertRaises(ValueError):
            self.test_r.result(7, StatusCode.PASS)


class TestTestResultAutoPass(unittest.TestCase):
    '''
    Test the autopass functionality of TestResult.
    '''
    def setUp(self):
        self.test_r = TestResult('test.sample5', 5)
        self.test_r.autopass()

    def test_test_result_autopass_score(self):
        '''
        Test autopass score set to max value.
        '''
        self.assertEqual(self.test_r.score, 5)

    def test_test_result_autopass_status_code(self):
        '''
        Test autopass status code value.
        '''
        self.assertTrue(self.test_r)


if __name__ == '__main__':
    unittest.main()
