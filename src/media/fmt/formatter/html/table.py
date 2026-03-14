#!/usr/bin/env python

#
# Copyright 2026 Chris Josephes
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

import xml.etree.ElementTree as ET
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
        element = ET.Element('table')
        if len(in_table.classes) > 0:
            c_str = ' '.join(in_table.classes)
            element.attrib['class'] = c_str
        element.append(Table._xml_colgroup(in_table))
        hdr = None
        hdr = Table._xml_table_header(in_table)
        if hdr:
            element.append(hdr)
        ca = []
        ca = Table._xml_body(in_table)
        if len(ca) > 0:
            for bochunk in ca:
                element.append(bochunk)
        self.count += 1
        return element

    @classmethod
    def _xml_colgroup(cls, in_table):
        element = ET.Element('colgroup')
        for col_iter in in_table.col_specs:
            col_element = ET.Element('col')
            if isinstance(col_iter, TableHeaderColumnSpec):
                col_element.attrib['class'] = 'headers'
            element.append(col_element)
        return element

    @classmethod
    def _xml_table_header(cls, in_table):
        has_hdr_text = False
        for col_iter in in_table.col_specs:
            if col_iter.hdr_text:
                has_hdr_text = True
                break
        if has_hdr_text:
            hdr_element = ET.Element('thead')
            hdr_row = ET.Element('tr')
            for col_iter in in_table.col_specs:
                hdr_cell = ET.Element('th')
                hdr_cell.text = sanitize_for_xml(col_iter.hdr_text)
                hdr_row.append(hdr_cell)
            hdr_element.append(hdr_row)
            return hdr_element
        return None

    @classmethod
    def _xml_body(cls, in_table):
        celements = []
        for chunk in in_table.bchunks:
            c_elem = TableBodyChunk.xml(chunk)
            celements.append(c_elem)
        if len(celements) > 0:
            return celements
        return None


class TableBodyChunk():
    '''
    A tbody element
    '''
    @classmethod
    def xml(cls, in_chunk):
        '''
        Return a body chunk for a HTML table.
        '''
        element = ET.Element('tbody')
        if in_chunk.body_header:
            col_count = len(in_chunk.table.col_specs)
            row = ET.Element('tr')
            hdr = ET.Element('th')
            hdr.attrib['colspan'] = str(col_count)
            hdr.text = in_chunk.body_header
            row.append(hdr)
            element.append(row)
        for row in in_chunk.rows:
            element.append(TableBodyRow.xml(row))
        return element


class TableBodyRow():
    '''
    Set up a row in a table.
    '''

    @classmethod
    def xml(cls, in_row):
        '''
        Return a row for a HTML table body.
        '''
        element = ET.Element('tr')
        for cell in in_row.cells:
            element.append(TableCell.xml(cell))
        return element


class TableCell():
    '''
    CSV Table Cell.

    A cell will contain both the value it needs,
    and the specification information on how to render it.
    '''

    @classmethod
    def xml(cls, in_cell):
        '''
        Return a HTML table cell.
        '''
        element = ET.Element('foo')
        if isinstance(in_cell.spec, TableHeaderColumnSpec):
            element.tag = 'th'
        else:
            element.tag = 'td'
        element.text = in_cell.value
        return element


class TableHeaderCell():
    '''
    A table header cell.
    '''
    @classmethod
    def xml(cls, in_colspan=0):
        '''
        Return a HTML table header cell.
        '''
        element = ET.Element('th')
        if in_colspan > 0:
            element.attrib['colspan'] = in_colspan
        return element
