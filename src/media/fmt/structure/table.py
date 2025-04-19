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
Data structure for tables.  A way to represent a table
without any specifics on output formatting.
'''

# pylint: disable=R0903


class Table():
    '''
    Table: The root of all rendered table classes

    Design Note
    -----------
    Most of the data assignment code is handled here.
    The rendering code is handled by the subclasses.

    No output should actually be generated until the
    render() call is made.
    '''
    def __init__(self):
        self._header = None
        self._footer = None
        self.bchunks = []
        self.col_specs = []
        self.classes = []
        self.id = ''

    def set_classes(self, in_classes):
        '''
        Set the class types for the table.
        '''
        self.classes = in_classes

    def set_id(self, in_id):
        '''
        Set an id value for the table.
        '''
        self.id = in_id

    def add_column(self, in_column_spec):
        '''
        Add a column specification to the table.
        '''
        in_column_spec.set_column_number(len(self.col_specs)+1)
        self.col_specs.append(in_column_spec)

    def set_columns(self, *in_cols):
        '''
        Setup the columns of the table.
        '''
        # self.col_specs = in_cols
        self.col_specs = []
        for col_i in in_cols:
            if isinstance(col_i, TableColumnSpec):
                self.col_specs.append(col_i)
            else:
                raise TableSetupException('Invalid column spec object')
        self.col_specs[-1].end_of_row = True
        self.col_specs[-1].build_py_format()

    def add_body(self, in_header=None):
        '''
        Add a data structure that holds a bunch of table rows.
        In HTML parlance, this is the equivelant of a TBODY element.
        '''
        self.bchunks.append(TableBodyChunk(self))
        self.bchunks[-1].set_body_header(in_header)

    def set_body_header(self, in_header=None):
        '''
        Set the header for a body chunk, if there is one.
        '''
        if len(self.bchunks) > 0:
            self.bchunks[-1].set_body_header(in_header)
        else:
            self.bchunks.append(TableBodyChunk(self))
            self.bchunks[-1].set_body_header(in_header)

    def add_row(self, *in_values):
        '''
        Add a row to the current body chunk.
        '''
        if len(self.bchunks) > 0:
            self.bchunks[-1].add_row(in_values)
        else:
            self.bchunks.append(TableBodyChunk(self))
            self.bchunks[-1].add_row(in_values)


class TableBodyChunk():
    '''
    A collection of rows in the main body
    of the table.

    A table will have at least one of these
    objects.
    '''
    def __init__(self, in_table):
        self.rows = []
        self.body_header = None
        self.table = in_table

    def add_row(self, in_values):
        '''
        Add a row to the body chunk.
        '''
        self.rows.append(TableBodyRow(self, in_values))

    def set_body_header(self, in_header):
        '''
        Set the optional header of the body chunk.
        '''
        self.body_header = in_header


class TableColumnAlign():
    '''
    Constants for table text justification.
    '''
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class TableColumnSpec():
    '''
    Specifications for a table column.  There is one
    instance of this class for every column of the table.
    '''
    def __init__(self, in_hdr_text='', in_width=20,
                 in_align=TableColumnAlign.LEFT):
        self.py_format = ''
        self.hdr_text = in_hdr_text
        self.width = in_width
        self.align = in_align
        self.end_of_row = False
        self.col_number = -1
        self.build_py_format()

    def set_column_number(self, in_co_no):
        '''
        Set the column number value.
        '''
        self.col_number = in_co_no

    def build_py_format(self):
        '''
        Setup a format string for the cell value.
        '''
        if self.align == TableColumnAlign.RIGHT:
            self.py_format = ">" + str(self.width)
        else:
            if self.end_of_row:
                self.py_format = ''
            else:
                self.py_format = str(self.width)


class TableBodyRow():
    '''
    Represents a single row in a table body.
    '''
    def __init__(self, in_chunk, in_values):
        self.cells = []
        self.body_chunk = in_chunk
        col_specs = self.body_chunk.table.col_specs
        col_iter = 0
        for val in in_values:
            self.cells.append(TableDataCell(val, col_specs[col_iter]))
            col_iter += 1


class TableHeaderCell():
    '''
    A single cell designed to contain header data.
    '''
    def __init__(self, in_value, in_spec):
        self.value = in_value
        self.spec = in_spec


class TableDataCell():
    '''
    A single cell, containing data.
    '''
    def __init__(self, in_value, in_spec):
        self.value = in_value
        self.spec = in_spec


class TableHeaderColumnSpec(TableColumnSpec):
    '''
    Class for a table column of sub-headers.

    It is essentially identical to the table column class,
    but with a different name so it can be differentiated.
    '''


class TableColFlags():
    '''
    Special option flags that apply to a column in a table.

    HEADER_COLUMN shows a column actually contains headers,
    and not values.

    '''
    HEADER_COLUMN = 1


class TableFlags():
    '''
    Special option flags that apply to a table.
    '''
    VERTICAL_HEADERS = 1


class TableSetupException(Exception):
    '''
    The TableSetupException class is for situation where the
    setup of the table isn't complete, or is missing
    data that makes it impossible to render.
    '''
    def __init__(self, in_message):
        super().__init__(in_message)
        self.message = in_message

    def __str__(self):
        return self.message
