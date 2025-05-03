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
Code for rendering a table in plain text.
'''

# pylint: disable=R0903
# pylint: disable=R0801

from media.fmt.structure.table import (TableSetupException)


class Table():
    '''
    Formatting class for a plain text table.
    '''
    def __init__(self):
        self.count = 0

    def render(self, in_table):
        '''
        Render the entire table.
        '''
        if len(in_table.col_specs) == 0:
            raise TableSetupException('No columns defined.')
        output = ''
        output += self._render_headers(in_table)
        output += self._render_separator_line(in_table)
        output += self._render_body(in_table)
        return output

    def _render_headers(self, in_table):
        output = ''
        has_hdr_text = False
        for col_iter in in_table.col_specs:
            if col_iter.hdr_text:
                has_hdr_text = True
                break
        if has_hdr_text:
            for col_iter in in_table.col_specs:
                output += f"{col_iter.hdr_text:{col_iter.py_format}} "
            output += "\n"
        return output

    def _render_body(self, in_table):
        output = ''
        for chunk in in_table.bchunks:
            output += TableBodyChunk.render(chunk)
        return output

    def _render_separator_line(self, in_table):
        output = ''
        symbol = ''
        for cs_iter in in_table.col_specs:
            if cs_iter.hdr_text == '':
                symbol = ' '
            else:
                symbol = '='
            if cs_iter.end_of_row:
                output += f"{symbol * cs_iter.width}\n"
            else:
                output += f"{symbol * cs_iter.width} "
        return output


class TableBodyChunk():
    '''
    The TableBodyChunk represents a group of table rows.

    Most of the init code is handled by the parent class.
    '''

    @classmethod
    def render(cls, in_chunk):
        '''
        Render the body chunk.
        '''
        output = ''
        if in_chunk.body_header:
            output += f"\n -- {in_chunk.body_header} --\n\n"
        for row in in_chunk.rows:
            output += TableBodyRow.render(row)
        return output


class TableBodyRow():
    '''
    Most of the init code is handled by the parent class.
    '''

    @classmethod
    def render(cls, in_row):
        '''
        Render the table row.
        '''
        output = ''
        for cell in in_row.cells:
            output += TableCell.render(cell)
        return output


class TableCell():
    '''
    CSV Table Cell.

    A cell will contain both the value it needs,
    and the specification information on how to render it.
    '''

    @classmethod
    def render(cls, in_cell):
        '''
        Render the table cell.
        '''
        if in_cell.spec.end_of_row:
            return f"{in_cell.value:{in_cell.spec.py_format}}\n"
        return f"{in_cell.value:{in_cell.spec.py_format}} "
