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
All object classes to store test status information.
'''

# pylint: disable=R0903

from media.data.media.medium.release import FormalType


class StatusCode():
    '''
    Simple status code.
    '''
    PASS = 0
    FAIL = 1

    @classmethod
    def to_str(cls, in_code):
        '''
        Return the status code as a string value.
        '''
        matrix = {StatusCode.PASS: 'Pass',
                  StatusCode.FAIL: 'Fail'}
        if in_code in matrix:
            return matrix[in_code]
        raise ValueError('Invalid Status Code')


class Tray():
    '''
    An object containing both a piece of media
    and requested testing parameters.
    '''
    def __init__(self, in_media, in_level):
        self.media = in_media
        self.level = in_level
        self.status = MediaStatus(in_media, in_level)

    def has_passed(self):
        '''
        Boolean identifier if a piece of media
        has passed all tests.
        '''
        return self.status.has_passed()


class AbstractStatus():
    '''
    An abstract status object
    '''
    def __init__(self, in_level):
        self.level = in_level

    @classmethod
    def rep_test_header(cls):
        '''
        Generate a header for a list of individual
        test results
        '''
        out = f"\n{'No':4s} {'Test':40s} {'Result':7s} " + \
              f"{'Score':5s} {'Max':5s} {'Faults':6s}\n" + \
              f"{'-'*4} {'-'*40} {'-'*7} {'-'*5} {'-'*5} {'-'*6}\n"
        return out

    @classmethod
    def rep_fault_header(cls):
        '''
        Generate a header for a list of fault
        details
        '''
        out = f"\n{' '*25}<<< FAULTS >>>\n\n" + \
              f"{'Test':40s} {'Level':10s} {'Message':s}\n" + \
              f"{'-'*40} {'-'*10} {'-'*20}\n"
        return out


class MediaStatus(AbstractStatus):
    '''
    A status object for a piece of media.
    '''
    def __init__(self, in_media, in_level):
        super().__init__(in_level)
        self.media = in_media
        self.contents = []
        self.test_results = []
        self.tally = Tally()
        self.faults = []
        self.setup()

    def setup(self):
        '''
        Set up ContentStatus objects for every piece of content.
        '''
        for media_con in self.media.contents:
            self.contents.append(ContentStatus(media_con, self.level))

    def add_result(self, in_test_result):
        '''
        Add a new test result object to the array, and
        update the total score tally information.
        '''
        self.tally.add_result_tally(in_test_result)
        self.test_results.append(in_test_result)

    def calculate(self):
        '''
        Combine the tally scores for all content objects.
        '''
        for con in self.contents:
            self.tally.merge_tally_object(con.tally)

    def has_passed(self):
        '''
        Boolean identifier if a piece of media has passed all tests.
        '''
        return self.tally.has_passed()

    def report(self):
        '''
        Generate a full report on all test results and the
        total score.
        '''
        out = ''
        out += self._report_header()
        out += self._report_main_summary()
        out += self._report_main_body()
        out += self._report_content_objects()
        return out

    def _report_header(self):
        ftype = FormalType.formal_convert(self.media.medium.release.type)
        out = f"\n{'='*72}\n" + \
              f"{self.media.title!s:61s} {ftype:>10s}\n" + \
              f"{'='*72}\n"
        return out

    def _report_main_summary(self):
        out = f"\n{'Score':>32s} : {self.tally.score_str():s}\n" + \
              f"{'Tests Run':>32s} : {self.tally.run:d}\n" + \
              f"{'Tests Skipped':>32s} : {self.tally.skipped:d}\n" + \
              f"{'Passed':>32s} : {self.tally.passed:d}\n" + \
              f"{'Failed':>32s} : {self.tally.failed:d}\n\n"
        return out

    def _report_main_body(self):
        out = ''
        out += MediaStatus.rep_test_header()
        top_level_faults = 0
        line_count = 1
        for test_result in self.test_results:
            out += f"{line_count:4d} {test_result}\n"
            line_count += 1
            if len(test_result.faults) > 0:
                top_level_faults += len(test_result.faults)
        if top_level_faults > 0:
            out += MediaStatus.rep_fault_header()
            for test_result in self.test_results:
                fault_count = 1
                for fault in test_result.faults:
                    if fault_count < 2:
                        out += f"{test_result.name:40s} " + \
                               f"{fault.lvl_str():10s} " + \
                               f"{fault.message}\n"
                    else:
                        out += f"{' ':40s} " + \
                               f"{fault.lvl_str():10s} " + \
                               f"{fault.message}\n"
                    fault_count += 1
        return out

    def _report_content_objects(self):
        out = ''
        for con_status in self.contents:
            line_count = 1
            out += f"\nContent: {con_status.item.title!s:55} {'(Movie)'}\n" + \
                   f"{'-'*72}\n" + \
                   MediaStatus.rep_test_header()
            cfc = 0
            for test_result in con_status.test_results:
                out += f"{line_count:4d} {test_result}\n"
                line_count += 1
                cfc += len(test_result.faults)
            if cfc > 0:
                out += MediaStatus.rep_fault_header()
                for test_result in con_status.test_results:
                    fault_count = 1
                    for fault in test_result.faults:
                        if fault_count < 2:
                            out += f"{test_result.name:40s} " + \
                                   f"{fault.lvl_str():10s} " + \
                                   f"{fault.message}\n"
                        else:
                            out += f"{' ':40s} " + \
                                   f"{fault.lvl_str():10s} " + \
                                   f"{fault.message}\n"
        return out


class ContentStatus(AbstractStatus):
    '''
    A status object for content in a piece
    of media.
    '''
    def __init__(self, in_content, in_level):
        super().__init__(in_level)
        self.item = in_content
        self.test_results = []
        self.tally = Tally()
        # self.fc = 0
        self.possible = 0
        self.actual = 0

    def add_result(self, in_test_result):
        '''
        Add a new test result object to the array
        and update the score totals.
        '''
        self.tally.add_result_tally(in_test_result)
        self.test_results.append(in_test_result)

    def calculate(self):
        '''
        Total up the tally results.

        (this method might not be used)
        '''
        for tst in self.test_results:
            if not tst.skipped:
                self.tally.max_points += tst.possible
                # self.possible += tst.possible
                self.tally.earned_points += tst.score
                # self.actual += tst.score
                if len(tst.faults) > 0:
                    self.tally.faults.extend(tst.faults)
                    # self.fc += len(tst.faults)


class Tally():
    '''
    A simple scoring object for tracking
    status scores.
    '''
    def __init__(self):
        self.run = 0
        self.skipped = 0
        self.passed = 0
        self.failed = 0
        self.max_points = 0
        self.earned_points = 0
        self.faults = []

    def add_result_tally(self, in_result):
        '''
        Add the scoring information from a single test result.
        '''
        if in_result.skipped:
            self.skipped += 1
        else:
            self.run += 1
            if in_result.status_code == StatusCode.PASS:
                self.passed += 1
            else:
                self.failed += 1
            self.max_points += in_result.possible
            self.earned_points += in_result.score
            if len(in_result.faults) > 0:
                self.faults.extend(in_result.faults)

    def merge_tally_object(self, in_other):
        '''
        Merge two tally objects together so
        all values are in one object.
        '''
        self.max_points += in_other.max_points
        self.earned_points += in_other.earned_points
        self.run += in_other.run
        self.skipped += in_other.skipped
        self.passed += in_other.passed
        self.failed += in_other.failed
        if len(in_other.faults) > 0:
            self.faults.extend(in_other.faults)

    def rs_str(self):
        '''
        Return a comparision of run vs. skipped tests.
        '''
        return f"{self.run:3d} {self.skipped:4d}"

    def pf_str(self):
        '''
        Return a comparision of passed vs. failed tests.
        '''
        return f"{self.passed:4d} {self.failed:4d}"

    def ratio(self):
        '''
        Return a score value of all passing tests
        as a value not to exceed 10.0.
        '''
        return self.earned_points / self.max_points * 10

    def has_passed(self):
        '''
        Quick result on whether a piece of media has
        passed all tests.
        '''
        return self.earned_points == self.max_points

    @classmethod
    def header(cls):
        '''
        Return a simple header line to match the
        output fields.
        '''
        return f"{'Media':40s} " + \
               f"{'Type':10s} " + \
               f"{'Score':10s} {'Run/Skip':8s} {'Pass/Fail':9s} " + \
               f"{'Faults':6s}\n" + \
               f"{'-'*40} {'-'*10} {'-'*10} {'-'*8} {'-'*9} {'-'*6}\n"

    def score_str(self):
        '''
        Return a string in the format of score value against the
        highest value 10.0
        '''
        return f"{self.ratio():.1f}/10.0"

    def __str__(self):
        '''
        Return score value, test run/skipped,
        tests passed/failed, and the number of faults.
        '''
        return f"{self.score_str():>10s} " + \
               f"{self.rs_str()} " + \
               f"{self.pf_str()} " + \
               f"{len(self.faults):6d}"


class TestResult():
    '''
    Keeps data tied to the result of a single test.
    '''
    def __init__(self, in_name, in_highest):
        self.name = in_name
        self.possible = in_highest
        self.score = 0
        self.skipped = False
        self.status_code = StatusCode.FAIL
        self.faults = []

    def skip(self):
        '''
        Identify a test as skipped, which
        would have no score.
        '''
        self.skipped = True
        self.score = 0
        self.possible = 0

    def result(self, in_score, in_pf, in_fault=None):
        '''
        Set the score value, the test status code,
        and a fault object, if any.
        '''
        if in_score > self.possible:
            raise ValueError('Score value too high.')
        self.score = in_score
        self.status_code = in_pf
        if in_fault:
            self.faults.append(in_fault)

    def autopass(self):
        '''
        Shortcut to automatically set a test as passing.
        '''
        self.score = self.possible
        self.status_code = StatusCode.PASS

    def add_fault(self, in_fault):
        '''
        Add a single fault to the fault array.
        '''
        self.faults.append(in_fault)

    def add_faults(self, in_fault_list):
        '''
        Add multiple faults to the fault array.
        '''
        self.faults.extend(in_fault_list)

    def __str__(self):
        if not self.skipped:
            return f"{self.name:40s} " + \
                   f"{StatusCode.to_str(self.status_code):7s} " + \
                   f"{self.score:5d} " + \
                   f"{self.possible:5d} " + \
                   f"{len(self.faults):6d}"
        return f"{self.name:40s} " + \
               f"{'Skipped':7s} " + \
               f"{'-':>5s} {'-':>5s} {'-':>6s}"
