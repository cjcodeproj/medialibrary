#!/usr/bin/env python

#
# Copyright 2025 Chris Josephes
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
Code for handling plain text output.
'''

# pylint: disable=R0903, R0801

from media.fmt.formatter.abstract import AbstractFormatter
from media.fmt.formatter.plaintext.table import Table
from media.fmt.formatter.plaintext.basics import Basics
import media.fmt.structure.table
import media.fmt.structure.basics


class DriverMain(AbstractFormatter):
    '''
    Formatter class for plain text output.
    '''

    structure_matrix = {
            media.fmt.structure.table.Table: Table,
            media.fmt.structure.basics.Paragraph: Basics,
            media.fmt.structure.basics.Header: Basics,
            }
