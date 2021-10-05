#!/usr/bin/env python
'''XML Namespace Constants'''

#
# This should actually check for a value error
#


def xs_bool(in_string):
    '''Takes an XSD boolean value and converts it to a Python bool'''
    if in_string in ['true', '1']:
        return True
    return False
