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
Code for HTML table output.
'''

# pylint:disable=R0903
# pylint:disable=R0801

from media.fmt.formatter.html.common import sanitize_for_xml
from media.fmt.structure.table import (TableHeaderColumnSpec,
                                       TableSetupException)


class Table():
    '''
    HTML table class.
    '''
    def __init__(self):
        self.count = 0

    def render(self, in_table):
        '''
        Generate a HTML table.
        '''
        if len(in_table.col_specs) == 0:
            raise TableSetupException('No columns defined')
        output = "<table>\n"
        output += self._render_column_setup(in_table)
        output += self._render_headers(in_table)
        output += self._render_body(in_table)
        output += "</table>\n"
        self.count += 1
        return output

    def _render_column_setup(self, in_table):
        output = ''
        output += " <colgroup>\n"
        for col_iter in in_table.col_specs:
            if isinstance(col_iter, TableHeaderColumnSpec):
                output += "  <col class='headers'/>\n"
            else:
                output += "  <col/>\n"
        output += " </colgroup>\n"
        return output

    def _render_headers(self, in_table):
        '''
        We want to output a the header row, but
        only if the table has defined headers.
        '''
        output = ''
        has_hdr_text = False
        for col_iter in in_table.col_specs:
            if col_iter.hdr_text:
                has_hdr_text = True
                break
        if has_hdr_text:
            output = " <thead>\n  <tr>\n"
            for col_iter in in_table.col_specs:
                output += f"   <th>{col_iter.hdr_text}</th>\n"
            output += "  </tr>\n </thead>\n"
        return output

    def _render_body(self, in_table):
        output = ''
        for chunk in in_table.bchunks:
            output += TableBodyChunk.render(chunk)
        return output


class TableBodyChunk():
    '''
    The TableBodyChunk represents a group of table rows.

    Most of the init code is handled by the parent class.
    '''

    @classmethod
    def render(cls, in_chunk):
        '''
        Generate a group of table rows.
        '''
        output = " <tbody>\n"
        col_count = len(in_chunk.table.col_specs)
        if in_chunk.body_header:
            output += "  <tr>\n"
            output += f"   <th colspan='{col_count}'>"
            output += f"{in_chunk.body_header}</th>\n  </tr>\n"
        for row in in_chunk.rows:
            output += TableBodyRow.render(row)
        output += " </tbody>\n"
        return output


class TableBodyRow():
    '''
    Most of the init code is handled by the parent class.
    '''

    @classmethod
    def render(cls, in_row):
        '''
        Generate a table row.
        '''
        output = "  <tr>\n"
        for cell in in_row.cells:
            output += TableCell.render(cell)
        output += "  </tr>\n"
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
        Generate a single table cell.
        '''
        if isinstance(in_cell.spec, TableHeaderColumnSpec):
            output = f"   <th>{sanitize_for_xml(in_cell.value)}</th>\n"
        else:
            output = f"   <td>{sanitize_for_xml(in_cell.value)}</td>\n"
        return output
