#!/usr/bin/env python
'''
Objects for representation of dates, either exact, or a date range.
'''

# pylint: disable=too-few-public-methods


class AbstractDate():
    '''
    Abstract class which has data shared by both
    child classes.
    '''
    def __init__(self):
        self.date = None


class ExactDate(AbstractDate):
    '''
    Representing an exact calendar date.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.date = in_element.text

    def __str__(self):
        return f"{self.date}"


class RangeDate(AbstractDate):
    '''
    Representation for a non-specific date, where both an estimated start
    and an estimated end is known.  For example, if something was acquired
    in 2014, the start value would be 2014-01-01, and the end value would be
    P1Y, to allow coverage for every day in 2014.
    '''
    def __init__(self, in_element_1, in_element_2):
        super().__init__()
        self.date = in_element_1.text
        self.end = in_element_2.text

    def __str__(self):
        return f"{self.date} -> {self.end}"
